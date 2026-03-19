import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime, timedelta
import json

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="ETUS · Sistema RH",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --blue: #1a56db;
    --green: #0a7a3c;
    --amber: #b45309;
    --red: #c0392b;
    --purple: #6d28d9;
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Main background */
.stApp {background: #eef1f7;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
section[data-testid="stSidebar"] * {color: #6b7a9a !important;}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 12px !important;
    padding: 6px 10px !important;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    color: #e2e8f0 !important;
    background: rgba(255,255,255,0.06) !important;
}

/* KPI Cards */
.kpi-card {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 4px 12px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 3px 3px 0 0;
}
.kpi-blue::before { background: #1a56db; }
.kpi-green::before { background: #0a7a3c; }
.kpi-amber::before { background: #b45309; }
.kpi-red::before { background: #c0392b; }
.kpi-purple::before { background: #6d28d9; }

.kpi-label {
    font-size: 9px;
    color: #6b7a9a;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-weight: 600;
    margin-bottom: 4px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-blue .kpi-value { color: #1a56db; }
.kpi-green .kpi-value { color: #0a7a3c; }
.kpi-amber .kpi-value { color: #b45309; }
.kpi-red .kpi-value { color: #c0392b; }
.kpi-purple .kpi-value { color: #6d28d9; }

.badge {
    font-size: 10px;
    padding: 2px 9px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}
.badge-green { background: #e8f5ee; color: #0a7a3c; border: 1px solid #9fd4b8; }
.badge-blue { background: #ebf1fd; color: #1a56db; border: 1px solid #b3caf5; }
.badge-amber { background: #fef3e2; color: #b45309; border: 1px solid #f6cc7e; }
.badge-red { background: #fdecea; color: #c0392b; border: 1px solid #f5b7b0; }
.badge-purple { background: #f0ebfe; color: #6d28d9; border: 1px solid #c4aaee; }
.badge-gray { background: #f3f5f9; color: #6b7a9a; border: 1px solid rgba(0,0,0,0.07); }

.notif-warn {
    background: #fef3e2;
    border: 1px solid #f6cc7e;
    color: #b45309;
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 12px;
    margin-bottom: 12px;
}
.notif-info {
    background: #ebf1fd;
    border: 1px solid #b3caf5;
    color: #1a56db;
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 12px;
    margin-bottom: 12px;
}
.notif-ok {
    background: #e8f5ee;
    border: 1px solid #9fd4b8;
    color: #0a7a3c;
    border-radius: 7px;
    padding: 10px 14px;
    font-size: 12px;
    margin-bottom: 12px;
}

.logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #60a5fa;
    letter-spacing: -1px;
}
.logo-sub {
    font-size: 9px;
    color: #4a6085;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Streamlit button overrides */
.stButton > button {
    border-radius: 7px;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid rgba(0,0,0,0.1);
    transition: all 0.15s;
}
.stButton > button[kind="primary"] {
    background: #1a56db;
    border-color: #1a56db;
    color: white;
}

/* Tables */
.stDataFrame {border-radius: 8px; overflow: hidden;}
thead tr th {
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: #6b7a9a !important;
    background: #f3f5f9 !important;
}

/* Form inputs */
.stTextInput input, .stSelectbox select, .stDateInput input, .stNumberInput input {
    border-radius: 7px !important;
    border: 1px solid rgba(0,0,0,0.1) !important;
    font-size: 12px !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 12px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
}

/* Section panels */
.panel-box {
    background: #fff;
    border: 1px solid rgba(0,0,0,0.07);
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    margin-bottom: 14px;
}
.panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #131929;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.dot-green { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #0a7a3c; }
.dot-blue { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #1a56db; }
.dot-amber { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #b45309; }
.dot-purple { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #6d28d9; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INIT ──
def init_state():
    defaults = {
        "modulo": "rh",
        "pagina": "indicadores",
        # RH data
        "vagas": [
            {"titulo": "Gerente de Operações", "time": "Operações", "status": "Ativa", "candidatos": 120, "dias": 17, "prioridade": "Alta"},
            {"titulo": "Analista Financeiro Sr.", "time": "Financeiro", "status": "Ativa", "candidatos": 85, "dias": 24, "prioridade": "Média"},
            {"titulo": "Dev Fullstack", "time": "Tecnologia", "status": "Banco", "candidatos": 12, "dias": 52, "prioridade": "Baixa"},
        ],
        "candidatos": [
            {"nome": "Ana Beatriz Lima", "local": "São Paulo, SP", "vaga": "Gerente de Operações", "fase": "Entrevista RH", "score": 82, "origem": "LinkedIn", "dias": 12, "status": "Em andamento"},
            {"nome": "Rodrigo Fernandes", "local": "Campinas, SP", "vaga": "Analista Financeiro Sr.", "fase": "Proposta", "score": 76, "origem": "Indicação", "dias": 47, "status": "Pendente"},
            {"nome": "Camila Souza", "local": "São Paulo, SP", "vaga": "Gerente de Operações", "fase": "Teste Online", "score": 91, "origem": "Indeed", "dias": 8, "status": "Em andamento"},
            {"nome": "Felipe Marques", "local": "Rio de Janeiro, RJ", "vaga": "Analista Financeiro Sr.", "fase": "Triagem", "score": 64, "origem": "Gupy", "dias": 3, "status": "Em andamento"},
            {"nome": "Mariana Costa", "local": "Barueri, SP", "vaga": "Gerente de Operações", "fase": "Aprovado", "score": 95, "origem": "LinkedIn", "dias": 17, "status": "Aprovado"},
            {"nome": "Paulo Rodrigues", "local": "São Paulo, SP", "vaga": "Analista Financeiro Sr.", "fase": "Triagem", "score": 71, "origem": "Site ETUS", "dias": 2, "status": "Em andamento"},
            {"nome": "Larissa Nunes", "local": "Guarulhos, SP", "vaga": "Gerente de Operações", "fase": "Entrevista RH", "score": 88, "origem": "LinkedIn", "dias": 15, "status": "Em andamento"},
        ],
        "onboarding": [
            {"nome": "Mariana Costa", "cargo": "Gerente de Operações", "time": "Operações", "inicio": "2026-03-10", "progresso": 65, "pendencias": ["Contrato assinado", "E-mail corporativo"]},
            {"nome": "Lucas Teixeira", "cargo": "Dev Fullstack", "time": "Tecnologia", "inicio": "2026-03-15", "progresso": 30, "pendencias": ["Documentação RH", "Crachá", "Acesso sistemas"]},
        ],
        # DP data
        "estagiarios": [
            {"nome": "Carlos Mendes", "instituicao": "USP", "time": "Tecnologia", "inicio": "2025-08-01", "fim": "2026-07-31", "carga": "20h/semana"},
            {"nome": "Juliana Ramos", "instituicao": "FGV", "time": "Financeiro", "inicio": "2025-09-01", "fim": "2026-08-31", "carga": "30h/semana"},
            {"nome": "Pedro Alves", "instituicao": "UNICAMP", "time": "Comercial", "inicio": "2025-10-01", "fim": "2026-09-30", "carga": "20h/semana"},
            {"nome": "Sofia Lima", "instituicao": "PUC-SP", "time": "Marketing", "inicio": "2026-01-10", "fim": "2027-01-09", "carga": "20h/semana"},
            {"nome": "Rafael Costa", "instituicao": "Mackenzie", "time": "Operações", "inicio": "2026-02-01", "fim": "2027-01-31", "carga": "30h/semana"},
            {"nome": "Ana Ferreira", "instituicao": "ESPM", "time": "Marketing", "inicio": "2026-02-15", "fim": "2027-02-14", "carga": "20h/semana"},
            {"nome": "Bruno Santos", "instituicao": "FEI", "time": "Tecnologia", "inicio": "2026-03-01", "fim": "2027-02-28", "carga": "20h/semana"},
            {"nome": "Isabela Rocha", "instituicao": "INSPER", "time": "Financeiro", "inicio": "2026-03-10", "fim": "2027-03-09", "carga": "30h/semana"},
        ],
        "colaboradores": [
            {"nome": "Diego Carvalho", "vinculo": "PJ", "cargo": "Dev Fullstack Sr.", "cnpj": "12.345.678/0001-90", "inicio": "2024-01-15", "valor": 12000},
            {"nome": "Priscila Moura", "vinculo": "PJ", "cargo": "Designer UX/UI", "cnpj": "98.765.432/0001-11", "inicio": "2024-06-01", "valor": 8500},
        ],
        "periodos": [
            {"nome": "Carlos Mendes", "cargo": "Estagiário Tecnologia", "time": "Tecnologia", "inicio": "2025-08-01", "status": "Concluído"},
            {"nome": "Juliana Ramos", "cargo": "Estagiária Financeiro", "time": "Financeiro", "inicio": "2025-09-01", "status": "Concluído"},
            {"nome": "Pedro Alves", "cargo": "Estagiário Comercial", "time": "Comercial", "inicio": "2025-10-01", "status": "Em avaliação"},
            {"nome": "Sofia Lima", "cargo": "Estagiária Marketing", "time": "Marketing", "inicio": "2026-01-10", "status": "Em andamento"},
            {"nome": "Rafael Costa", "cargo": "Estagiário Operações", "time": "Operações", "inicio": "2026-02-01", "status": "Vencendo"},
            {"nome": "Ana Ferreira", "cargo": "Estagiária Marketing", "time": "Marketing", "inicio": "2026-02-15", "status": "Vencendo"},
        ],
        # Financeiro data
        "notas_ifood": [],
        "pagamentos": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 16px 0">
        <div class="logo-text">● ETUS</div>
        <div class="logo-sub">Sistema de Gestão</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:9px;color:#374151;letter-spacing:2px;text-transform:uppercase;font-weight:600;margin-bottom:8px">Módulos</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👥 RH", use_container_width=True, type="primary" if st.session_state.modulo == "rh" else "secondary"):
            st.session_state.modulo = "rh"
            st.session_state.pagina = "indicadores"
            st.rerun()
    with col2:
        if st.button("📋 DP", use_container_width=True, type="primary" if st.session_state.modulo == "dp" else "secondary"):
            st.session_state.modulo = "dp"
            st.session_state.pagina = "dashboard"
            st.rerun()
    with col3:
        if st.button("💰 Fin", use_container_width=True, type="primary" if st.session_state.modulo == "fin" else "secondary"):
            st.session_state.modulo = "fin"
            st.session_state.pagina = "ifood"
            st.rerun()

    st.markdown("---")
    st.markdown('<div style="font-size:9px;color:#374151;letter-spacing:2px;text-transform:uppercase;font-weight:600;margin-bottom:8px">Navegação</div>', unsafe_allow_html=True)

    nav_config = {
        "rh": [("indicadores", "◈ Indicadores"), ("vagas", "📋 Vagas"), ("candidatos", "⚙ Candidatos"), ("onboarding", "🚀 Onboarding")],
        "dp": [("dashboard", "◈ Dashboard DP"), ("estagiarios", "🎓 Estagiários"), ("colaboradores", "👥 Colaboradores"), ("periodo", "⏳ Período de Experiência")],
        "fin": [("ifood", "🍔 iFood"), ("outros", "💸 Outros Pagamentos"), ("dashboard", "◈ Dashboard Financeiro")],
    }

    for pg_id, pg_lbl in nav_config[st.session_state.modulo]:
        is_active = st.session_state.pagina == pg_id
        btn_style = "primary" if is_active else "secondary"
        if st.button(pg_lbl, use_container_width=True, type=btn_style, key=f"nav_{pg_id}"):
            st.session_state.pagina = pg_id
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="display:flex;align-items:center;gap:9px;padding:4px 0">
        <div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0">AD</div>
        <div>
            <div style="font-size:11px;font-weight:500;color:#e2e8f0">Admin ETUS</div>
            <div style="font-size:9px;color:#6b7a9a">Gerente RH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── HELPER FUNCTIONS ──
def kpi_card(label, value, color="blue", badge_text=None, badge_type="nt", meta=None):
    badge_colors = {"up": "green", "dn": "red", "nt": "amber", "ok": "green"}
    bc = badge_colors.get(badge_type, "gray")
    badge_html = f'<span class="badge badge-{bc}">{badge_text}</span>' if badge_text else ""
    meta_html = f'<div style="font-size:10px;color:#6b7a9a;margin-top:4px">{meta}</div>' if meta else ""
    st.markdown(f"""
    <div class="kpi-card kpi-{color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {badge_html}
        {meta_html}
    </div>
    """, unsafe_allow_html=True)

def panel_header(title, dot_color="blue"):
    st.markdown(f'<div class="panel-title"><span class="dot-{dot_color}"></span>{title}</div>', unsafe_allow_html=True)

def plotly_defaults():
    return dict(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", size=11, color="#6b7a9a"),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
    )

# ══════════════════════════════════════
#  MODULE: RH
# ══════════════════════════════════════
def page_rh_indicadores():
    st.markdown("## ◈ Indicadores de Recrutamento")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Vagas Abertas", "3", "blue", "↔ estável", "nt", "2 ativas · 1 banco")
    with c2: kpi_card("Candidatos Ativos", "217", "green", "↑ +12%", "up", "este mês")
    with c3: kpi_card("Tempo Médio Contrat.", "24d", "amber", "⚠ acima meta", "dn", "meta: 30d")
    with c4: kpi_card("Taxa de Aprovação", "3.7%", "purple", "↑ +0.4pp", "up", "últimos 90d")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Funil", "⏱ Tempo", "🔍 Fontes"])

    with tab1:
        col_left, col_right = st.columns([1, 1.2])
        with col_left:
            panel_header("Vagas por Posição", "blue")
            fig = go.Figure(go.Pie(
                labels=["Gerente de Operações", "Analista Financeiro", "Banco de Talentos"],
                values=[120, 85, 12],
                hole=0.72,
                marker=dict(colors=["#1a56db", "#6d28d9", "#0277bd"], line=dict(color="#fff", width=3)),
            ))
            fig.update_layout(**plotly_defaults(), height=200)
            fig.update_traces(textinfo="none", hovertemplate="%{label}: %{value} candidatos<extra></extra>")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Legend
            for lbl, val, color in [("Gerente de Operações", 120, "#1a56db"), ("Analista Financeiro Sr.", 85, "#6d28d9"), ("Banco de Talentos", 12, "#0277bd")]:
                st.markdown(f'<div style="display:flex;align-items:center;gap:8px;font-size:11px;margin-bottom:4px"><span style="width:10px;height:10px;border-radius:50%;background:{color};display:inline-block"></span>{lbl} <strong style="margin-left:auto">{val}</strong></div>', unsafe_allow_html=True)

        with col_right:
            panel_header("Vagas Ativas", "green")
            for v in st.session_state.vagas:
                prio_color = {"Alta": "red", "Média": "amber", "Baixa": "blue"}.get(v["prioridade"], "gray")
                st.markdown(f"""
                <div style="background:#f9fafb;border:1px solid rgba(0,0,0,0.07);border-radius:7px;padding:10px 14px;margin-bottom:8px">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div>
                            <div style="font-weight:600;font-size:13px">{v['titulo']}</div>
                            <div style="font-size:10px;color:#6b7a9a">{v['time']} · {v['candidatos']} candidatos · {v['dias']}d aberta</div>
                        </div>
                        <span class="badge badge-{prio_color}">{v['prioridade']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        panel_header("Funil de Recrutamento", "blue")
        funil_data = [217, 130, 64, 28, 12, 8]
        funil_labels = ["Candidatos", "Triagem RH", "Teste Online", "Entrevista", "Proposta", "Aprovados"]
        colors = ["#1a56db", "#4f46e5", "#6d28d9", "#0a7a3c", "#0277bd", "#10b981"]

        fig = go.Figure()
        max_v = funil_data[0]
        for i, (lbl, val, clr) in enumerate(zip(funil_labels, funil_data, colors)):
            pct = val / max_v * 100
            fig.add_trace(go.Bar(
                x=[pct], y=[lbl], orientation='h',
                marker_color=clr, name=lbl,
                text=f"{val}", textposition="inside",
                hovertemplate=f"{lbl}: {val} candidatos ({pct:.0f}%)<extra></extra>",
            ))

        fig.update_layout(**plotly_defaults(), height=280, showlegend=False,
            xaxis=dict(visible=False), yaxis=dict(tickfont=dict(size=11, color="#374151")),
            barmode="overlay")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Conversion rates
        cols = st.columns(5)
        for i in range(len(funil_data) - 1):
            pct = round(funil_data[i+1] / funil_data[i] * 100, 1)
            with cols[i]:
                st.metric(f"{funil_labels[i]}→{funil_labels[i+1]}", f"{pct}%")

    with tab3:
        panel_header("Histórico de Tempo de Contratação", "blue")
        meses = ["Set/25", "Out/25", "Nov/25", "Dez/25", "Jan/26", "Fev/26", "Mar/26"]
        tempos = [22, 28, 52, 31, 11, 24, 17]
        meta = [30] * 7

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=tempos, name="Tempo real (dias)",
            line=dict(color="#1a56db", width=2.5), fill="tozeroy",
            fillcolor="rgba(26,86,219,0.07)", mode="lines+markers",
            marker=dict(size=6, color="#fff", line=dict(color="#1a56db", width=2))))
        fig.add_trace(go.Scatter(x=meses, y=meta, name="Meta SLA 30d",
            line=dict(color="rgba(192,57,43,0.6)", width=1.5, dash="dot"), mode="lines"))
        fig.update_layout(**plotly_defaults(), height=250, showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1, font=dict(size=10)),
            yaxis=dict(ticksuffix="d", gridcolor="rgba(0,0,0,0.04)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0.04)"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        panel_header("Dias Médios por Fase", "amber")
        fases = ["Triagem", "Teste", "Entrevista", "Proposta"]
        dias_fase = [3, 5, 6, 8]
        clrs = ["rgba(26,86,219,0.8)", "rgba(109,40,217,0.8)", "rgba(10,122,60,0.8)", "rgba(180,83,9,0.8)"]
        fig2 = go.Figure(go.Bar(x=fases, y=dias_fase, marker_color=clrs, text=[f"{d}d" for d in dias_fase],
            textposition="outside", marker_line_width=0))
        fig2.update_layout(**plotly_defaults(), height=180,
            yaxis=dict(ticksuffix="d", gridcolor="rgba(0,0,0,0.04)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with tab4:
        panel_header("Candidatos por Canal", "blue")
        canais = ["LinkedIn", "Gupy", "Indeed", "Indicação", "Site ETUS", "Outros"]
        qtd = [98, 54, 32, 20, 8, 5]
        clrs_c = ["#1a56db", "#6d28d9", "#0277bd", "#0a7a3c", "#b45309", "#9eacc0"]
        fig = go.Figure(go.Bar(y=canais, x=qtd, orientation="h",
            marker_color=clrs_c, text=qtd, textposition="outside"))
        fig.update_layout(**plotly_defaults(), height=250,
            xaxis=dict(gridcolor="rgba(0,0,0,0.04)"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        panel_header("Taxa de Conversão por Fonte (%)", "green")
        conv = [("Indicação", 15.0, "#0a7a3c"), ("LinkedIn", 5.2, "#1a56db"),
                ("Site ETUS", 4.8, "#b45309"), ("Gupy", 3.1, "#6d28d9"),
                ("Indeed", 2.4, "#0277bd"), ("Outros", 1.1, "#9eacc0")]
        for nome, pct, clr in conv:
            bar_w = int(pct / 15 * 100)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;font-size:11px">
                <div style="width:80px;text-align:right;color:#6b7a9a;font-weight:500">{nome}</div>
                <div style="flex:1;height:22px;background:#f3f5f9;border-radius:5px;overflow:hidden;border:1px solid rgba(0,0,0,0.07)">
                    <div style="width:{bar_w}%;height:100%;background:{clr};border-radius:5px;display:flex;align-items:center;padding-left:8px;font-size:10px;font-weight:700;color:#fff">{pct}%</div>
                </div>
                <div style="width:30px;font-weight:600;color:#374151">{pct}</div>
            </div>
            """, unsafe_allow_html=True)


def page_rh_vagas():
    st.markdown("## 📋 Gestão de Vagas")

    with st.expander("➕ Cadastrar Nova Vaga", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            titulo = st.text_input("Título da Vaga", placeholder="Ex: Analista de Marketing")
            time_vaga = st.selectbox("Time", ["Tecnologia", "Financeiro", "Comercial", "Operações", "Marketing", "RH"])
        with c2:
            prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            status_vaga = st.selectbox("Status", ["Ativa", "Banco de Talentos", "Encerrada"])

        descricao = st.text_area("Descrição / Requisitos", height=80, placeholder="Descreva os requisitos da vaga...")

        if st.button("+ Cadastrar Vaga", type="primary"):
            if titulo:
                st.session_state.vagas.append({
                    "titulo": titulo, "time": time_vaga, "status": status_vaga,
                    "candidatos": 0, "dias": 0, "prioridade": prioridade
                })
                st.success("✅ Vaga cadastrada com sucesso!")
                st.rerun()
            else:
                st.error("Preencha o título da vaga.")

    st.markdown("---")

    kpis = st.columns(3)
    ativas = sum(1 for v in st.session_state.vagas if v["status"] == "Ativa")
    banco = sum(1 for v in st.session_state.vagas if v["status"] == "Banco de Talentos")
    total_cands = sum(v["candidatos"] for v in st.session_state.vagas)
    with kpis[0]: kpi_card("Vagas Ativas", ativas, "blue", "↔", "nt")
    with kpis[1]: kpi_card("Banco de Talentos", banco, "purple", "↔", "nt")
    with kpis[2]: kpi_card("Total Candidatos", total_cands, "green", "↑", "up")

    st.markdown("---")
    panel_header("Lista de Vagas", "blue")

    if st.session_state.vagas:
        df = pd.DataFrame(st.session_state.vagas)
        df.columns = ["Título", "Time", "Status", "Candidatos", "Dias Aberta", "Prioridade"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma vaga cadastrada.")


def page_rh_candidatos():
    st.markdown("## ⚙ Candidatos")

    with st.expander("➕ Adicionar Candidato", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            nome_c = st.text_input("Nome Completo", key="cand_nome")
            local_c = st.text_input("Cidade/Estado", placeholder="São Paulo, SP", key="cand_local")
            vaga_c = st.selectbox("Vaga", [v["titulo"] for v in st.session_state.vagas] or ["Sem vagas"], key="cand_vaga")
        with c2:
            fase_c = st.selectbox("Fase", ["Triagem", "Teste Online", "Entrevista RH", "Proposta", "Aprovado"], key="cand_fase")
            origem_c = st.selectbox("Origem", ["LinkedIn", "Gupy", "Indeed", "Indicação", "Site ETUS", "Outros"], key="cand_origem")
            score_c = st.number_input("Score (%)", 0, 100, 70, key="cand_score")

        if st.button("+ Adicionar Candidato", type="primary"):
            if nome_c:
                status_map = {"Triagem": "Em andamento", "Teste Online": "Em andamento", "Entrevista RH": "Em andamento", "Proposta": "Pendente", "Aprovado": "Aprovado"}
                st.session_state.candidatos.append({
                    "nome": nome_c, "local": local_c, "vaga": vaga_c, "fase": fase_c,
                    "score": score_c, "origem": origem_c, "dias": 0,
                    "status": status_map.get(fase_c, "Em andamento")
                })
                st.success(f"✅ {nome_c} adicionado!")
                st.rerun()
            else:
                st.error("Preencha o nome do candidato.")

    st.markdown("---")

    # Filter
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Buscar candidato", placeholder="Nome, vaga, fase...", key="cand_search")
    with col_filter:
        fase_filter = st.selectbox("Filtrar por fase", ["Todas", "Triagem", "Teste Online", "Entrevista RH", "Proposta", "Aprovado"], key="cand_fase_filter")

    cands = st.session_state.candidatos
    if search_term:
        cands = [c for c in cands if search_term.lower() in c["nome"].lower() or search_term.lower() in c["vaga"].lower()]
    if fase_filter != "Todas":
        cands = [c for c in cands if c["fase"] == fase_filter]

    st.markdown(f'<div style="font-size:10px;color:#6b7a9a;margin-bottom:8px">Exibindo {len(cands)} candidatos</div>', unsafe_allow_html=True)

    fase_colors = {"Triagem": "blue", "Teste Online": "purple", "Entrevista RH": "blue",
                   "Proposta": "amber", "Aprovado": "green"}

    for c in cands:
        fc = fase_colors.get(c["fase"], "gray")
        score_color = "#0a7a3c" if c["score"] >= 80 else ("#b45309" if c["score"] >= 60 else "#c0392b")
        st.markdown(f"""
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);border-radius:8px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:14px;box-shadow:0 1px 3px rgba(0,0,0,0.05)">
            <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0">{c['nome'][:2].upper()}</div>
            <div style="flex:1">
                <div style="font-weight:600;font-size:13px">{c['nome']}</div>
                <div style="font-size:10px;color:#6b7a9a">{c['local']} · {c['vaga']} · {c['origem']} · {c['dias']}d</div>
            </div>
            <span class="badge badge-{fc}">{c['fase']}</span>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:15px;color:{score_color};min-width:35px;text-align:right">{c['score']}</div>
        </div>
        """, unsafe_allow_html=True)


def page_rh_onboarding():
    st.markdown("## 🚀 Onboarding")

    st.markdown('<div class="notif-warn">⚠️ Hygor Lessa tem documentos pendentes. Prazo: 25/03/2026.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(3)[:2]
    with c1: kpi_card("Em Onboarding", len(st.session_state.onboarding), "blue", "↔", "nt")
    with c2: kpi_card("Concluídos (30d)", "3", "green", "↑ +1", "up")

    st.markdown("---")
    panel_header("Processos Ativos", "blue")

    for o in st.session_state.onboarding:
        pct = o["progresso"]
        bar_color = "#0a7a3c" if pct >= 80 else ("#1a56db" if pct >= 40 else "#b45309")
        pendencias_html = " · ".join([f'<span class="badge badge-amber">{p}</span>' for p in o["pendencias"]])
        st.markdown(f"""
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);border-radius:8px;padding:14px 16px;margin-bottom:10px">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                <div>
                    <div style="font-weight:600;font-size:13px">{o['nome']}</div>
                    <div style="font-size:10px;color:#6b7a9a">{o['cargo']} · {o['time']} · Início: {o['inicio']}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:18px;color:{bar_color}">{pct}%</div>
            </div>
            <div style="height:6px;background:#f3f5f9;border-radius:3px;overflow:hidden;margin-bottom:8px">
                <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:3px"></div>
            </div>
            <div style="display:flex;gap:6px;flex-wrap:wrap">{pendencias_html}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════
#  MODULE: DP
# ══════════════════════════════════════
def page_dp_dashboard():
    st.markdown("## ◈ Dashboard — Departamento Pessoal")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Total Colaboradores", "10", "blue", "↔", "nt", "headcount atual")
    with c2: kpi_card("Estagiários Ativos", len(st.session_state.estagiarios), "green", "↑ +1 mês", "up", "5 times")
    with c3: kpi_card("Exp. Vencendo (30d)", "2", "amber", "⚠ atenção", "dn", "avaliar esta semana")
    with c4: kpi_card("Contratos Vigentes", str(len(st.session_state.estagiarios) + len(st.session_state.colaboradores)), "purple", "↔", "nt", "estágio + PJ")

    st.markdown("---")

    col_donut, col_times, col_evol = st.columns([1, 1.4, 1.4])

    with col_donut:
        panel_header("Distribuição por Vínculo", "green")
        n_est = len(st.session_state.estagiarios)
        n_pj = len(st.session_state.colaboradores)
        fig = go.Figure(go.Pie(
            labels=["Estagiários", "PJ"],
            values=[n_est, n_pj],
            hole=0.68,
            marker=dict(colors=["#0a7a3c", "#1a56db"], line=dict(color="#fff", width=3)),
        ))
        fig.update_layout(**plotly_defaults(), height=180)
        fig.update_traces(textinfo="none")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        total = n_est + n_pj
        for lbl, val, clr in [("Estagiários", n_est, "#0a7a3c"), ("PJ", n_pj, "#1a56db")]:
            pct = round(val/total*100) if total else 0
            st.markdown(f'<div style="display:flex;align-items:center;gap:7px;font-size:11px;margin-bottom:4px"><span style="width:9px;height:9px;border-radius:50%;background:{clr};display:inline-block"></span>{lbl} <strong style="margin-left:auto">{val}</strong> <span style="color:#6b7a9a">{pct}%</span></div>', unsafe_allow_html=True)

    with col_times:
        panel_header("Estagiários por Time", "blue")
        times_count = {}
        for e in st.session_state.estagiarios:
            times_count[e["time"]] = times_count.get(e["time"], 0) + 1
        if times_count:
            fig2 = go.Figure(go.Bar(
                x=list(times_count.keys()), y=list(times_count.values()),
                marker_color=["#1a56db", "#6d28d9", "#0a7a3c", "#b45309", "#0277bd"],
                text=list(times_count.values()), textposition="outside",
            ))
            fig2.update_layout(**plotly_defaults(), height=200,
                xaxis=dict(gridcolor="rgba(0,0,0,0)"), yaxis=dict(gridcolor="rgba(0,0,0,0.04)"))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col_evol:
        panel_header("Evolução de Contratos", "blue")
        meses = ["Out/25", "Nov/25", "Dez/25", "Jan/26", "Fev/26", "Mar/26"]
        contratos = [5, 5, 6, 7, 8, 8 + len(st.session_state.estagiarios) - 8]
        fig3 = go.Figure(go.Scatter(x=meses, y=contratos, fill="tozeroy",
            line=dict(color="#1a56db", width=2.5), fillcolor="rgba(26,86,219,0.07)",
            mode="lines+markers", marker=dict(size=6, color="#fff", line=dict(color="#1a56db", width=2))))
        fig3.update_layout(**plotly_defaults(), height=200,
            yaxis=dict(gridcolor="rgba(0,0,0,0.04)"), xaxis=dict(gridcolor="rgba(0,0,0,0.04)"))
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("---")
    panel_header("Progresso dos Contratos de Estágio", "amber")

    today = date.today()
    for e in st.session_state.estagiarios:
        try:
            ini = date.fromisoformat(e["inicio"])
            fim = date.fromisoformat(e["fim"])
            total_days = (fim - ini).days
            elapsed = (today - ini).days
            pct = min(100, max(0, int(elapsed / total_days * 100))) if total_days > 0 else 0
            dias_rest = (fim - today).days
            bar_color = "#c0392b" if pct > 85 else ("#b45309" if pct > 60 else "#1a56db")
            st.markdown(f"""
            <div style="margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                    <div>
                        <span style="font-size:13px;font-weight:600">{e['nome']}</span>
                        <span style="font-size:10px;color:#6b7a9a;margin-left:8px">{e['time']}</span>
                    </div>
                    <div style="text-align:right">
                        <span style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:{bar_color}">{pct}%</span>
                        <span style="font-size:9px;color:#6b7a9a;display:block">{dias_rest}d restantes</span>
                    </div>
                </div>
                <div style="height:7px;background:#f3f5f9;border-radius:4px;overflow:hidden;border:1px solid rgba(0,0,0,0.07)">
                    <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:4px;transition:width 1s"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except:
            pass


def page_dp_estagiarios():
    st.markdown("## 🎓 Estagiários")

    col_form, col_list = st.columns(2)

    with col_form:
        panel_header("Novo Registro", "green")
        with st.container():
            nome_e = st.text_input("Nome Completo", key="e_nome")
            inst_e = st.text_input("Instituição de Ensino", placeholder="Ex: USP, FGV, UNICAMP...")
            c1, c2 = st.columns(2)
            with c1:
                time_e = st.selectbox("Time", ["Tecnologia", "Financeiro", "Comercial", "Operações", "Marketing"])
                ini_e = st.date_input("Início", value=date.today())
            with c2:
                carga_e = st.selectbox("Carga Horária", ["20h/semana", "30h/semana"])
                fim_e = st.date_input("Fim", value=date.today() + timedelta(days=180))

            if st.button("+ Cadastrar Estagiário", type="primary", use_container_width=True):
                if nome_e:
                    st.session_state.estagiarios.append({
                        "nome": nome_e, "instituicao": inst_e, "time": time_e,
                        "inicio": ini_e.isoformat(), "fim": fim_e.isoformat(), "carga": carga_e
                    })
                    st.success(f"✅ {nome_e} cadastrado!")
                    st.rerun()
                else:
                    st.error("Preencha o nome do estagiário.")

    with col_list:
        panel_header(f"Estagiários · Total: {len(st.session_state.estagiarios)}", "blue")
        for e in st.session_state.estagiarios:
            st.markdown(f"""
            <div style="background:#f9fafb;border:1px solid rgba(0,0,0,0.07);border-radius:7px;padding:10px 14px;margin-bottom:7px;display:flex;align-items:center;gap:10px">
                <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;flex-shrink:0">{e['nome'][:2].upper()}</div>
                <div style="flex:1">
                    <div style="font-weight:600;font-size:12.5px">{e['nome']}</div>
                    <div style="font-size:10px;color:#6b7a9a">{e['instituicao']} · {e['time']} · {e['carga']}</div>
                </div>
                <span class="badge badge-green">Ativo</span>
            </div>
            """, unsafe_allow_html=True)


def page_dp_colaboradores():
    st.markdown("## 👥 Colaboradores PJ")

    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Total PJ", len(st.session_state.colaboradores), "blue", "↔", "nt")
    with c2: kpi_card("Contratos Ativos", len(st.session_state.colaboradores), "green", "↔", "nt")
    with c3: kpi_card("Benefícios Pendentes", "0", "amber", "✓ ok", "ok")

    st.markdown("---")

    with st.expander("➕ Novo Colaborador", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            nome_cl = st.text_input("Nome", key="cl_nome")
            cargo_cl = st.text_input("Cargo", placeholder="Ex: Dev Fullstack Sr.")
            ini_cl = st.date_input("Início", value=date.today(), key="cl_ini")
        with c2:
            vinculo_cl = st.selectbox("Vínculo", ["PJ", "CLT"])
            cnpj_cl = st.text_input("CNPJ / CPF", placeholder="00.000.000/0001-00")
            valor_cl = st.number_input("Valor Mensal (R$)", min_value=0.0, step=100.0, key="cl_valor")

        if st.button("+ Cadastrar Colaborador", type="primary"):
            if nome_cl:
                st.session_state.colaboradores.append({
                    "nome": nome_cl, "vinculo": vinculo_cl, "cargo": cargo_cl,
                    "cnpj": cnpj_cl, "inicio": ini_cl.isoformat(), "valor": valor_cl
                })
                st.success(f"✅ {nome_cl} cadastrado!")
                st.rerun()
            else:
                st.error("Preencha o nome.")

    panel_header("Lista de Colaboradores", "blue")
    for c in st.session_state.colaboradores:
        valor_fmt = f"R$ {c['valor']:,.0f}".replace(",", ".")
        st.markdown(f"""
        <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);border-radius:8px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px">
            <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#0a7a3c,#1a56db);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0">{c['nome'][:2].upper()}</div>
            <div style="flex:1">
                <div style="font-weight:600;font-size:13px">{c['nome']}</div>
                <div style="font-size:10px;color:#6b7a9a">{c['cargo']} · CNPJ: {c['cnpj']} · Desde {c['inicio']}</div>
            </div>
            <span class="badge badge-blue">{c['vinculo']}</span>
            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:14px">{valor_fmt}</div>
        </div>
        """, unsafe_allow_html=True)


def page_dp_periodo():
    st.markdown("## ⏳ Período de Experiência")

    st.markdown('<div class="notif-warn">⏰ 2 avaliações vencem nos próximos 30 dias. Revise antes dos prazos.</div>', unsafe_allow_html=True)

    col_form, col_list = st.columns(2)

    with col_form:
        panel_header("Cadastrar Novo Período", "green")
        nome_p = st.text_input("Nome do Prestador / Estagiário", key="p_nome")
        cargo_p = st.text_input("Cargo", placeholder="Ex: Analista Trainee", key="p_cargo")
        c1, c2 = st.columns(2)
        with c1:
            time_p = st.selectbox("Time", ["Tecnologia", "Financeiro", "Comercial", "Operações", "RH"])
        with c2:
            ini_p = st.date_input("Data de Início", value=date.today(), key="p_ini")

        if st.button("+ Cadastrar Controle", type="primary", use_container_width=True):
            if nome_p:
                st.session_state.periodos.append({
                    "nome": nome_p, "cargo": cargo_p, "time": time_p,
                    "inicio": ini_p.isoformat(), "status": "Em andamento"
                })
                st.success("✅ Controle cadastrado!")
                st.rerun()
            else:
                st.error("Preencha o nome.")

    with col_list:
        panel_header(f"Avaliações (90 dias) · Total: {len(st.session_state.periodos)}", "amber")
        status_colors = {"Concluído": "green", "Em avaliação": "purple", "Em andamento": "blue", "Vencendo": "red"}

        today = date.today()
        for p in st.session_state.periodos:
            try:
                ini = date.fromisoformat(p["inicio"])
                fim_90 = ini + timedelta(days=90)
                dias_rest = (fim_90 - today).days
                pct = min(100, max(0, int((today - ini).days / 90 * 100)))
                sc = status_colors.get(p["status"], "gray")
                bar_color = "#c0392b" if pct > 85 else ("#b45309" if pct > 60 else "#1a56db")
            except:
                dias_rest, pct, sc, bar_color = 0, 0, "gray", "#1a56db"

            st.markdown(f"""
            <div style="background:#f9fafb;border:1px solid rgba(0,0,0,0.07);border-radius:7px;padding:10px 14px;margin-bottom:8px">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                    <div>
                        <div style="font-weight:600;font-size:12.5px">{p['nome']}</div>
                        <div style="font-size:10px;color:#6b7a9a">{p['cargo']} · {p['time']}</div>
                    </div>
                    <span class="badge badge-{sc}">{p['status']}</span>
                </div>
                <div style="height:5px;background:#eef1f7;border-radius:3px;overflow:hidden">
                    <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:3px"></div>
                </div>
                <div style="font-size:9px;color:#6b7a9a;margin-top:4px">{pct}% concluído · {max(0, dias_rest)}d restantes</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════
#  MODULE: FINANCEIRO
# ══════════════════════════════════════
def page_fin_ifood():
    st.markdown("## 🍔 Notas Fiscais iFood")

    notas = st.session_state.notas_ifood
    total_v = sum(n["valor"] for n in notas)
    pendentes = sum(1 for n in notas if n["status"] == "Pendente")

    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Notas Cadastradas", len(notas), "green", "↔ este mês", "nt")
    with c2: kpi_card("Total Faturado", f"R${total_v:,.0f}".replace(",", "."), "blue", "↔", "nt")
    with c3: kpi_card("Pendentes Emissão", pendentes, "amber", "✓ ok" if pendentes == 0 else f"⚠ {pendentes}", "ok" if pendentes == 0 else "dn")

    st.markdown("---")

    with st.expander("➕ Nova Nota Fiscal iFood", expanded=len(notas) == 0):
        c1, c2 = st.columns(2)
        with c1:
            empresa_if = st.selectbox("Empresa Emitente", ["ETUS Digital LLC", "Evolution", "BRAZ", "BRIUS", "EMGC"])
            valor_if = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f", key="if_valor")
            num_nf = st.text_input("Número da NF", placeholder="00000", key="if_nf")
        with c2:
            mes_if = st.selectbox("Mês de Referência", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
            data_if = st.date_input("Data de Emissão", value=date.today(), key="if_data")
            status_if = st.selectbox("Status", ["Emitida", "Pendente", "Cancelada"])

        if st.button("+ Registrar Nota", type="primary"):
            if valor_if > 0:
                st.session_state.notas_ifood.append({
                    "empresa": empresa_if, "mes": mes_if, "valor": valor_if,
                    "data": data_if.isoformat(), "nf": num_nf, "status": status_if
                })
                st.success("✅ Nota registrada!")
                st.rerun()
            else:
                st.error("Preencha o valor da nota.")

    st.markdown("---")
    panel_header("Histórico de Notas iFood", "green")

    if notas:
        for n in notas:
            sc = {"Emitida": "green", "Pendente": "amber", "Cancelada": "red"}.get(n["status"], "gray")
            valor_fmt = f"R$ {n['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            st.markdown(f"""
            <div style="background:#fff;border:1px solid rgba(0,0,0,0.07);border-radius:8px;padding:10px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px">
                <div style="font-size:20px">🍔</div>
                <div style="flex:1">
                    <div style="font-weight:600;font-size:13px">{n['empresa']}</div>
                    <div style="font-size:10px;color:#6b7a9a">NF {n['nf']} · {n['mes']} · {n['data']}</div>
                </div>
                <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:14px">{valor_fmt}</div>
                <span class="badge badge-{sc}">{n['status']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;padding:40px;color:#6b7a9a">
            <div style="font-size:40px;margin-bottom:10px">💸</div>
            <div style="font-weight:600;margin-bottom:4px">Nenhuma nota registrada</div>
            <div style="font-size:12px">Registre notas fiscais iFood usando o formulário acima</div>
        </div>
        """, unsafe_allow_html=True)


def page_fin_outros():
    st.markdown("## 💸 Outros Pagamentos")

    pags = st.session_state.pagamentos
    total_pags = sum(p["valor"] for p in pags)

    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Pagamentos (Mês)", len(pags), "green", "↔", "nt")
    with c2: kpi_card("Total Pago", f"R${total_pags:,.0f}".replace(",", "."), "blue", "↔", "nt")
    with c3: kpi_card("Aguard. Comprovante", "0", "amber", "✓ ok", "ok")

    st.markdown("---")

    col_form, col_hist = st.columns(2)

    with col_form:
        panel_header("Lançar Novo Pagamento", "green")
        empresa_pg = st.selectbox("Empresa", ["Plusdin São Bernardo", "ETUS Digital LLC", "Evolution", "BRAZ", "BRIUS", "EMGC"], key="pg_emp")
        mes_pg = st.selectbox("Mês de Referência", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"], key="pg_mes")
        c1, c2 = st.columns(2)
        with c1:
            valor_pg = st.number_input("Valor (R$)", min_value=0.0, step=0.01, format="%.2f", key="pg_val")
            data_env = st.date_input("Data Envio", value=date.today(), key="pg_env")
        with c2:
            motivo_pg = st.text_input("Motivo", placeholder="Ex: Internet, Aluguel...", key="pg_mot")
            data_pg = st.date_input("Data Pagamento", value=date.today(), key="pg_dat")

        if st.button("Registrar Pagamento", type="primary", use_container_width=True):
            if valor_pg > 0 and motivo_pg:
                st.session_state.pagamentos.append({
                    "empresa": empresa_pg, "motivo": motivo_pg, "mes": mes_pg,
                    "valor": valor_pg, "data_envio": data_env.isoformat(),
                    "data_pagamento": data_pg.isoformat()
                })
                st.success("✅ Pagamento registrado!")
                st.rerun()
            else:
                st.error("Preencha valor e motivo.")

    with col_hist:
        panel_header("Histórico de Pagamentos", "blue")
        if pags:
            for p in pags:
                valor_fmt = f"R$ {p['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                st.markdown(f"""
                <div style="background:#f9fafb;border:1px solid rgba(0,0,0,0.07);border-radius:7px;padding:10px 14px;margin-bottom:7px">
                    <div style="display:flex;align-items:center;justify-content:space-between">
                        <div>
                            <div style="font-weight:600;font-size:12.5px">{p['empresa']}</div>
                            <div style="font-size:10px;color:#6b7a9a">{p['motivo']} · {p['mes']} · {p['data_pagamento']}</div>
                        </div>
                        <div style="text-align:right">
                            <div style="font-family:'Syne',sans-serif;font-weight:700;color:#0a7a3c;font-size:14px">{valor_fmt}</div>
                            <span class="badge badge-green">✓ Pago</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:30px;color:#6b7a9a">
                <div style="font-size:36px;margin-bottom:8px">💸</div>
                <div style="font-weight:600">Nenhum pagamento registrado</div>
            </div>
            """, unsafe_allow_html=True)


def page_fin_dashboard():
    st.markdown("## ◈ Dashboard Financeiro")

    notas = st.session_state.notas_ifood
    pags = st.session_state.pagamentos
    total_ifood = sum(n["valor"] for n in notas)
    total_outros = sum(p["valor"] for p in pags)
    total_colabs = len(st.session_state.estagiarios) + len(st.session_state.colaboradores)
    custo_por_colab = (total_ifood + total_outros) / total_colabs if total_colabs > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Receita iFood (Mês)", f"R${total_ifood:,.0f}".replace(",", "."), "green", "↔", "nt")
    with c2: kpi_card("Outros Pagamentos", f"R${total_outros:,.0f}".replace(",", "."), "blue", "↔", "nt")
    with c3: kpi_card("Custo/Colaborador", f"R${custo_por_colab:,.0f}".replace(",", "."), "amber", "↔", "nt")
    with c4: kpi_card("Notas Pendentes", sum(1 for n in notas if n["status"] == "Pendente"), "red", "✓ ok", "ok")

    if not notas and not pags:
        st.markdown('<div class="notif-info">ℹ️ Cadastre notas e pagamentos para visualizar os indicadores automaticamente.</div>', unsafe_allow_html=True)

    st.markdown("---")

    col_bar, col_dist = st.columns(2)

    with col_bar:
        panel_header("Receita vs Custos", "green")
        meses_labels = ["Out/25", "Nov/25", "Dez/25", "Jan/26", "Fev/26", "Mar/26"]
        receitas = [0, 0, 0, 0, 0, total_ifood]
        custos = [0, 0, 0, 0, 0, total_outros]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=meses_labels, y=receitas, name="Receita", marker_color="#0a7a3c",
            marker_line_width=0, text=[f"R${v:,.0f}" if v > 0 else "" for v in receitas], textposition="outside"))
        fig.add_trace(go.Bar(x=meses_labels, y=custos, name="Custos", marker_color="#c0392b",
            marker_line_width=0, text=[f"R${v:,.0f}" if v > 0 else "" for v in custos], textposition="outside"))
        fig.update_layout(**plotly_defaults(), height=250, showlegend=True, barmode="group",
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1, font=dict(size=10)),
            yaxis=dict(tickprefix="R$", gridcolor="rgba(0,0,0,0.04)"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_dist:
        panel_header("Distribuição de Custos", "blue")
        if total_ifood > 0 or total_outros > 0:
            labels = ["iFood", "Pagamentos"]
            vals = [total_ifood, total_outros]
            fig2 = go.Figure(go.Pie(
                labels=labels, values=vals, hole=0.68,
                marker=dict(colors=["rgba(10,122,60,0.7)", "rgba(26,86,219,0.7)"], line=dict(color="#fff", width=3)),
            ))
            fig2.update_layout(**plotly_defaults(), height=200)
            fig2.update_traces(textinfo="percent+label")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="text-align:center;padding:40px;color:#6b7a9a;font-size:12px">Sem dados · Cadastre notas e pagamentos</div>', unsafe_allow_html=True)


# ══════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════
mod = st.session_state.modulo
pg = st.session_state.pagina

router = {
    ("rh", "indicadores"): page_rh_indicadores,
    ("rh", "vagas"): page_rh_vagas,
    ("rh", "candidatos"): page_rh_candidatos,
    ("rh", "onboarding"): page_rh_onboarding,
    ("dp", "dashboard"): page_dp_dashboard,
    ("dp", "estagiarios"): page_dp_estagiarios,
    ("dp", "colaboradores"): page_dp_colaboradores,
    ("dp", "periodo"): page_dp_periodo,
    ("fin", "ifood"): page_fin_ifood,
    ("fin", "outros"): page_fin_outros,
    ("fin", "dashboard"): page_fin_dashboard,
}

page_fn = router.get((mod, pg))
if page_fn:
    page_fn()
else:
    st.warning("Página não encontrada.")
