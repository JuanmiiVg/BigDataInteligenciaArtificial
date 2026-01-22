"""
Frontend Streamlit para monitoreo en tiempo real
"""
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CONFIG STREAMLIT ==========
st.set_page_config(
    page_title="Monitoreo de Consumos",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .anomaly-card-critical {
        background-color: #ffe6e6;
        border-left: 4px solid #d62728;
    }
    .anomaly-card-high {
        background-color: #fff4e6;
        border-left: 4px solid #ff7f0e;
    }
    </style>
""", unsafe_allow_html=True)

# ========== CONFIG API ==========
# Backend REST API - usar nombre del servicio Docker para comunicación entre contenedores
API_BASE_URL = "http://backend:8000"

def hacer_request(endpoint: str):
    """Realiza una petición a la API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Error de conexión con la API. ¿Está corriendo el backend?")
        return None
    except Exception as e:
        st.error(f"❌ Error en la petición: {str(e)}")
        return None

# ========== PÁGINA PRINCIPAL ==========
def main():
    st.title("⚡ Sistema de Monitoreo de Consumo en Tiempo Real")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Opciones")
        page = st.radio(
            "Selecciona una página:",
            ["📊 Dashboard Principal", "🔍 Buscar Cliente", "📅 Consumo Mensual", "🚨 Anomalías", "📈 Análisis"]
        )
        
        st.markdown("---")
        auto_refresh = st.checkbox("🔄 Auto-actualizar (30s)", value=False)
        
        if auto_refresh:
            time.sleep(2)
            st.rerun()
    
    # Enrutar páginas
    if page == "📊 Dashboard Principal":
        page_dashboard()
    elif page == "🔍 Buscar Cliente":
        page_cliente()
    elif page == "📅 Consumo Mensual":
        page_mensual()
    elif page == "🚨 Anomalías":
        page_anomalias()
    elif page == "📈 Análisis":
        page_analisis()

def page_dashboard():
    """Dashboard principal"""
    st.header("📊 Dashboard Principal")
    
    # Resumen global
    datos_resumen = hacer_request("/api/estadisticas/resumen")
    
    if datos_resumen:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total Anomalías",
                datos_resumen.get('total_anomalias', 0),
                delta="últimas 24h"
            )
        
        with col2:
            st.metric(
                "🔴 Críticas",
                datos_resumen.get('anomalias_criticas', 0),
                delta=None
            )
        
        with col3:
            st.metric(
                "🟠 Altas",
                datos_resumen.get('anomalias_altas', 0)
            )
        
        with col4:
            st.metric(
                "🟡 Medias",
                datos_resumen.get('anomalias_medias', 0)
            )
        
        with col5:
            st.metric(
                "👥 Clientes Afectados",
                datos_resumen.get('clientes_afectados', 0)
            )
        
        st.markdown("---")
        
        # Tipos de anomalías más frecuentes
        tipos = datos_resumen.get('tipos_mas_frecuentes', [])
        if tipos:
            st.subheader("📊 Tipos de Anomalías Más Frecuentes")
            fig = px.bar(
                x=tipos,
                y=list(range(len(tipos), 0, -1)),
                orientation='h',
                labels={'x': 'Tipo de Anomalía', 'y': 'Frecuencia'},
                title="Anomalías Detectadas"
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Top clientes con anomalías
    st.subheader("🔝 Clientes con Más Anomalías")
    datos_top = hacer_request("/api/dashboard/top-anomalias?limit=10")
    
    if datos_top and datos_top.get('clientes'):
        df_top = pd.DataFrame(datos_top['clientes'])
        df_top = df_top.rename(columns={
            '_id': 'Cliente',
            'total_anomalias': 'Total Anomalías',
            'anomalias_criticas': 'Críticas'
        })
        
        # Colorear por severidad
        def color_row(row):
            if row['Críticas'] > 0:
                return ['background-color: #ffcccc'] * len(row)
            elif row['Total Anomalías'] > 5:
                return ['background-color: #fff3cd'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            df_top.style.apply(color_row, axis=1),
            use_container_width=True,
            height=400
        )

def page_cliente():
    """Búsqueda de cliente específico"""
    st.header("🔍 Búsqueda de Cliente")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        propietario_id = st.text_input(
            "ID del Cliente",
            value="CLI_00001",
            placeholder="Ej: CLI_00001"
        )
    
    with col2:
        buscar = st.button("🔍 Buscar", use_container_width=True)
    
    if buscar and propietario_id:
        # Obtener estadísticas del cliente
        stats = hacer_request(f"/api/estadisticas/cliente/{propietario_id}")
        
        if stats:
            # Métricas principales
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Consumo Promedio", f"{stats['consumo_promedio_24h']:.2f} kW")
            with col2:
                st.metric("Consumo Mínimo", f"{stats['consumo_minimo']:.2f} kW")
            with col3:
                st.metric("Consumo Máximo", f"{stats['consumo_maximo']:.2f} kW")
            with col4:
                st.metric("Anomalías Detectadas", stats['anomalias_detectadas'])
            with col5:
                sospechoso = "🚩 SÍ" if stats['es_cliente_sospechoso'] else "✅ NO"
                st.metric("Cliente Sospechoso?", sospechoso)
            
            st.markdown("---")
            
            # Gráfico de consumo 24h
            st.subheader("📈 Consumo Últimas 24 Horas")
            consumos = hacer_request(f"/api/consumos/últimas24h/{propietario_id}")
            
            if consumos:
                df_consumos = pd.DataFrame(consumos)
                df_consumos['timestamp'] = pd.to_datetime(df_consumos['timestamp'])
                df_consumos = df_consumos.sort_values('timestamp')
                
                fig = go.Figure()
                
                # Línea de consumo
                fig.add_trace(go.Scatter(
                    x=df_consumos['timestamp'],
                    y=df_consumos['consumo_kwh'],
                    mode='lines+markers',
                    name='Consumo (kW)',
                    line=dict(color='#1f77b4', width=2),
                    fill='tozeroy'
                ))
                
                # Marcar anomalías
                anomalias = df_consumos[df_consumos['anomalia_detectada'] == True]
                if not anomalias.empty:
                    fig.add_trace(go.Scatter(
                        x=anomalias['timestamp'],
                        y=anomalias['consumo_kwh'],
                        mode='markers',
                        name='Anomalías',
                        marker=dict(
                            size=12,
                            color=anomalias['score_anomalia'],
                            colorscale='Reds',
                            showscale=True,
                            colorbar=dict(title="Score")
                        )
                    ))
                
                fig.update_layout(
                    title="Consumo por Hora",
                    xaxis_title="Hora",
                    yaxis_title="Consumo (kW)",
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de anomalías del cliente
            st.subheader("⚠️ Anomalías Detectadas")
            anomalias_cliente = hacer_request(f"/api/anomalias/cliente/{propietario_id}?dias=7")
            
            if anomalias_cliente:
                df_anomalias = pd.DataFrame(anomalias_cliente)
                if not df_anomalias.empty:
                    df_anomalias = df_anomalias[[
                        'timestamp_consumo', 'consumo_kwh', 'hora',
                        'severidad', 'score_anomalia'
                    ]].head(20)
                    
                    st.dataframe(df_anomalias, use_container_width=True)
                else:
                    st.info("✅ No hay anomalías detectadas para este cliente")
            else:
                st.info("✅ No hay anomalías detectadas para este cliente")

def page_anomalias():
    """Página de anomalías detectadas"""
    st.header("🚨 Anomalías Detectadas")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        severidad = st.selectbox(
            "Filtrar por severidad:",
            ["Todas", "crítica", "alta", "media"]
        )
    
    with col2:
        horas = st.number_input("Últimas N horas:", value=24, min_value=1, max_value=720)
    
    # Obtener anomalías
    anomalias = None
    if severidad == "Todas":
        if st.button("Obtener Anomalías Críticas (últimas 24h)"):
            anomalias = hacer_request("/api/anomalias/críticas")
    else:
        anomalias = hacer_request(f"/api/anomalias/últimas?limit=100&severidad={severidad}")
    
    if anomalias:
        df = pd.DataFrame(anomalias)
        
        st.metric("Total de Anomalías", len(df))
        
        # Tabs
        tab1, tab2 = st.tabs(["📊 Tabla", "📈 Gráficos"])
        
        with tab1:
            st.dataframe(
                df.sort_values('score_anomalia', ascending=False),
                use_container_width=True,
                height=500
            )
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribución por severidad
                fig_sev = px.pie(
                    df,
                    names='severidad',
                    title="Distribución por Severidad"
                )
                st.plotly_chart(fig_sev, use_container_width=True)
            
            with col2:
                # Top tipos de anomalías
                tipos_count = {}
                for tipos_list in df['tipos_anomalia']:
                    for tipo in tipos_list:
                        tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
                
                df_tipos = pd.DataFrame(list(tipos_count.items()), columns=['Tipo', 'Cantidad'])
                fig_tipos = px.bar(df_tipos, x='Cantidad', y='Tipo', orientation='h')
                st.plotly_chart(fig_tipos, use_container_width=True)

def page_mensual():
    """Página de análisis mensual"""
    st.header("📅 Consumo Mensual")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        propietario_id = st.text_input(
            "ID del Cliente",
            value="CLI_00001",
            placeholder="Ej: CLI_00001"
        )
    
    with col2:
        mes = st.date_input(
            "Selecciona Mes",
            value=pd.Timestamp.now()
        )
    
    with col3:
        buscar = st.button("🔍 Buscar Mensual", use_container_width=True)
    
    if buscar and propietario_id and mes:
        mes_str = mes.strftime("%Y-%m")
        
        # Obtener datos mensuales
        stats_mensual = hacer_request(f"/api/estadisticas/mensual/{propietario_id}?mes={mes_str}")
        
        if stats_mensual:
            # Métricas principales
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Consumo Total", f"{stats_mensual.get('consumo_total', 0):.2f} kW")
            with col2:
                st.metric("Consumo Promedio", f"{stats_mensual.get('consumo_promedio', 0):.2f} kW")
            with col3:
                st.metric("Máximo", f"{stats_mensual.get('consumo_maximo', 0):.2f} kW")
            with col4:
                st.metric("Mínimo", f"{stats_mensual.get('consumo_minimo', 0):.2f} kW")
            with col5:
                st.metric("Anomalías", stats_mensual.get('anomalias_detectadas', 0))
            
            st.markdown("---")
            
            # Desglose de anomalías
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🔴 Críticas",
                    stats_mensual.get('anomalias_criticas', 0)
                )
            with col2:
                st.metric(
                    "🟠 Altas",
                    stats_mensual.get('anomalias_altas', 0)
                )
            with col3:
                st.metric(
                    "🟡 Medias",
                    stats_mensual.get('anomalias_medias', 0)
                )
            with col4:
                sospechoso = "🚩 SÍ" if stats_mensual.get('tiene_comportamiento_sospechoso') else "✅ NO"
                st.metric("Sospechoso?", sospechoso)
            
            st.markdown("---")
            
            # Gráficos
            st.subheader("📊 Análisis Mensual")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Consumo por tramo horario
                data = {
                    'Tramo': ['Noche\n(0-6, 23)', 'Valle\n(7-17)', 'Punta\n(18-22)'],
                    'Consumo': [
                        stats_mensual.get('consumo_noche_promedio', 0),
                        stats_mensual.get('consumo_promedio', 0),
                        stats_mensual.get('consumo_punta_promedio', 0)
                    ]
                }
                df_tramos = pd.DataFrame(data)
                fig = px.bar(df_tramos, x='Tramo', y='Consumo', title="Consumo por Tramo Horario")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Score de anomalía
                fig = go.Figure(data=[
                    go.Indicator(
                        mode="gauge+number+delta",
                        value=stats_mensual.get('avg_score_anomalia', 0),
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Score de Anomalía Promedio"},
                        delta={'reference': 0.5},
                        gauge={
                            'axis': {'range': [0, 1]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 0.33], 'color': "lightgray"},
                                {'range': [0.33, 0.66], 'color': "orange"},
                                {'range': [0.66, 1], 'color': "red"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 0.75
                            }
                        }
                    )
                ])
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Tabla de detalles
            st.subheader("📋 Detalles del Mes")
            detalles = {
                'Métrica': [
                    'Consumo Total (kW)',
                    'Consumo Promedio (kW)',
                    'Consumo Noche (kW)',
                    'Consumo Punta (kW)',
                    'Desviación Estándar',
                    'Score Anomalía Máximo',
                    'Score Anomalía Promedio',
                    'Registros'
                ],
                'Valor': [
                    f"{stats_mensual.get('consumo_total', 0):.3f}",
                    f"{stats_mensual.get('consumo_promedio', 0):.3f}",
                    f"{stats_mensual.get('consumo_noche_promedio', 0):.3f}",
                    f"{stats_mensual.get('consumo_punta_promedio', 0):.3f}",
                    f"{stats_mensual.get('consumo_desviacion', 0):.3f}",
                    f"{stats_mensual.get('max_score_anomalia', 0):.3f}",
                    f"{stats_mensual.get('avg_score_anomalia', 0):.3f}",
                    stats_mensual.get('num_registros', 0)
                ]
            }
            df_detalles = pd.DataFrame(detalles)
            st.dataframe(df_detalles, use_container_width=True)

def page_analisis():
    """Página de análisis avanzado"""
    st.header("📈 Análisis Avanzado")
    
    st.info("⏳ Análisis detallado de patrones de consumo y tendencias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Anomalías por Hora del Día")
        datos_resumen = hacer_request("/api/estadisticas/resumen")  # Última semana
        
        if datos_resumen:
            st.write(f"Total anomalías (últimos 7 días): {datos_resumen['total_anomalias']}")
            st.write(f"Clientes únicos afectados: {datos_resumen['clientes_afectados']}")
    
    with col2:
        st.subheader("⏱️ Anomalías por Período")
        periodo = st.radio("Selecciona período:", ["24h", "7 días", "30 días"])
        
        horas_map = {"24h": 24, "7 días": 168, "30 días": 720}
        datos = hacer_request(f"/api/estadisticas/resumen?horas={horas_map[periodo]}")
        
        if datos:
            st.metric("Anomalías", datos['total_anomalias'])
            st.metric("Críticas", datos['anomalias_criticas'])

if __name__ == "__main__":
    main()
