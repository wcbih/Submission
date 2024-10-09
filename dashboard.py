import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

# Mengabaikan peringatan
warnings.simplefilter(action='ignore', category=FutureWarning)

# Membaca file CSV langsung tanpa direktori 'data/'
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Menampilkan header judul untuk dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# --- Exploratory Data Analysis (EDA) ---
st.header("Exploratory Data Analysis (EDA)")

# Cek nilai null dan hapus jika ada
if day_df.isnull().values.any():
    st.warning("Terdapat nilai yang hilang dalam data. Nilai tersebut akan dihapus untuk analisis.")
    day_df = day_df.dropna()

# Analisis Korelasi
st.subheader("Analisis Korelasi")
correlation = day_df.corr(numeric_only=True)  # Hanya menggunakan kolom numerik
plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Korelasi Antara Fitur')
st.pyplot(plt.gcf())

st.write("""
Dari heatmap korelasi di atas, kita dapat melihat hubungan antara berbagai fitur dalam dataset. 
Fitur-fitur seperti suhu (temp) dan total penyewaan (cnt) menunjukkan hubungan positif yang cukup kuat, 
sedangkan kelembapan (hum) memiliki hubungan negatif dengan total penyewaan sepeda.
""")

# Distribusi Total Penyewaan Sepeda per Jam
st.subheader("Distribusi Total Penyewaan Sepeda per Jam")
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
sns.histplot(day_df['cnt'], kde=True, ax=ax_hist)
ax_hist.set_title('Distribusi Total Penyewaan Sepeda per Jam')
ax_hist.set_xlabel('Total Rentals')
st.pyplot(fig_hist)

st.write("""
Distribusi total penyewaan sepeda ini menggambarkan jumlah penyewaan sepeda pada rentang waktu harian. 
Histogram ini menunjukkan pola umum dari penyewaan, yang dapat memberikan wawasan tentang distribusi penyewaan di berbagai jam sepanjang hari.
""")

# --- Visualization & Explanatory Analysis ---
st.header("Visualization & Explanatory Analysis")

# --- Analisis dan visualisasi untuk pertanyaan 1 ---
st.subheader("Pertanyaan 1: Bagaimana distribusi total penyewaan sepeda per jam?")
# Menampilkan distribusi total rental sepeda
# (Bagian ini tidak diubah, akan ada di bawah EDA)

# Visualisasi Penyewaan Sepeda Berdasarkan Situasi Cuaca menggunakan boxplot
st.subheader("Penyewaan Sepeda Berdasarkan Situasi Cuaca")
fig_weather_boxplot, ax_weather_boxplot = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax_weather_boxplot)
ax_weather_boxplot.set_title('Penyewaan Sepeda Berdasarkan Situasi Cuaca')
ax_weather_boxplot.set_xlabel('Situasi Cuaca (1: Clear, 2: Misty, 3: Light Snow/Rain)')
ax_weather_boxplot.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig_weather_boxplot)

st.write("""
Visualisasi ini menggambarkan hubungan antara situasi cuaca dengan jumlah penyewaan sepeda. 
Boxplot ini memberikan informasi mengenai distribusi penyewaan sepeda pada berbagai kondisi cuaca, termasuk median dan rentang interkuartil. 
Cuaca cerah (Clear) cenderung lebih banyak mempengaruhi orang untuk menyewa sepeda, dibandingkan dengan cuaca berkabut (Misty) atau hujan ringan/salju (Light Snow/Rain).
""")
# --- Selesai analisis dan visualisasi untuk pertanyaan 1 ---

# Menghapus outlier untuk analisis yang lebih bersih
Q1 = day_df[['temp', 'atemp', 'hum', 'windspeed']].quantile(0.25)
Q3 = day_df[['temp', 'atemp', 'hum', 'windspeed']].quantile(0.75)
IQR = Q3 - Q1

mask = ~((day_df[['temp', 'atemp', 'hum', 'windspeed']] < (Q1 - 1.5 * IQR)) |
         (day_df[['temp', 'atemp', 'hum', 'windspeed']] > (Q3 + 1.5 * IQR)))

day_df_clean = day_df[mask.all(axis=1)]

# --- Analisis dan visualisasi untuk pertanyaan 2 ---
st.subheader("Pertanyaan 2: Apa saja faktor-faktor yang memengaruhi penyewaan sepeda?")
# Visualisasi tambahan: Suhu vs Total Rental
st.subheader("Temperatur vs Total Rentals (Hari kerja vs Hari libur)")
# Visualisasi Temperatur vs Total Rentals
plt.figure(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', hue='workingday', data=day_df)
plt.title('Temperatur vs Total Rentals (Hari kerja vs Hari libur)')
plt.xlabel('Temperatur normal')
plt.ylabel('Total Rentals')
st.pyplot(plt.gcf())

st.write("""
Analisis berikutnya adalah hubungan antara temperatur dan total penyewaan sepeda. Visualisasi berikut memisahkan data berdasarkan hari kerja dan hari libur untuk melihat bagaimana temperatur mempengaruhi penyewaan pada kedua kondisi tersebut.
""")

# Ringkasan Akhir
st.subheader("Kesimpulan Analisis")
st.write("""
Dari analisis di atas, kita bisa melihat beberapa pola menarik dalam penyewaan sepeda:
1. **Distribusi Waktu:** Penyewaan sepeda meningkat pada jam-jam sibuk, dan lebih tinggi pada akhir pekan.
2. **Pengaruh Cuaca dan Suhu:** Cuaca cerah dan suhu yang nyaman memiliki pengaruh positif terhadap jumlah penyewaan sepeda. Cuaca ekstrem atau suhu yang terlalu tinggi dapat mempengaruhi secara negatif.
""")
