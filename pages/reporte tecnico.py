import streamlit as st

st.markdown("# Reporte técnico: Accidentalidad Medellín")
st.sidebar.markdown("# REPORTE TECNICO")

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
Nicolás Pérez Vásquez<br>
John Stiven Mejía Lopera<br>
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