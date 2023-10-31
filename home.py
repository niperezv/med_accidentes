import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Home",
        page_icon="👋",
    )

    st.write("# En Medellín,cada 16 minutos hay un lesionado en las vías por accidentes")

    st.sidebar.success("Select a demo above.")

    st.subheader('Según la Secretaría de Movilidad de Medellín, este año se ha presentado un 8% más de incidentes de todo tipo en las vías de la ciudad.')
    
    texto_formateado ="""Los accidentes en las vías de Medellín han aumentado este año, si se compara con
    el año pasado, según los registros de la Secretaría de Movilidad. En este 2022
    se han presentado 32.109 accidentes, con corte al 1.° de octubre, registrándose
    un aumento del 8% si se compara con el mismo periodo del año pasado."""
    st.markdown(f'<u style="color: yellow;">{texto_formateado}</u>', unsafe_allow_html=True)

    st.markdown(
        """
        En estos hechos se reportan 12.419 lesionados, de los cuales el 61%
        son conductores de motocicleta y el 13% eran peatones. Si se comparan
        los datos con el 2021, se contabilizan un alza del 9%. Tan solo la
        semana pasada se presentaron 945 incidentes viales que dejaron 754 lesionados,
        según la autoridad de movilidad municipal. Para ver la noticia original consulte [aqui](https://www.elcolombiano.com/antioquia/cada-16-minutos-hay-un-lesionado-en-accidentes-en-medellin-JE18857295)
    """
    )

    st.header('🎬Video Promocional🎬')

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

if __name__ == "__main__":
    run()