import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Configuración de la página (esto hace que use todo el ancho)
st.set_page_config(layout="wide", page_title="Monitor Financiero - SMA")

st.title("Panel de Análisis Técnico (Media Móvil)")

# --- SIDEBAR: Configuración del Usuario ---
st.sidebar.header("Configuración")
ticker_simbolo = st.sidebar.selectbox(
    "Selecciona un Activo", 
    ["BTC-USD", "ETH-USD", "AAPL", "TSLA", "MSFT", "GOOGL"]
)

rango = st.sidebar.selectbox(
    "Rango de Tiempo",
    options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    format_func=lambda x: {"1mo":"1 Mes", "3mo":"3 Meses", "6mo":"6 Meses", "1y":"1 Año", "2y":"2 Años", "5y":"5 Años"}[x]
)

# --- OBTENCIÓN DE DATOS ---
@st.cache_data(ttl=3600) # Optimización: datos frescos cada hora
def cargar_datos(simbolo, periodo):
    df = yf.download(simbolo, period=periodo, interval="1d")
    # Calculamos la Media Móvil Simple (SMA) de 20 días
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    # Limpieza de columnas MultiIndex para yfinance moderno
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

data = cargar_datos(ticker_simbolo, rango)

# --- CREACIÓN DEL GRÁFICO (SOLO SMA) ---
# Creamos una figura vacía
fig = go.Figure()

# !!! AQUÍ ESTÁ EL CAMBIO PRINCIPAL !!!
# He ELIMINADO por completo el bloque "fig.add_trace(go.Candlestick(...))"

# 1. Agregar SOLO la Media Móvil (SMA 20) como una línea Scatter
# Usamos Scatter con mode='lines' para dibujar una línea continua
fig.add_trace(go.Scatter(
    x=data.index,
    y=data['SMA20'],
    mode='lines', # Especificamos que es solo línea
    line=dict(color='orange', width=2), # Línea naranja profesional
    name='SMA 20 períodos'
))

# --- ESTÉTICA DEL GRÁFICO ---
fig.update_layout(
    title=f"Gráfico de Media Móvil (SMA 20): {ticker_simbolo}",
    yaxis_title="Precio (USD)",
    xaxis_title="Fecha",
    template="plotly_dark", # Fondo oscuro para que se vea más profesional
    xaxis_rangeslider_visible=False, # Quitamos el slider de abajo
    height=600
)

# --- MOSTRAR EN STREAMLIT ---
# Mostramos métricas rápidas ARRIBA del gráfico
col1, col2, col3 = st.columns(3)

# --- CORRECCIÓN DE SINTAXIS EN MÉTRICAS ---
# Usamos la sintaxis correcta .iloc[-1] para obtener el último valor numérico
try:
    ultimo_precio = float(data['Close'].iloc[-1])
    precio_apertura = float(data['Open'].iloc[-1])
    # Aseguramos que los valores sean números simples, no Series
    if isinstance(ultimo_precio, pd.Series): ultimo_precio = ultimo_precio.item()
    if isinstance(precio_apertura, pd.Series): precio_apertura = precio_apertura.item()
    
    variacion = ultimo_precio - precio_apertura

    col1.metric("Precio Actual", f"${ultimo_precio:,.2f}")
    # Añadimos delta para mostrar la flechita de variación
    col2.metric("Variación del Día", f"${variacion:,.2f}", delta=f"{variacion:,.2f}")
    col3.metric("Activo", ticker_simbolo)
except Exception as e:
    st.error(f"Error al calcular métricas: {e}")

# El gráfico con la nueva sintaxis de ancho (stretch para 2026)
st.plotly_chart(fig, width="stretch")

# Tabla histórica corregida
with st.expander("Ver datos históricos (Tabla)"):
    df_tabla = data.copy()
    # Doble verificación de columnas MultiIndex
    if isinstance(df_tabla.columns, pd.MultiIndex):
        df_tabla.columns = df_tabla.columns.get_level_values(0)
    
    # Seleccionamos las columnas clave, incluyendo la SMA20
    cols = [c for c in ['Open', 'High', 'Low', 'Close', 'SMA20'] if c in df_tabla.columns]
    
    st.dataframe(
        df_tabla[cols].sort_index(ascending=False), 
        width="stretch" # Actualizado para 2026
    )
