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
st.write("También se hace la carga de un archivo.csv que contiene la información de las veredas, los barrios, las comunas de Medellín y los días festivos. La información vista en las siguientes 2 tablas será importante más adelante para hacer el mapeo de la accidentalidad en Medellín en diversos mapas.")
st.write(datam)
st.subheader("1.2 Días feriados")
st.write("Para las fechas especiales se crean dos nuevas variables; FESTIVIDAD y FECHA. Estas variables provienen de una base de datos externa que se adiciona a la base de análisis y abarca los días feriados en Colombia desde 2014 hasta 2022")
st.write(datam2)
st.subheader("1.3 Depuración")
texto2 = '''A continuación se eliminan las columnas consideradas como innecesarias para el modelo: ["CBML", "DIRECCION ENCASILLADA", "EXPEDIENTE", "FECHA_ACCIDENTES", "NRO_RADICADO", "X", "Y"]. También se cruzan las fechas festivos con los días de la base de datos principal y se eliminan los valores nulos de ellas.

Luego de hacer la revisión de las variables y eliminar los datos irrecuperables, procedemos a eliminar las variables temporales que creamos y otras variables presentes en la base de datos las cuales consideramos que no son necesarias para realizar el proyecto.dat

Luego del proceso de depuración la base de datos se ve de esta manera:
'''
st.markdown(texto2)
st.write(datam3)
st.sidebar.markdown("### Informe Completo")
st.sidebar.write("Para visualizar el informe completo, haga clic en el enlace o en la imagen a continuación:")
url_informe = "https://deepnote.com/@fundamentos-analitica-2023-2/AccidentesViales-e684d2cc-6f62-46a5-b8ee-0e6d44f83490"
imagen_informe = "45339858.png"
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