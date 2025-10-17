import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat
from openai import OpenAI
import re

# ======================================================
# 1️⃣ Carrega variáveis de ambiente (.env)
# ======================================================
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
username = os.getenv("ORACLE_USER", "IKVANNA")
password = os.getenv("ORACLE_PASS", "M1th0s")
dsn = os.getenv("ORACLE_DSN", "localhost:1521/?service_name=XEPDB1")

# ======================================================
# 2️⃣ Conexão Oracle via SQLAlchemy
# ======================================================
engine = create_engine(f"oracle+oracledb://{username}:{password}@{dsn}")

# ======================================================
# 3️⃣ Inicialização do modelo Vanna
# ======================================================
class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config):
        ChromaDB_VectorStore.__init__(self, config)
        client = OpenAI(api_key=config["openai"]["api_key"])
        OpenAI_Chat.__init__(self, client=client, config={"model": config["openai"]["model"]})
        self.allow_llm_to_see_data = True

vn = MyVanna(
    config={
        "openai": {"api_key": api_key, "model": "gpt-4o"},
        "chroma": {"persist_directory": "chroma_db"},
        "allow_llm_to_see_data": True,
    }
)

# ======================================================
# 4️⃣ Sanitização do SQL (garante compatibilidade Oracle)
# ======================================================
def sanitize_sql_for_oracle(sql: str) -> str:
    if not sql:
        return ""
    fixed = sql.strip()
    fixed = re.sub(r"\bLIMIT\s+(\d+)\b", r"FETCH FIRST \1 ROWS ONLY", fixed, flags=re.I)
    fixed = re.sub(r"(?<!DATE\s)'(\d{4})-(\d{2})-(\d{2})'", r"DATE '\1-\2-\3'", fixed)
    fixed = fixed.replace('"', "")
    fixed = re.sub(r";\s*$", "", fixed)
    return fixed.strip()

# ======================================================
# 5️⃣ Execução Segura da Pergunta
# ======================================================
def run_query_from_question(question: str):
    try:
        sql_raw = vn.generate_sql(question=question)
        sql_fixed = sanitize_sql_for_oracle(sql_raw)
        df = pd.read_sql(sql_fixed, engine)
        df.index = df.index + 1
        df.index.name = "Nº"
        return {"sql": sql_fixed, "data": df, "error": None}
    except Exception as e:
        return {"sql": None, "data": None, "error": str(e)}