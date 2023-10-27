import streamlit as st
st.sidebar.title("Frecuencia en la que deseas visualizar los datos")
checkbox_diario = st.sidebar.checkbox("Diariamente")
checkbox_semanal = st.sidebar.checkbox("Semanalmente")
checkbox_mensual = st.sidebar.checkbox("Mensualmente")
checkbox_anual = st.sidebar.checkbox("Anualmente")

tab1, tab2, tab3 = st.tabs(["Datos historicos", "Predecir Accidentalidad", "Mapa accidentalidad"])

with tab1:
    st.header("Datos historicos")
    options = st.multiselect('label',
                             ['Atropello', 'Caída de Ocupante', 'Choque', 'Incendio', 'Volcamiento', 'Otro'],
                             ['Atropello'], label_visibility="hidden")
    d = st.date_input("Desde que fecha desea visualizar los incidentes", value = None)

with tab2:
    st.header("Predecir accidentalidad")
    options2 = st.multiselect('label2',
                             ['Atropello', 'Caída de Ocupante', 'Choque', 'Incendio', 'Volcamiento', 'Otro'],
                             ['Atropello'], label_visibility="hidden")
    d2 = st.date_input("Ingresa una fecha", value = None)

with tab3:
    st.header("Mapa accidentalidad")