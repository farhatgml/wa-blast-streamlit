import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(page_title="WA Blast Generator", layout="centered")

st.title("📤 WhatsApp Blast Generator")
st.write("Upload your Excel file and select a greeting to auto-generate WA messages.")

# Select greeting
greeting = st.selectbox("Pilih Waktu (Template Waktu):", ["Selamat pagi", "Selamat siang", "Selamat sore"])

# File uploader
uploaded_file = st.file_uploader("Upload Excel (.xlsx)", type="xlsx")

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    required_columns = {"Name", "Phone Number", "Produk", "Limit Kredit"}
    if not required_columns.issubset(df.columns):
        st.error(f"File must include columns: {required_columns}")
    else:
        st.success("File loaded successfully. Preview below:")
        st.dataframe(df)

        st.subheader("Generated Messages & WA Links:")

        for idx, row in df.iterrows():
            name = row["Name"]
            phone = str(row["Phone Number"])
            produk = row["Produk"]
            limit = row["Limit Kredit"]

            message = (
                f"{greeting}, {name}. Selamat! Sekarang kamu sudah menjadi nasabah terpilih dari produk unggulan Bank Mandiri, yaitu {produk}. "
                f"Berdasarkan data historis Saudara dan track record pinjaman yang sudah dilunaskan, Saudara berhak mendapatkan pinjaman dengan limit sebesar {limit}. "
                "Balas pesan ini apabila Anda tertarik untuk melakukan pengajuan! Tahapnya mudah, cepat, dan pastinya terpercaya bersama Bank Mandiri!"
            )

            wa_link = f"https://wa.me/{phone}?text={quote(message)}"

            st.markdown(f"**{name}**: [Kirim WA]({wa_link})")