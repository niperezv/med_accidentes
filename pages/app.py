import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.pylab as plt

#inputs para la frecuencia
st.sidebar.title("Frecuencia en la que deseas visualizar los datos")
checkbox_diario = st.sidebar.checkbox("Diariamente")
checkbox_semanal = st.sidebar.checkbox("Semanalmente")
checkbox_mensual = st.sidebar.checkbox("Mensualmente")

#carga de datos y procesaminto
datam = pd.read_csv("resultados_incidentes_viales2.csv", sep=',', on_bad_lines='skip', dtype={'NUMCOMUNA': 'bytes', 'ANO': 'int'})
datam['FECHA'] = pd.to_datetime(datam['FECHA'])
datam['CLASE_ACCIDENTE'] = datam['CLASE_ACCIDENTE'].replace('Caida Ocupante', 'Caída de Ocupante')
#datam['ANO'] = datam['ANO'].str.replace('.', '').astype(int)

#funcion para mostrar df segun fecha
def load_df(year):
    fecha_especifica = pd.to_datetime(year)
    data_fecha_especifica = datam[datam['FECHA'].dt.date == fecha_especifica.date()]
    st.write(data_fecha_especifica)

#funcion para mostrar df segun año

def load_df2(year,type_a):
    data_fecha_especifica = datam[(datam['ANO'] == year) & (datam['CLASE_ACCIDENTE'] == type_a)] 
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
    options2 = st.multiselect('label2',
                             ['Atropello', 'Caída de Ocupante', 'Choque', 'Incendio', 'Volcamiento', 'Otro'],
                             ['Atropello'], label_visibility="hidden")
    d2 = st.date_input("Ingresa una fecha", value = None)

with tab3:
    st.header("Mapa accidentalidad")