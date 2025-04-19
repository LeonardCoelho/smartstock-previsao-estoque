import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="SmartStock - Previsão de Demanda", layout="wide")

st.title("📦 SmartStock - Previsão Inteligente de Estoque")
st.markdown("Simulação de previsão de demanda usando IA + alertas automáticos para logística.")

@st.cache_data
def carregar_dados():
    # Lê as previsões
    previsoes = pd.read_csv("output/previsoes.csv", sep=";", encoding="utf-8")

    # Lê os alertas
    alertas = pd.read_csv("output/alertas.csv", sep=";", encoding="utf-8")

    # Ajustes no formato das colunas em previsões
    previsoes["Previsao_Venda"] = previsoes["Previsao_Venda"].astype(str).str.replace(",", ".").astype(float)
    previsoes["Data"] = pd.to_datetime(previsoes["Data"], dayfirst=True)

    # Ajusta a média prevista dos alertas
    alertas["Media_Prevista"] = alertas["Media_Prevista"].astype(str).str.replace(",", ".").astype(float)

    return previsoes, alertas

previsoes, alertas = carregar_dados()

produto_sel = st.sidebar.selectbox("🔍 Selecione o Produto", sorted(previsoes['Produto'].unique()))

st.sidebar.markdown("📥 Baixe os resultados:")
with open("output/previsoes_alertas.xlsx", "rb") as file:
    st.sidebar.download_button(
        label="📊 Baixar Excel",
        data=file,
        file_name="previsoes_alertas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Mostra os alertas filtrados pelo produto
alerta_produto = alertas[alertas['Produto'] == produto_sel]
st.markdown(f"### 🔔 Status do Produto: **{produto_sel}**")
st.dataframe(alerta_produto, use_container_width=True)

# Gráfico
st.markdown("### 📈 Gráfico de Tendência das Vendas")
imagem = Image.open("output/grafico_vendas.png")
st.image(imagem, caption="Evolução de vendas e média móvel")

# Previsões detalhadas
st.markdown("### 📅 Previsões para os próximos 15 dias")
df_sel = previsoes[previsoes['Produto'] == produto_sel]
st.dataframe(df_sel[['Data', 'Previsao_Venda', 'Estoque_Atual', 'Status']], use_container_width=True)
