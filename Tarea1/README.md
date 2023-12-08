Tarea 1: SQL Server: Multitienda “MultiUSM”

Creadores del sistema: 

- Nombre: Pedro Angel Cisternas Arce
- Rol : 202056597-k
- Carrera: Ingeniería Civil Telemática 

- Nombre: Fabian Luis Miranda San Martin
- Rol : 202030515-3
- Carrera: Ingeniería Civil Telemática 

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Descripción:

Con este programa que le presentamos, el usuario dispondrá de una simulación de compra online de una Multitienda llamada “MultiUSM”, la cual utiliza conexión entre un código escrito en el lenguaje de programación “Python” junto al manejo de la creación de una base de datos en un servidor SQL. Con ella, podrá realizar distintas acciones mediante la ejecución del código “main” o principal, como lo son realizar las compras y búsquedas de productos de distinta índole como los que encontraría en un supermercado.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Requerimientos previos:

- Debe tener instalado Microsoft SQL Server 2019
- Debe tener una IDE a gusto personal para ejecutar un código Python (a la vez de tener instaladas las librerías “pyodbc”, “sys” y “re” de Python)
- Tener un archivo “ProductosVF2.csv” en donde se siga la siguiente estructura de ejemplo:

(línea 1)	prod_id;prod_name;prod_description;prod_brand;category;prod_unit_price
(línea 2)	320912;Coca Cola:Coca Cola 3 lt lleve 2 pague 3;COCA COLA;Bebidas;2000
(línea 3)	......................................................................

en donde cada elemento separado por un “;” es una casilla separada en Excel y los puntos consecutivos de la línea 3 indican que pueden haber cuantos productos más se quieran en los datos.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Instrucciones de ejecución:

- Abrir Microsoft SQL Server una nueva Database llamada “MultiUSM”
(click derecho en Databases =>  New Database => Database name: MultiUSM => OK)
- Abrir directorio donde se encuentra el archivo “main.py”
- El archivo de extensión .csv se debe encontrar también en el mismo directorio.
- Conectarse a su respectiva base de datos 'DRIVER={SQL Server};SERVER=....\SQLEXPRESS;DATABASE=...;Trusted_Connection=yes;' (cambiar en el .py)
- 'Run Python File' en el IDE de Visual Studio Code (variará la manera de ejecutar el código dependiendo de su IDE uitilzada)
- Seguido de esto, se mostrará el respectivo menú principal, en el cual se indicarán las opciones correspondientes para interactuar entre el código y la base de datos del servidor SQL.
- Entre las opciones que se muestran en pantalla, hay una opción oculta la cual se realiza escribiendo “0”. Ésta creará las tablas correspondientes en el servidor SQL e ingresará los datos pertenecientes al archivo “ProductosVF2.csv” en cuestión (es importante que los parámetros dentro del archivo de texto sean tal cual como que indican en los requerimientos previos). Cualquier error relacionado a la creación de estas tablas en el servidor SQL y posterior ingreso de datos serán mencionadas en pantalla durante la ejecución de esta opción oculta.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Datos del codigo:
- Es necesario tener creadas las tablas e insertados los datos en la base del servidor SQL para el correcto funcionamiento del programa (opción “0” del menú principal).

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

