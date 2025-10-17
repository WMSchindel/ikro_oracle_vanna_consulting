import streamlit as st
from app_backend import run_query_from_question

# ======================================================
# Configuração da Página
# ======================================================
st.set_page_config(page_title="Consulta Oracle com IA", layout="wide")
st.title("🔍 Consulta Inteligente ao Banco Oracle (Vanna + GPT-4o)")

st.markdown("""
Esta aplicação permite digitar perguntas em **linguagem natural** (português ou inglês),
e o sistema gera automaticamente a query **SQL Oracle** correspondente,
executando-a no seu banco local.
""")

# ======================================================
# Interface de Entrada
# ======================================================
pergunta = st.text_area("Digite sua pergunta:", placeholder="Ex: Liste o faturamento total por UF em 2024", height=100)

if st.button("Gerar e Executar SQL"):
    if not pergunta.strip():
        st.warning("⚠️ Por favor, digite uma pergunta antes de continuar.")
    else:
        with st.spinner("Gerando e executando consulta..."):
            result = run_query_from_question(pergunta)

        if result["error"]:
            st.error(f"❌ Ocorreu um erro: {result['error']}")
        else:
            st.subheader("🧠 SQL Gerado")
            st.code(result["sql"], language="sql")

            if result["data"] is not None and not result["data"].empty:
                st.subheader("📊 Resultado da Consulta")
                st.dataframe(result["data"], use_container_width=True)
                csv = result["data"].to_csv(index=False).encode("utf-8")
                st.download_button("📥 Baixar CSV", csv, "resultado.csv", "text/csv")
            else:
                st.info("ℹ️ Nenhum dado retornado pela consulta.")


