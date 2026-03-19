import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="ETUS · Sistema RH",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS — força tema claro, legível em qualquer ambiente ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Reset e base ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    color: #131929 !important;
    background-color: #eef1f7 !important;
}

/* ── Esconde elementos Streamlit ── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] {
    display: none !important;
    visibility: hidden !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(255,255,255,.08) !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #94a3b8 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.08) !important;
}
/* Botões da sidebar */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 7px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-align: left !important;
    transition: all .15s !important;
    width: 100% !important;
    padding: 6px 10px !important;
    height: auto !important;
    min-height: 36px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,.08) !important;
    color: #e2e8f0 !important;
    border-color: rgba(255,255,255,.2) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(26,86,219,.35) !important;
    color: #93c5fd !important;
    border-color: rgba(96,165,250,.4) !important;
    font-weight: 600 !important;
}

/* ── Área de conteúdo principal ── */
.main .block-container {
    padding: 20px 28px 40px 28px !important;
    max-width: 100% !important;
    background: #eef1f7 !important;
}

/* ── Títulos de página ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #131929 !important;
    font-weight: 700 !important;
}
h2 { font-size: 22px !important; margin-bottom: 4px !important; }

/* ── Botões principais ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    height: 36px !important;
    transition: all .15s !important;
    cursor: pointer !important;
    border: 1px solid rgba(0,0,0,.12) !important;
    background: #ffffff !important;
    color: #374151 !important;
}
.stButton > button[kind="primary"] {
    background: #1a56db !important;
    border-color: #1a56db !important;
    color: #ffffff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1744b0 !important;
    box-shadow: 0 2px 8px rgba(26,86,219,.35) !important;
}
.stButton > button:hover {
    border-color: rgba(0,0,0,.22) !important;
    background: #f8faff !important;
}

/* ── Inputs / selects ── */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox > div > div,
.stTextArea textarea {
    background: #ffffff !important;
    color: #131929 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
}
.stTextInput input:focus,
.stNumberInput input:focus,
.stSelectbox > div > div:focus {
    border-color: #1a56db !important;
    box-shadow: 0 0 0 3px rgba(26,86,219,.12) !important;
}
.stTextInput label,
.stNumberInput label,
.stDateInput label,
.stSelectbox label,
.stTextArea label {
    color: #374151 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
}
/* Dropdown options */
[data-baseweb="select"] * { color: #131929 !important; background: #fff !important; }
[data-baseweb="popover"] * { color: #131929 !important; }
[data-baseweb="menu"] { background: #fff !important; }
[data-baseweb="menu"] li { color: #131929 !important; }
[data-baseweb="menu"] li:hover { background: #ebf1fd !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    color: #131929 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
}
.streamlit-expanderHeader:hover {
    background: #f8faff !important;
    border-color: #1a56db !important;
}
.streamlit-expanderContent {
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 16px !important;
    color: #131929 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #f3f4f6 !important;
    border-radius: 8px !important;
    padding: 4px !important;
    border: 1px solid #e5e7eb !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7280 !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    border: none !important;
    font-family: 'Inter', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #131929 !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,.1) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 16px 0 !important;
}

/* ── Métricas ── */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetric"] label {
    color: #6b7280 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #131929 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── Dataframe / tabela ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    background: #fff !important;
}
.dvn-scroller { background: #fff !important; }

/* ── Divisores ── */
hr { border-color: #e5e7eb !important; margin: 12px 0 !important; }

/* ── Alertas / info boxes ── */
.stAlert { border-radius: 8px !important; font-size: 13px !important; }

/* ── KPI cards (HTML customizado) ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05), 0 4px 10px rgba(0,0,0,.03);
    position: relative;
    overflow: hidden;
    height: 100%;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 3px 3px 0 0;
}
.kpi-blue::before  { background: #1a56db; }
.kpi-green::before { background: #0a7a3c; }
.kpi-amber::before { background: #b45309; }
.kpi-red::before   { background: #c0392b; }
.kpi-purple::before{ background: #6d28d9; }

.kpi-icon { font-size: 18px; margin-bottom: 8px; }
.kpi-label {
    font-size: 10px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-bottom: 4px;
    font-family: 'Inter', sans-serif;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 6px;
    color: #131929;
}
.kpi-blue  .kpi-value { color: #1a56db; }
.kpi-green .kpi-value { color: #0a7a3c; }
.kpi-amber .kpi-value { color: #b45309; }
.kpi-red   .kpi-value { color: #c0392b; }
.kpi-purple.kpi-value { color: #6d28d9; }
.kpi-meta { font-size: 11px; color: #9ca3af; margin-top: 4px; font-family:'Inter',sans-serif; }

/* ── Badges ── */
.bdg {
    font-size: 10px; padding: 2px 9px; border-radius: 20px;
    font-weight: 600; display: inline-block; font-family: 'Inter', sans-serif;
    white-space: nowrap;
}
.bdg-green  { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.bdg-blue   { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.bdg-amber  { background: #fffbeb; color: #92400e; border: 1px solid #fcd34d; }
.bdg-red    { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }
.bdg-purple { background: #f5f3ff; color: #5b21b6; border: 1px solid #c4b5fd; }
.bdg-gray   { background: #f9fafb; color: #6b7280; border: 1px solid #e5e7eb; }

/* ── Notificações ── */
.notif {
    border-radius: 8px; padding: 11px 16px; font-size: 12.5px;
    margin-bottom: 12px; font-family: 'Inter', sans-serif; font-weight: 500;
}
.notif-warn   { background: #fffbeb; border: 1px solid #fcd34d; color: #92400e; }
.notif-info   { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; }
.notif-ok     { background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; }

/* ── Cards de lista (colaboradores, candidatos, etc) ── */
.list-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 9px;
    padding: 12px 16px;
    margin-bottom: 8px;
    box-shadow: 0 1px 2px rgba(0,0,0,.04);
    transition: box-shadow .15s;
    font-family: 'Inter', sans-serif;
}
.list-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,.08); }
.list-card-title { font-weight: 600; font-size: 13px; color: #111827; }
.list-card-sub   { font-size: 11px; color: #6b7280; margin-top: 2px; }

/* ── Panel (caixa branca) ── */
.panel {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.pdot-green  { width:7px;height:7px;border-radius:50%;background:#0a7a3c;display:inline-block;flex-shrink:0; }
.pdot-blue   { width:7px;height:7px;border-radius:50%;background:#1a56db;display:inline-block;flex-shrink:0; }
.pdot-amber  { width:7px;height:7px;border-radius:50%;background:#b45309;display:inline-block;flex-shrink:0; }
.pdot-purple { width:7px;height:7px;border-radius:50%;background:#6d28d9;display:inline-block;flex-shrink:0; }

/* ── Avatar círculo ── */
.avatar {
    width:36px; height:36px; border-radius:50%;
    background: linear-gradient(135deg,#3b82f6,#8b5cf6);
    display:inline-flex; align-items:center; justify-content:center;
    font-size:11px; font-weight:700; color:#fff;
    flex-shrink:0; font-family:'Inter',sans-serif;
}

/* ── Progress bar ── */
.prog-wrap {
    height: 7px; background: #f3f4f6; border-radius: 4px;
    overflow: hidden; border: 1px solid #e5e7eb;
}
.prog-fill { height:100%; border-radius:4px; transition: width 0.8s ease; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════
def init_state():
    defaults = {
        "modulo": "rh",
        "pagina": "indicadores",
        "vagas": [
            {"titulo": "Gerente de Operações",    "time": "Operações",  "status": "Ativa",            "candidatos": 120, "dias": 17, "prioridade": "Alta"},
            {"titulo": "Analista Financeiro Sr.", "time": "Financeiro", "status": "Ativa",            "candidatos": 85,  "dias": 24, "prioridade": "Média"},
            {"titulo": "Dev Fullstack",           "time": "Tecnologia", "status": "Banco de Talentos","candidatos": 12,  "dias": 52, "prioridade": "Baixa"},
        ],
        "candidatos": [
            {"nome":"Ana Beatriz Lima",   "local":"São Paulo, SP",       "vaga":"Gerente de Operações",    "fase":"Entrevista RH", "score":82, "origem":"LinkedIn",  "dias":12, "status":"Em andamento"},
            {"nome":"Rodrigo Fernandes",  "local":"Campinas, SP",        "vaga":"Analista Financeiro Sr.", "fase":"Proposta",      "score":76, "origem":"Indicação", "dias":47, "status":"Pendente"},
            {"nome":"Camila Souza",       "local":"São Paulo, SP",       "vaga":"Gerente de Operações",    "fase":"Teste Online",  "score":91, "origem":"Indeed",    "dias":8,  "status":"Em andamento"},
            {"nome":"Felipe Marques",     "local":"Rio de Janeiro, RJ",  "vaga":"Analista Financeiro Sr.", "fase":"Triagem",       "score":64, "origem":"Gupy",      "dias":3,  "status":"Em andamento"},
            {"nome":"Mariana Costa",      "local":"Barueri, SP",         "vaga":"Gerente de Operações",    "fase":"Aprovado",      "score":95, "origem":"LinkedIn",  "dias":17, "status":"Aprovado"},
            {"nome":"Paulo Rodrigues",    "local":"São Paulo, SP",       "vaga":"Analista Financeiro Sr.", "fase":"Triagem",       "score":71, "origem":"Site ETUS", "dias":2,  "status":"Em andamento"},
            {"nome":"Larissa Nunes",      "local":"Guarulhos, SP",       "vaga":"Gerente de Operações",    "fase":"Entrevista RH", "score":88, "origem":"LinkedIn",  "dias":15, "status":"Em andamento"},
        ],
        "onboarding": [
            {"nome":"Mariana Costa",  "cargo":"Gerente de Operações", "time":"Operações",  "inicio":"2026-03-10", "progresso":65, "pendencias":["Contrato assinado","E-mail corporativo"]},
            {"nome":"Lucas Teixeira", "cargo":"Dev Fullstack",        "time":"Tecnologia", "inicio":"2026-03-15", "progresso":30, "pendencias":["Documentação RH","Crachá","Acesso sistemas"]},
        ],
        "estagiarios": [
            {"nome":"Carlos Mendes",  "instituicao":"USP",     "time":"Tecnologia", "inicio":"2025-08-01","fim":"2026-07-31","carga":"20h/semana"},
            {"nome":"Juliana Ramos",  "instituicao":"FGV",     "time":"Financeiro", "inicio":"2025-09-01","fim":"2026-08-31","carga":"30h/semana"},
            {"nome":"Pedro Alves",    "instituicao":"UNICAMP", "time":"Comercial",  "inicio":"2025-10-01","fim":"2026-09-30","carga":"20h/semana"},
            {"nome":"Sofia Lima",     "instituicao":"PUC-SP",  "time":"Marketing",  "inicio":"2026-01-10","fim":"2027-01-09","carga":"20h/semana"},
            {"nome":"Rafael Costa",   "instituicao":"Mackenzie","time":"Operações", "inicio":"2026-02-01","fim":"2027-01-31","carga":"30h/semana"},
            {"nome":"Ana Ferreira",   "instituicao":"ESPM",    "time":"Marketing",  "inicio":"2026-02-15","fim":"2027-02-14","carga":"20h/semana"},
            {"nome":"Bruno Santos",   "instituicao":"FEI",     "time":"Tecnologia", "inicio":"2026-03-01","fim":"2027-02-28","carga":"20h/semana"},
            {"nome":"Isabela Rocha",  "instituicao":"INSPER",  "time":"Financeiro", "inicio":"2026-03-10","fim":"2027-03-09","carga":"30h/semana"},
        ],
        "colaboradores": [
            {"nome":"Diego Carvalho", "vinculo":"PJ","cargo":"Dev Fullstack Sr.","cnpj":"12.345.678/0001-90","inicio":"2024-01-15","valor":12000},
            {"nome":"Priscila Moura", "vinculo":"PJ","cargo":"Designer UX/UI",   "cnpj":"98.765.432/0001-11","inicio":"2024-06-01","valor":8500},
        ],
        "periodos": [
            {"nome":"Carlos Mendes", "cargo":"Estagiário Tecnologia","time":"Tecnologia","inicio":"2025-08-01","status":"Concluído"},
            {"nome":"Juliana Ramos", "cargo":"Estagiária Financeiro", "time":"Financeiro","inicio":"2025-09-01","status":"Concluído"},
            {"nome":"Pedro Alves",   "cargo":"Estagiário Comercial",  "time":"Comercial", "inicio":"2025-10-01","status":"Em avaliação"},
            {"nome":"Sofia Lima",    "cargo":"Estagiária Marketing",  "time":"Marketing", "inicio":"2026-01-10","status":"Em andamento"},
            {"nome":"Rafael Costa",  "cargo":"Estagiário Operações",  "time":"Operações", "inicio":"2026-02-01","status":"Vencendo"},
            {"nome":"Ana Ferreira",  "cargo":"Estagiária Marketing",  "time":"Marketing", "inicio":"2026-02-15","status":"Vencendo"},
        ],
        "notas_ifood": [],
        "pagamentos": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:12px 0 20px 0">
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#60a5fa;letter-spacing:-0.5px">
            ● ETUS
        </div>
        <div style="font-size:9px;color:#4a6085;letter-spacing:2px;text-transform:uppercase;margin-top:3px">
            Sistema de Gestão
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Módulos
    st.markdown('<p style="font-size:9px;color:#374151;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin:0 0 8px 0">Módulos</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    mods = [("rh","👥 RH",c1), ("dp","📋 DP",c2), ("fin","💰 Fin",c3)]
    for mid, mlbl, col in mods:
        with col:
            t = "primary" if st.session_state.modulo == mid else "secondary"
            if st.button(mlbl, key=f"mod_{mid}", use_container_width=True, type=t):
                first = {"rh":"indicadores","dp":"dashboard","fin":"ifood"}[mid]
                st.session_state.modulo = mid
                st.session_state.pagina = first
                st.rerun()

    st.divider()

    # Navegação
    st.markdown('<p style="font-size:9px;color:#374151;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin:0 0 8px 0">Navegação</p>', unsafe_allow_html=True)
    nav = {
        "rh":  [("indicadores","◈  Indicadores"),("vagas","📋  Vagas"),("candidatos","⚙  Candidatos"),("onboarding","🚀  Onboarding")],
        "dp":  [("dashboard","◈  Dashboard DP"),("estagiarios","🎓  Estagiários"),("colaboradores","👥  Colaboradores"),("periodo","⏳  Período de Experiência")],
        "fin": [("ifood","🍔  iFood"),("outros","💸  Outros Pagamentos"),("dashboard","◈  Dashboard Financeiro")],
    }
    for pid, plbl in nav[st.session_state.modulo]:
        t = "primary" if st.session_state.pagina == pid else "secondary"
        if st.button(plbl, key=f"nav_{pid}", use_container_width=True, type=t):
            st.session_state.pagina = pid
            st.rerun()

    st.divider()
    # Usuário
    st.markdown("""
    <div style="display:flex;align-items:center;gap:9px">
        <div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;flex-shrink:0">AD</div>
        <div>
            <div style="font-size:11px;font-weight:600;color:#e2e8f0">Admin ETUS</div>
            <div style="font-size:9px;color:#6b7a9a">Gerente RH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════
def kpi(label, value, color="blue", badge="", meta="", icon=""):
    badge_html = f'<div style="margin-top:6px"><span class="bdg bdg-{color}">{badge}</span></div>' if badge else ""
    meta_html  = f'<div class="kpi-meta">{meta}</div>' if meta else ""
    icon_html  = f'<div class="kpi-icon">{icon}</div>' if icon else ""
    st.markdown(f"""
    <div class="kpi-card kpi-{color}">
        {icon_html}
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {badge_html}{meta_html}
    </div>
    """, unsafe_allow_html=True)

def ph(title, dot="blue"):
    st.markdown(f'<div class="panel-title"><span class="pdot-{dot}"></span>{title}</div>', unsafe_allow_html=True)

def avatar(name):
    return name[:2].upper()

def plo():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11, color="#6b7280"),
        margin=dict(l=10,r=10,t=24,b=10), showlegend=False,
    )

def badge(text, color="gray"):
    return f'<span class="bdg bdg-{color}">{text}</span>'

def list_card(title, sub, right_html=""):
    st.markdown(f"""
    <div class="list-card">
        <div style="display:flex;align-items:center;justify-content:space-between">
            <div>
                <div class="list-card-title">{title}</div>
                <div class="list-card-sub">{sub}</div>
            </div>
            <div>{right_html}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  RH — INDICADORES
# ══════════════════════════════════════
def pg_rh_indicadores():
    st.markdown("## ◈ Indicadores de Recrutamento")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Vagas Abertas","3","blue","↔ estável","2 ativas · 1 banco","📋")
    with c2: kpi("Candidatos Ativos","217","green","↑ +12% mês","pipeline total","👥")
    with c3: kpi("Tempo Médio","24d","amber","⚠ meta: 30d","contratação","⏱")
    with c4: kpi("Taxa Aprovação","3.7%","purple","↑ +0.4pp","últimos 90d","✅")

    st.markdown("---")

    tab1,tab2,tab3,tab4 = st.tabs(["📊 Visão Geral","📈 Funil","⏱ Tempo","🔍 Fontes"])

    with tab1:
        cl, cr = st.columns([1,1.2])
        with cl:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            ph("Vagas por Posição","blue")
            fig = go.Figure(go.Pie(
                labels=["Gerente de Operações","Analista Financeiro","Banco de Talentos"],
                values=[120,85,12], hole=0.72,
                marker=dict(colors=["#1a56db","#6d28d9","#0277bd"],line=dict(color="#fff",width=3)),
            ))
            fig.update_layout(**plo(),height=190); fig.update_traces(textinfo="none")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
            for lbl,val,c in [("Gerente de Operações",120,"#1a56db"),("Analista Financeiro Sr.",85,"#6d28d9"),("Banco de Talentos",12,"#0277bd")]:
                st.markdown(f'<div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#374151;margin-bottom:5px;font-family:Inter,sans-serif"><span style="width:9px;height:9px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0"></span>{lbl}<strong style="margin-left:auto;color:#111827">{val}</strong></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with cr:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            ph("Vagas Ativas","green")
            prio_c = {"Alta":"red","Média":"amber","Baixa":"blue"}
            for v in st.session_state.vagas:
                pc = prio_c.get(v["prioridade"],"gray")
                st.markdown(f"""
                <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:11px 14px;margin-bottom:8px;font-family:Inter,sans-serif">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div>
                            <div style="font-weight:600;font-size:13px;color:#111827">{v['titulo']}</div>
                            <div style="font-size:11px;color:#6b7280;margin-top:2px">{v['time']} · {v['candidatos']} candidatos · {v['dias']}d aberta</div>
                        </div>
                        {badge(v['prioridade'],pc)}
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        ph("Funil de Recrutamento","blue")
        labels = ["Candidatos","Triagem RH","Teste Online","Entrevista","Proposta","Aprovados"]
        vals   = [217,130,64,28,12,8]
        colors = ["#1a56db","#4f46e5","#6d28d9","#0a7a3c","#0277bd","#10b981"]
        fig = go.Figure()
        for lbl,val,clr in zip(labels,vals,colors):
            pct = val/vals[0]*100
            fig.add_trace(go.Bar(x=[pct],y=[lbl],orientation='h',marker_color=clr,name=lbl,
                text=f"{val}",textposition="inside",textfont=dict(color="#fff",size=11),
                hovertemplate=f"{lbl}: {val} ({pct:.0f}%)<extra></extra>"))
        fig.update_layout(**plo(),height=260,showlegend=False,xaxis=dict(visible=False),
            yaxis=dict(tickfont=dict(size=12,color="#374151")))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        cconv = st.columns(5)
        for i in range(len(vals)-1):
            p = round(vals[i+1]/vals[i]*100,1)
            with cconv[i]:
                st.metric(f"{labels[i][:6]}→{labels[i+1][:6]}",f"{p}%")

    with tab3:
        ph("Histórico — Tempo de Contratação","blue")
        meses = ["Set/25","Out/25","Nov/25","Dez/25","Jan/26","Fev/26","Mar/26"]
        tempos = [22,28,52,31,11,24,17]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses,y=tempos,name="Tempo real",
            line=dict(color="#1a56db",width=2.5),fill="tozeroy",fillcolor="rgba(26,86,219,.08)",
            mode="lines+markers",marker=dict(size=6,color="#fff",line=dict(color="#1a56db",width=2))))
        fig.add_trace(go.Scatter(x=meses,y=[30]*7,name="Meta 30d",
            line=dict(color="rgba(192,57,43,.6)",width=1.5,dash="dot"),mode="lines",showlegend=True))
        fig.update_layout(**plo(),height=240,showlegend=True,
            legend=dict(orientation="h",y=1.12,x=1,xanchor="right",font=dict(size=11)),
            yaxis=dict(ticksuffix="d",gridcolor="rgba(0,0,0,.05)"),
            xaxis=dict(gridcolor="rgba(0,0,0,.05)"))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        ph("Dias Médios por Fase","amber")
        fases = ["Triagem","Teste","Entrevista","Proposta"]
        df_f  = [3,5,6,8]
        cf    = ["rgba(26,86,219,.85)","rgba(109,40,217,.85)","rgba(10,122,60,.85)","rgba(180,83,9,.85)"]
        fig2  = go.Figure(go.Bar(x=fases,y=df_f,marker_color=cf,text=[f"{d}d" for d in df_f],
            textposition="outside",textfont=dict(color="#374151",size=11),marker_line_width=0))
        fig2.update_layout(**plo(),height=180,
            yaxis=dict(ticksuffix="d",gridcolor="rgba(0,0,0,.05)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    with tab4:
        cl, cr = st.columns(2)
        with cl:
            ph("Candidatos por Canal","blue")
            canais = ["LinkedIn","Gupy","Indeed","Indicação","Site ETUS","Outros"]
            qtd    = [98,54,32,20,8,5]
            cc     = ["#1a56db","#6d28d9","#0277bd","#0a7a3c","#b45309","#9ca3af"]
            fig = go.Figure(go.Bar(y=canais,x=qtd,orientation="h",marker_color=cc,
                text=qtd,textposition="outside",textfont=dict(size=11,color="#374151"),
                marker_line_width=0))
            fig.update_layout(**plo(),height=240,
                xaxis=dict(gridcolor="rgba(0,0,0,.05)"),yaxis=dict(gridcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        with cr:
            ph("Taxa de Conversão por Fonte","green")
            conv = [("Indicação",15.0,"#0a7a3c"),("LinkedIn",5.2,"#1a56db"),
                    ("Site ETUS",4.8,"#b45309"),("Gupy",3.1,"#6d28d9"),
                    ("Indeed",2.4,"#0277bd"),("Outros",1.1,"#9ca3af")]
            for nm,pct,clr in conv:
                w = int(pct/15*100)
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;font-family:Inter,sans-serif">
                    <div style="width:72px;text-align:right;color:#6b7280;font-size:11px;font-weight:500">{nm}</div>
                    <div style="flex:1;height:22px;background:#f3f4f6;border-radius:5px;overflow:hidden;border:1px solid #e5e7eb">
                        <div style="width:{w}%;height:100%;background:{clr};display:flex;align-items:center;padding-left:8px;font-size:10px;font-weight:700;color:#fff">{pct}%</div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  RH — VAGAS
# ══════════════════════════════════════
def pg_rh_vagas():
    st.markdown("## 📋 Gestão de Vagas")

    with st.expander("➕ Cadastrar Nova Vaga"):
        c1,c2 = st.columns(2)
        with c1:
            titulo   = st.text_input("Título da Vaga", placeholder="Ex: Analista de Marketing")
            time_v   = st.selectbox("Time",["Tecnologia","Financeiro","Comercial","Operações","Marketing","RH"])
        with c2:
            prio_v   = st.selectbox("Prioridade",["Alta","Média","Baixa"])
            status_v = st.selectbox("Status",["Ativa","Banco de Talentos","Encerrada"])
        if st.button("+ Cadastrar Vaga", type="primary"):
            if titulo:
                st.session_state.vagas.append({"titulo":titulo,"time":time_v,"status":status_v,"candidatos":0,"dias":0,"prioridade":prio_v})
                st.success("✅ Vaga cadastrada!"); st.rerun()
            else: st.error("Preencha o título.")

    c1,c2,c3 = st.columns(3)
    ativas = sum(1 for v in st.session_state.vagas if v["status"]=="Ativa")
    banco  = sum(1 for v in st.session_state.vagas if v["status"]=="Banco de Talentos")
    total  = sum(v["candidatos"] for v in st.session_state.vagas)
    with c1: kpi("Vagas Ativas",ativas,"blue","↔","","📋")
    with c2: kpi("Banco de Talentos",banco,"purple","↔","","🗂️")
    with c3: kpi("Total Candidatos",total,"green","↑","","👥")

    st.markdown("---")
    ph("Lista de Vagas","blue")
    prio_c = {"Alta":"red","Média":"amber","Baixa":"blue"}
    stat_c = {"Ativa":"green","Banco de Talentos":"purple","Encerrada":"gray"}
    for v in st.session_state.vagas:
        pc = prio_c.get(v["prioridade"],"gray")
        sc = stat_c.get(v["status"],"gray")
        st.markdown(f"""
        <div class="list-card">
            <div style="display:flex;align-items:center;gap:12px">
                <div style="flex:1">
                    <div class="list-card-title">{v['titulo']}</div>
                    <div class="list-card-sub">{v['time']} · {v['candidatos']} candidatos · {v['dias']}d aberta</div>
                </div>
                <div style="display:flex;gap:6px;align-items:center">
                    {badge(v['status'],sc)}
                    {badge(v['prioridade'],pc)}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  RH — CANDIDATOS
# ══════════════════════════════════════
def pg_rh_candidatos():
    st.markdown("## ⚙ Candidatos")

    with st.expander("➕ Adicionar Candidato"):
        c1,c2 = st.columns(2)
        with c1:
            nc = st.text_input("Nome Completo",key="cn")
            lc = st.text_input("Cidade/Estado",placeholder="São Paulo, SP",key="cl")
            vc = st.selectbox("Vaga",[v["titulo"] for v in st.session_state.vagas] or ["—"],key="cv")
        with c2:
            fc  = st.selectbox("Fase",["Triagem","Teste Online","Entrevista RH","Proposta","Aprovado"],key="cf")
            oc  = st.selectbox("Origem",["LinkedIn","Gupy","Indeed","Indicação","Site ETUS","Outros"],key="co")
            sc_ = st.number_input("Score (%)",0,100,70,key="cs")
        if st.button("+ Adicionar",type="primary"):
            if nc:
                sm = {"Triagem":"Em andamento","Teste Online":"Em andamento","Entrevista RH":"Em andamento","Proposta":"Pendente","Aprovado":"Aprovado"}
                st.session_state.candidatos.append({"nome":nc,"local":lc,"vaga":vc,"fase":fc,"score":sc_,"origem":oc,"dias":0,"status":sm.get(fc,"Em andamento")})
                st.success(f"✅ {nc} adicionado!"); st.rerun()
            else: st.error("Preencha o nome.")

    cs1,cs2 = st.columns([2,1])
    with cs1: busca = st.text_input("🔍 Buscar",placeholder="Nome, vaga, fase...",key="busca_cand",label_visibility="collapsed")
    with cs2: ff = st.selectbox("Fase",["Todas","Triagem","Teste Online","Entrevista RH","Proposta","Aprovado"],key="ff",label_visibility="collapsed")

    cands = st.session_state.candidatos
    if busca: cands = [c for c in cands if busca.lower() in c["nome"].lower() or busca.lower() in c["vaga"].lower()]
    if ff != "Todas": cands = [c for c in cands if c["fase"] == ff]

    st.markdown(f'<p style="font-size:11px;color:#6b7280;margin-bottom:8px;font-family:Inter,sans-serif">Exibindo {len(cands)} candidatos</p>', unsafe_allow_html=True)

    fase_c = {"Triagem":"blue","Teste Online":"purple","Entrevista RH":"blue","Proposta":"amber","Aprovado":"green"}
    for c in cands:
        fc_   = fase_c.get(c["fase"],"gray")
        sc_v  = "#0a7a3c" if c["score"]>=80 else ("#b45309" if c["score"]>=60 else "#c0392b")
        st.markdown(f"""
        <div class="list-card" style="display:flex;align-items:center;gap:12px">
            <div class="avatar">{avatar(c['nome'])}</div>
            <div style="flex:1">
                <div class="list-card-title">{c['nome']}</div>
                <div class="list-card-sub">{c['local']} · {c['vaga']} · {c['origem']} · {c['dias']}d</div>
            </div>
            {badge(c['fase'],fc_)}
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:16px;color:{sc_v};min-width:32px;text-align:right">{c['score']}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  RH — ONBOARDING
# ══════════════════════════════════════
def pg_rh_onboarding():
    st.markdown("## 🚀 Onboarding")
    st.markdown('<div class="notif notif-warn">⚠️ Hygor Lessa tem documentos pendentes. Prazo: 25/03/2026.</div>', unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1: kpi("Em Onboarding",len(st.session_state.onboarding),"blue","↔","","🔄")
    with c2: kpi("Concluídos (30d)","3","green","↑ +1","","✅")

    st.markdown("---")
    ph("Processos Ativos","blue")
    for o in st.session_state.onboarding:
        pct   = o["progresso"]
        bc    = "#0a7a3c" if pct>=80 else ("#1a56db" if pct>=40 else "#b45309")
        pends = " ".join([badge(p,"amber") for p in o["pendencias"]])
        st.markdown(f"""
        <div class="list-card">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
                <div>
                    <div class="list-card-title">{o['nome']}</div>
                    <div class="list-card-sub">{o['cargo']} · {o['time']} · Início: {o['inicio']}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:20px;color:{bc}">{pct}%</div>
            </div>
            <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%;background:{bc}"></div></div>
            <div style="display:flex;gap:5px;flex-wrap:wrap;margin-top:8px">{pends}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  DP — DASHBOARD
# ══════════════════════════════════════
def pg_dp_dashboard():
    st.markdown("## ◈ Dashboard — Departamento Pessoal")

    n_est = len(st.session_state.estagiarios)
    n_pj  = len(st.session_state.colaboradores)
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Total Colaboradores", n_est+n_pj,"blue","↔","headcount","👥")
    with c2: kpi("Estagiários Ativos",  n_est,      "green","↑ +1 mês","5 times","🎓")
    with c3: kpi("Exp. Vencendo (30d)", "2",         "amber","⚠ atenção","avaliar","⏳")
    with c4: kpi("Contratos Vigentes",  n_est+n_pj,  "purple","↔","estágio + PJ","📋")

    st.markdown("---")
    c1,c2,c3 = st.columns([1,1.4,1.4])

    with c1:
        ph("Distribuição por Vínculo","green")
        fig = go.Figure(go.Pie(labels=["Estagiários","PJ"],values=[n_est,n_pj],hole=0.68,
            marker=dict(colors=["#0a7a3c","#1a56db"],line=dict(color="#fff",width=3))))
        fig.update_layout(**plo(),height=170); fig.update_traces(textinfo="none")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        total = n_est+n_pj
        for lbl,val,cl in [("Estagiários",n_est,"#0a7a3c"),("PJ",n_pj,"#1a56db")]:
            pct = round(val/total*100) if total else 0
            st.markdown(f'<div style="display:flex;align-items:center;gap:7px;font-size:12px;color:#374151;margin-bottom:5px;font-family:Inter,sans-serif"><span style="width:9px;height:9px;border-radius:50%;background:{cl};display:inline-block"></span>{lbl}<strong style="margin-left:auto;color:#111827">{val}</strong><span style="color:#9ca3af;font-size:11px">{pct}%</span></div>', unsafe_allow_html=True)

    with c2:
        ph("Estagiários por Time","blue")
        tc = {}
        for e in st.session_state.estagiarios:
            tc[e["time"]] = tc.get(e["time"],0)+1
        if tc:
            fig2 = go.Figure(go.Bar(x=list(tc.keys()),y=list(tc.values()),
                marker_color=["#1a56db","#6d28d9","#0a7a3c","#b45309","#0277bd"][:len(tc)],
                text=list(tc.values()),textposition="outside",textfont=dict(size=11,color="#374151"),
                marker_line_width=0))
            fig2.update_layout(**plo(),height=200,
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),yaxis=dict(gridcolor="rgba(0,0,0,.05)"))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})

    with c3:
        ph("Evolução de Contratos","blue")
        meses = ["Out/25","Nov/25","Dez/25","Jan/26","Fev/26","Mar/26"]
        vals  = [5,5,6,7,8,n_est]
        fig3  = go.Figure(go.Scatter(x=meses,y=vals,fill="tozeroy",
            line=dict(color="#1a56db",width=2.5),fillcolor="rgba(26,86,219,.08)",
            mode="lines+markers",marker=dict(size=6,color="#fff",line=dict(color="#1a56db",width=2))))
        fig3.update_layout(**plo(),height=200,
            yaxis=dict(gridcolor="rgba(0,0,0,.05)"),xaxis=dict(gridcolor="rgba(0,0,0,.05)"))
        st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

    st.markdown("---")
    ph("Progresso dos Contratos de Estágio","amber")
    today = date.today()
    for e in st.session_state.estagiarios:
        try:
            ini  = date.fromisoformat(e["inicio"])
            fim  = date.fromisoformat(e["fim"])
            tot  = (fim-ini).days
            ela  = (today-ini).days
            pct  = min(100,max(0,int(ela/tot*100))) if tot>0 else 0
            dr   = (fim-today).days
            bc   = "#c0392b" if pct>85 else ("#b45309" if pct>60 else "#1a56db")
        except: pct,dr,bc = 0,0,"#1a56db"
        st.markdown(f"""
        <div style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px;font-family:Inter,sans-serif">
                <div>
                    <span style="font-size:13px;font-weight:600;color:#111827">{e['nome']}</span>
                    <span style="font-size:11px;color:#6b7280;margin-left:8px">{e['time']}</span>
                </div>
                <div style="text-align:right">
                    <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:{bc}">{pct}%</span>
                    <span style="font-size:10px;color:#9ca3af;display:block">{max(0,dr)}d restantes</span>
                </div>
            </div>
            <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%;background:{bc}"></div></div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  DP — ESTAGIÁRIOS
# ══════════════════════════════════════
def pg_dp_estagiarios():
    st.markdown("## 🎓 Estagiários")
    c1,c2 = st.columns(2)

    with c1:
        ph("Novo Registro","green")
        ne = st.text_input("Nome Completo",key="en")
        ie = st.text_input("Instituição de Ensino",placeholder="Ex: USP, FGV...",key="ei")
        ca,cb = st.columns(2)
        with ca:
            te = st.selectbox("Time",["Tecnologia","Financeiro","Comercial","Operações","Marketing"])
            di = st.date_input("Início",value=date.today(),key="ed_i")
        with cb:
            ce = st.selectbox("Carga",["20h/semana","30h/semana"])
            df = st.date_input("Fim",value=date.today()+timedelta(days=180),key="ed_f")
        if st.button("+ Cadastrar Estagiário",type="primary",use_container_width=True):
            if ne:
                st.session_state.estagiarios.append({"nome":ne,"instituicao":ie,"time":te,"inicio":di.isoformat(),"fim":df.isoformat(),"carga":ce})
                st.success(f"✅ {ne} cadastrado!"); st.rerun()
            else: st.error("Preencha o nome.")

    with c2:
        ph(f"Estagiários · Total: {len(st.session_state.estagiarios)}","blue")
        for e in st.session_state.estagiarios:
            st.markdown(f"""
            <div class="list-card" style="display:flex;align-items:center;gap:10px">
                <div class="avatar" style="background:linear-gradient(135deg,#0a7a3c,#1a56db)">{avatar(e['nome'])}</div>
                <div style="flex:1">
                    <div class="list-card-title">{e['nome']}</div>
                    <div class="list-card-sub">{e['instituicao']} · {e['time']} · {e['carga']}</div>
                </div>
                {badge("Ativo","green")}
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  DP — COLABORADORES
# ══════════════════════════════════════
def pg_dp_colaboradores():
    st.markdown("## 👥 Colaboradores PJ")
    c1,c2,c3 = st.columns(3)
    with c1: kpi("Total PJ",len(st.session_state.colaboradores),"blue","↔","","👥")
    with c2: kpi("Contratos Ativos",len(st.session_state.colaboradores),"green","↔","","📄")
    with c3: kpi("Benef. Pendentes","0","amber","✓ ok","","💰")

    with st.expander("➕ Novo Colaborador"):
        c1,c2 = st.columns(2)
        with c1:
            ncl = st.text_input("Nome",key="cln")
            ccl = st.text_input("Cargo",placeholder="Ex: Dev Fullstack Sr.",key="clc")
            icl = st.date_input("Início",value=date.today(),key="cli")
        with c2:
            vcl = st.selectbox("Vínculo",["PJ","CLT"])
            dcl = st.text_input("CNPJ / CPF",placeholder="00.000.000/0001-00",key="cld")
            vlcl= st.number_input("Valor Mensal (R$)",min_value=0.0,step=100.0,key="clv")
        if st.button("+ Cadastrar Colaborador",type="primary"):
            if ncl:
                st.session_state.colaboradores.append({"nome":ncl,"vinculo":vcl,"cargo":ccl,"cnpj":dcl,"inicio":icl.isoformat(),"valor":vlcl})
                st.success(f"✅ {ncl} cadastrado!"); st.rerun()
            else: st.error("Preencha o nome.")

    st.markdown("---")
    ph("Lista de Colaboradores","blue")
    for c in st.session_state.colaboradores:
        vf = f"R$ {c['valor']:,.0f}".replace(",",".")
        st.markdown(f"""
        <div class="list-card" style="display:flex;align-items:center;gap:12px">
            <div class="avatar" style="background:linear-gradient(135deg,#0a7a3c,#1a56db)">{avatar(c['nome'])}</div>
            <div style="flex:1">
                <div class="list-card-title">{c['nome']}</div>
                <div class="list-card-sub">{c['cargo']} · {c['cnpj']} · desde {c['inicio']}</div>
            </div>
            {badge(c['vinculo'],"blue")}
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:14px">{vf}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  DP — PERÍODO
# ══════════════════════════════════════
def pg_dp_periodo():
    st.markdown("## ⏳ Período de Experiência")
    st.markdown('<div class="notif notif-warn">⏰ 2 avaliações vencem nos próximos 30 dias. Revise antes dos prazos.</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        ph("Cadastrar Novo Período","green")
        np = st.text_input("Nome do Colaborador",key="pn")
        cp = st.text_input("Cargo",placeholder="Ex: Analista Trainee",key="pc_")
        ta,tb = st.columns(2)
        with ta: tp = st.selectbox("Time",["Tecnologia","Financeiro","Comercial","Operações","RH"])
        with tb: ip = st.date_input("Data de Início",value=date.today(),key="pi")
        if st.button("+ Cadastrar Controle",type="primary",use_container_width=True):
            if np:
                st.session_state.periodos.append({"nome":np,"cargo":cp,"time":tp,"inicio":ip.isoformat(),"status":"Em andamento"})
                st.success("✅ Cadastrado!"); st.rerun()
            else: st.error("Preencha o nome.")

    with c2:
        ph(f"Avaliações (90 dias) · {len(st.session_state.periodos)} registros","amber")
        sc_map = {"Concluído":"green","Em avaliação":"purple","Em andamento":"blue","Vencendo":"red"}
        today  = date.today()
        for p in st.session_state.periodos:
            try:
                ini = date.fromisoformat(p["inicio"])
                fim = ini + timedelta(days=90)
                dr  = (fim-today).days
                pct = min(100,max(0,int((today-ini).days/90*100)))
                bc  = "#c0392b" if pct>85 else ("#b45309" if pct>60 else "#1a56db")
            except: dr,pct,bc = 0,0,"#1a56db"
            sc_ = sc_map.get(p["status"],"gray")
            st.markdown(f"""
            <div class="list-card">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:7px">
                    <div>
                        <div class="list-card-title">{p['nome']}</div>
                        <div class="list-card-sub">{p['cargo']} · {p['time']}</div>
                    </div>
                    {badge(p['status'],sc_)}
                </div>
                <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%;background:{bc}"></div></div>
                <div style="font-size:10px;color:#9ca3af;margin-top:4px;font-family:Inter,sans-serif">{pct}% · {max(0,dr)}d restantes</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
#  FIN — IFOOD
# ══════════════════════════════════════
def pg_fin_ifood():
    st.markdown("## 🍔 Notas Fiscais iFood")
    notas = st.session_state.notas_ifood
    tv  = sum(n["valor"] for n in notas)
    pend= sum(1 for n in notas if n["status"]=="Pendente")

    c1,c2,c3 = st.columns(3)
    with c1: kpi("Notas Cadastradas",len(notas),"green","↔ este mês","","🍔")
    with c2: kpi("Total Faturado",f"R${tv:,.0f}".replace(",","."),"blue","↔","","💰")
    with c3: kpi("Pendentes Emissão",pend,"amber","✓ ok" if pend==0 else f"⚠ {pend}","","⏳")

    with st.expander("➕ Nova Nota Fiscal iFood",expanded=len(notas)==0):
        c1,c2 = st.columns(2)
        with c1:
            ei = st.selectbox("Empresa Emitente",["ETUS Digital LLC","Evolution","BRAZ","BRIUS","EMGC"])
            vi = st.number_input("Valor (R$)",min_value=0.0,step=0.01,format="%.2f",key="ifv")
            ni = st.text_input("Número da NF",placeholder="00000",key="ifn")
        with c2:
            mi = st.selectbox("Mês de Referência",["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"])
            di = st.date_input("Data de Emissão",value=date.today(),key="ifd")
            si = st.selectbox("Status",["Emitida","Pendente","Cancelada"])
        if st.button("+ Registrar Nota",type="primary"):
            if vi>0:
                st.session_state.notas_ifood.append({"empresa":ei,"mes":mi,"valor":vi,"data":di.isoformat(),"nf":ni,"status":si})
                st.success("✅ Nota registrada!"); st.rerun()
            else: st.error("Preencha o valor.")

    st.markdown("---")
    ph("Histórico de Notas iFood","green")
    sc_c = {"Emitida":"green","Pendente":"amber","Cancelada":"red"}
    if notas:
        for n in notas:
            vf = f"R$ {n['valor']:,.2f}".replace(",","X").replace(".",",").replace("X",".")
            sc_= sc_c.get(n["status"],"gray")
            st.markdown(f"""
            <div class="list-card" style="display:flex;align-items:center;gap:12px">
                <div style="font-size:22px">🍔</div>
                <div style="flex:1">
                    <div class="list-card-title">{n['empresa']}</div>
                    <div class="list-card-sub">NF {n['nf']} · {n['mes']} · {n['data']}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:15px">{vf}</div>
                {badge(n['status'],sc_)}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center;padding:40px;color:#9ca3af;font-family:Inter,sans-serif"><div style="font-size:36px;margin-bottom:8px">💸</div><div style="font-weight:600">Nenhuma nota registrada</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════
#  FIN — OUTROS PAGAMENTOS
# ══════════════════════════════════════
def pg_fin_outros():
    st.markdown("## 💸 Outros Pagamentos")
    pags = st.session_state.pagamentos
    tp   = sum(p["valor"] for p in pags)

    c1,c2,c3 = st.columns(3)
    with c1: kpi("Pagamentos (Mês)",len(pags),"green","↔","","💸")
    with c2: kpi("Total Pago",f"R${tp:,.0f}".replace(",","."),"blue","↔","","💰")
    with c3: kpi("Aguard. Comprovante","0","amber","✓ ok","","⏳")

    c_form, c_hist = st.columns(2)

    with c_form:
        ph("Lançar Novo Pagamento","green")
        ep  = st.selectbox("Empresa",["Plusdin São Bernardo","ETUS Digital LLC","Evolution","BRAZ","BRIUS","EMGC"],key="pge")
        mp  = st.selectbox("Mês de Referência",["Janeiro","Fevereiro","Março","Abril","Maio","Junho"],key="pgm")
        ca,cb = st.columns(2)
        with ca:
            vp  = st.number_input("Valor (R$)",min_value=0.0,step=0.01,format="%.2f",key="pgv")
            den = st.date_input("Data Envio",value=date.today(),key="pgen")
        with cb:
            mop = st.text_input("Motivo",placeholder="Ex: Internet, Aluguel...",key="pgmo")
            dpg = st.date_input("Data Pagamento",value=date.today(),key="pgpg")
        if st.button("Registrar Pagamento",type="primary",use_container_width=True):
            if vp>0 and mop:
                st.session_state.pagamentos.append({"empresa":ep,"motivo":mop,"mes":mp,"valor":vp,"data_envio":den.isoformat(),"data_pagamento":dpg.isoformat()})
                st.success("✅ Pagamento registrado!"); st.rerun()
            else: st.error("Preencha valor e motivo.")

    with c_hist:
        ph("Histórico de Pagamentos","blue")
        if pags:
            for p in pags:
                vf = f"R$ {p['valor']:,.2f}".replace(",","X").replace(".",",").replace("X",".")
                st.markdown(f"""
                <div class="list-card">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div>
                            <div class="list-card-title">{p['empresa']}</div>
                            <div class="list-card-sub">{p['motivo']} · {p['mes']} · {p['data_pagamento']}</div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:14px">{vf}</div>
                            {badge("✓ Pago","green")}
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;padding:30px;color:#9ca3af;font-family:Inter,sans-serif"><div style="font-size:32px;margin-bottom:6px">💸</div><div style="font-weight:600">Nenhum pagamento registrado</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════
#  FIN — DASHBOARD
# ══════════════════════════════════════
def pg_fin_dashboard():
    st.markdown("## ◈ Dashboard Financeiro")
    notas = st.session_state.notas_ifood
    pags  = st.session_state.pagamentos
    tif   = sum(n["valor"] for n in notas)
    tp    = sum(p["valor"] for p in pags)
    nc    = len(st.session_state.estagiarios)+len(st.session_state.colaboradores)
    cpc   = (tif+tp)/nc if nc>0 else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Receita iFood",   f"R${tif:,.0f}".replace(",","."),"green","↔","","💰")
    with c2: kpi("Outros Pagamentos",f"R${tp:,.0f}".replace(",","."),"blue","↔","","💸")
    with c3: kpi("Custo/Colaborador",f"R${cpc:,.0f}".replace(",","."),"amber","↔","","📊")
    with c4: kpi("Notas Pendentes", sum(1 for n in notas if n["status"]=="Pendente"),"red","✓ ok","","⚠️")

    if not notas and not pags:
        st.markdown('<div class="notif notif-info">ℹ️ Cadastre notas e pagamentos para visualizar os indicadores automaticamente.</div>', unsafe_allow_html=True)

    st.markdown("---")
    c1,c2 = st.columns(2)

    with c1:
        ph("Receita vs Custos","green")
        ml = ["Out/25","Nov/25","Dez/25","Jan/26","Fev/26","Mar/26"]
        rec=[0,0,0,0,0,tif]; cus=[0,0,0,0,0,tp]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ml,y=rec,name="Receita",marker_color="#0a7a3c",marker_line_width=0))
        fig.add_trace(go.Bar(x=ml,y=cus,name="Custos", marker_color="#c0392b",marker_line_width=0))
        fig.update_layout(**plo(),height=240,showlegend=True,barmode="group",
            legend=dict(orientation="h",y=1.12,x=1,xanchor="right",font=dict(size=11)),
            yaxis=dict(tickprefix="R$",gridcolor="rgba(0,0,0,.05)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

    with c2:
        ph("Distribuição de Custos","blue")
        if tif>0 or tp>0:
            fig2 = go.Figure(go.Pie(labels=["iFood","Pagamentos"],values=[max(tif,.1),max(tp,.1)],hole=0.68,
                marker=dict(colors=["rgba(10,122,60,.75)","rgba(26,86,219,.75)"],line=dict(color="#fff",width=3))))
            fig2.update_layout(**plo(),height=230)
            fig2.update_traces(textinfo="percent+label",textfont=dict(size=11))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        else:
            st.markdown('<div style="text-align:center;padding:50px;color:#9ca3af;font-size:12px;font-family:Inter,sans-serif">Sem dados — cadastre notas e pagamentos</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════
router = {
    ("rh","indicadores"): pg_rh_indicadores,
    ("rh","vagas"):        pg_rh_vagas,
    ("rh","candidatos"):   pg_rh_candidatos,
    ("rh","onboarding"):   pg_rh_onboarding,
    ("dp","dashboard"):    pg_dp_dashboard,
    ("dp","estagiarios"):  pg_dp_estagiarios,
    ("dp","colaboradores"):pg_dp_colaboradores,
    ("dp","periodo"):      pg_dp_periodo,
    ("fin","ifood"):       pg_fin_ifood,
    ("fin","outros"):      pg_fin_outros,
    ("fin","dashboard"):   pg_fin_dashboard,
}

fn = router.get((st.session_state.modulo, st.session_state.pagina))
if fn:
    fn()
else:
    st.warning("Página não encontrada.")
