import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from io import BytesIO

st.set_page_config(page_title="SmartStock - Previsão de Demanda", layout="wide")
st.title("📦 SmartStock - Previsão Inteligente de Estoque")
st.markdown("Simulação de previsão de demanda usando IA + alertas automáticos para logística.")

# 1. Gerar dados fictícios
@st.cache_data
def gerar_dados():
    np.random.seed(int(pd.Timestamp.now().timestamp()))
    dias = pd.date_range(start='2024-01-01', periods=90, freq='D')
    produtos = ['Produto A', 'Produto B', 'Produto C']
    dados = []

    for produto in produtos:
        vendas = np.random.poisson(lam=50 + 10 * produtos.index(produto), size=90)
        for i in range(90):
            dados.append({
                'Data': dias[i],
                'Produto': produto,
                'Venda': vendas[i]
            })

    df = pd.DataFrame(dados)
    return df

df = gerar_dados()

# 2. Processamento
df['Data'] = pd.to_datetime(df['Data'])
df = df.sort_values(by=['Produto', 'Data'])
df['Media_Movel_7'] = df.groupby('Produto')['Venda'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# 3. Previsões e Alertas
previsoes = []
alertas = []

estoque_atual = {produto: np.random.randint(30, 101) for produto in df['Produto'].unique()}

for produto in df['Produto'].unique():
    dados_p = df[df['Produto'] == produto].copy()
    dados_p['Dias'] = (dados_p['Data'] - dados_p['Data'].min()).dt.days

    X = dados_p[['Dias']]
    y = dados_p['Venda']

    modelo = LinearRegression()
    modelo.fit(X, y)

    dias_futuros = pd.DataFrame(
        range(dados_p['Dias'].max() + 1, dados_p['Dias'].max() + 16),
        columns=['Dias']
    )

    previsao = modelo.predict(dias_futuros)
    datas_futuras = pd.date_range(start=df['Data'].max() + pd.Timedelta(days=1), periods=15)

    previsao_df = pd.DataFrame({
        'Data': datas_futuras,
        'Produto': produto,
        'Previsao_Venda': previsao
    })

    media_prevista = previsao_df['Previsao_Venda'].mean()
    estoque = estoque_atual[produto]

    if media_prevista > estoque:
        status = '⚠️ ESTOQUE BAIXO'
    elif media_prevista < estoque * 0.4:
        status = '📦 ESTOQUE ENCALHADO'
    else:
        status = '✅ OK'

    previsao_df['Estoque_Atual'] = estoque
    previsao_df['Status'] = status

    previsoes.append(previsao_df)
    alertas.append({
        'Produto': produto,
        'Estoque_Atual': estoque,
        'Media_Prevista': round(media_prevista, 2),
        'Status': status
    })

df_previsoes = pd.concat(previsoes)
df_alertas = pd.DataFrame(alertas)

# 4. Sidebar
produto_sel = st.sidebar.selectbox("🔍 Selecione o Produto", sorted(df_previsoes['Produto'].unique()))

# Exportar Excel direto
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    df_previsoes.to_excel(writer, sheet_name="Previsoes", index=False)
    df_alertas.to_excel(writer, sheet_name="Alertas", index=False)

excel_buffer.seek(0)
st.sidebar.markdown("📥 Baixe os resultados:")
st.sidebar.download_button(
    label="📊 Baixar Excel",
    data=excel_buffer,
    file_name="previsoes_alertas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# 5. Alertas
st.markdown(f"### 🔔 Status do Produto: **{produto_sel}**")
st.dataframe(df_alertas[df_alertas['Produto'] == produto_sel], use_container_width=True)

# 6. Gráfico
st.markdown("### 📈 Vendas e Tendência dos Produtos (últimos 90 dias)")

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(14, 6))

for produto in df['Produto'].unique():
    dados_produto = df[df['Produto'] == produto]
    ax.plot(dados_produto['Data'], dados_produto['Venda'], label=f'{produto} - Vendas')
    ax.plot(dados_produto['Data'], dados_produto['Media_Movel_7'], linestyle='--', label=f'{produto} - Média Móvel')

ax.set_title('Vendas e Tendência dos Produtos (últimos 90 dias)')
ax.set_xlabel('Data')
ax.set_ylabel('Quantidade Vendida')
ax.legend()
ax.grid(True)
plt.tight_layout()

st.pyplot(fig)

# 7. Previsões Detalhadas
st.markdown("### 📅 Previsões para os próximos 15 dias")
df_sel = df_previsoes[df_previsoes['Produto'] == produto_sel]
st.dataframe(df_sel[['Data', 'Previsao_Venda', 'Estoque_Atual', 'Status']], use_container_width=True)
