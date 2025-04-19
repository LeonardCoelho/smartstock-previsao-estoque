# 📦 SmartStock - Previsão de Estoque com IA

**SmartStock** é um projeto de previsão de vendas com inteligência artificial voltado para logística.  
Utiliza dados fictícios gerados dinamicamente para simular cenários reais de estoque e demanda, ajudando na tomada de decisão com alertas automáticos.

## 🎯 Objetivo

Aplicar ciência de dados e machine learning para prever vendas dos próximos dias e cruzar com o estoque atual, gerando insights como:

- Previsões de demanda para 15 dias
- Classificação de estoque (baixo, ideal, encalhado)
- Visualização de tendências por média móvel
- Gráfico histórico + dashboard interativo com Streamlit

## 🔍 Funcionalidades

- Geração automática de base fictícia de vendas (90 dias)
- Simulação de estoque aleatório a cada execução
- Previsões por regressão linear
- Alerta visual do status do estoque
- Exportação dos dados em Excel
- Interface com Streamlit

## 🧠 Tecnologias usadas

- Python
- Pandas, NumPy, Matplotlib, Seaborn
- Scikit-learn (regressão)
- Streamlit (dashboard interativo)

## 🏁 Como executar localmente

```bash
# Clonar o projeto
git clone https://github.com/seu-usuario/smartstock.git
cd smartstock

# Instalar dependências
pip install -r requirements.txt

# Gerar nova simulação
python src/previsao_completa.py

# Rodar o app
streamlit run app.py