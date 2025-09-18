import streamlit as st
import pandas as pd
import base64

# ---------- Helper Function ----------
def get_csv_download_button(df: pd.DataFrame, filename: str, button_text: str):
    """Generates a styled HTML button for downloading a CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"""
    <a href="data:file/csv;base64,{b64}" download="{filename}">
        <button style="
            background-color:#4CAF50;
            border:none;
            color:white;
            padding:10px 20px;
            text-align:center;
            text-decoration:none;
            display:inline-block;
            font-size:16px;
            margin:5px;
            border-radius:8px;
            cursor:pointer;">
            {button_text}
        </button>
    </a>
    """
    return href

# ---------- Page Config ----------
st.set_page_config(page_title="Retail Analyzer", layout="wide")

st.title("📊 Retail Sales Analyzer")
st.write("Upload your sales Excel file and get insights instantly.")

# ---------- File Upload ----------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        st.subheader("📄 Raw Data")
        st.dataframe(df, use_container_width=True)

        # ---------- Basic Stats ----------
        st.subheader("📈 Summary Statistics")
        st.write(df.describe())

        # ---------- Profit / Loss Analysis ----------
        if "Profit" in df.columns:
            profit_df = df[df["Profit"] > 0]
            loss_df = df[df["Profit"] < 0]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Profit Data")
                st.dataframe(profit_df)
                st.markdown(
                    get_csv_download_button(profit_df, "profit_data.csv", "📥 Download Profit Data"),
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown("### ❌ Loss Data")
                st.dataframe(loss_df)
                st.markdown(
                    get_csv_download_button(loss_df, "loss_data.csv", "📥 Download Loss Data"),
                    unsafe_allow_html=True
                )

        # ---------- Full Report Download ----------
        st.subheader("📥 Download Full Report")
        st.markdown(
            get_csv_download_button(df, "full_report.csv", "📥 Download Full Report"),
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
