import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def home_page():
    st.title("Home Page")
    st.header("Selamat datang di sistem Topic Modeling")
    st.write(
        "Topic Modeling dilakukan menggunakan BERTopic untuk menganalisis topik-topik dalam artikel berita online terkait Pemilihan Umum (Pemilu) Indonesia 2024. Data yang digunakan merupakan meta deskripsi artikel berita pada [sub kanal pemilu di Detik.com](https://news.detik.com/pemilu) mulai dari tanggal 1 September 2023 hingga 14 Februari 2024."
    )
    
    st.write("Berikut langkah-langkah yang dilakukan pada penelitian ini:")
    st.write("1. Preprocessing : Case Folding, Cleaning, Tokenizing dan Removal Stopword")
    st.write("2. Pemodelan Topik dengan BERTopic")

    # Menampilkan gambar dari file lokal
    st.image('default.svg', width=400) 
    st.markdown("[Kunjungi BERTopic](https://maartengr.github.io/BERTopic/algorithm/algorithm.html)")

def proses_page():
    st.title("BERTopic Page")        

    st.write("Menampilkan hasil preprocessing dan pemodelan yang sudah dilakukan")

    # Membaca hasil preprocessing
    train = pd.read_csv('dataset.csv')
    st.write("Hasil Preprocessing")
    st.write(train[['description', 'description_lower_case', 'description_clean', 'description_stopword']].head())

    # Membaca hasil embedding dan reduksi dimensi
    data = pd.read_csv('embed.csv')
    st.write("Hasil Embedding dan Reduksi Dimensi")
    st.write(data.head())

    # Membaca hasil clustering
    topic_info_all_koherensi = pd.read_csv("topic_info_all_koherensi.csv")
    st.write("Informasi Topik dengan Koherensi")
    st.write(topic_info_all_koherensi.head())

    # Membaca informasi dokumen
    document_info = pd.read_csv('document_info.csv')
    st.write("Informasi Dokumen")
    st.write(document_info.head())

    # Membuat Word Cloud dari topik
    top_words = pd.read_csv('top_words.csv')
    all_representations = ' '.join(top_words['words'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_representations)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Menampilkan plot interaktif untuk trend pemberitaan
    import plotly.express as px
    df_document_info = pd.read_csv('document_info.csv')
    df_document_info['date'] = pd.to_datetime(df_document_info['date'], format='%d/%m/%Y')
    date_counts = df_document_info['date'].value_counts().sort_index().reset_index()
    date_counts.columns = ['date', 'count']
    fig = px.line(date_counts, x='date', y='count', title='Trend Pemberitaan Berdasarkan Tanggal')
    fig.update_xaxes(title='Tanggal')
    fig.update_yaxes(title='Jumlah Dokumen')
    fig.update_layout(xaxis=dict(tickformat="%d-%m-%Y", tickangle=45), hovermode='x')
    st.plotly_chart(fig)

    # Trend untuk topik teratas
    topic_counts = df_document_info.groupby(['Name', 'date']).size().reset_index(name='count')
    top_5_topics = topic_counts.groupby('Name')['count'].sum().nlargest(5).index
    fig = px.line(topic_counts[topic_counts['Name'].isin(top_5_topics)], 
                  x='date', 
                  y='count', 
                  color='Name', 
                  title='Trend Pemberitaan Berdasarkan Tanggal untuk 5 Topik Utama')
    fig.update_xaxes(title='Tanggal', tickformat="%d-%m-%Y", tickangle=45)
    fig.update_yaxes(title='Jumlah Dokumen')
    fig.update_layout(hovermode='x')
    st.plotly_chart(fig)

# Menjalankan aplikasi Streamlit
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih halaman", ["Home", "Proses"])

if page == "Home":
    home_page()
else:
    proses_page()
