import streamlit as st
import plotly.express as px
import pandas as pd
import requests
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
    
    # Terjemahkan kategori produk jika ada
    kategori_terjemahan = {
        "utilidades_domesticas": "Peralatan Rumah Tangga",
        "perfumaria": "Parfum",
        "automotivo": "Otomotif",
        "pet_shop": "Toko Hewan Peliharaan",
        "papelaria": "Alat Tulis",
        "moveis_decoracao": "Dekorasi Rumah",
        "moveis_escritorio": "Furniture Kantor",
        "ferramentas_jardim": "Peralatan Taman",
        "informatica_acessorios": "Aksesori Komputer",
        "cama_mesa_banho": "Peralatan Tidur & Mandi",
        "brinquedos": "Mainan",
        "construcao_ferramentas": "Alat Konstruksi",
        "telefonia": "Telepon & Aksesori",
        "beleza_saude": "Kecantikan & Kesehatan",
        "eletronicos": "Elektronik",
        "bebes": "Perlengkapan Bayi",
        "cool_stuff": "Barang Unik",
        "relogios_presentes": "Jam & Hadiah",
        "climatizacao": "Pengatur Iklim",
        "esporte_lazer": "Olahraga & Rekreasi",
        "livros_interesse_geral": "Buku Umum",
        "eletroportateis": "Peralatan Elektronik",
        "alimentos": "Makanan",
        "malas_acessorios": "Koper & Aksesori"
    }
    
    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].map(kategori_terjemahan).fillna(df['product_category_name'])
        selected_category = st.sidebar.multiselect(
            "🛍️ Pilih Kategori Produk:", df['product_category_name'].unique(), default=df['product_category_name'].unique()
        )
        df = df[df['product_category_name'].isin(selected_category)]
    
    # Menampilkan data contoh
    st.write("**📄 Preview Data:**")
    st.write(df.head())
    
    # Membuat grafik distribusi harga produk
    fig_price_distribution = px.histogram(df, x='price', nbins=50, title='Distribusi Harga Produk')
    
    # Membuat tren jumlah pesanan per bulan
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

