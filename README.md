# 🔍 Oracle Vanna Streamlit

Aplicação Streamlit integrada com **Oracle Database**, **Vanna + ChromaDB** e **GPT-4o**, que permite realizar consultas SQL automáticas a partir de perguntas em **linguagem natural** (português ou inglês).

---

## 🚀 Funcionalidades
✅ Conversão automática de perguntas em SQL Oracle puro  
✅ Execução direta no banco Oracle via SQLAlchemy  
✅ Interface intuitiva com Streamlit  
✅ Download de resultados em CSV  
✅ Tratamento de erros sem travar o app  
✅ Pronto para deploy no **Streamlit Cloud**

oracle_vanna_streamlit/
├── streamlit_app.py ← Frontend Streamlit (UI)
├── app_backend.py ← Backend com Oracle + Vanna + GPT-4o
├── requirements.txt ← Dependências Python
├── .env.example ← Modelo de variáveis de ambiente
└── chroma_db/ ← Persistência vetorial (criada em runtime

## ⚙️ 1️⃣ Configuração do Ambiente Local

### 🔧 Pré-requisitos
- Python 3.9+  
- Oracle Database XE (ou superior) em execução local  
- Variável `OPENAI_API_KEY` válida  
- Rede local ou VPN que permita acesso ao Oracle

### 📦 Instalação
1. Clone o repositório ou extraia o arquivo `.zip`:
   ```bash
   unzip oracle_vanna_streamlit.zip
   cd oracle_vanna_streamlit
Crie um ambiente virtual (opcional, mas recomendado):

bash
Copiar código
python -m venv .venv
source .venv/bin/activate    # (Linux/Mac)
.venv\Scripts\activate       # (Windows)
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt