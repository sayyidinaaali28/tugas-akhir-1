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
    df['order_year'] = df['order_purchase_timestamp'].dt.year

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
    st.title('📊 Dashboard Analisis Tren Pesanan')
    
    # Visualisasi Tren Jumlah Pesanan Per Bulan
    st.subheader("Tren Jumlah Pesanan Per Bulan (2016-2018)")
    df_orders_by_month = df_filtered.groupby('order_month').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='order_month', y='order_count', data=df_orders_by_month, marker='o', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan Per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight untuk Tren Pesanan
    st.markdown("Insight: Jumlah pesanan mengalami kenaikan signifikan pada bulan-bulan tertentu, terutama menjelang akhir tahun (November-Desember). Lonjakan ini kemungkinan besar disebabkan oleh musim liburan dan promosi besar seperti Harbolnas dan Black Friday.")
    
    # Visualisasi Lonjakan Pesanan
    st.subheader("Pola Lonjakan Pesanan")
    df_orders_by_year = df_filtered.groupby('order_year').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='order_year', y='order_count', data=df_orders_by_year, ax=ax)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Jumlah Pesanan per Tahun")
    st.pyplot(fig)
    
    # Insight untuk Lonjakan Pesanan
    st.markdown("Insight: Terdapat peningkatan jumlah pesanan yang konsisten setiap tahunnya, dengan lonjakan terbesar terjadi pada akhir tahun. Perusahaan dapat memanfaatkan pola ini untuk mengoptimalkan strategi pemasaran dan manajemen stok guna meningkatkan keuntungan.")
    
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")
