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

# ── GLOBAL CSS (SEU CSS ORIGINAL INTEGRAL) ──
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

/* ── Métricas e KPI cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
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
.kpi-purple::before{ background: #6d28d9; }

.kpi-icon { font-size: 18px; margin-bottom: 8px; }
.kpi-label { font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 4px; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 700; color: #131929; }
.kpi-meta { font-size: 11px; color: #9ca3af; margin-top: 4px; }

/* ── Badges ── */
.bdg { font-size: 10px; padding: 2px 9px; border-radius: 20px; font-weight: 600; display: inline-block; }
.bdg-green  { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.bdg-blue   { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.bdg-amber  { background: #fffbeb; color: #92400e; border: 1px solid #fcd34d; }
.bdg-red    { background: #fef2f2; color: #991b1b; border: 1px solid #fca5a5; }

/* ── Panel e List Cards ── */
.panel { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 18px; margin-bottom: 14px; }
.panel-title { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
.pdot-blue { width:7px; height:7px; border-radius:50%; background:#1a56db; }
.list-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 9px; padding: 12px 16px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,.04); }
.list-card-title { font-weight: 600; font-size: 13px; color: #111827; }
.list-card-sub   { font-size: 11px; color: #6b7280; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
def init_state():
    defaults = {
        "modulo": "rh",
        "pagina": "indicadores",
        "vagas": [
            {"titulo": "Gerente de Operações", "time": "Operações", "status": "Ativa", "candidatos": 120, "dias": 17, "prioridade": "Alta"},
            {"titulo": "Analista Financeiro Sr.", "time": "Financeiro", "status": "Ativa", "candidatos": 85, "dias": 24, "prioridade": "Média"},
        ],
        "candidatos": [
            {"nome":"Ana Beatriz Lima", "vaga":"Gerente de Operações", "fase":"Entrevista RH", "score":82, "status":"Em andamento"},
            {"nome":"Mariana Costa", "vaga":"Gerente de Operações", "fase":"Aprovado", "score":95, "status":"Aprovado"},
        ]
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── HELPERS ──
def kpi(label, value, color="blue", badge_txt="", meta="", icon=""):
    badge_html = f'<div style="margin-top:6px"><span class="bdg bdg-{color}">{badge_txt}</span></div>' if badge_txt else ""
    st.markdown(f"""
    <div class="kpi-card kpi-{color}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {badge_html}
        <div class="kpi-meta">{meta}</div>
    </div>
    """, unsafe_allow_html=True)

def ph(title, dot="blue"):
    st.markdown(f'<div class="panel-title"><span class="pdot-{dot}"></span>{title}</div>', unsafe_allow_html=True)

def badge(text, color="blue"):
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

def plo():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11, color="#6b7280"),
        margin=dict(l=10,r=10,t=24,b=10), showlegend=False,
    )

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px 0">
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#60a5fa;letter-spacing:-0.5px">● ETUS</div>
        <div style="font-size:9px;color:#4a6085;letter-spacing:2px;text-transform:uppercase;margin-top:3px">Sistema de Gestão</div>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown('<p style="font-size:9px;color:#374151;letter-spacing:2px;text-transform:uppercase;font-weight:700;margin:0 0 8px 0">Navegação</p>', unsafe_allow_html=True)
    nav = {
        "rh":  [("indicadores","◈ Indicadores"),("vagas","📋 Vagas"),("candidatos","⚙ Candidatos")],
        "dp":  [("dashboard","◈ Dashboard DP")],
        "fin": [("ifood","🍔 iFood")],
    }
    for pid, plbl in nav[st.session_state.modulo]:
        t = "primary" if st.session_state.pagina == pid else "secondary"
        if st.button(plbl, key=f"nav_{pid}", use_container_width=True, type=t):
            st.session_state.pagina = pid
            st.rerun()

# ── PÁGINAS DO RH ──
def pg_rh_indicadores():
    st.markdown("## ◈ Indicadores de Recrutamento")
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Vagas Abertas","3","blue","↔ estável","2 ativas · 1 banco","📋")
    with c2: kpi("Candidatos Ativos","217","green","↑ +12% mês","pipeline total","👥")
    with c3: kpi("Tempo Médio","24d","amber","⚠ meta: 30d","contratação","⏱")
    with c4: kpi("Taxa Aprovação","3.7%","purple","↑ +0.4pp","últimos 90d","✅")
    
    st.markdown("---")
    cl, cr = st.columns([1,1.2])
    with cl:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        ph("Vagas por Posição","blue")
        fig = go.Figure(go.Pie(labels=["Gerente","Analista","Banco"], values=[120,85,12], hole=0.72, marker=dict(colors=["#1a56db","#6d28d9","#0277bd"])))
        fig.update_layout(**plo(), height=200)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with cr:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        ph("Vagas Ativas")
        for v in st.session_state.vagas:
            list_card(v['titulo'], f"{v['time']} · {v['candidatos']} candidatos", badge(v['prioridade'], "red" if v['prioridade']=="Alta" else "amber"))
        st.markdown('</div>', unsafe_allow_html=True)

def pg_rh_vagas():
    st.markdown("## 📋 Gestão de Vagas")
    with st.expander("➕ Cadastrar Nova Vaga"):
        titulo = st.text_input("Título")
        if st.button("+ Salvar"):
            st.session_state.vagas.append({"titulo":titulo, "time":"Novo", "status":"Ativa", "candidatos":0, "dias":0, "prioridade":"Média"})
            st.rerun()
    for v in st.session_state.vagas:
        list_card(v['titulo'], f"{v['time']} · {v['status']}", badge(v['prioridade'], "blue"))

def pg_rh_candidatos():
    st.markdown("## ⚙ Candidatos")
    with st.expander("➕ Adicionar Candidato"):
        nome = st.text_input("Nome Completo")
        if st.button("+ Adicionar"):
            st.session_state.candidatos.append({"nome":nome, "vaga":"Nova", "fase":"Triagem", "score":0, "status":"Em andamento"})
            st.rerun()
    for c in st.session_state.candidatos:
        list_card(c['nome'], f"{c['vaga']} · {c['fase']}", badge(f"{c['score']}%", "green"))

# ── ROTEADOR (ESTA É A PARTE QUE RESTAURA O MENU) ──
if st.session_state.modulo == "rh":
    if st.session_state.pagina == "indicadores": pg_rh_indicadores()
    elif st.session_state.pagina == "vagas": pg_rh_vagas()
    elif st.session_state.pagina == "candidatos": pg_rh_candidatos()
elif st.session_state.modulo == "dp":
    st.info("Módulo DP em desenvolvimento.")
elif st.session_state.modulo == "fin":
    st.info("Módulo Financeiro em desenvolvimento.")
