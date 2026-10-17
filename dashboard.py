
import streamlit as st
import plotly.express as px

from db_connection import get_monthly_summary
from rag_chat import financial_chain


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="SQL + RAG Financial Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 SQL + RAG Financial Dashboard")
st.caption("Financial analytics and AI-powered document search")


# --------------------------------------------------
# Load SQL Data
# --------------------------------------------------
try:
    df = get_monthly_summary()

    if df.empty:
        st.warning("No financial data found in MySQL.")
        st.stop()

    # Ensure financial columns are numeric
    financial_columns = [
        "total_revenue",
        "total_expenses",
        "net_profit",
    ]

    for column in financial_columns:
        df[column] = df[column].astype(float)

    # --------------------------------------------------
    # Financial KPIs
    # --------------------------------------------------
    total_revenue = df["total_revenue"].sum()
    total_expenses = df["total_expenses"].sum()
    total_profit = df["net_profit"].sum()

    st.subheader("Overall Financial Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}",
    )

    col2.metric(
        "Total Expenses",
        f"₹{total_expenses:,.2f}",
    )

    col3.metric(
        "Net Profit",
        f"₹{total_profit:,.2f}",
    )

    # --------------------------------------------------
    # Monthly Financial Chart
    # --------------------------------------------------
    st.divider()
    st.subheader("Monthly Financial Performance")

    chart_df = df.melt(
        id_vars=["month"],
        value_vars=["total_revenue", "total_expenses"],
        var_name="Type",
        value_name="Amount",
    )

    chart_df["Type"] = chart_df["Type"].map({
        "total_revenue": "Revenue",
        "total_expenses": "Expenses",
    })

    fig = px.bar(
        chart_df,
        x="month",
        y="Amount",
        color="Type",
        barmode="group",
        title="Monthly Revenue vs Expenses",
        labels={
            "month": "Month",
            "Amount": "Amount (₹)",
            "Type": "Financial Category",
        },
        text_auto=".2s",
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount (₹)",
        legend_title="Category",
        hovermode="x unified",
    )

    st.plotly_chart(fig, width="stretch")

    # --------------------------------------------------
    # Monthly Financial Summary
    # --------------------------------------------------
    st.divider()
    st.subheader("Monthly Financial Summary")

    display_df = df.copy()

    for column in financial_columns:
        display_df[column] = display_df[column].map(
            lambda value: f"₹{value:,.2f}"
        )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )

except Exception as e:
    st.error(f"Could not load SQL data: {e}")
    st.stop()


# --------------------------------------------------
# RAG Chatbot
# --------------------------------------------------
st.divider()
st.header("💬 Ask Your Financial Assistant")

st.write(
    "Ask questions about revenue, expenses, profit, "
    "or explanations documented in your financial notes."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Example: Why did salary expenses increase in September?"
)

if question:
    st.session_state.chat_history.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing SQL data and financial notes..."):
            try:
                answer = financial_chain.invoke(question)
                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception as e:
                st.error(f"Could not generate an answer: {e}")