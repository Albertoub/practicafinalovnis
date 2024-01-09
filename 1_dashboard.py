import pandas as pd

import streamlit as st
import plotly.express as px

import matplotlib
from matplotlib.backends.backend_agg import RendererAgg

import requests
import seaborn as sns
@st.cache_data
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    mijson = r.json()
    listado = mijson['ufos']
    df = pd.DataFrame.from_records(listado) ## o listado o mijson

    return df

data = load_data('http://fastapi:8000/ufo_sightings')

# Título del Dashboard con estilo alien y color verde
st.markdown(
    """
    <style>
        h1 {
            color: #00ff00 !important;
            font-family: 'Alien', sans-serif !important;
            text-align: center !important;
        }
    </style>
    <h1>Análisis de Avistamientos de OVNIs alrededor del mundo</h1>
    """,
    unsafe_allow_html=True
)
#############################################################################################################

# Carga del conjunto de datos desde un archivo CSV

#############################################################################################################

# Calcular los países principales
top_countries = data['Country'].value_counts().head(5)

# Crear gráfico de barras horizontales centrado
fig_countries = px.bar(
    x=top_countries,
    y=top_countries.index,
    orientation='h',
    labels={'y': 'País', 'x': 'Cantidad de Avistamientos'},
    title='Top 5 Países con más Avistamientos de OVNIs'
)
fig_countries.update_layout(showlegend=False)  # Ocultar la leyenda

# Crear gráfico de pastel con Plotly y definir colores
colors = {'Summer': 'yellow', 'Winter': 'blue', 'Spring': 'green', 'Autumn': 'orange'}
fig_season = px.pie(
    data,
    names='Season',
    title='Estacionalidad de Avistamientos',
    labels={'Season': 'Estación del Año'},
    color_discrete_map=colors
)

# Usar las columnas de Streamlit para alinear los gráficos
col1, col2 = st.columns(2)

# Agregar el gráfico de barras en la primera columna
with col1:
    st.plotly_chart(fig_countries)

# Agregar el gráfico de pastel en la segunda columna
with col2:
    st.plotly_chart(fig_season)

###################################################################################################################

# Widget interactivo para filtrar por país
country_filter = st.selectbox('Seleccionar país:', data['Country'].unique())

# Crear medidor (gauge) para la cantidad de avistamientos en el país seleccionado
st.subheader(f'Cantidad de avistamientos en {country_filter}')
sightings_in_selected_country = data['Country'].value_counts().get(country_filter, 0)
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=sightings_in_selected_country,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': 'Avistamientos'},
    gauge={'axis': {'range': [None, max(data['Country'].value_counts())]}}
))

# Crear un gráfico de histograma con Plotly
fig_histogram = px.histogram(data, x='Hour', title='Número de Avistamientos por Hora', labels={'Hour': 'Hora', 'count': 'Número de Avistamientos'})

# Ajustar el tamaño del gráfico y permitir el ajuste automático
fig_histogram.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=20),  # Ajusta los márgenes para centrar el gráfico
)

# Usar columns para mostrar el widget y los gráficos en la misma fila
col1, col2 = st.columns(2)

# Agregar el widget interactivo en la primera columna
with col1:
    st.plotly_chart(fig_gauge)

# Agregar el gráfico de histograma en la segunda columna
with col2:
    st.subheader('Comparación de avistamientos entre horas')
    st.plotly_chart(fig_histogram)


###################################################################################################
# Mostrar la tabla de datos filtrados por país
st.subheader(f'Detalles de avistamientos en {country_filter}')
filtered_data = data[data['Country'] == country_filter]
st.write(filtered_data)

#############################################################################################################

#############################################################################################################

# Sección de Duración y Descripción de los Avistamientos
st.header('Forma de los Avistamientos')
st.subheader('Forma de los OVNIs')
st.bar_chart(data['UFO_shape'].value_counts())


#############################################################################################################

# Título de la sección
st.header('Descripciones de los Avistamientos')

# Configuración para mostrar un número limitado de filas de la tabla inicialmente
num_rows_to_display = st.number_input('Número de descripciones a mostrar:', value=10, min_value=1)

# Crear una tabla con las descripciones
st.table(data['Description'].head(num_rows_to_display))

# Botón para mostrar más descripciones
if len(data['Description']) > num_rows_to_display:
    show_more = st.button('Mostrar más descripciones')
    if show_more:
        num_rows_to_display = st.number_input('Número adicional de descripciones a mostrar:', value=10, min_value=1)
        st.table(data['Description'][:num_rows_to_display])



registros = str(df_merged.shape[0])
adjudicatarios = str(len(df_merged.adjuducatario.unique()))
centro = str(len(df_merged.centro_seccion.unique()))
tipologia = str(len(df_merged.tipo.unique()))
presupuesto_medio = str(round(df_merged.presupuesto_con_iva.mean(),2))
adjudicado_medio = str(round(df_merged.importe_adj_con_iva.mean(),2))

sns.set_palette("pastel")


st.header("Información general")

col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)
with col1:
    col1.subheader('# contratos')
    info_box(registros)
with col2:
    col2.subheader('# adjudicatarios')
    info_box(adjudicatarios)
with col3:
    col3.subheader('# centros')
    info_box(centro)

with col4:
    col4.subheader('# tipologias')
    info_box(tipologia)

## Clases de medios digitales de publicacion
with col5:
    col5.subheader('# presupuesto medio')
    info_box(presupuesto_medio, col5)
with col6:
    ## publicaciones
    col6.subheader('# importe medio adjud')
    info_box(adjudicado_medio, col6)

# with st.beta_container('Información general sobre obras')
#        datos = df_merged[['id', 'agno_i', 'clasemicro1']]
tab1, tab2 = st.tabs(["Procedimientos negociados sin publicidad", "Distribución de importe en procedimiento Negociado sin publicidad"])

fig1 = px.scatter(df_merged,x='importe_adj_con_iva',y='presupuesto_con_iva',size='numlicit',color='procedimiento')

fig2 = px.box(df_merged.query("procedimiento == 'Negociado sin publicidad'"),x='importe_adj_con_iva')
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig2, theme=None, use_container_width=True)
