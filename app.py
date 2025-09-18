import pandas as pd
import streamlit as st

st.set_page_config(page_title="Retail Sales Analyzer", page_icon="🛒", layout="wide")

st.title("🛒 Retail Sales Analyzer")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # ✅ Force pandas to use openpyxl engine
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # Expected columns in your sheet
    required_cols = [
        "Barcode", "Sale Date & Time", "Category", "Subcategory",
        "Product Name", "Cost Price(Rs.)", "Selling Price(Rs.)",
        "Units Sold", "Total Sale(Rs.)"
    ]

    if all(col in df.columns for col in required_cols):

        # ✅ Recalculate Total Sale
        df["Total Sale(Rs.)"] = df["Selling Price(Rs.)"] * df["Units Sold"]

        # ✅ Add Profit/Loss column
        df["Profit/Loss"] = (df["Selling Price(Rs.)"] - df["Cost Price(Rs.)"]) * df["Units Sold"]

        # ================= OVERALL SUMMARY =================
        total_units = df["Units Sold"].sum()
        total_sales = df["Total Sale(Rs.)"].sum()
        total_profit = df[df["Profit/Loss"] > 0]["Profit/Loss"].sum()
        total_loss = df[df["Profit/Loss"] < 0]["Profit/Loss"].sum()

        st.subheader("📊 Overall Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Units Sold", f"{total_units:,}")
        col2.metric("Total Sales", f"₹{total_sales:,.2f}")
        col3.metric("Total Profit", f"₹{total_profit:,.2f}")
        col4.metric("Total Loss", f"₹{total_loss:,.2f}")

        # ================= CATEGORY SUMMARY =================
        st.subheader("📂 Category-wise Summary")
        category_summary = df.groupby("Category").agg({
            "Units Sold": "sum",
            "Total Sale(Rs.)": "sum",
            "Profit/Loss": "sum"
        }).sort_values("Total Sale(Rs.)", ascending=False)

        st.dataframe(category_summary, use_container_width=True)
        st.bar_chart(category_summary["Total Sale(Rs.)"], use_container_width=True)

        # ================= PRODUCT SUMMARY =================
        st.subheader("🛍️ Product-wise Summary")
        product_summary = df.groupby("Product Name").agg({
            "Units Sold": "sum",
            "Total Sale(Rs.)": "sum",
            "Profit/Loss": "sum"
        }).sort_values("Total Sale(Rs.)", ascending=False)

        st.dataframe(product_summary, use_container_width=True)

        # ================= DOWNLOAD OPTIONS =================
        st.download_button(
            label="⬇️ Download Product Summary (CSV)",
            data=product_summary.to_csv().encode("utf-8"),
            file_name="product_summary.csv",
            mime="text/csv"
        )

        st.download_button(
            label="⬇️ Download Category Summary (CSV)",
            data=category_summary.to_csv().encode("utf-8"),
            file_name="category_summary.csv",
            mime="text/csv"
        )

    else:
        st.error(f"❌ Excel must have these columns: {', '.join(required_cols)}")
