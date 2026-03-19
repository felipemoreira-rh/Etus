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


## Tecnologias usadas

- **Python 3.9+**
- **Streamlit** — interface e hospedagem
- **Plotly** — gráficos interativos (funil, donut, barras, linha)
- **Pandas** — manipulação de dados
