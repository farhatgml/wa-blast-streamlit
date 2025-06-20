import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(page_title="WA Blast Generator", layout="centered")

st.title("📤 WhatsApp Blast Generator")
st.write("Pilih metode input dan atur template pesan untuk mengirim pesan WhatsApp secara otomatis.")

# Select greeting
greeting = st.selectbox("Pilih Waktu (Template Waktu):", ["Selamat pagi", "Selamat siang", "Selamat sore"])

# Message template input
st.subheader("✍️ Customize Message Template")
default_template = (
    "{{waktu}}, {{name}}.\n\n"
    "Selamat! Sekarang kamu sudah menjadi nasabah terpilih dari produk unggulan Bank Mandiri, yaitu {{produk}}. "
    "Berdasarkan data historis Saudara dan track record pinjaman yang sudah dilunaskan, Saudara berhak mendapatkan pinjaman dengan limit sebesar {{limit}}.\n\n"
    "Mohon balas pesan ini apabila Anda tertarik untuk melakukan pengajuan! Tahapnya mudah, cepat, dan pastinya terpercaya bersama Bank Mandiri!"
)
template = st.text_area("Edit your message template here:", value=default_template, height=200)

# Select input mode
input_mode = st.radio("Pilih metode input data:", ["📁 Upload Excel", "✍️ Input Manual"])

df = None

if input_mode == "📁 Upload Excel":
    uploaded_file = st.file_uploader("Upload Excel (.xlsx)", type="xlsx")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        required_columns = {"Name", "Phone Number", "Produk", "Limit Kredit"}
        if not required_columns.issubset(df.columns):
            st.error(f"File must include columns: {required_columns}")
            df = None
        else:
            st.success("File loaded successfully. Preview below:")
            st.dataframe(df)

elif input_mode == "✍️ Input Manual":
    st.info("Silakan isi data di bawah ini.")
    name_input = st.text_input("Nama")
    phone_input = st.text_input("Nomor WhatsApp (contoh: 6281234567890)")
    produk_input = st.text_input("Nama Produk")
    limit_number = st.number_input("Limit Kredit (angka saja)", min_value=0, step=1000000)
    limit_input = f"Rp{limit_number:,.0f}".replace(",", ".")
    st.caption(f"Format yang akan digunakan: **{limit_input}**")

    if name_input and phone_input and produk_input and limit_input:
        df = pd.DataFrame([{
            "Name": name_input,
            "Phone Number": phone_input,
            "Produk": produk_input,
            "Limit Kredit": limit_input
        }])
    else:
        st.warning("Silakan lengkapi semua isian untuk melihat hasil.")

# Generate messages
if df is not None:
    st.subheader("Generated Messages & WA Links:")

    for idx, row in df.iterrows():
        name = row["Name"]
        phone = str(row["Phone Number"])
        produk = row["Produk"]
        limit = row["Limit Kredit"]

        # Replace placeholders in the user-defined template
        message = template.replace("{{waktu}}", greeting)\
                          .replace("{{name}}", name)\
                          .replace("{{produk}}", produk)\
                          .replace("{{limit}}", str(limit))

        wa_link = f"https://wa.me/{phone}?text={quote(message)}"
        st.markdown(f"**{name}**: [Kirim WA]({wa_link})")
