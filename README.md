# **_$elf Control_**
## **_Denisse Delgado y Daniel Cedeño_** 
### CS50x.ni Y22C1
## **Video Demo:**
### https://youtu.be/FIOLXaRNhiI
## **Description:**

### Funcionamiento general: 
#### *$elf Control es una aplicación web, que tiene como objetivo ser una herramienta que permite a los usuarios llevar un control de sus finanzas en ella, el usuario puede registrarse y observar un resumen de sus finanzas de forma gráfica, así mismo tiene la opción de observar ciertas tablas que contienen sus ultimas transacciones de ingresos, egresos y las cuentas que ha creado.*

### Funcionamiento del resumen:
#### *La hoja de resumen contiene diversos gráficos y tablas que sirven para mostrar como es la distribución de gastos, ingresos y un promedio de los ingresos mensuales para esto fueron utilizados codigos OpenSource como Chart.js, lo que dio lugar a crear gráficos de manera simple, permitiendo la edición y configuración de estos a través de un código JavaScript que contiene todos los parametros que dan formato y que contiene la información mostrada. Este gráfico fue alimentado mediante información recopilada. de nuestra base de datos a través de varios query y codigos en python, y enviada al html mediante una variable en jinja*

###  Funcionamiento del registro de información:
#### *Se habilitó un html dedicado al registro de información por parte del usuario, es decir, mediante los elementos desplegados en esta página, el usuario es capaz de insertar en nuestra base de datos, sus ingresos por categoría, sus egresos y las cuentas que desea afectar, esto permite un mejor control de la información al momento de realizar las segmentaciones de consulta, además que da lugar a futuras caracteristicas que darán una mejor experiencia al usuario.*

###  Funcionamiento del login y register:
#### *Una de las partes esenciales de este proyecto es tener la capacidad de poder ingresar distintos usuarios a la aplicación para poder llevar su control financiero, para ello se diseñaron funciones de login y de register, dichas funciones cumplen con el rol de obtener información suministrada por el usuario en el html, y mediante un get element by Id se almacenan en distintas variables que se insertaran en la base de datos diseñada para este proyecto, uno de los principales aditivos a estas funciones, es el uso de hash, lo que permite codificar la contraseña del usuario, evitando ciertas vulnerabilidades que pueden ocurrir al no hacer uso de la codificación de contraseña*

###  Funcionamiento de la base de datos:
#### *la base de datos de este proyecto se trabajó mediante sqlite3 debido a que da la facilidad de poder trabajar de forma local y desde la consola, facilitando el prediseño de los querys que dan lugar a la obtención de información, a su vez, se utilizó una aplicación web que permitio la estructuración de la base de datos para poder entender y generar una referencia gráfica de las dependencias y relaciones que se generaban en las distintas tablas contenidas. Nuestra base de datos cuenta con un total de 7 tablas distintas que permiten mantener más ordenada la información necesaria para el proyecto*

### Tecnologías utilizadas:
#### *Para el desarrollo de este proyecto, fueron utilizadas las siguientes herramientas:*
#### *-JavaScript*
#### *-Python*
#### *-Flask*
#### *-SQLite3*
#### *-Html*
#### *-CSS*
#### *-Figma*
#### *-Bootstrap*

## **_Agradecemos de forma especial a nuestra tutora Cristel Gutierrez, quien fue un apoyo importante en nuestro aprendizaje y desarrollo_**