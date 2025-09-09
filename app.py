import pandas as pd
import streamlit as st

# Title
st.title("🛒 Retail Sales Analyzer")

# Upload Excel File
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel
    df = pd.read_excel(uploaded_file)

    # Make sure columns exist
    if all(col in df.columns for col in ["ProductID", "Category", "CostPrice", "SellingPrice"]):
        
        # Calculate Profit
        df["Profit"] = df["SellingPrice"] - df["CostPrice"]
        
        # Totals
        total_sales = df["SellingPrice"].sum()
        total_cost = df["CostPrice"].sum()
        total_profit = df["Profit"].sum()
        
        # Show Summary
        st.subheader("📊 Overall Summary")
        st.write(f"**Total Sales:** {total_sales}")
        st.write(f"**Total Cost:** {total_cost}")
        st.write(f"**Total Profit/Loss:** {total_profit}")
        
        # Category Breakdown
        st.subheader("📂 Category-wise Summary")
        category_summary = df.groupby("Category").agg({
            "SellingPrice": "sum",
            "CostPrice": "sum",
            "Profit": "sum"
        })
        st.dataframe(category_summary)
        
        # Download Option
        st.download_button(
            "⬇️ Download Category Report",
            category_summary.to_csv().encode("utf-8"),
            "report_summary.csv",
            "text/csv"
        )
    else:
        st.error("❌ Your Excel must have these columns: ProductID, Category, CostPrice, SellingPrice")
