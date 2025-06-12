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

st.sidebar.markdown("""---""")

tipos_cozinha = st.sidebar.multiselect(
    'Escolha os tipos de cozinha que Deseja visualizar as Informações',
    ['Italian', 'European', 'Asian', 'Filipino', 'American', 'Bakery',
       'Korean', 'Grill', 'Coffee', 'Pizza', 'Taiwanese', 'Japanese',
       'Latin American', 'Sushi', 'Ramen', 'Chinese', 'Desserts', 'Steak',
       'Seafood', 'Indian', 'Mexican', 'Burger', 'Singaporean',
       'Street Food', 'Vietnamese', 'Korean BBQ', 'Mediterranean',
       'Healthy Food', 'Cafe', 'Fast Food', 'French', 'Brazilian',
       'Argentine', 'Contemporary', 'Arabian', 'Tex-Mex', 'Bar Food',
       'International', 'German', 'North Eastern', 'Peruvian',
       'Ice Cream', 'Gourmet Fast Food', 'Vegetarian', 'Thai', 'Juices',
       'Beverages', 'Lebanese', 'Spanish', 'Author', 'BBQ', 'Mineira',
       'Mongolian', 'Portuguese', 'Tapas', 'Sandwich', 'Greek', 'Fusion',
       'Dumplings', 'Modern Australian', 'African', 'Coffee and Tea',
       'Cafe Food', 'Australian', 'Middle Eastern', 'Afghan', 'Malaysian',
       'Patisserie', 'Southern', 'Cajun', 'Pub Food', 'Diner',
       'Southwestern', 'New American', 'Breakfast', 'Bagels', 'Donuts',
       'Salad', 'Cuban', 'Caribbean', 'Taco', 'Dim Sum', 'Irish',
       'Turkish', 'Modern European', 'Canadian', 'Deli', 'Bubble Tea',
       'Kebab', 'Teriyaki', 'Eastern European', 'Soul Food',
       'New Mexican', 'Belgian', 'Polish', 'California', 'British', 'Tea',
       'Creole', 'Floribbean', 'Crepes', 'South American',
       'Fish and Chips', 'Others', "Po'Boys", 'Venezuelan', 'Ukrainian',
       'Moroccan', 'Hawaiian', 'Yum Cha', 'Pacific Northwest', 'Burmese',
       'Russian', 'Continental', 'South Indian', 'North Indian', 'Malay',
       'Cantonese', 'Western', 'Finger Food', 'Jamaican', 'Mandi',
       'Emirati', 'Mughlai', 'Biryani', 'Pakistani', 'Hyderabadi',
       'Kerala', 'Rajasthani', 'Gujarati', 'Poké', 'Nepalese', 'Goan',
       'Iranian', 'Indonesian', 'Bengali', 'Yemeni', 'Rolls', 'Momos',
       'Mithai', 'Wraps', 'Maharashtrian', 'Parsi', 'Modern Indian',
       'Andhra', 'Tibetan', 'Chettinad', 'Mishti', 'Israeli', 'Konkan',
       'Assamese', 'Naga', 'Awadhi', 'Lucknowi', 'Drinks Only',
       'Charcoal Chicken', 'Mangalorean', 'Egyptian', 'Roast Chicken',
       'Malwani', 'Armenian', 'Bihari', 'Himachali', 'Belanda', 'Dimsum',
       'Bakmi', 'Sunda', 'Asian Fusion', 'Sichuan', 'Fried Chicken',
       'Kiwi', 'Pacific', 'Hot Pot', 'Pan Asian', 'Teppanyaki', 'Pho',
       'Vegan', 'Balti', 'Scottish', 'Curry', 'Sri Lankan', 'Khaleeji',
       'South African', 'Durban', 'Ethiopian', 'World Cuisine',
       'Turkish Pizza', 'Izgara', 'Giblets', 'Home-made', 'Fresh Fish',
       'Restaurant Cafe', 'Kumpir', 'Döner', 'Ottoman',
       'Old Turkish Bars', 'Kokoreç', 'Eastern Anatolia', 'Börek'],
            default = [ 'Italian', 'Asian', 'Japanese', 'Pizza', 'Vegetarian'])
st.sidebar.markdown("""---""")

#filtro paises
df['Country'] = df['Country Code'].apply(country_name)
linhas_selecionadas = df['Country'].isin(qtd_paises)
df = df.loc[linhas_selecionadas, :]
#filtro tipos de cozinha
df['Cuisines'] = df['Cuisines'].fillna('').apply(lambda x: [c.strip() for c in x.split(',')])
linhas_selecionadas = df['Cuisines'].apply(lambda lista: any(cozinha in tipos_cozinha for cozinha in lista))
df = df.loc[linhas_selecionadas, :]
df_base = df.copy()

#========================================================
# Layout no Streamlit
#========================================================
st.title('🍽️ Visão Cozinhas')
st.subheader('Melhores restaurantes dos tipos culinários')

with st.container():
    df_temp = df_base.copy()
    df_temp['Cuisines'] = df_temp['Cuisines'].apply(lambda x: x if isinstance(x, list) else [x])
    df1_exploded = df_temp.explode('Cuisines')
    df1_exploded['Cuisines'] = df1_exploded['Cuisines'].str.strip()

    top_cuisines = (
        df1_exploded
        .groupby('Cuisines')['Restaurant Name']
        .count()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    df_top = df1_exploded[df1_exploded['Cuisines'].isin(top_cuisines)]

    colunas = ['Restaurant ID', 'Restaurant Name', 'City', 'Average Cost for two', 'Aggregate rating', 'Cuisines']
    df_resultado = df_top[colunas]

    st.dataframe(df_resultado)
st.sidebar.markdown("""---""")    

with st.container():
    df_temp = df_base.copy()
 
    df_temp['Cuisines'] = df_temp['Cuisines'].apply(lambda x: x if isinstance(x, list) else [x])

    df1_exploded = df_temp.explode('Cuisines')

    df1_exploded['Cuisines'] = df1_exploded['Cuisines'].astype(str).str.strip()
    top_cuisines = (
        df1_exploded
        .groupby('Cuisines')['Aggregate rating']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    # Criação do gráfico
    fig = px.bar(
        top_cuisines.reset_index(),
        x='Cuisines',
        y='Aggregate rating',
        title='Tipos de cozinha com as melhores Notas Médias',
        labels={'Cuisines': 'Tipos de Cozinha', 'Aggregate rating': 'Nota Média'},
        color='Cuisines',
        template='plotly_white'
    )

    fig.update_traces(width=0.8, textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
st.sidebar.markdown("""---""")   
 
with st.container():
    df_temp = df_base.copy()
 
    df_temp['Cuisines'] = df_temp['Cuisines'].apply(lambda x: x if isinstance(x, list) else [x])

    df1_exploded = df_temp.explode('Cuisines')

    df1_exploded['Cuisines'] = df1_exploded['Cuisines'].astype(str).str.strip()
    top_cuisines = (
        df1_exploded
        .groupby('Cuisines')['Aggregate rating']
        .mean()
        .sort_values(ascending=True)
        .head(10)
    )

    # Criação do gráfico
    fig = px.bar(
        top_cuisines.reset_index(),
        x='Cuisines',
        y='Aggregate rating',
        title='Tipos de Cozinha com Piores Notas',
        labels={'Cuisines': 'Tipos de Cozinha', 'Aggregate rating': 'Nota Média'},
        color='Cuisines',
        template='plotly_white'
    )

    fig.update_traces(width=0.8, textposition='outside')
    st.plotly_chart(fig, use_container_width=True)    