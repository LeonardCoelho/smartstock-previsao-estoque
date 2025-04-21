import streamlit as st
import io
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

# Gera o arquivo Excel combinando os dados
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    previsoes.to_excel(writer, sheet_name="Previsoes", index=False)
    alertas.to_excel(writer, sheet_name="Alertas", index=False)

excel_buffer.seek(0)  # Volta o ponteiro para o início do arquivo

produto_sel = st.sidebar.selectbox("🔍 Selecione o Produto", sorted(previsoes['Produto'].unique()))

st.sidebar.markdown("📥 Baixe os resultados:")
st.sidebar.download_button(
    label="📊 Baixar Excel",
    data=excel_buffer,
    file_name="previsoes_alertas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Mostra os alertas filtrados pelo produto
alerta_produto = alertas[alertas['Produto'] == produto_sel]
st.markdown(f"### 🔔 Status do Produto: **{produto_sel}**")
st.dataframe(alerta_produto, use_container_width=True)

# Gráfico geral no app com seaborn e matplotlib
st.markdown("### 📈 Vendas e Tendência dos Produtos (últimos 90 dias)")

import seaborn as sns

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(14, 6))

produtos = previsoes['Produto'].unique()

for produto in produtos:
    dados_produto = previsoes[previsoes['Produto'] == produto]
    dados_produto = dados_produto.sort_values('Data')  # só pra garantir a ordem no gráfico
    dados_produto['Media_Movel_7'] = dados_produto['Previsao_Venda'].rolling(window=7).mean()

    ax.plot(dados_produto['Data'], dados_produto['Previsao_Venda'], label=f'{produto} - Previsões')
    ax.plot(dados_produto['Data'], dados_produto['Media_Movel_7'], linestyle='--', label=f'{produto} - Média Móvel')

ax.set_title('Vendas e Tendência dos Produtos (últimos 90 dias)')
ax.set_xlabel('Data')
ax.set_ylabel('Unidades Previstas')
ax.legend()
ax.grid(True)
plt.tight_layout()

st.pyplot(fig)

# Previsões detalhadas
st.markdown("### 📅 Previsões para os próximos 15 dias")
df_sel = previsoes[previsoes['Produto'] == produto_sel]
st.dataframe(df_sel[['Data', 'Previsao_Venda', 'Estoque_Atual', 'Status']], use_container_width=True)
