import streamlit as st
import plotly.express as px
import pandas as pd
import requests  # Tambahkan import requests
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
    # Menampilkan data contoh
    st.write("**Preview Data:**")
    st.write(df.head())

    # Konversi kolom tanggal ke format datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

    # Membuat grafik distribusi harga produk
    fig_price_distribution = px.histogram(df, x='price', nbins=50, title='Distribusi Harga Produk')

    # Membuat tren jumlah pesanan per bulan
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    df_orders_by_month = df.groupby('order_month').size().reset_index(name='order_count')
    fig_orders_trend = px.line(df_orders_by_month, x='order_month', y='order_count', title='Tren Jumlah Pesanan Per Bulan')

    # Membuat dashboard dengan Streamlit
    st.title('📊 Dashboard Analisis Data')
    
    # Menampilkan grafik
    st.subheader("Distribusi Harga Produk")
    st.plotly_chart(fig_price_distribution)

    st.subheader("Tren Jumlah Pesanan Per Bulan")
    st.plotly_chart(fig_orders_trend)
else:
    st.error("Data tidak tersedia. Periksa kembali link Google Drive.")
