import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

st.set_page_config(page_title="SmartStock - Previsão de Demanda", layout="wide")

st.title("📦 SmartStock - Previsão Inteligente de Estoque")
st.markdown("Simulação de previsão de demanda usando IA + alertas automáticos para logística.")

@st.cache_data
def carregar_dados():
    previsoes = pd.read_csv("output/previsoes.csv", sep=";", encoding="utf-8")
    alertas = pd.read_csv("output/alertas.csv", sep=";", encoding="utf-8")

    previsoes["Previsao_Venda"] = previsoes["Previsao_Venda"].astype(str).str.replace(",", ".").astype(float)
    previsoes["Data"] = pd.to_datetime(previsoes["Data"], dayfirst=True)

    alertas["Previsao_Venda"] = alertas["Previsao_Venda"].astype(str).str.replace(",", ".").astype(float)
    alertas["Data"] = pd.to_datetime(alertas["Data"], dayfirst=True)

    return previsoes, alertas

previsoes, alertas = carregar_dados()

produto_sel = st.sidebar.selectbox("🔍 Selecione o Produto", sorted(previsoes['Produto'].unique()))

# 🔽 Download do Excel, se existir
excel_path = "output/previsoes_alertas.xlsx"
if os.path.exists(excel_path):
    st.sidebar.markdown("📥 Baixe os resultados:")
    with open(excel_path, "rb") as file:
        st.sidebar.download_button(
            label="📊 Baixar Excel",
            data=file,
            file_name="previsoes_alertas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.sidebar.warning("⚠️ Arquivo Excel não encontrado.")

# 🔔 Tabela de alertas
alerta_produto = alertas[alertas['Produto'] == produto_sel]
st.markdown(f"### 🔔 Status do Produto: **{produto_sel}**")
st.dataframe(alerta_produto, use_container_width=True)

# 📈 Gráfico de vendas
grafico_path = "output/grafico_vendas.png"
if os.path.exists(grafico_path):
    st.markdown("### 📈 Gráfico de Tendência das Vendas")
    imagem = Image.open(grafico_path)
    st.image(imagem, caption="Evolução de vendas e média móvel")
else:
    st.warning("⚠️ Gráfico não encontrado.")

# 📅 Tabela de previsões
st.markdown("### 📅 Previsões para os próximos 15 dias")
df_sel = previsoes[previsoes['Produto'] == produto_sel]
st.dataframe(df_sel[['Data', 'Previsao_Venda', 'Estoque_Atual', 'Status']], use_container_width=True)
