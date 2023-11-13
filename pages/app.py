import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import joblib

#inputs para la frecuencia
st.sidebar.title("Frecuencia en la que deseas visualizar los datos")
checkbox_diario = st.sidebar.checkbox("Diariamente")
checkbox_semanal = st.sidebar.checkbox("Semanalmente")
checkbox_mensual = st.sidebar.checkbox("Mensualmente")

#carga de datos y procesaminto
datam = pd.read_csv("resultados_incidentes_viales2.csv", sep=',', on_bad_lines='skip', dtype={'NUMCOMUNA': 'bytes', 'ANO': 'int'})
datam['FECHA'] = pd.to_datetime(datam['FECHA'])
datam['CLASE_ACCIDENTE'] = datam['CLASE_ACCIDENTE'].replace('Caida Ocupante', 'Caída de Ocupante')

modelo = joblib.load('modelo_glm2.pkl')
#datam['ANO'] = datam['ANO'].str.replace('.', '').astype(int)

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
   index=None,
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

    # Crear un DataFrame a partir de la nueva entrada
    nueva_entrada_df = pd.DataFrame([nueva_entrada2])

    # Realizar la predicción usando el modelo results2
    prediccion = modelo.predict(nueva_entrada_df)

    # Mostrar el número predicho de accidentes en la aplicación Streamlit
    st.write("Número predicho de accidentes:", prediccion[0])


with tab3:
    st.header("Mapa accidentalidad")


st.warning("Advertencia: La predicción de accidentes se basa en datos de accidentalidad y no garantiza resultados precisos o absolutos.")