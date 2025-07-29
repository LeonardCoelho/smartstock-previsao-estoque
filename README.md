# 📦 SmartStock - Previsão de Estoque com IA

**SmartStock** é uma simulação inteligente de previsão de vendas e análise de estoque, voltada para profissionais de logística e supply chain. Ele utiliza Machine Learning para prever a demanda futura com base em séries temporais, sinalizando se o estoque está OK, encalhado ou baixo.

---

## 🎯 Objetivo

Aplicar ciência de dados na previsão de vendas dos próximos dias, comparando com o estoque atual para gerar **alertas automáticos** que auxiliem a tomada de decisão logística.

---

## 🔍 Funcionalidades

- ✅ Geração automática de base fictícia de vendas (90 dias)
- 📈 Previsão de demanda para os próximos 15 dias
- 📉 Média móvel para tendência
- 🚨 Alertas de estoque:  
  - `⚠️ Estoque Baixo`  
  - `📦 Encalhado`  
  - `✅ OK`
- 🧾 Exportação em Excel com abas de previsão e resumo de alertas
- 🖥️ Dashboard interativo com Streamlit

---

## 🧠 Tecnologias usadas

- **Python**
- **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**
- **Scikit-learn** (regressão linear)
- **Streamlit** (para dashboard interativo)

---

## 📂 Estrutura do Projeto

```bash
smartstock-previsao-estoque/
├── src/
│   ├── app.py                # Interface com Streamlit
│   └── previsao_completa.py # Script principal de previsão
├── data/                     # Dados gerados
├── output/                   # Resultados: gráfico + Excel
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

---

## 🚀 Como rodar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/LeonardCoelho/smartstock-previsao-estoque.git
cd smartstock-previsao-estoque
```

### 2. (Opcional) Criar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Gerar previsão via script

```bash
python src/previsao_completa.py
```

> Resultado salvo em `output/previsoes_alertas.xlsx` e `output/grafico_vendas.png`.

### 5. Rodar o dashboard interativo

```bash
streamlit run src/app.py
```

---

## ☁️ Como rodar na nuvem (Streamlit Cloud)

1. Suba seu repositório para o GitHub
2. Vá em: https://streamlit.io/cloud
3. Clique em "New App"
4. Selecione seu repositório
5. No campo **"Main file path"**, coloque:

```
src/app.py
```

6. Clique em "Deploy" e pronto 🚀

---

## 🧪 Exemplo de Saída

- 📅 Previsões diárias para cada produto
- 📊 Gráfico com vendas reais + média móvel
- 🚨 Alertas indicando risco de ruptura ou excesso
- 📥 Download do Excel com os resultados

---

## 💡 Ideias de melhoria

- Subir dados reais via CSV
- Incluir novos modelos (ARIMA, Prophet, etc.)
- Calcular custo de ruptura ou excesso
- Criar histórico de execução
- Deploy com Docker, Streamlit Cloud ou HuggingFace Spaces

---

## 👨‍💻 Autor

**Leonardo Coelho**  
🚛 Analista de Transportes | 📊 Pós em Data Science & Machine Learning  
📍 Campinas - SP | [linkedin.com/in/leonardcoelho](https://www.linkedin.com/in/leonardcoelho)

---
