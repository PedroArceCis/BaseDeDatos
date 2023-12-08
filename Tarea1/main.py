import pyodbc
import csv
import sys
import re

try:
    print("Conectando a la base de datos...")
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-54G5RGPK\SQLEXPRESS;DATABASE=MultiUSM;Trusted_Connection=yes;')
    print("Conexion exitosa.")
    cursor = connection.cursor()

except:
    sys.exit("Error de conexion, favor intente nuevamente.")

def n_lineas():
    n=0
    archivo = open('ProductosVF2.csv','r', encoding = "utf-8")
    texto = archivo.read()
    for i in texto:
        if i == '\n':
            n+=1
    return n

nlineas = int(n_lineas())
arch = open('ProductosVF2.csv','r', encoding="utf-8")

def remover_caracter(s, n):
    inicio = 0
    fin = len(s)
    resultado = s[inicio:n] + s[n+1:fin]
    return resultado

def encontrar_caracter(s, n):
    cont = 0
    for i in s:
        if i == n:
            return cont
        cont+=1
    return -1

def separar_oferta(oferta): #"pague 2 lleve 3" => "2x3"
    separado = re.split("\s",oferta)
    cont=0
    flag=False
    for palabra in separado:
        cont+=1
        if palabra=="pague" and separado[cont+1]=="lleve": #se respeta el formato "pague M lleve N"
            pague = separado[cont]
            lleve = separado[cont+2]
            try:
                int(pague)
                int(lleve) #para asegurar que estos son int
                flag=True
                break
            except:
                break
    if flag:
        return pague+"x"+lleve
    else:
        return "1x1"


print("\n| Bienvenido a MultiUSM |")
opc=1

while opc>=0 and opc<=10:
    print("\nPor favor, seleccione una de las siguientes opciones:")
    print("1. Mostrar mi carrito.")
    print("2. Agregar productos al carrito.")
    print("3. Mostrar Top 5 productos mas caros.")
    print("4. Mostrar los 5 productos mas caros segun categoria.")
    #se debe solicitar la categoria al momento de seleccionar esta opcion
    print("5. Finalizar compra.")
    print("6. Mostrar mi boleta.")
    print("7. Mostrar valor total.")
    print("8. Buscar producto.")
    #segun nombre que muestre toda la informacion asociada a este desde la tabla Productos.
    print("9. Vaciar carrito.")
    print("10. Eliminar producto del carrito.")
    print("Para finalizar el servicio cualquier otro numero.")
    while True:
        try:
            opc=int(input("Opcion: "))
            break
        except:
            print("\n| ERROR: Por favor, intente nuevamente solo con numeros. |")

    #Creacion de tablas, una view, una funcion y un procedimiento almacenado en la base de datos
    if opc==0:
        print("\nCreando tablas...")
        try:
            tabla="productos"
            cursor.execute("CREATE TABLE "+tabla+" (prod_id bigint primary key, prod_name VARCHAR(150), prod_description VARCHAR(150), prod_brand VARCHAR(150), category VARCHAR(150), prod_unit_price int)")
            tabla="carrito"
            cursor.execute("CREATE TABLE "+tabla+" (prod_id bigint, prod_name VARCHAR(150), prod_brand VARCHAR(150), quantity bigint)")
            tabla="boleta"
            cursor.execute("CREATE TABLE "+tabla+" (prod_id bigint, offer VARCHAR(150), total_value bigint, final_value bigint)")
            tabla="oferta"
            cursor.execute("CREATE TABLE "+tabla+" (prod_id bigint, offer VARCHAR(150))")
        except:
            print("| ERROR: Ya existe la tabla '"+tabla+"' en la base de datos. Por favor, elimine o renombre esta tabla e intente nuevamente. |")
            print("(Servidor SQL => Databases => MultiUSM => Tables)")
            continue
        # insercion de datos desde archivo csv
        lectura = arch.readline().split(';')
        for i in range(nlineas - 1):
            lectura = arch.readline().split(';')

            pos1 = encontrar_caracter(lectura[1], "'")
            if pos1 != -1:
                lectura[1] = remover_caracter(lectura[1], pos1)

            pos2 = encontrar_caracter(lectura[2], "'")
            if pos2 != -1:
                lectura[2] = remover_caracter(lectura[2], pos2)

            pos3 = encontrar_caracter(lectura[3], "'")
            if pos3 != -1:
                lectura[3] = remover_caracter(lectura[3], pos3)

            pos4 = encontrar_caracter(lectura[4], "'")
            if pos4 != -1:
                lectura[4] = remover_caracter(lectura[4], pos4)

            if lectura[1]=="#N/A":
                lectura[1]=""

            insertar_producto = "INSERT INTO productos VALUES ('"+lectura[0]+"', '"+lectura[1]+"', '"+lectura[2]+"', '"+lectura[3]+"', '"+lectura[4]+"', '"+lectura[5].rstrip()+"')"
            cursor.execute(insertar_producto)

        print("Tablas creadas correctamente.")

        #Insertar ofertas
        cursor.execute("SELECT * FROM productos WHERE prod_description LIKE '%pague%'")
        res = cursor.fetchall()
        resultado = list(res)
        for producto in resultado:
            offer = separar_oferta(producto[2])
            if offer!="1x1":
                cursor.execute("INSERT INTO oferta VALUES ('"+str(producto[0])+"', '"+offer+"')")

        #Creacion de view
        print("\nCreando view...")
        try:
            cursor.execute("CREATE VIEW preciosid AS SELECT prod_id, prod_unit_price FROM productos")
            print("View creada correctamente.")
        except:
            print("| ERROR: Ya existe la view 'preciosid' en la base de datos. Por favor, elimine o renombre esta view e intente nuevamente. |")
            print("(Servidor SQL => Databases => MultiUSM => Views)")
            continue

        #Creacion de funcion SQL que será util a la hora de finalizar compra e insertar valores en boleta.
        print("\nCreando funcion SQL...")
        try:
            cursor.execute("CREATE FUNCTION VALORxCANTIDAD(@costo INTEGER) RETURNS INTEGER"
                           " AS BEGIN"
                           "  DECLARE @cantidad INTEGER"
                           "  SELECT @cantidad = quantity FROM carrito"
                           "  RETURN @costo*@cantidad"
                           " END")
            print("Funcion creada correctamente.")
        except:
            print("| ERROR: Ya existe la funcion 'VALORxCANTIDAD' en la base de datos. Por favor, elimine o renombre esta funcion e intente nuevamente. |")
            print("(Servidor SQL => Databases => MultiUSM => Programmability => Functions => Scalar-valued Functions)")
            continue
        #Intento fallido de creacion de procedimiento almacenado para buscar producto
        #print("\nCreando procedimiento almacenado...")
        #try:
        #cursor.execute("CREATE PROCEDURE buscador @nombre VARCHAR(150) AS SELECT productos FROM productos WHERE prod_name LIKE %@nombre%")
        #print("Procedimiento creado correctamente.")
        #except:
        #    print(
        #        "| ERROR: Ya existe el procedimiento 'buscador' en la base de datos. Por favor, elimine o renombre esta funcion e intente nuevamente. |")
        #    print("(Servidor SQL => Databases => MultiUSM => Programmability => Stored Procedures)")
        #    continue

    #Mostrar carrito
    elif opc==1:
        cursor.execute("SELECT prod_name, quantity FROM carrito")
        res = cursor.fetchall()
        resultado = list(res)
        print("")
        if len(resultado)==0:
            print("Su carrito esta vacio.")
        else:
            for producto in resultado:
                print(producto[0]+" | Cantidad = "+str(producto[1]))

    #Agregar productos al carrito
    elif opc==2:
        cursor.execute("SELECT DISTINCT category FROM productos")
        res = cursor.fetchall()
        resultado = list(res)
        print("\nCategorias: ")
        cont = 1
        for cat in resultado:
            print(str(cont) + ".- " + cat[0])
            cont += 1
        while True:
            try:
                num_cat = int(input("Seleccione categoria: "))
                if num_cat<1 or num_cat>len(resultado):
                    print("\n| ERROR: Por favor, intente nuevamente con una categoria existente. |\n")
                else:
                    break
            except:
                print("\n| ERROR: Por favor, intente nuevamente solo con numeros. |\n")
        cat_elegida = resultado[num_cat - 1][0]
        cursor.execute("SELECT * FROM productos WHERE category = '"+cat_elegida+"'")
        res_final = cursor.fetchall()
        resultado_final = list(res_final)
        ids = []
        print("")
        for info in resultado_final:
            print("ID: "+str(info[0])+" | "+info[1]+" | "+info[2]+" | Marca: "+info[3]+" | Precio: $"+str(info[5]))
            ids.append(info[0])
        while True:
            try:
                seleccion = int(input("Seleccione su producto (por ID): "))
                if seleccion not in ids:
                    print("\n| ERROR: Por favor, intente nuevamente con un ID existente. |\n")
                else:
                    break
            except:
                print("\n| ERROR: Por favor, intente nuevamente solo con numeros. |\n")
        pos_prod = ids.index(seleccion)
        print("\nProducto seleccionado: | "+resultado_final[pos_prod][2]+" | Precio: $"+str(resultado_final[pos_prod][5])+" |")
        while(True):
            try:
                cantidad = int(input("¿Cantidad del producto deseado?: "))
                if cantidad < 1:
                    print("\n| ERROR: Por favor, intente nuevamente con una cantidad valida (mayor que 1). |\n")
                else:
                    break
            except:
                print("\n| ERROR: Por favor, intente nuevamente solo con numeros. |\n")
        producto = resultado_final[pos_prod]
        cursor.execute("SELECT prod_id FROM carrito")
        prods_carrito = list(cursor.fetchall())
        ids_carrito = []
        contador = 0
        if len(prods_carrito) != 0: #hay productos previos en el carrito
            for prod in prods_carrito:
                ids_carrito.append(prod[0])
            for i in ids_carrito:
                if i == seleccion: #se esta comprando mas de un producto ya existente en el carrito
                    cursor.execute("SELECT quantity FROM carrito WHERE prod_id = '"+str(i)+"'")
                    cant_actual = (list(cursor.fetchall())[0])[0] #cantidad actual de producto en el carrito
                    agregar_carrito = "UPDATE carrito SET quantity = '"+str(cant_actual+cantidad)+"' WHERE prod_id = '"+str(i)+"'"
                    break
                else:
                    contador+=1
        if contador==len(ids_carrito): #el carrito esta vacio / no existe en el carrito el producto nuevo que se quiere agregar
            agregar_carrito = "INSERT INTO carrito VALUES ('"+str(producto[0])+"', '" +producto[1]+"', '"+producto[3]+"', '"+str(cantidad)+"')"
        cursor.execute(agregar_carrito)
        if cantidad==1:
            print("\nProducto agregado satisfactoriamente.")
        elif cantidad>1:
            print("\nProductos agregados satisfactoriamente.")

    #Top 5 productos mas caros
    elif opc==3: #top 5 productos mas caros
        cursor.execute("SELECT * FROM productos ORDER BY prod_unit_price DESC")
        res = cursor.fetchall()
        resultado = list(res)
        cont = 1
        for fila in resultado:
            print(str(cont)+".- "+fila[1]+"| Precio = $"+str(fila[5]))
            cont+=1
            if cont==6:
                break

    #Top 5 productos mas caros por categoria
    elif opc==4:
        cursor.execute("SELECT DISTINCT category FROM productos")
        res = cursor.fetchall()
        resultado = list(res)
        print("\nCategorias: ")
        cont=1
        for cat in resultado:
            print(str(cont)+".- "+cat[0])
            cont+=1
        num_cat = int(input("Seleccione categoria: "))
        cat_elegida = resultado[num_cat-1][0]
        cursor.execute("SELECT * FROM productos WHERE category = '"+cat_elegida+"' ORDER BY prod_unit_price DESC")
        res_final = cursor.fetchall()
        resultado_final = list(res_final)
        cont = 1
        print("")
        for fila in resultado_final:
            print(str(cont)+".- "+fila[1]+"| Precio = $"+str(fila[5]))
            cont+=1
            if cont==6:
                break

    #Finalizar compra (generacion de boleta)
    elif opc==5:
        #creamos trigger que automaticamente vaciara el carrito cuando se empiecen a insertar datos en la boleta
        cursor.execute("CREATE OR ALTER TRIGGER vaciarcarrito ON boleta FOR INSERT AS TRUNCATE TABLE carrito")
        cursor.execute("SELECT prod_id, quantity FROM carrito")
        carrito = list(cursor.fetchall())
        precios = []
        for producto in carrito:
            ide = producto[0]
            cursor.execute("SELECT prod_unit_price FROM preciosid WHERE prod_id = '"+str(ide)+"'")
            lista = list(cursor.fetchall())
            precios.append(lista[0][0])
        preciosxcant = []
        cont = 0
        for producto in carrito:
            cantidad = int(producto[1])
            precio_tot = cantidad*precios[cont]
            preciosxcant.append(precio_tot)
            cont += 1
        ofertas = []
        for producto in carrito:
            ide = producto[0]
            cursor.execute("SELECT offer FROM oferta WHERE prod_id = '" + str(ide) + "'")
            lista = list(cursor.fetchall())
            if len(lista) == 0:
                ofertas.append("1x1")
            else:
                ofertas.append(lista[0][0])
        cont = 0
        prods_gratis = [] #cantidad de "productos gratis" en base a la cantidad de veces de una oferta aplicada
        for offer in ofertas:
            regalo = 0 # "producto gratis"
            if offer != "1x1":
                quantity = carrito[cont][1]
                mxn = offer.split("x") # "2x3" => ['2', '3']
                m = int(mxn[0])  #formato "pague M lleve N" de oferta
                n = int(mxn[1])
                while True:
                    if quantity >= n:
                        regalo+=(n-m)
                        quantity-=n
                    else:
                        break
            prods_gratis.append(regalo)
            cont+=1
        cont-=cont #se vuelve a reiniciar el contador
        cursor.execute("TRUNCATE TABLE boleta") #borrando posibles datos de boleta previa
        for valor_total in preciosxcant:
            valor_final = valor_total-(precios[cont]*prods_gratis[cont])
            cursor.execute("INSERT INTO boleta VALUES ('"+str(carrito[cont][0])+"', '"+ofertas[cont]+"', '"+str(valor_total)+"', '"+str(valor_final)+"')")
            #cursor.execute("INSERT INTO boleta VALUES ('"+str(carrito[cont][0])+"', '"+ofertas[cont]+"', dbo.VALORxCANTIDAD("+str(precios[cont])+"), '"+str(valor_final)+"')")
            cont+=1
        print("\nCompra realizada con exito, muchas gracias por preferir MultiUSM, su boleta ya ha sido generada.\nDevolviendo al menu principal...")

    #Mostrar la boleta
    elif opc==6:
        cursor.execute("SELECT prod_id, offer, total_value, final_value FROM boleta")
        boleta = list(cursor.fetchall())
        print("")
        if len(boleta) == 0:
            print("Su boleta no ha sido previamente generada.")
        else:
            for producto in boleta:
                cursor.execute("SELECT prod_name FROM productos WHERE prod_id = '"+str(producto[0])+"'")
                nombre = (list(cursor.fetchall()))[0][0]
                print("ID: "+str(producto[0])+" | "+nombre+" | Oferta: "+producto[1]+" | Valor a pagar (sin oferta): $"+str(producto[2])+" | Valor total a pagar: $"+str(producto[3]))

    #Mostrar valor total
    elif opc==7:
        cursor.execute("SELECT final_value FROM boleta")
        valores = list(cursor.fetchall())
        final_value = 0
        for valor in valores:
            final_value+=int(valor[0])
        print("\nEl valor total a pagar es de: $"+str(final_value))
        print("(Favor asegurarse de haber finalizado su compra previamente para generar su boleta...)")

    #Buscar producto segun nombre
    elif opc==8:
        opcion = input("\n--Información de productos--\nIngrese nombre o palabra asociada de un producto: ")
        cursor.execute("SELECT prod_id,prod_name,prod_description,prod_brand,category,prod_unit_price FROM productos WHERE prod_name LIKE '%" + opcion + "%'")
        #cursor.execute("exec buscador "+opcion) #si es que funcionase el procedimiento almacenado usaria una sintaxis asi
        informacion = list(cursor.fetchall())
        print("\nResultados que contengan '"+opcion+"':\n")
        if len(informacion)==0:
            print("No existen resultados que contengan '"+opcion+"'.")
            print("Tal vez su busqueda fue escrita con faltas ortograficas, intente buscar utilizando tilde en sus palabras.")
        else:
            for info in informacion:
                print("ID: "+str(info[0])+" | "+info[1]+" | "+info[2]+" | Marca: "+info[3]+" | Categoria: "+info[4]+" | Precio: $"+str(info[5]))

    #Eliminar todos los productos del carrito
    elif opc==9:
        while True:  # Resuelve problematica de ingresar cualquier tipo de dato o palabras que no sean si/no.
            delete = input("\n¿Desea vaciar el carrito de compras?\nIngrese SI/NO: ")
            if (delete == 'si' or delete == 'SI' or delete == 'Si' or delete == 'sI'):
                print("\nUsted ha seleccionado SI, vaciando carrito...")
                cursor.execute("TRUNCATE TABLE carrito")
                print("Productos del carrito eliminados.")
                break
            elif (delete == 'no' or delete == 'NO' or delete == 'No' or delete == 'nO'):
                print("\nUsted ha seleccionad NO, volviendo al menu...")
                break
            else:
                print("\n| ERROR: Por favor, vuelva a intentarlo respondiendo solamente 'SI' o 'NO'. |")

    #Eliminar producto
    elif opc==10:
        while True:
            delete_producto = input("\nIngrese nombre o palabra asociada del producto a borrar: ")
            cursor.execute("SELECT prod_id,prod_name,prod_brand,quantity FROM carrito WHERE prod_name LIKE '" + delete_producto + "%'")
            lista = list(cursor.fetchall())
            cont = 0
            print("")
            if len(lista)==0:
                print("No existe un producto en el carrito que contenga '"+delete_producto+"'.")
                print("Tal vez su busqueda fue escrita con faltas ortograficas, intente buscar utilizando tilde en sus palabras.")
                break
            else:
                for producto in lista:
                    print("ID: "+str(producto[0])+" | "+producto[1]+" | Cantidad = "+str(producto[3]))
            if len(lista)>1: #hay mas de un producto que coincide
                print("")
                while True:
                    try:
                        print("¿Cual de estos productos desea eliminar?")
                        prod_elegido = int(input("Escriba su ID: "))
                        contador=0
                        for producto in lista:
                            if producto[0] == prod_elegido:
                                print("\nUsted ha seleccionado: "+producto[1])
                                id_eliminar = producto[0]
                                break
                            contador+=1
                        if contador == len(lista): #ingreso un id no existente en la lista
                            print("\n| ERROR: Por favor, intente nuevamente con un ID valido. |\n")
                        else:
                            break
                    except:
                        print("\n| ERROR: Por favor, intente nuevamente solo con numeros. |\n")
            else:
                id_eliminar = lista[0][0]
            while True:
                seleccion = input("¿Desea borrar este producto? Ingrese SI/NO: ")
                if seleccion == 'si' or seleccion == 'SI' or seleccion == 'Si' or seleccion == 'sI':
                    print("\nUsted ha seleccionado SI, eliminando producto...")
                    cursor.execute("DELETE FROM carrito WHERE prod_id='" + str(id_eliminar) + "'")
                    break
                elif seleccion == 'no' or seleccion == 'NO' or seleccion == 'No' or seleccion == 'nO':
                    print("\nUsted ha seleccionad NO, volviendo al menu...")
                    break
                else:
                    print("\n| ERROR: Por favor, vuelva a intentarlo respondiendo solamente 'SI' o 'NO'. |")
            break

    connection.commit()

arch.close()
print("\n| Servicio finalizado. Muchas gracias por su compra. |")