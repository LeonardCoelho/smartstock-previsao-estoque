# 📦 SmartStock - Previsão Inteligente de Estoque

SmartStock é uma simulação de previsão de demanda de produtos usando **Machine Learning**, voltada para profissionais de logística e supply chain. O projeto gera alertas automáticos de estoque e dashboards interativos para auxiliar a tomada de decisão.

🔗 **[Acesse o App Online](https://smartstock-previsao-estoque-wjjphgcdqbwhk6h3vunddk.streamlit.app/)**

---

## 🎯 Objetivo

Aplicar ciência de dados na previsão de vendas dos próximos dias e comparar com o estoque atual para gerar alertas automáticos:

- ⚠️ **Estoque Baixo**
- 📦 **Estoque Encalhado**
- ✅ **OK**

---

## 🔍 Funcionalidades

- Geração automática de base fictícia de vendas (90 dias)
- Previsão de demanda para os próximos 15 dias usando **Regressão Linear**
- Média móvel de 7 dias para identificar tendência
- Alertas automáticos de estoque
- Exportação de resultados em Excel (`previsoes_alertas.xlsx`)
- Dashboard interativo com **Streamlit**

---

## 📂 Estrutura do Projeto

```text
📂 smartstock-previsao-estoque
  ┣ 📂 data                 # Base de vendas fictícia
  ┣ 📂 output               # Resultados e gráficos gerados
  ┣ 📂 src                  # Scripts e app Streamlit
  ┣ ├─ app.py               # Dashboard interativo
  ┣ └─ previsao_completa.py # Script de geração de previsões + alertas
  ┣ 📜 requirements.txt     # Dependências do projeto
  ┗ 📜 README.md            # Documentação
```

---

## 🧠 Como o modelo funciona

1. Para cada produto, calcula-se a **média móvel de 7 dias** para identificar tendências.
2. Treina um **modelo de regressão linear** com os últimos 90 dias de vendas.
3. Gera previsões para os próximos 15 dias.
4. Compara a média das previsões com o estoque atual e define o **status do produto**.

---

## 📸 Demonstração

![App Preview](imagem%20app%201.png)

---

## 🧪 Como rodar localmente

```bash
# 1. Clonar repositório
git clone https://github.com/LeonardCoelho/smartstock-previsao-estoque.git
cd smartstock-previsao-estoque

# 2. (Opcional) Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Gerar previsão via script
python src/previsao_completa.py

# 5. Rodar dashboard interativo
streamlit run src/app.py
```

---

## ☁️ Rodar na nuvem (Streamlit Cloud)

1. Suba o repositório no GitHub
2. Vá para: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em **New App** e selecione seu repositório
4. No campo `Main file path`, coloque: `src/app.py`
5. Clique em **Deploy** 🚀

A aplicação estará online para visualização e download dos resultados.

---

## 👨‍💻 Autor

**Leonardo Coelho**\
🚛 Analista de Transportes | 📊 Pós em Data Science & Machine Learning\
📍 Campinas - SP\
🔗 [GitHub](https://github.com/LeonardCoelho) | [LinkedIn](https://linkedin.com/in/leonardcoelho)

