import streamlit as st
import pandas as pd

datam = pd.read_csv("barrios_comunas.csv", sep=',', on_bad_lines='skip')
datam2 = pd.read_csv("dias_festivos_21.csv", sep=',', on_bad_lines='skip')
datam3 = pd.read_csv("resultados_incidentes_viales2.csv", sep=',', on_bad_lines='skip', dtype={'NUMCOMUNA': 'bytes', 'ANO': 'int'})
datam3['FECHA'] = pd.to_datetime(datam3['FECHA'])
datam3['CLASE_ACCIDENTE'] = datam3['CLASE_ACCIDENTE'].replace('Caida Ocupante', 'Caída de Ocupante')
st.sidebar.markdown("# REPORTE TECNICO")
st.markdown("# Reporte técnico: Accidentalidad en Medellín periodo de 2014 a 2020 y predicción de accidentalidad para los años 2021 y 2022")
st.caption('Fecha: 2023-10-26')
st.caption('Amilder Stewin Ospina Tobón')
st.caption('John Stiven Mejía Lopera')
st.caption('Nicolás Pérez Vásquez')
st.header("Introducción")
st.write("El siguiente informe, trata acerca del análisis de accidentalidad en Medellín durante los periodos 2014 a 2020. Realizaremos una revisión de los datos con el fin de encontrar el comportamiento de estos, segmentando por diferentes tipos de variables. Paralelamente, realizaremos el agrupamiento mediante técnicas de clustering y analizaremos el comportamiento según los diferentes grupos. Se realizará el entrenamiento de un modelo con el fin de realizar una predicción para los años 2021 y 2022, a su vez, crearemos una aplicación web en la que se podrán ver los agrupamientos y ver la predicción por diferentes tipos de segmentación para los años 2021 y 2022.")
st.header("1. Datos")
st.write("Los datos fueron obtenidos de la plataforma metadata: (https://medata.gov.co/dataset/incidentes-viales) que contiene información relacionada a la accidentalidad vial entre los años 2014 y 2020. En la siguiente sección realizaremos la limpieza de los datos y organización de los mismos para realizar un análisis descriptivo de estos.")

texto_datos = """
**AÑO:** año de ocurrencia del incidente. (2014 hasta 2016)

**CBML:** es el código catastral que corresponde al código comuna, barrio, manzana, lote catastral de un predio. En este encontramos 18.156 vacíos y adicionalmente tiene 962 registros con caracteres extraños como: AUC1, AUC2, Inst_14, Inst_16, Inst_18, Inst_19, Sin Inf, SN01, para un total de 19.118 registros mal estructurados o vacíos.

**CLASE_ACCIDENTE:** clasificación del IPAT (Informe Policivo de Accidente de tránsito) sobre la clase de accidente de tránsito, hay 5 tipos de clasificación, choque, atropello, volcamiento, caída de ocupante, incendio y adicional se hay otra clasificación denominada como “otro”. En esta variable encontramos un total de 6 datos vacíos los cuales se cambiarán por “otro”.

**DISEÑO:** esta corresponde al sitio donde ocurrió el accidente (Ciclorruta, Glorieta, Intersección, Lote o Predio, Paso a Nivel, Paso Elevado, Paso Inferior, Pontón, Puente, Tramo de vía, Túnel, Vía peatonal). En esta encontramos 1.148 vacíos los cuales se reemplazarán por “otro”.

**BARRIO:** barrio de ocurrencia del incidente vial, en este encontramos 19.006 vacíos, además se tienen 1.822 registros adicionales con caracteres como: números entre 0 y 9.086, AUC1, AUC2, Inst, Sin Inf, Sin nombre.

**COMUNA:** denominación con la cual se identifica cada Comuna o Corregimiento, en este encontramos 12.798 vacíos además se tienen 7.064 registros adicionales con caracteres como: No Georef, 0, In, AU, Sin Inf, SN.

**NUMCOMUNA:** número de la comuna en la que ocurrió incidente vial, se encontraron 20.116 registros adicionales con caracteres como: AU, In, Sin Inf, SN.

**LOCATION:** fuente de información con la cual se realizó la geo codificación, contiene la latitud y longitud, Posteriormente será separada en dos variables.

**X:** coordenada X en metros del accidente, en sistema de coordenadas MAGNA Medellín Local.

**Y:** coordenada Y en metros del accidente, en sistema de coordenadas MAGNA Medellín Local.

**NRO_RADICADO:** consecutivo que asigna UNE, según el orden de llegada de los expedientes para su diligenciamiento.

**MES:** mes de ocurrencia del incidente vial. Esta variable no se modifica.

**GRAVEDAD_ACCIDENTE:** clasificación del IPAT (Informe Policial de Accidentes de Tránsito) sobre la gravedad del accidente, corresponde al resultado más grave presentado en el accidente. Daños materiales “Sólo daños”, accidente con heridos “Herido”, accidente con muertos “Muerto”, en esta variable se cambia la codificación a UTF-8

**FECHA_ACCIDENTES:** fecha de los accidentes (formato YYYY-MM-DD hh:mi:ss), proviene del IPAT (Informe Policial de accidentes de Tránsito)

**FECHA_ACCIDENTE:** fecha del accidente, proviene del IPAT (Informe Policial de accidente de Tránsito) esta variable posteriormente se elimina debido a que proporciona menos información que la variable FECHA_ACCIDENTES.

**EXPEDIENTE:** consecutivo que asigna UNE, según el orden de llegada de los expedientes para su diligenciamiento. Esta variable posteriormente se elimina.

**DIRECCION ENCASILLADA:** dirección encasillada que entrega el geo codificador. Esta variable se elimina.

**DIRECCION:** dirección donde ocurrió el incidente. Esta variable no se modifica.

**NRO_RADICADO:** consecutivo que asigna UNE, según el orden de llegada de los expedientes para su diligenciamiento.
"""

st.markdown(texto_datos)
st.subheader("1.1. Integración de datos Geo-Medellín")
st.write("También se hace la carga de la *Tabla 1* que contiene la información de las veredas, los barrios, las comunas de Medellín y los días festivos. La información vista en las siguientes 2 tablas será importante más adelante para hacer el mapeo de la accidentalidad en Medellín en diversos mapas.")
st.image('images/_tabla_1.PNG', caption='Tabla 1: Tabla de barrios y comunas')
st.subheader("1.2 Días feriados")
st.write("Para las fechas especiales se crean dos nuevas variables; FESTIVIDAD y FECHA. Estas variables provienen de una base de datos externa que se adiciona a la base de análisis y abarca los días feriados en Colombia desde 2014 hasta 2022")
st.image('images/_tabla_2.PNG', caption='Tabla 2: Tabla de festividades')
st.subheader("1.3 Depuración")
texto2 = '''A continuación se eliminan las columnas consideradas como innecesarias para el modelo: ["CBML", "DIRECCION ENCASILLADA", "EXPEDIENTE", "FECHA_ACCIDENTES", "NRO_RADICADO", "X", "Y"]. También se cruzan las fechas festivos con los días de la base de datos principal y se eliminan los valores nulos de ellas.

Luego de hacer la revisión de las variables y eliminar los datos irrecuperables, procedemos a eliminar las variables temporales que creamos y otras variables presentes en la base de datos las cuales consideramos que no son necesarias para realizar el proyecto.dat

Luego del proceso de depuración la base de datos se ve de esta manera:
'''
st.markdown(texto2)
st.image('images/_tabla_3_.PNG', caption='Tabla 3: Tabla de base de datos depurada')
st.header("2. Análisis descriptivo")
st.subheader("2.1 Distribución de accidentes por gravedad")
texto3 = '''A continuación en el Gráfico 1 se muestran los tipos (o la severidad) de los accidentes. Se observa que la gran mayoría de accidentes son accidentes que terminan en heridos y en solamente daños materiales. Se resalta la gran diferencia que tienen estos dos tipos de accidentes al compararlos con los accidentes que involucran fatalidades.
 La mayor cantidad de accidentes resultan en personas heridas, seguidos por accidentes que solo involucran daños materiales. Los accidentes con muertos son una gran minoría en comparación.
'''
st.markdown(texto3)
st.image('images/_grafico_1.png', caption='Gráfico 1: Histograma de frecuencias de accidentes por gravedad')
st.subheader("2.2 Distribución de Accidentes por Festividad (o NO FESTIVO)")
texto4 = '''En el Gráfico 2 de distribución de accidentes por festividad podemos observar la cantidad de accidentes presentados en Medellín diferenciados por el tipo de festividad de ese día. Como es de esperar, la mayor cantidad de accidentes se presentan en los NO FESTIVOS.
 La razón de ello parece ser lógica, la cantidad de días festivos en el año es muy inferior a la cantidad de días "normales". Esta relación entre cantidad de días y cantidad de accidentes se denota también en las demás variables.
'''
st.markdown(texto4)
st.image('images/_grafico_2.png', caption='Gráfico 2: Histograma de accidentes por festividad')
st.subheader("2.3 Distribución de accidentes por día de la semana")
texto5 = '''El día que presenta mayor cantidad de personas accidentadas, es el día viernes seguido del día martes, con una diferencia de 669 accidentes registrados.
 Seguido de esto los días (miércoles  jueves) y (lunes  sábado), presentan una accidentalidad similar con una diferencia de 331 y 46 accidentes de diferencia, respectivamente, y el día domingo es el día con menor número de accidentes registrados.
'''
st.markdown(texto5)
st.image('images/_grafico_3.png', caption='Gráfico 3: Histograma de accidentes por día de la semana')
st.subheader("2.4 Distribución de accidentes por mes")
texto6 = '''En la segmentación por mes, podemos ver que el mes con mayor numero de accidentes es el mes #8: Agosto,
 con 24640 accidentes registrados, algo contrastante con el mes de diciembre el cual es el mes donde mas fiestas se registran y el cual cuenta con un número de accidentes de 21101. El mes con menor accidentes fue el #4: Abril con 17579.
'''
st.markdown(texto6)
st.image('images/_grafico_4.png', caption='Gráfico 4: Histograma de frecuencia de accidentes por mes')
st.subheader("2.5 Distribución de accidentes por año")
texto7 = '''En los accidentes registrado entre los años 2015 a 2019 podemos ver que no hay mucha variación entre el numero de accidentes registrados en cada uno de estos,
 a diferencia de los años 2014 y 2020 los cuales en el dataset proporcionado solo contamos con datos desde el 4 de julio a 31 de diciembre, para los datos del 2014,
y desde el 1 de enero hasta el 31 de agosto para los datos del año 2020, por esto es que podemos ver una diferencia notoria de estos dos años, respecto a los tomados de 2015 a 2019.
'''
st.markdown(texto7)
st.image('images/_grafico_5.png', caption='Gráfico 5: Histograma de accidentes por año')
st.subheader("2.6 Serie de tiempo mensual de accidentes viales")
texto8 = '''A continuación en el Gráfico 6 se muestra la serie de tiempo mensual de accidentes viales durante los años que la base de datos contiene (2014 - 2020).
 Se puede observar que desde el año 2014 hasta el 2020, el número de accidentes se había mantenido en un intervalo aproximado de 3000 a 4000 accidentes al mes. 
 Desde 2020 en adelante se puede observar un decrecimiento anormal en la cantidad de accidentes hasta llegar por debajo de los 1000. Una posible explicación podría ser la pandemia del COVID-19 que comprendió esas fechas. 
'''
st.markdown(texto8)
st.image('images/_grafico_6.png', caption='Gráfico 6: Serie de tiempo accidentes mensuales')
st.subheader("2.7 Distribución de accidentes por tipo de accidente")
texto9 = '''En la siguiente grafica (Gráfico 7) podemos ver que el tipo de accidente más común es de tipo “choque”, además de esto analizamos los tipos gravedad de accidentes y podemos evidenciar que el tipo de gravedad mas concurrente es “con heridos”.
'''
st.markdown(texto9)
st.image('images/_grafico_7.png', caption='Gráfico 7: Histograma de accidentes por clase')
st.subheader("2.8 Cantidad de accidentes en una fecha en específico (22/10/2014)")
st.write("Así se verían los accidentes en un día particular x.")
st.image('images/_grafico_8.png', caption='Gráfico 8: Histograma de clase de accidente en el 22 de octubre del 2014')
st.subheader("2.9 Histograma de accidentes de choque semanal en el año 2014")
st.write("Se muestra también el histograma de accidentes por semana durante el año 2014.")
st.image('images/_grafico_9.png', caption='Gráfico 9: Histograma de accidentes semanalmente de choque en el 2014 ')
st.subheader("2.10 Histograma de accidentes de choque semanal en el año 2015")
st.write("También podemos observar lo mismo para el año 2015")
st.image('images/_grafico_10.png', caption='Gráfico 10: Histograma de accidentes semanalmente de choque en el 2015')
st.subheader("2.11 Histograma de accidentes de choque mensual en el año 2015")
st.write("El siguiente histograma nos permite ver la distribución de los accidentes de choques en el 2015 diferenciado por mes (1 - 12). Se observa que en este año fue enero el mes con menos accidentes y octubre fue el que mas tuvo. ")
st.image('images/_grafico_11.png', caption='Gráfico 11: Histograma de accidentes Mensualmente de choque en el 2015')

st.header("3.Modelamiento y predicción")
texto1 = '''Una vez preparados los datos geoespaciales, se procedió a realizar el modelamiento y la predicción de accidentes de tránsito. Para ello, se eliminaron columnas innecesarias y se creó una nueva variable para indicar si un día es de quincena.
Los modelos predictivos que veremos se construirán con los datos de los años 2014, 2015, 2016, 2017 y 2018; esta será la base para entrenamiento. Los accidentes del año 2019 y 2020 se usarán para validar los modelos.
El criterio de éxito de los modelos predictivos será el MAE de la predicción.
'''
st.markdown(texto1)
st.subheader("3.1.1 Modelo 1 GLM Poisson")
texto2 = '''El primer modelo se basó en un Modelo Lineal Generalizado (GLM) con distribución Poisson. Se ajustó el modelo utilizando diferentes variables, como la quincena, festividades y día de la semana.

Como nos interesa predecir el número de accidentes por unidad de tiempo, resulta conveniente utilizar un modelo lineal generalizado con la distribución Poisson. Para este primer modelo, consideraremos únicamente las variables FESTIVIDAD Y DIA_SEMANA para predecir la accidentalidad.
'''
st.markdown(texto2)
st.image('images/_tabla_4.PNG', caption='Tabla 4: Tabla de entrada para el modelo GLM Poisson')
st.write("Podemos ver a continuación los resultados generalizados del modelo de regresión propuesto.")
st.image('images/_imagen_1.PNG', caption='Imagen 1: Serie de tiempo original vs predicción.')
st.subheader("3.1.2 Serie de tiempo mensual de NRO_ACCID vs predicción")
st.write("A continuación podemos ver el ajuste del modelo en comparación con la gráfica de series de tiempo mostrada anteriormente.")
st.image('images/_grafico_12.png', caption='Gráfico 12: Serie de tiempo original vs predicción. ')
st.subheader("Métricas")
st.write("Entrenamiento 2014 - 2018: Para los datos de entrenamiento, se obtiene un MAE de 14.7347, un MSE de 382.8113, y un R2 de 0.4565.")
st.write("Prediccion y evaluación del año 2019 Se muestran las predicciones realizadas para el año 2019. El día primero de enero es representado con un 0 y el 31 de diciembre con el 364.")
st.image('images/_tabla_5.PNG', caption='Tabla 5: Predicciones 2019. ')
st.write("Métricas de predicción y evaluación año 2019: Para los datos de validación del año 2019, se obtiene un MAE de 17.5274, y un R2 de 0.4123. ")
st.write("Métricas de predicción y evaluación año 2020: Para los datos de validación del año 2020, se obtiene un MAE de 46.03012, y un R2 de -0.9211. Estos valores son mucho mejores que los obtenidos con el modelo anterior.")
st.subheader("3.2. Modelo 2 GLM con variable CLASE_ACCIDENTE")
st.write("El segundo modelo también se basó en un Modelo Lineal Generalizado (GLM) con distribución Poisson, pero esta vez se incluyó la variable 'CLASE_ACCIDENTE' como una variable categórica adicional.")
st.image('images/_tabla_6.PNG', caption='Tabla 6: Tabla de entrada para el modelo 2 GLM Poisson')
st.write("Podemos ver a continuación los resultados generalizados del modelo de regresión propuesto.")
st.image('images/_imagen_2.PNG', caption='Imagen 2: Generalized Linear Model Regression Results')
st.subheader("3.2.1 Serie de tiempo mensual de NRO_ACCID vs predicción")
texto3 = '''A continuación podemos ver el ajuste del modelo en comparación con la gráfica de series de tiempo mostrada anteriormente. Podemos notar que si bien el modelo parece ajustarse bien a la media de la base de datos original,
 este tiene una varianza menor.
'''
st.markdown(texto3)
st.image('images/_grafico_13.png', caption='Gráfico 13: Serie de tiempo 2 original vs predicción. ')
st.subheader("3.2.2 Métricas")
st.write("Entrenamiento 2014-2018: Para los datos de entrenamiento, se obtiene un MAE de 4.7453, un MSE de 60.07008, y un R2 de 0.9299.")
st.write("Métricas de predicción y evaluación año 2019: Para los datos de validación del año 2019, se obtiene un MAE de 5.0494, y un R2 de 0.92411. Estos valores son mucho mejores que los obtenidos con el modelo anterior.")
st.write("Métricas de predicción y evaluación año 2020: Para los datos de validación del año 2020, se obtiene un MAE de 10.2246, y un R2 de 0.2026. Este MAE tan alto y este R2 bajo indican que el modelo se ajusta muy pobremente a los datos del año 2020.")
texto4 = '''Sin embargo, tal como hemos visto con anterioridad, ningún modelo se ajusta bien al año 2020. Esto se puede explicar por dos posibles razones:

       1. En 2020 fue el inicio de la pandemia, y hubo muchos menos accidentes.
       2. En 2020 solo hay observaciones hasta el mes de agosto.

Por tanto, el año 2020 no nos será muy útil para validar los modelos, ya que el comportamiento de este año es muy diferente a los demás años con los que se entrenó el modelo.
'''
st.markdown(texto4)
st.header("4.Agrupamiento")
texto5 = '''Creamos una base de datos que nos diga el número de accidentes por gravedad, asi mismo nos indica la lógica en la cual python toma el orden de los accidentes, siendo con heridos, con muertos y Solo danos. Esto será útil para la construcción correcta de la matriz para el agrupamiento.

Creamos una base de datos con la gravedad de los accidentes para ser usada para el agrupamiento

Para encontrar un k optimo se usarán la curva del codo, estadístico de Gap y el coeficiente de la silueta.
'''
st.markdown(texto5)
st.subheader("4.1. Método de la curva de codo")
st.write("Como podemos ver en la curva del codo nos da a entender un k ideal con un valor de 5 ó 6")
st.image('images/_grafico_14.png', caption='Gráfico 14: Gráfico curva de codo ')
st.subheader("4.2 Método de la silueta")
st.write("Con el método del coeficiente de la silueta nos muestra que un k ideal tiende a ser 2 ya que es el valor k con el puntaje del coeficiente de silueta más alto.")
st.image('images/_grafico_15.png', caption='Gráfico 15: Gráfico metodo de la silueta')
st.subheader("4.3 Estadístico de GAP")
st.image('images/_grafico_16.png')
st.image('images/_grafico_17.png')
st.image('images/_grafico_18.png')
st.image('images/_grafico_19.png')
st.image('images/_grafico_20.png')
st.write("Gráfico 16: Gráficos Gap y diff ")
st.subheader("4.3 Grupos")
texto6 = '''Con la función summary clasificamos los grupos

El grupo 1 está caracterizado por tener una cantidad muy baja de accidentes en general, a excepción de los choques pues cuenta con una media de 576.
'''
st.markdown(texto6)
st.image('images/_tabla_7.PNG', caption='Tabla 7: Tabla de clasificación Grupo 1')
st.write("El grupo 2 es el que representa la mayor accidentalidad de tipo choque, con una media de 2850. También tiene una gran cantidad de accidentes en los demás tipos.")
st.image('images/_tabla_8.PNG', caption='Tabla 8: Tabla de clasificación Grupo 2')
st.write("En general, el grupo 3 cuenta con la menor cantidad de accidentes si lo comparamos con los demás grupos.")
st.image('images/_tabla_9.PNG', caption='Tabla 9: Tabla de clasificación Grupo 3')
st.write("El grupo 4 contiene una cantidad media de choques relativamente alta. Los demás parámetros son bajos.")
st.image('images/_tabla_10.PNG', caption='Tabla 10: Tabla de clasificación Grupo 4')
st.write("El grupo 5 también tiene una cantidad de choques alta y es el que más incendios contiene, teniendo en cuenta este parámetro es bajo. Notamos un alza en accidentes de tipo 'otro'.")
st.image('images/_tabla_11.PNG', caption='Tabla 12: Tabla de clasificación Grupo 5')
st.header("Referencias")
texto1 = '''
•de Medellín, A. (s/f). MEDATA. Alcaldía de Medellín. Recuperado el 15 de octubre de 2023, de https://medata.gov.co/dataset/incidentes-viales

•de Medellín, A. (s/f-a). Geomedellín. Municipio de Medellín. Recuperado el 20 de octubre de 2023, de https://geomedellin-m-medellin.opendata.arcgis.com/404
'''
st.markdown(texto1)
st.sidebar.markdown("### Informe Completo")
st.sidebar.write("Para visualizar el informe completo, haga clic en el enlace o en la imagen a continuación:")
url_informe = "https://deepnote.com/@fundamentos-analitica-2023-2/AccidentesViales-e684d2cc-6f62-46a5-b8ee-0e6d44f83490"
imagen_informe = "images\45339858.png"
st.sidebar.markdown(f"[Informe Completo en Deepnote]({url_informe})")
st.sidebar.markdown("[![Foo](https://avatars.githubusercontent.com/u/45339858?s=280&v=4)](https://deepnote.com/@fundamentos-analitica-2023-2/AccidentesViales-e684d2cc-6f62-46a5-b8ee-0e6d44f83490)")


st.markdown(
        """
        <style>
        .footer {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .footer a {
            color: white;
            text-decoration: none;
            margin: 0 10px;
        }
        </style>
        """,unsafe_allow_html=True)
        
st.markdown(
    """
    <style>
    .custom-space {
        margin-top: 3cm;
    }
    </style>
    """,unsafe_allow_html=True)
st.markdown('<div class="custom-space"></div>', unsafe_allow_html=True)
# Contenido del footer
footer_content = """
<div class="footer">
Amilder Stewin Ospina Tobón<br>
John Stiven Mejía Lopera<br>
Nicolás Pérez Vásquez<br>
|
<a href="https://github.com/niperezv/med_accidentes" target="_blank">
Repositorio GitHub
</a> | 
<a href="https://medata.gov.co/dataset/incidentes-viales" target="_blank">
Dataset
</a> |
</div>
"""

# Mostrar el contenido del footer
st.markdown(footer_content, unsafe_allow_html=True)