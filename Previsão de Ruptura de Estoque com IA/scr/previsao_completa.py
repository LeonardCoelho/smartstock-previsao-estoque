import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os

# Preparar pastas
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

# 1. Gerar base fictícia
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
df.to_csv('data/vendas_ficticias.csv', index=False)

# 2. Processamento
df['Data'] = pd.to_datetime(df['Data'])
df = df.sort_values(by=['Produto', 'Data'])
df['Media_Movel_7'] = df.groupby('Produto')['Venda'].transform(lambda x: x.rolling(7, min_periods=1).mean())

# 3. Visualização
sns.set(style="whitegrid")
plt.figure(figsize=(14, 6))

for produto in produtos:
    dados_produto = df[df['Produto'] == produto]
    plt.plot(dados_produto['Data'], dados_produto['Venda'], label=f'{produto} - Vendas')
    plt.plot(dados_produto['Data'], dados_produto['Media_Movel_7'], linestyle='--', label=f'{produto} - Média Móvel')

plt.title('Vendas e Tendência dos Produtos (últimos 90 dias)')
plt.xlabel('Data')
plt.ylabel('Quantidade Vendida')
plt.legend()
plt.tight_layout()
plt.savefig("output/grafico_vendas.png")
plt.close()

# 4. Previsão e Alertas
previsoes = []
alertas = []

# Estoques aleatórios entre 30 e 100 unidades
estoque_atual = {
    produto: np.random.randint(30, 101) for produto in produtos
}

for produto in produtos:
    dados_p = df[df['Produto'] == produto].copy()
    dados_p['Dias'] = (dados_p['Data'] - dados_p['Data'].min()).dt.days

    X = dados_p[['Dias']]
    y = dados_p['Venda']

    modelo = LinearRegression()
    modelo.fit(X, y)

    # AJUSTE: dias_futuros como DataFrame com coluna 'Dias'
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

resultado = pd.concat(previsoes)
df_alertas = pd.DataFrame(alertas)

with pd.ExcelWriter("output/previsoes_alertas.xlsx") as writer:
    resultado.to_excel(writer, sheet_name="Previsoes", index=False)
    df_alertas.to_excel(writer, sheet_name="Alertas_Resumo", index=False)

print("\n✅ Previsão concluída!")
print("🔍 Resultados em: output/previsoes_alertas.xlsx + output/grafico_vendas.png\n")
print(df_alertas.to_string(index=False))