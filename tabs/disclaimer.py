import streamlit as st

def show_disclaimer():
    """显示免责声明页面内容"""
    st.title("Disclaimer")

    st.markdown("""
    ## Disclaimer

    This non-profit server and its associated data and services are intended solely for academic and research purposes.
     The Protein Structure and Bioinformatics Group at Lund University endeavors to provide high-quality tools and datasets;
      however, we do not accept responsibility for the outcomes derived from the use of this server, including any results, analyses, or interpretations.

    ## Liability

    While every effort has been made to ensure the accuracy and timeliness of the information provided on this site, 
    no warranties—explicit or implied—are given regarding its correctness, completeness, 
    or suitability for any specific purpose. 
    Users agree that Lund University and its staff or affiliates bear no liability for any direct, indirect, incidental, or consequential damages arising from the use of this service. 
    Use of any process, method, or product based on this site’s content is at the user’s own risk.
    """)
