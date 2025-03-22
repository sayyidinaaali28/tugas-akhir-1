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
    
    # Grafik 2: Rata-rata Biaya Pengiriman Per Bulan
    st.subheader("Rata-rata Biaya Pengiriman Per Bulan")
    df_shipping_cost = df_filtered.groupby('order_month')['freight_value'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='order_month', y='freight_value', data=df_shipping_cost, color='orange', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Biaya Pengiriman")
    ax.set_title("Rata-rata Biaya Pengiriman per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight untuk Grafik 2
    st.markdown("Insight: Rata-rata biaya pengiriman per bulan menunjukkan adanya variasi harga sepanjang waktu. Peningkatan biaya pengiriman dapat dipengaruhi oleh faktor eksternal seperti kenaikan harga bahan bakar, perubahan kebijakan logistik, atau fluktuasi dalam jumlah pesanan. Perusahaan dapat menggunakan data ini untuk mengoptimalkan biaya pengiriman dan menawarkan opsi pengiriman yang lebih hemat bagi pelanggan.")
    
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")
