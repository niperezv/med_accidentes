import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import joblib
import geopandas as gpd
import folium
import pandas as pd
import json
import os


#inputs para la frecuencia
st.sidebar.title("Frecuencia en la que deseas visualizar los datos")
checkbox_diario = st.sidebar.checkbox("Diariamente")
checkbox_semanal = st.sidebar.checkbox("Semanalmente")
checkbox_mensual = st.sidebar.checkbox("Mensualmente")

#carga de datos y procesaminto
final = pd.read_csv("final.csv")
datam = pd.read_csv("resultados_incidentes_viales2.csv", sep=',', on_bad_lines='skip', dtype={'NUMCOMUNA': 'bytes', 'ANO': 'int'})
datam['FECHA'] = pd.to_datetime(datam['FECHA'])
datam['CLASE_ACCIDENTE'] = datam['CLASE_ACCIDENTE'].replace('Caida Ocupante', 'Caída de Ocupante')

modelo = joblib.load('modelo_glm2.pkl')
#datam['ANO'] = datam['ANO'].str.replace('.', '').astype(int)

#funcion para definir estilo del mapa
def style_function2(feature):
    return {
        "fillColor": feature["properties"]["color"],
        "fillOpacity": 0.72,
        "stroke": True,
        "strokeOpacity": 0.2,
        "color": "black",
        "weight": 1,
    }

#funcion para crear mapa
def crear_mapa_todo(datos,diccionario,color_dict,Grupo):
  barrios_med = gpd.read_file('Barrio_Vereda.dbf')
  barrios_med['color'] = 'gray'
  barrios_med['grupo'] = 'No clasificado'


  for lista, barrios in diccionario.items():
    color = color_dict.get(lista, 'gray')  # Obtiene el color correspondiente a la lista o 'gray' si no se encuentra
    grupo = Grupo.get(lista, 'No clasificado')

    barrios_med.loc[barrios_med['NOMBRE'].isin(barrios), 'color'] = color
    barrios_med.loc[barrios_med['NOMBRE'].isin(barrios), 'grupo'] = grupo

  mapa = folium.Map(width=800, height=400, zoom_start=11, location=[6.27,-75.60])
  folium.TileLayer('openstreetmap').add_to(mapa)
  folium.GeoJson(data = barrios_med,
               name = 'NOMBRE',
               style_function = style_function2,
               popup = folium.GeoJsonPopup(
                  fields = ['NOMBRE','grupo'],
                  aliases = ['Barrio', 'Accidentalidad']
               )
               ).add_to(mapa)


  mapa.save('mapa_grupoJ.html')
  st.markdown('<iframe src="mapa_grupoJ.html" width=800 height=400></iframe>', unsafe_allow_html=True)
#funcion para mostrar df segun fecha
def load_df(year):
    fecha_especifica = pd.to_datetime(year)
    data_fecha_especifica = datam[datam['FECHA'].dt.date == fecha_especifica.date()]
    st.write(data_fecha_especifica)

#funcion para mostrar df segun año

def load_df2(year,type_a):
    data_fecha_especifica = datam[(datam['ANO'] == year) & (datam['CLASE_ACCIDENTE'] == type_a)]
    st.write(data_fecha_especifica) 
    return data_fecha_especifica

tab1, tab2, tab3 = st.tabs(["Datos historicos", "Predecir Accidentalidad", "Mapa accidentalidad"])

with tab1:
    st.header("Datos historicos")
    options = st.selectbox(
   "Que tipo de accidente desea visualizar?",
   ("Atropello", "Caída de Ocupante", "Choque", "Incendio", "Volcamiento", "Otro"),
   index=0,
   placeholder="Seleccionar tipo accidente...",
   )
    #d = st.date_input("Desde que fecha desea visualizar los incidentes", datetime.date(2014,10,22))
    option_ano = st.selectbox('Seleccione un año',
                              ('2014','2015','2016','2017','2018','2019','2020'))
    st.write("Datos cargados")
    #semanal
    #weekly_counts = data_actual['SEMANA'].value_counts().sort_index()
    #mensual
    #month_counts = data_actual['MES'].value_counts().sort_index()
    #graficas
    #diariamente
    if option_ano is not None:  # Verifica que se haya seleccionado un año
        option_ano = int(option_ano)
        data_actual = load_df2(option_ano, options)

        if data_actual is not None:
            #metricas
            #diario
            if checkbox_diario:
                st.subheader("Diariamente")
                date_range = pd.date_range(start='2014-07-04', end='2014-12-31')
                day_counts = data_actual['FECHA'].dt.date.value_counts().reindex(date_range, fill_value=0)
                st.bar_chart(day_counts)
            else:
                st.info("Marca la casilla 'Diariamente' para ver la gráfica diaria.")
            if checkbox_semanal:
                st.subheader("Semanalmente")
                weekly_counts = data_actual['SEMANA'].value_counts().sort_index()
                st.bar_chart(weekly_counts)
            else:
                st.info("Marca la casilla 'Semanalmente' para ver la gráfica semanal.")
            if checkbox_mensual:
                st.subheader("Mensualmente")
                month_counts = data_actual['MES'].value_counts().sort_index()
                st.bar_chart(month_counts)
            else:
                st.info("Marca la casilla 'Mensualmente' para ver la gráfica anual.")
        else:
            st.warning("No se han cargado datos. Asegúrate de cargar los datos primero.")
    else:
        st.warning("No se han cargado datos. Asegúrate de cargar los datos primero.")

with tab2:
    st.header("Predecir accidentalidad")
    int_min = datetime.date(2021, 1, 1)
    int_max = datetime.date(2022, 12, 31)
    prect_fecha = st.date_input("Ingresa una fecha", value=None, min_value=int_min, max_value=int_max)
    prect_festi = st.selectbox("Es festivo?",
                               ("NO FESTIVO", "FESTIVO", "SEM_SANTA", "NAVIDAD", "MADRES", "BRUJAS", "A_NUEVO"),
                               index=None,
                               placeholder="Seleccione No Festivo o el tipo de día feriado")
    prect_dia = st.selectbox("Que día de la semana es?",
                             ("Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"),
                             index=None)
    prect_quincena = st.selectbox("Es quincena?",
                                  (0, 1),
                                  index=None,
                                  placeholder="Seleccione 1:Si, 0:No")
    prect_clase = st.selectbox("Que clase de accidente es?",
                              ("Atropello", "Caída de Ocupante", "Choque", "Incendio", "Volcamiento", "Otro"),
                              index=None)
    # Crear un diccionario con los valores de las variables independientes para la nueva entrada
    nueva_entrada = {
        'FECHA': prect_fecha,
        'FESTIVIDAD': prect_festi,
        'DIA_SEMANA': prect_dia,
        'DIA_QUINCENA': prect_quincena,
        'CLASE_ACCIDENTE': prect_clase
    }

    prect_fecha = str(prect_fecha)
    prect_festi = prect_festi
    prect_dia = prect_dia
    prect_quincena = prect_quincena
    prect_clase = prect_clase

    nueva_entrada2 = {
    'FECHA':prect_fecha,
    'FESTIVIDAD':prect_festi,
    'DIA_SEMANA':prect_dia,
    'DIA_QUINCENA':prect_quincena,
    'CLASE_ACCIDENTE': prect_clase
    }
    if prect_fecha is not None and prect_festi is not None and prect_dia is not None and prect_quincena is not None and prect_clase is not None:
        # Crear un DataFrame a partir de la nueva entrada
        nueva_entrada_df = pd.DataFrame([nueva_entrada2])

        # Realizar la predicción usando el modelo results2
        prediccion = modelo.predict(nueva_entrada_df)

        st.write("Número predicho de accidentes:", prediccion[0])
    else:
        st.error("Por favor, complete todas las entradas antes de realizar la predicción.")
    # Mostrar el número predicho de accidentes en la aplicación Streamlit


with tab3:
    st.header("Mapa accidentalidad")
    with open('diccionario.json', 'r') as f:
        diccionario = json.load(f)
    color_dict = {
    'cluster_0': '#ba5252',
    'cluster_1': '#fc3d73',
    'cluster_2': '#AA8F85',
    'cluster_3' : '#FF0F53',
    'cluster_4' : '#52CAA7',
    'cluster_5': '#52E6A7'
    }
    Grupo = {
    'cluster_0': 'Media-Alta',
    'cluster_1': 'Alta',
    'cluster_2': 'Media-Baja',
    'cluster_3' : 'Muy alta',
    'cluster_4' : 'Baja',
    'cluster_5': 'Muy baja'
    }
    ruta_html1 = 'mapa_grupoJ.html'
    ruta_html = 'pages/mapa_grupoJ.html'
    with open(ruta_html1, "r", encoding="utf-8") as file:
        contenido_html = file.read()
        #st.write("Ruta del archivo HTML:", ruta_html)
    components.html(contenido_html, width = 800, height = 400, scrolling = False)
st.warning("Advertencia: La predicción de accidentes se basa en datos de accidentalidad y no garantiza resultados precisos o absolutos.")