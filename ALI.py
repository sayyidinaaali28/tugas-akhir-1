import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Fungsi untuk mengunduh dan membaca data dari Google Drive (dengan caching)
@st.cache_data
def load_data():
    file_id = "1k-PdcMNikrVJ79-TNZc09dsPXZWNRse6"  # Ganti dengan file ID terbaru jika berubah
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
    
    # Dashboard Judul
    st.title('📊 Dashboard Analisis Tren Pesanan')
    
    # Visualisasi Tren Jumlah Pesanan Per Bulan
    st.subheader("📈 Tren Jumlah Pesanan Per Bulan")
    df_orders_by_month = df_filtered.groupby('order_month').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='order_month', y='order_count', data=df_orders_by_month, marker='o', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Jumlah Pesanan Per Bulan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Insight Tren Pesanan
    st.markdown(
        "Insight: Data menunjukkan adanya lonjakan jumlah pesanan pada bulan tertentu, "
        "terutama menjelang akhir tahun (November-Desember). Pola ini dapat dimanfaatkan "
        "untuk strategi pemasaran dan pengelolaan stok." 
    )
    
    # Analisis Lonjakan Pesanan
    st.subheader("📊 Pola Lonjakan Pesanan")
    peak_months = ['2017-11', '2017-12', '2018-11', '2018-12']  # Contoh bulan dengan lonjakan
    df_peak = df_orders_by_month[df_orders_by_month['order_month'].isin(peak_months)]
    
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x='order_month', y='order_count', data=df_peak, ax=ax, palette='coolwarm')
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Lonjakan Pesanan di Bulan Tertentu")
    st.pyplot(fig)
    
    st.markdown(
        "Insight: Peningkatan pesanan terjadi pada akhir tahun, kemungkinan dipengaruhi oleh "
        "momen liburan dan diskon besar seperti Harbolnas atau Black Friday. Bisnis dapat menyesuaikan "
        "strategi promosi dan stok untuk memaksimalkan keuntungan." 
    )
    
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")
