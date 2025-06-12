import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv('zomato.csv')
print(df.head())

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
st.header('🏙️  Visão Cidades')

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
    df1_aux = df.groupby('City')['Restaurant Name'].nunique().sort_values(ascending=False).reset_index().head(10)
    fig = px.bar(
        df1_aux,
        x='City',
        y='Restaurant Name',
        title='Top 10 cidades com mais restaurantes na base de Dados',
        labels={'City':'Cidades','Restaurant Name':'Quantidade de Restaurantes'},
        color='City',
        template='plotly_white'      
    )    
    fig.update_traces(width=0.8)  
    fig.update_traces(textposition='outside')  
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.markdown( """---""" )  
    col1, col2 = st.columns(2)
    with col1:
        df1_aux = df.groupby('City')['Aggregate rating'].mean().reset_index()
        df1_dados = df1_aux.sort_values(by='Aggregate rating').head(7)
        df1_dados['Aggregate rating'] = df1_dados['Aggregate rating'].round(2)
        fig = px.bar(
            df1_dados,
            x='City',
            y='Aggregate rating',
            title='Top 7 cidades com as piores médias de avaliação',
            labels={'City':'Cidades','Aggregate rating':'Nota média'},
            color='City',
            text='Aggregate rating',
            template='plotly_white'
        )        
        fig.update_traces(width=0.8)  
        fig.update_traces(textposition='outside')    
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        df1_aux = df.groupby('City')['Aggregate rating'].mean()
        df1_dados = df1_aux.sort_values(ascending=False).reset_index().head(7)
        df1_dados['Aggregate rating'] = df1_dados['Aggregate rating'].round(2)
        fig = px.bar(
            df1_dados,
            x='City',
            y='Aggregate rating',
            title='Top 7 cidades com as melhores médias de avaliação',
            labels={'City':'Cidades','Aggregate rating':'Nota média'},
            color='City',
            text='Aggregate rating',
            template='plotly_white'
        )        
        fig.update_traces(width=0.8)  
        fig.update_traces(textposition='outside')  
        st.plotly_chart(fig, use_container_width=True)
with st.container():
    df1_aux = df[['City','Cuisines']].copy()
    df1_aux['Cuisines'] = df1_aux['Cuisines'].str.split(',')
    df_aux = df1_aux.explode('Cuisines')
    df_grouped = df_aux.groupby('City')['Cuisines'].nunique()
    top = df_grouped.sort_values(ascending=False).head(10).reset_index()  
    fig = px.bar(
        top,
        x='City',
        y='Cuisines',
        title='top 10 cidades com mais tipos de culinarias distintos',
        labels={'City':'Cidades','Cuisines':'Tipos de comida'},
        color='City',
        text='Cuisines',
        template='plotly_white'
)        
fig.update_traces(width=0.8)  
fig.update_traces(textposition='outside')   
st.plotly_chart(fig, use_container_width=True)