import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="AI Risk Manager", layout="wide")

@st.cache_resource
def get_connection():
    return psycopg2.connect(st.secrets["DB_CONNECTION_STRING"])

@st.cache_data(ttl=60)
def load_audit_trail():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM audit_trail ORDER BY created_at DESC", conn)

st.title("🛡️ AI Risk Manager — Revenue Leakage Radar")
st.caption("Defense-only detection and response for fraud, returns, chargebacks, and abuse rings")

df = load_audit_trail()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Unified Risk Feed", "🔴 Fraud Spike", "📦 Return Risk", "💳 Chargebacks", "🕸️ Abuse Rings"
])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Decisions Logged", len(df))
    col2.metric("Modules Active", df['module'].nunique())
    col3.metric("Flagged/Hold Actions", (df['decision'].isin(['hold','flag_for_review','flag_ring'])).sum())
    col4.metric("Latest Activity", df['created_at'].max().strftime('%Y-%m-%d %H:%M') if len(df) else "—")

    fig = px.histogram(df, x='module', color='decision', title='Decisions by Module')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Decisions (all modules)")
    st.dataframe(df.head(50), use_container_width=True)

for tab, module_name in zip([tab2, tab3, tab4, tab5], ['fraud_spike','return_risk','chargeback','abuse_ring']):
    with tab:
        sub = df[df['module'] == module_name]
        if len(sub) == 0:
            st.info(f"No logged decisions yet for {module_name}")
        else:
            c1, c2 = st.columns(2)
            c1.metric("Total scored", len(sub))
            c2.metric("Avg score", round(sub['score'].mean(), 3))
            fig = px.histogram(sub, x='score', color='decision', title=f'{module_name} score distribution')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(sub, use_container_width=True)