Monitor de Análisis de Tendencias Financieras
Este repositorio contiene una solución técnica desarrollada en Python para el monitoreo y análisis de activos financieros en tiempo real. La aplicación procesa datos de mercado y genera visualizaciones interactivas de indicadores técnicos, facilitando la identificación de tendencias mediante el uso de computación científica y análisis de series temporales.

Arquitectura y Tecnologías
El proyecto ha sido desarrollado utilizando un stack tecnológico estándar en la industria de ciencia de datos y finanzas cuantitativas:

Lenguaje: Python 3.12+

Gestión de Datos: Pandas para el tratamiento de series temporales y normalización de estructuras de datos complejas (MultiIndex).

Ingesta de Datos: API de Yahoo Finance (yfinance) para la recuperación automatizada de datos históricos y actuales.

Visualización: Plotly Graph Objects para la renderización de gráficos interactivos de alta precisión.

Interfaz de Usuario: Streamlit para el despliegue de la aplicación web y gestión eficiente del estado de la sesión.

Características Técnicas
1. Procesamiento de Indicadores
La aplicación calcula dinámicamente la Media Móvil Simple (SMA) de 20 períodos. Este algoritmo permite suavizar la volatilidad del precio de cierre y extraer la dirección de la tendencia primaria de manera automatizada según el rango de tiempo seleccionado.

2. Optimización de Recursos
Se ha implementado una estrategia de almacenamiento en caché mediante decoradores de Streamlit (@st.cache_data). Esta técnica reduce significativamente la latencia en consultas repetitivas y minimiza el consumo de ancho de banda al limitar las peticiones a la API externa.

3. Visualización de Datos
El motor gráfico utiliza un renderizado interactivo que permite realizar operaciones de zoom, desplazamiento y lectura de datos puntuales (hover-tools). La interfaz ofrece versatilidad visual, permitiendo al usuario alternar entre modos de alto contraste (Oscuro), Claro o sincronización automática con el sistema operativo para garantizar legibilidad en cualquier entorno.
