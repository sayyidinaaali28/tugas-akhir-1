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

    # Terapkan filter tanggal
    df_filtered = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                     (df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    
    # Menampilkan data contoh
    st.write("📄 Preview Data:")
    st.write(df_filtered.head())
    
    # Membuat dashboard dengan Streamlit
    st.title('📊 Dashboard Analisis Data')
    
    # Grafik 1: Tren Jumlah Pesanan Per Bulan (Asli dari Notebook)
    st.subheader("Tren Jumlah Pesanan Per Bulan")
    df_orders_by_month = df_filtered.groupby('order_month').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='order_month', y='order_count', data=df_orders_by_month, marker='o', ax=ax, color='blue')
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan Per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight untuk Tren Pesanan
    st.markdown("Insight: Tren jumlah pesanan per bulan menunjukkan pola lonjakan signifikan pada bulan-bulan tertentu, terutama di akhir tahun (November–Desember). Lonjakan ini kemungkinan besar dipengaruhi oleh musim liburan serta promo besar seperti Harbolnas dan Black Friday. Setelah periode puncak, jumlah pesanan tetap tinggi tetapi mulai mengalami penurunan bertahap.")
    
    # Grafik 2: Tren Jumlah Pesanan dengan Skala Waktu yang Berbeda
    st.subheader("Tren Jumlah Pesanan dengan Skala Waktu Berbeda")
    df_orders_by_month['order_month'] = pd.to_datetime(df_orders_by_month['order_month'])
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='order_month', y='order_count', data=df_orders_by_month, marker='o', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan dalam Periode yang Lebih Detail")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight untuk Grafik 2
    st.markdown("Insight: Lonjakan pesanan terjadi secara konsisten pada periode tertentu setiap tahunnya, menunjukkan adanya pola musiman yang dapat diprediksi. Faktor eksternal seperti tren pasar, perubahan kebijakan harga, dan strategi pemasaran juga berperan dalam perubahan jumlah pesanan dari waktu ke waktu. Untuk mengoptimalkan keuntungan, bisnis dapat menyusun strategi pemasaran dengan fokus pada periode lonjakan pesanan serta menyesuaikan pengelolaan stok agar dapat menangani peningkatan volume pesanan dengan lebih efisien.")
    
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")
