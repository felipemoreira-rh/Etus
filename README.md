# ETUS · Sistema RH — Streamlit

Sistema completo de gestão de RH, Departamento Pessoal e Financeiro, 
recriado em Python/Streamlit a partir do protótipo HTML original.

## Módulos

### 👥 RH — Recrutamento
- **Indicadores**: KPIs, funil de recrutamento, tempo de contratação, fontes
- **Vagas**: Cadastro e gestão de vagas abertas
- **Candidatos**: Listagem, filtros por fase/origem, score
- **Onboarding**: Acompanhamento de processos de admissão

### 📋 DP — Departamento Pessoal
- **Dashboard DP**: Headcount, distribuição por vínculo, evolução contratos
- **Estagiários**: Cadastro completo com progresso de contrato
- **Colaboradores**: Gestão de PJ/CLT
- **Período de Experiência**: Controle de 90 dias com alertas

### 💰 Financeiro
- **iFood**: Notas fiscais, status de emissão
- **Outros Pagamentos**: Lançamentos avulsos
- **Dashboard Financeiro**: Receita vs custos, distribuição

---

## Instalação e execução local

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar o app
streamlit run app.py
```

O sistema abrirá automaticamente em `http://localhost:8501`

---

## Deploy no Streamlit Community Cloud (gratuito)

### Passo a passo:

1. **Crie uma conta** em [share.streamlit.io](https://share.streamlit.io)

2. **Suba o projeto para o GitHub:**
   ```bash
   git init
   git add .
   git commit -m "ETUS Sistema RH - v1"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/etus-sistema.git
   git push -u origin main
   ```

3. **No Streamlit Cloud:**
   - Clique em "New app"
   - Selecione o repositório GitHub
   - Defina `app.py` como arquivo principal
   - Clique em "Deploy!"

4. **URL gerada:** `https://seu-usuario-etus-sistema-app-xxxxx.streamlit.app`

---

## Estrutura de arquivos

```
etus_sistema/
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências Python
└── README.md         # Este arquivo
```

---

## Tecnologias usadas

- **Python 3.9+**
- **Streamlit** — interface e hospedagem
- **Plotly** — gráficos interativos (funil, donut, barras, linha)
- **Pandas** — manipulação de dados

---

## Notas

- Os dados são mantidos em `st.session_state` (memória da sessão)
- Para persistência entre sessões, integre com banco de dados (SQLite, Supabase, etc.)
- Fontes Google (Syne, DM Sans) carregadas via CSS customizado
