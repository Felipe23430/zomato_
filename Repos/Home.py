import streamlit as st
import pandas as pd
df = pd.read_csv('zomato.csv')
st.set_page_config(page_title='Main page', page_icon='📊')

#------------------------------------------------------------

st.sidebar.header(' Zomato.com')
st.sidebar.markdown('## For the love of Food')
st.sidebar.markdown("""---""")

#------------------------------------------------------------
st.title('Zomato.com')
st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')


with st.container():
    col1, col2, col3, col4 = st.columns(4, gap='large')
    with col1:
        total = len(df['Restaurant ID'].unique())
        col1.metric('Qtd. Restaurantes', total )
    with col2:
        total2 = len(df['Country Code'].unique())
        col2.metric('Países Cadastrados', total2)
    with col3:    
        total3=len(df['City'].unique())
        col3.metric('Cidades cadastradas', total3)
    with col4:
        df1_temp = df.copy()
        df1_temp['Cuisines'] = df1_temp['Cuisines'].str.split(',')
        df1_aux = df1_temp.explode('Cuisines')
        df1_aux['Cuisines'] = df1_aux['Cuisines'].str.strip()
        total4 = len(df1_aux['Cuisines'].unique())
        col4.metric('Tipos Cozinha', total4) 
        
        
with st.container():
    st.title('Guia de Uso do Painel de Análise')

    st.subheader('🌍 Visão por Países')
    st.markdown('Veja métricas gerais sobre o alcance dos restaurantes em diferentes países.')
        
    st.subheader('🏙️ Visão por Cidades')
    st.markdown('Explore dados sobre o comportamento dos clientes em diversas cidades.')

    st.subheader('🍽️ Visão por Tipos de Cozinha')
    st.markdown('Analise a variedade e a popularidade das categorias de culinária.')