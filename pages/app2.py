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
datam = datam.drop(["DIRECCION","DISENO","NUMCOMUNA","FECHA_ACCIDENTE","BARRIO","COMUNA","LONGITUD","LATITUD",], axis=1)

predicciondf = pd.read_csv("predict.csv", sep=',', on_bad_lines='skip')
predicciondf['FECHA'] = pd.to_datetime(predicciondf['FECHA'])

prediccionauxdf = pd.read_csv("predictaux.csv", sep=',', on_bad_lines='skip')
prediccionauxdf['FECHA'] = pd.to_datetime(predicciondf['FECHA'])

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

def load_df3(year):
    data_fecha_especifica = datam[datam['ANO']== year]
    st.write(data_fecha_especifica)
    return data_fecha_especifica

tab1, tab2, tab3 = st.tabs(["Datos historicos", "Predecir Accidentalidad", "Mapa accidentalidad"])

with tab1:
    st.header("Datos historicos")
    options = st.selectbox(
   "Que tipo de accidente desea visualizar?",
   ("Atropello", "Caída de Ocupante", "Choque", "Incendio", "Volcamiento", "Otro","No diferenciar por tipo"),
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
        

        if options == "No diferenciar por tipo":
            data_actual2 = load_df3(option_ano)
            if data_actual2 is not None:
                if checkbox_diario:
                    st.subheader("Diariamente")
                    date_range = pd.date_range(start=data_actual2.loc[data_actual2.index[0], "FECHA"], end=data_actual2.loc[data_actual2.index[-1], "FECHA"])
                    day_counts = data_actual2['FECHA'].dt.date.value_counts().reindex(date_range, fill_value=0)
                    st.bar_chart(day_counts)
                else:
                    st.info("Marca la casilla 'Diariamente' para ver la gráfica diaria.")
                if checkbox_semanal:
                    st.subheader("Semanalmente")
                    weekly_counts = data_actual2['SEMANA'].value_counts().sort_index()
                    st.bar_chart(weekly_counts)
                else:
                    st.info("Marca la casilla 'Semanalmente' para ver la gráfica semanal.")
                if checkbox_mensual:
                    st.subheader("Mensualmente")
                    month_counts = data_actual2['MES'].value_counts().sort_index()
                    st.bar_chart(month_counts)
                else:
                    st.info("Marca la casilla 'Mensualmente' para ver la gráfica anual.")
            else:
                st.warning("No se han cargado datos. Asegúrate de cargar los datos primero.")
                
        else:
            #metricas
            #diario
            data_actual = load_df2(option_ano, options)
            if data_actual is not None:
                if checkbox_diario:
                    st.subheader("Diariamente")
                    date_range = pd.date_range(start=data_actual.loc[data_actual.index[0], "FECHA"], end=data_actual.loc[data_actual.index[-1], "FECHA"])
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
        st.warning("No se ha seleccionado un año.")

with tab2:
    st.header("Predecir accidentalidad")

    # Agregar widgets en la barra lateral para que el usuario ingrese las fechas y configure las clases de accidente
    int_min = datetime.date(2020, 9, 1)
    int_max = datetime.date(2024, 12, 31)

    fecha_inicio = st.date_input('Fecha de inicio', value=None, min_value=int_min, max_value=int_max)
    fecha_fin = st.date_input('Fecha de fin', value=None, min_value=int_min, max_value=int_max)

    # Verificar que la fecha inicial sea estrictamente menor que la fecha final
    if fecha_inicio >= fecha_fin:
        st.error('Error: La fecha de inicio debe ser menor que la fecha de fin.')
        st.stop()
    
    prect_clase = st.selectbox("Que clase de accidente es?",
                              ("Atropello", "Caída de Ocupante", "Choque", "Incendio", "Volcamiento", "Otro","No diferenciar por tipo"),
                              index=None)
    # Filtrar el DataFrame de festividades según el intervalo seleccionado por el usuario
    Prediccion_intervalo = predicciondf[(predicciondf['FECHA'] >= pd.to_datetime(fecha_inicio)) & (predicciondf['FECHA'] <= pd.to_datetime(fecha_fin))]
    Prediccion_intervalo["CLASE_ACCIDENTE"] = prect_clase

    Prediccion_intervalo_aux = prediccionauxdf[(prediccionauxdf['FECHA'] >= fecha_inicio) & (prediccionauxdf['FECHA'] <= fecha_fin)]
    Prediccion_intervalo_aux["CLASE_ACCIDENTE"] = prect_clase

    # Crear un diccionario con los valores de las variables independientes para la nueva entrada

    if fecha_inicio is not None and fecha_fin is not None and prect_clase is not None:

        # Realizar la predicción usando el modelo results2
        prediccion = modelo.predict(Prediccion_intervalo)
        Prediccion_intervalo_df = pd.DataFrame({"PREDICCION": prediccion})
        Prediccion_intervalo2 = pd.concat([Prediccion_intervalo_aux, Prediccion_intervalo_df], axis=1)
        st.write("Predicciones en el intervalo definido")
        st.write(Prediccion_intervalo2)
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
    ruta_html1 = 'med_accidentes/mapa_grupoJ.html'
    ruta_html = 'mapa_grupoJ.html'
    with open(ruta_html, "r", encoding="utf-8") as file:
        contenido_html = file.read()
        #st.write("Ruta del archivo HTML:", ruta_html)
    components.html(contenido_html, width = 800, height = 400, scrolling = False)
st.warning("Advertencia: La predicción de accidentes se basa en datos de accidentalidad y no garantiza resultados precisos o absolutos.")
