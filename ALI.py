import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Fungsi untuk mengunduh dan membaca data dari Google Drive (dengan caching)
@st.cache_data
def load_data():
    file_id = "1k-PdcMNikrVJ79-TNZc09dsPXZWNRse6"
    url = f"https://drive.google.com/uc?id={file_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(BytesIO(response.content))
        return df
    else:
        st.error("Gagal mengunduh data dari Google Drive.")
        return None

# Load dataset
df = load_data()

if df is not None:
    # Konversi kolom tanggal ke format datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    # Sidebar untuk filter interaktif
    st.sidebar.header("🔍 Filter Data")
    
    # Filter berdasarkan rentang tanggal
    min_date = df['order_purchase_timestamp'].min()
    max_date = df['order_purchase_timestamp'].max()
    start_date, end_date = st.sidebar.date_input(
        "📅 Pilih Rentang Tanggal:", [min_date, max_date], min_value=min_date, max_value=max_date
    )
    df = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & (df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    
    # Menampilkan data contoh
    st.write("**📄 Preview Data:**")
    st.write(df.head())
    
    # Membuat dashboard dengan Streamlit
    st.title('📊 Dashboard Analisis Data')
    
    # Visualisasi Distribusi Harga Produk
    st.subheader("Distribusi Harga Produk")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df['price'], bins=100, kde=True, ax=ax)
    ax.set_xlabel("Harga")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Distribusi Harga Produk")
    st.pyplot(fig)
    
    # Insight untuk Distribusi Harga Produk
    st.markdown("** Insight:** Sebagian besar harga produk berada di bawah 500, dengan sedikit produk yang memiliki harga tinggi. Ini menunjukkan bahwa mayoritas produk yang dijual memiliki harga yang cukup terjangkau.")
    
    # Visualisasi Tren Jumlah Pesanan Per Bulan
    st.subheader("Tren Jumlah Pesanan Per Bulan")
    df_orders_by_month = df.groupby('order_month').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='order_month', y='order_count', data=df_orders_by_month, marker='o', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan Per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight untuk Tren Pesanan
    st.markdown("** Insight:** Terlihat adanya pola kenaikan jumlah pesanan pada bulan-bulan tertentu, yang bisa mengindikasikan adanya faktor musiman dalam pembelian.")
    
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")

