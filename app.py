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

# ── SEU CSS ORIGINAL INTEGRAL ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif !important; color: #131929 !important; background-color: #eef1f7 !important; }
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }
[data-testid="stSidebar"] { background: #111827 !important; border-right: 1px solid rgba(255,255,255,.08) !important; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div { color: #94a3b8 !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] .stButton > button { background: transparent !important; color: #94a3b8 !important; border: 1px solid rgba(255,255,255,.1) !important; border-radius: 7px !important; font-size: 12px !important; text-align: left !important; width: 100% !important; padding: 6px 10px !important; }
[data-testid="stSidebar"] .stButton > button:hover { background: rgba(255,255,255,.08) !important; color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stButton > button[kind="primary"] { background: rgba(26,86,219,.35) !important; color: #93c5fd !important; border-color: rgba(96,165,250,.4) !important; font-weight: 600 !important; }
.main .block-container { padding: 20px 28px 40px 28px !important; background: #eef1f7 !important; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #131929 !important; font-weight: 700 !important; }
.stButton > button { font-family: 'Inter', sans-serif !important; font-size: 12px !important; font-weight: 600 !important; border-radius: 7px !important; height: 36px !important; background: #ffffff !important; color: #374151 !important; }
.stButton > button[kind="primary"] { background: #1a56db !important; color: #ffffff !important; }
.kpi-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,.05); position: relative; overflow: hidden; height: 100%; }
.kpi-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 3px 3px 0 0; }
.kpi-blue::before  { background: #1a56db; } .kpi-green::before { background: #0a7a3c; } .kpi-amber::before { background: #b45309; } .kpi-purple::before{ background: #6d28d9; }
.kpi-label { font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; margin-bottom: 4px; }
.kpi-value { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 700; color: #131929; }
.bdg { font-size: 10px; padding: 2px 9px; border-radius: 20px; font-weight: 600; display: inline-block; }
.bdg-green  { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
.bdg-blue   { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; }
.panel { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 18px; margin-bottom: 14px; }
.list-card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 9px; padding: 12px 16px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "modulo" not in st.session_state: st.session_state.modulo = "rh"
if "pagina" not in st.session_state: st.session_state.pagina = "indicadores"
if "vagas" not in st.session_state:
    st.session_state.vagas = [
        {"titulo": "Gerente de Operações", "time": "Operações", "status": "Ativa", "candidatos": 120, "dias": 17, "prioridade": "Alta"},
        {"titulo": "Analista Financeiro Sr.", "time": "Financeiro", "status": "Ativa", "candidatos": 85, "dias": 24, "prioridade": "Média"},
    ]
if "candidatos" not in st.session_state:
    st.session_state.candidatos = [
        {"nome":"Ana Beatriz Lima", "vaga":"Gerente de Operações", "fase":"Entrevista RH", "score":82, "status":"Em andamento"},
    ]

# ── HELPERS ──
def kpi(label, value, color="blue", badge_txt="", meta="", icon=""):
    badge_html = f'<div style="margin-top:6px"><span class="bdg bdg-{color}">{badge_txt}</span></div>' if badge_txt else ""
    st.markdown(f'<div class="kpi-card kpi-{color}"><div class="kpi-label">{icon} {label}</div><div class="kpi-value">{value}</div>{badge_html}<div class="kpi-meta">{meta}</div></div>', unsafe_allow_html=True)

def list_card(title, sub, right_html=""):
    st.markdown(f'<div class="list-card"><div style="display:flex;align-items:center;justify-content:space-between"><div><div style="font-weight:600;font-size:13px">{title}</div><div style="font-size:11px;color:#6b7280">{sub}</div></div><div>{right_html}</div></div></div>', unsafe_allow_html=True)

# ── PÁGINAS DO RH ──
def pg_rh_indicadores():
    st.markdown("## ◈ Indicadores de Recrutamento")
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("Vagas Abertas", len(st.session_state.vagas), "blue", "↔ estável")
    with c2: kpi("Candidatos", "217", "green", "↑ +12% mês")
    with c3: kpi("Tempo Médio", "24d", "amber", "⚠ meta: 30d")
    with c4: kpi("Taxa Aprovação", "3.7%", "purple", "↑ +0.4pp")

def pg_rh_vagas():
    st.markdown("## 📋 Gestão de Vagas")
    for v in st.session_state.vagas:
        list_card(v['titulo'], f"{v['time']} · {v['candidatos']} candidatos", f'<span class="bdg bdg-blue">{v["prioridade"]}</span>')

def pg_rh_candidatos():
    st.markdown("## ⚙ Candidatos")
    for c in st.session_state.candidatos:
        list_card(c['nome'], f"{c['vaga']} · {c['fase']}", f'<span class="bdg bdg-green">{c["score"]}%</span>')

# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div style="font-family:Syne;font-size:22px;font-weight:800;color:#60a5fa;padding:10px 0">● ETUS</div>', unsafe_allow_html=True)
    
    # Seletor de Módulos
    st.markdown('<p style="font-size:9px;text-transform:uppercase;font-weight:700">Módulos</p>', unsafe_allow_html=True)
    cm1, cm2, cm3 = st.columns(3)
    if cm1.button("👥 RH", type="primary" if st.session_state.modulo=="rh" else "secondary", use_container_width=True):
        st.session_state.modulo = "rh"; st.session_state.pagina = "indicadores"; st.rerun()
    if cm2.button("📋 DP", type="primary" if st.session_state.modulo=="dp" else "secondary", use_container_width=True):
        st.session_state.modulo = "dp"; st.session_state.pagina = "dashboard"; st.rerun()
    if cm3.button("💰 Fin", type="primary" if st.session_state.modulo=="fin" else "secondary", use_container_width=True):
        st.session_state.modulo = "fin"; st.session_state.pagina = "ifood"; st.rerun()

    st.divider()

    # Seletor de Páginas (Dinâmico conforme o módulo)
    st.markdown('<p style="font-size:9px;text-transform:uppercase;font-weight:700">Navegação</p>', unsafe_allow_html=True)
    
    opcoes = {
        "rh": [("indicadores","◈ Indicadores"), ("vagas","📋 Vagas"), ("candidatos","⚙ Candidatos")],
        "dp": [("dashboard","◈ Dashboard DP"), ("estagiarios","🎓 Estagiários")],
        "fin": [("ifood","🍔 iFood")]
    }

    for id_pag, label_pag in opcoes[st.session_state.modulo]:
        if st.button(label_pag, type="primary" if st.session_state.pagina == id_pag else "secondary", use_container_width=True):
            st.session_state.pagina = id_pag
            st.rerun()

# ── ÁREA PRINCIPAL (EXECUÇÃO) ──
# Esta parte agora está fora de qualquer função, no nível mestre do script
if st.session_state.modulo == "rh":
    if st.session_state.pagina == "indicadores": pg_rh_indicadores()
    elif st.session_state.pagina == "vagas": pg_rh_vagas()
    elif st.session_state.pagina == "candidatos": pg_rh_candidatos()

elif st.session_state.modulo == "dp":
    st.markdown(f"## {st.session_state.pagina.capitalize()}")
    st.info("Página do módulo DP carregada.")

elif st.session_state.modulo == "fin":
    st.markdown(f"## {st.session_state.pagina.upper()}")
    st.info("Página do módulo Financeiro carregada.")
