"""
AgriSense - Sistema de Automação Agrícola
Dashboard principal para monitoramento e controle em tempo real
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from streamlit_autorefresh import st_autorefresh

# Configuração da página
st.set_page_config(
    page_title="AgriSense - Automação Agrícola",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh a cada 5 segundos (5000ms)
st_autorefresh(interval=5000, key="datarefresh")

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-ok {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-warning {
        color: #FF9800;
        font-weight: bold;
    }
    .status-critical {
        color: #F44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌾 AgriSense - Sistema de Automação Agrícola</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2E7D32/FFFFFF?text=AgriSense", use_container_width=True)
    st.markdown("### 📊 Painel de Controle")
    
    # Seleção de área
    area_selecionada = st.selectbox(
        "Selecione a Área:",
        ["Área 1 - Soja", "Área 2 - Milho", "Área 3 - Trigo", "Área 4 - Café"]
    )
    
    st.markdown("---")
    
    # Status do sistema
    st.markdown("### 🔧 Status do Sistema")
    st.markdown("🟢 Sensores: **Online**")
    st.markdown("🟢 Protocolo CAN: **Ativo**")
    st.markdown("🟢 ISOBUS: **Conectado**")
    st.markdown("🟢 GPS: **Sinal Forte**")
    
    st.markdown("---")
    
    # Informações do projeto
    st.markdown("### ℹ️ Sobre")
    st.info("""
    **AgriSense v1.0**
    
    Sistema de automação para agricultura de precisão com:
    - Monitoramento em tempo real
    - Protocolo CAN/ISOBUS
    - Controle de irrigação
    - Análise de solo
    """)
    
    st.markdown("---")
    st.markdown("👨‍💻 **Desenvolvido por:** Daniel")
    st.markdown("📅 **Data:** " + datetime.now().strftime("%d/%m/%Y"))

# Função para gerar dados simulados
def gerar_dados_sensores():
    import random
    
    return {
        'temperatura': round(random.uniform(20, 35), 1),
        'umidade_ar': round(random.uniform(40, 80), 1),
        'umidade_solo': round(random.uniform(30, 70), 1),
        'nitrogenio': round(random.uniform(10, 50), 1),
        'fosforo': round(random.uniform(5, 30), 1),
        'potassio': round(random.uniform(15, 60), 1),
        'ph_solo': round(random.uniform(5.5, 7.5), 2),
        'luminosidade': round(random.uniform(500, 1000), 0)
    }

# Gerar dados
dados = gerar_dados_sensores()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌡️ Temperatura",
        value=f"{dados['temperatura']}°C",
        delta=f"{round(dados['temperatura'] - 25, 1)}°C"
    )

with col2:
    st.metric(
        label="💧 Umidade do Solo",
        value=f"{dados['umidade_solo']}%",
        delta=f"{round(dados['umidade_solo'] - 50, 1)}%"
    )

with col3:
    st.metric(
        label="🌫️ Umidade do Ar",
        value=f"{dados['umidade_ar']}%",
        delta=f"{round(dados['umidade_ar'] - 60, 1)}%"
    )

with col4:
    st.metric(
        label="🧪 pH do Solo",
        value=f"{dados['ph_solo']}",
        delta=f"{round(dados['ph_solo'] - 6.5, 2)}"
    )

st.markdown("---")

# Tabs para diferentes seções
tab1, tab2, tab3, tab4 = st.tabs(["📊 Monitoramento", "🚜 Atuadores", "📡 Protocolos", "🗺️ Mapa de Calor"])

with tab1:
    st.markdown("### 📊 Monitoramento em Tempo Real")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Gráfico de nutrientes
        st.markdown("#### 🧪 Níveis de Nutrientes (NPK)")
        
        nutrientes = pd.DataFrame({
            'Nutriente': ['Nitrogênio', 'Fósforo', 'Potássio'],
            'Valor': [dados['nitrogenio'], dados['fosforo'], dados['potassio']],
            'Ideal_Min': [20, 10, 25],
            'Ideal_Max': [40, 25, 50]
        })
        
        fig_nutrientes = go.Figure()
        fig_nutrientes.add_trace(go.Bar(
            name='Valor Atual',
            x=nutrientes['Nutriente'],
            y=nutrientes['Valor'],
            marker_color=['#4CAF50', '#2196F3', '#FF9800']
        ))
        
        fig_nutrientes.update_layout(
            height=300,
            showlegend=False,
            yaxis_title="Concentração (mg/kg)",
            template="plotly_white"
        )
        
        st.plotly_chart(fig_nutrientes, use_container_width=True)
    
    with col_right:
        # Gráfico de temperatura e umidade
        st.markdown("#### 🌡️ Condições Ambientais")
        
        # Criar dados históricos simulados
        horas = [(datetime.now() - timedelta(hours=i)).strftime("%H:%M") for i in range(12, -1, -1)]
        temps = [round(dados['temperatura'] + (i - 6) * 0.5, 1) for i in range(13)]
        umidades = [round(dados['umidade_solo'] + (i - 6) * 1.2, 1) for i in range(13)]
        
        fig_ambiente = go.Figure()
        
        fig_ambiente.add_trace(go.Scatter(
            x=horas,
            y=temps,
            mode='lines+markers',
            name='Temperatura (°C)',
            line=dict(color='#FF5722', width=2)
        ))
        
        fig_ambiente.add_trace(go.Scatter(
            x=horas,
            y=umidades,
            mode='lines+markers',
            name='Umidade Solo (%)',
            line=dict(color='#2196F3', width=2),
            yaxis='y2'
        ))
        
        fig_ambiente.update_layout(
            height=300,
            yaxis=dict(title='Temperatura (°C)'),
            yaxis2=dict(title='Umidade (%)', overlaying='y', side='right'),
            template="plotly_white",
            legend=dict(x=0, y=1.1, orientation='h')
        )
        
        st.plotly_chart(fig_ambiente, use_container_width=True)

with tab2:
    st.markdown("### 🚜 Controle de Atuadores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💧 Sistema de Irrigação")
        
        irrigacao_status = st.toggle("Irrigação Automática", value=True)
        
        if irrigacao_status:
            st.success("✅ Sistema de irrigação ATIVO")
            vazao = st.slider("Vazão (L/min)", 0, 100, 45)
            st.info(f"💦 Vazão atual: **{vazao} L/min**")
        else:
            st.warning("⏸️ Sistema de irrigação PAUSADO")
        
        st.markdown("---")
        
        st.markdown("**📊 Estatísticas de Irrigação:**")
        st.write(f"- Tempo de operação hoje: **4h 23min**")
        st.write(f"- Volume total: **12.450 L**")
        st.write(f"- Próxima irrigação: **{(datetime.now() + timedelta(hours=6)).strftime('%H:%M')}**")
    
    with col2:
        st.markdown("#### 🌱 Sistema de Fertilização")
        
        fertilizacao_status = st.toggle("Fertilização Automática", value=False)
        
        if fertilizacao_status:
            st.success("✅ Sistema de fertilização ATIVO")
            
            npk_tipo = st.selectbox("Tipo de Fertilizante:", ["NPK 20-10-10", "NPK 10-20-20", "NPK 15-15-15"])
            taxa_aplicacao = st.slider("Taxa de Aplicação (kg/ha)", 0, 200, 80)
            
            st.info(f"🌱 Aplicando: **{npk_tipo}** a **{taxa_aplicacao} kg/ha**")
        else:
            st.info("⏸️ Sistema de fertilização em STANDBY")
        
        st.markdown("---")
        
        st.markdown("**📊 Estatísticas de Fertilização:**")
        st.write(f"- Última aplicação: **há 3 dias**")
        st.write(f"- Total aplicado (mês): **2.4 toneladas**")
        st.write(f"- Próxima aplicação: **{(datetime.now() + timedelta(days=4)).strftime('%d/%m/%Y')}**")

with tab3:
    st.markdown("### 📡 Monitoramento de Protocolos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔌 Protocolo CAN Bus")
        
        st.code("""
CAN ID: 0x18FF5017
Status: ACTIVE
Baudrate: 250 kbps
Mensagens/seg: 87
Erros: 0
        """, language="text")
        
        st.progress(0.87, text="Taxa de utilização do bus: 87%")
        
        st.markdown("**Últimas mensagens CAN:**")
        st.text("0x123 -> [01 02 03 04 05 06 07 08]")
        st.text("0x456 -> [FF EE DD CC BB AA 99 88]")
        st.text("0x789 -> [12 34 56 78 9A BC DE F0]")
    
    with col2:
        st.markdown("#### 🚜 Protocolo ISOBUS")
        
        st.code("""
ECU Name: AgriSense Control Unit
Address: 0xF4
Task Controller: CONNECTED
Implement Type: Sprayer
Working State: ACTIVE
        """, language="text")
        
        st.markdown("**Comandos ISOBUS Ativos:**")
        
        comandos_df = pd.DataFrame({
            'Comando': ['SET_WORKSTATE', 'SET_VALUE', 'REQUEST_DATA'],
            'Status': ['✅ OK', '✅ OK', '⏳ Processando'],
            'Timestamp': ['14:23:45', '14:23:46', '14:23:47']
        })
        
        st.dataframe(comandos_df, use_container_width=True, hide_index=True)

with tab4:
    st.markdown("### 🗺️ Mapa de Calor - Produtividade")
    
    st.info("🚧 **Em desenvolvimento:** Integração com GPS para mapeamento de produtividade por zona")
    
    # Simulação de mapa de calor
    import numpy as np
    
    # Criar dados simulados de produtividade
    x = np.linspace(0, 100, 20)
    y = np.linspace(0, 100, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X/10) * np.cos(Y/10) * 50 + 50
    
    fig_mapa = go.Figure(data=go.Heatmap(
        z=Z,
        x=x,
        y=y,
        colorscale='RdYlGn',
        colorbar=dict(title="Produtividade<br>(sacas/ha)")
    ))
    
    fig_mapa.update_layout(
        title="Mapa de Produtividade - Área Selecionada",
        xaxis_title="Longitude (m)",
        yaxis_title="Latitude (m)",
        height=500
    )
    
    st.plotly_chart(fig_mapa, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Produtividade Média", "68.5 sc/ha")
    
    with col2:
        st.metric("🏆 Zona Mais Produtiva", "85.2 sc/ha")
    
    with col3:
        st.metric("⚠️ Zona Menos Produtiva", "42.1 sc/ha")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🌾 <strong>AgriSense - Sistema de Automação Agrícola</strong></p>
        <p>Desenvolvido para demonstração de sistemas embarcados em agricultura de precisão</p>
        <p>📧 Contato: daniel@agrisense.com | 🌐 GitHub: github.com/Daniel-1984</p>
    </div>
""", unsafe_allow_html=True)