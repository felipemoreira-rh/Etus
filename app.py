import streamlit as st
import pandas as pd
from datetime import date

# ── CONFIGURAÇÃO DA PÁGINA ──
st.set_page_config(
    page_title="ETUS · Sistema RH",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── INJEÇÃO DE CSS (Baseado no seu HTML) ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset e Variáveis */
:root {
  --bg: #eef1f7; --txt: #131929; --mut: #6b7a9a; --blue: #1a56db;
  --green: #0a7a3c; --amber: #b45309; --red: #c0392b;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Ocultar elementos padrão do Streamlit */
#MainMenu, footer, header {display: none !important;}

/* Sidebar Estilizada */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Estilo dos Botões da Sidebar */
.stButton > button {
    width: 100% !important;
    text-align: left !important;
    background-color: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid transparent !important;
    border-radius: 7px !important;
    padding: 8px 16px !important;
    font-size: 13px !important;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: rgba(255,255,255,0.05) !important;
    color: #fff !important;
}

.stButton > button[kind="primary"] {
    background-color: rgba(26,86,219,0.2) !important;
    color: #60a5fa !important;
    border-left: 3px solid #60a5fa !important;
    border-radius: 0 7px 7px 0 !important;
}

/* Componentes de UI (KPIs e Painéis) */
.kc-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid rgba(0,0,0,0.07);
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    margin-bottom: 10px;
}

.kc-label { font-size: 10px; text-transform: uppercase; color: var(--mut); font-weight: 700; letter-spacing: 1px; }
.kc-value { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: var(--txt); }

.bdg { font-size: 10px; padding: 2px 8px; border-radius: 20px; font-weight: 600; }
.bdg-blue { background: #ebf1fd; color: #1a56db; }
</style>
""", unsafe_allow_html=True)

# ── INICIALIZAÇÃO DO ESTADO (STATE) ──
if "modulo" not in st.session_state: st.session_state.modulo = "RH"
if "pagina" not in st.session_state: st.session_state.pagina = "Indicadores"

# ── COMPONENTES REUTILIZÁVEIS ──
def draw_kpi(label, value, trend="", color="blue"):
    st.markdown(f"""
        <div class="kc-card">
            <div class="kc-label">{label}</div>
            <div class="kc-value">{value}</div>
            <div style="color: {color}; font-size: 11px; font-weight: 600;">{trend}</div>
        </div>
    """, unsafe_allow_html=True)

# ── FUNÇÕES DAS PÁGINAS (CONTEÚDO) ──

def pg_indicadores():
    st.markdown("### ◈ Indicadores de Recrutamento")
    c1, c2, c3, c4 = st.columns(4)
    with c1: draw_kpi("Vagas Abertas", "12", "↔ Estável", "#1a56db")
    with c2: draw_kpi("Candidatos", "217", "↑ +12% mês", "#0a7a3c")
    with c3: draw_kpi("Tempo Médio", "24d", "⚠ Meta: 30d", "#b45309")
    with c4: draw_kpi("Taxa Aprovação", "3.7%", "↑ +0.4pp", "#6d28d9")
    
    st.markdown("#### Funil de Recrutamento")
    st.info("Aqui entram os gráficos de barras e tabelas de performance do seu HTML.")

def pg_vagas():
    st.markdown("### 📋 Gestão de Vagas")
    vagas = [
        {"titulo": "Gerente de Operações", "time": "Operações", "status": "Ativa", "prioridade": "Alta"},
        {"titulo": "Analista Financeiro Sr.", "time": "Financeiro", "status": "Ativa", "prioridade": "Média"},
    ]
    for v in vagas:
        with st.container():
            st.markdown(f"""
            <div class="kc-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-weight:700; font-size:14px;">{v['titulo']}</div>
                        <div style="font-size:12px; color:gray;">{v['time']}</div>
                    </div>
                    <span class="bdg bdg-blue">{v['prioridade']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def pg_dp_dashboard():
    st.markdown("### ◈ Dashboard DP")
    st.write("Visão geral de colaboradores, contratos e benefícios.")

# ── SIDEBAR (NAVEGAÇÃO) ──
with st.sidebar:
    st.markdown('<div style="font-family:Syne; font-size:24px; font-weight:800; color:#60a5fa; padding-bottom:20px;">● ETUS</div>', unsafe_allow_html=True)
    
    # Seleção de Módulos (Estilo Abas)
    st.markdown('<p style="font-size:10px; color:#4b5563; font-weight:700; text-transform:uppercase;">Módulos</p>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    if m1.button("👥 RH", type="primary" if st.session_state.modulo == "RH" else "secondary"):
        st.session_state.modulo = "RH"
        st.session_state.pagina = "Indicadores"
        st.rerun()
    if m2.button("📋 DP", type="primary" if st.session_state.modulo == "DP" else "secondary"):
        st.session_state.modulo = "DP"
        st.session_state.pagina = "Dashboard DP"
        st.rerun()
    if m3.button("💰 FIN", type="primary" if st.session_state.modulo == "FIN" else "secondary"):
        st.session_state.modulo = "FIN"
        st.rerun()

    st.markdown("---")
    
    # Navegação Dinâmica conforme o Módulo
    st.markdown('<p style="font-size:10px; color:#4b5563; font-weight:700; text-transform:uppercase;">Menu</p>', unsafe_allow_html=True)
    
    if st.session_state.modulo == "RH":
        menu = [("Indicadores", "◈ Indicadores"), ("Vagas", "📋 Vagas"), ("Candidatos", "⚙ Candidatos"), ("Onboarding", "🚀 Onboarding")]
    elif st.session_state.modulo == "DP":
        menu = [("Dashboard DP", "◈ Dashboard"), ("Colaboradores", "👥 Colaboradores"), ("Estagiários", "🎓 Estagiários")]
    else:
        menu = [("iFood", "🍔 iFood")]

    for id_pag, label in menu:
        if st.button(label, type="primary" if st.session_state.pagina == id_pag else "secondary"):
            st.session_state.pagina = id_pag
            st.rerun()

# ── ROTEAMENTO DE CONTEÚDO (MAIN AREA) ──
if st.session_state.pagina == "Indicadores":
    pg_indicadores()
elif st.session_state.pagina == "Vagas":
    pg_vagas()
elif st.session_state.pagina == "Dashboard DP":
    pg_dp_dashboard()
else:
    st.title(st.session_state.pagina)
    st.write(f"Conteúdo da página {st.session_state.pagina} em desenvolvimento.")
