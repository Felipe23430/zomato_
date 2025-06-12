import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv('zomato.csv')


# ------------------------------ funções -------------------------------------


#  Preenchimento do nome dos países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]


#========================================================
# Barra lateral
#========================================================
st.header('🌍 Visão Países')

st.sidebar.header(' Zomato.com')
st.sidebar.markdown('## For the love of Food')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Filtros')
qtd_paises = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar as Informações',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
     'Canada', 'Singapure', 'United Arab Emirates', 'India',
     'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
     'Sri Lanka', 'Turkey'],
        default = ['India', 'United States of America','England','Turkey','South Africa' ])

#filtro paises
df['Country'] = df['Country Code'].apply(country_name)
linhas_selecionadas = df['Country'].isin(qtd_paises)
df = df.loc[linhas_selecionadas, :]

#========================================================
# Layout no Streamlit
#========================================================
with st.container():
        df['Country'] = df['Country Code'].apply(country_name)
        df1_aux = df.groupby('Country')['Restaurant ID'].nunique().reset_index(name='Quantidade de Restaurantes')
        fig =px.bar(
        df1_aux,
        x='Country',
        y='Quantidade de Restaurantes',
        title='Quantidade de Restaurantes por País',
        labels={'Country': 'País', 'Restaurant Count': 'Quantidade de Restaurantes'},
        color='Country',            
        template='plotly_white'     
)
fig.update_traces(width=0.8)     
fig.update_traces(textposition='outside') 
st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown( """---""" )  
    df['Country'] = df['Country Code'].apply(country_name)
    df1_aux = df.groupby('Country')['City'].nunique().reset_index(name= 'Cidades')
    fig =px.bar(
        df1_aux,
        x='Country',
        y='Cidades',
        title='Quantidade de Cidades por País',
        labels={'Country': 'País'},
        color='Country',            
        template='plotly_white'     
)
fig.update_traces(width=0.8)  
fig.update_traces(textposition='outside')
st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown( """---""" )  
    df['Country'] = df['Country Code'].apply(country_name)
    df1_aux = df.groupby('Country')['Votes'].mean().reset_index(name='Avaliações')
    fig =px.bar(
        df1_aux,
        x='Country',
        y='Avaliações',
        title='Média de avaliações feitas por País',
        labels={'Country': 'País'},
        color='Country',            
        template='plotly_white'     
)
fig.update_traces(width=0.8)  
fig.update_traces(textposition='outside')  
st.plotly_chart(fig, use_container_width=True)

with st.container():
    df1_aux = df.groupby('Country Code')['Average Cost for two'].mean().reset_index()
    # Adicionar coluna com nome do país usando sua função
    df1_aux['Country'] = df1_aux['Country Code'].apply(country_name)
    # Arredondar os valores para 2 casas decimais
    df1_aux['Average Cost for two'] = df1_aux['Average Cost for two'].round(2)
    # Reorganizar as colunas
    df1_aux = df1_aux[['Country', 'Average Cost for two']]
    # Criar o gráfico
    fig = px.bar(
        df1_aux,
        x='Country',
        y='Average Cost for two',
        title='Preço médio para dois por país',
        text='Average Cost for two',
        labels={'Average Cost for two': 'Custo Médio', 'Country': 'País'},
        template='plotly_white'
    )

fig.update_yaxes(type='log')
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)
