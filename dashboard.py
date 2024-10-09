import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings

# Mengabaikan peringatan
warnings.simplefilter(action='ignore', category=FutureWarning)

# Membaca file CSV
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Menampilkan header judul untuk dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

# Menampilkan jumlah nilai hilang
st.subheader("Analisis Missing Value")
st.write("Jumlah missing value day: ")
st.write(day_df.isna().sum())
st.write("Jumlah missing value hour: ")
st.write(hour_df.isna().sum())

# Menghapus duplikat dan nilai hilang
day_df.dropna(inplace=True)
day_df.drop_duplicates(inplace=True)
hour_df.dropna(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Menampilkan visualisasi Outliers
st.subheader("Visualisasi Outliers")
fig_outliers, ax_outliers = plt.subplots(figsize=(10, 6))
sns.boxplot(data=day_df[['temp', 'atemp', 'hum', 'windspeed']], ax=ax_outliers)
ax_outliers.set_title('Outliers in Day Dataset')
st.pyplot(fig_outliers)

# Menghapus outlier
Q1 = day_df[['temp', 'atemp', 'hum', 'windspeed']].quantile(0.25)
Q3 = day_df[['temp', 'atemp', 'hum', 'windspeed']].quantile(0.75)
IQR = Q3 - Q1

mask = ~((day_df[['temp', 'atemp', 'hum', 'windspeed']] < (Q1 - 1.5 * IQR)) |
         (day_df[['temp', 'atemp', 'hum', 'windspeed']] > (Q3 + 1.5 * IQR)))

day_df_clean = day_df[mask.all(axis=1)]

# Menampilkan ringkasan statistik dari data yang sudah dibersihkan
st.subheader("Ringkasan Statistik dari Data yang Sudah Dibersihkan")
st.write(day_df_clean.describe())

# Visualisasi distribusi total rental sepeda
st.subheader("Distribusi Total Penyewaan Sepeda per Jam")
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
sns.histplot(day_df_clean['cnt'], kde=True, ax=ax_hist)
ax_hist.set_title('Total Distribusi Rental Sepeda')
ax_hist.set_xlabel('Total Rentals')
st.pyplot(fig_hist)

st.write("""
Grafik histogram ini menunjukkan distribusi total penyewaan sepeda per jam, 
dengan sumbu horizontal menampilkan jumlah total penyewaan dan 
sumbu vertikal menunjukkan frekuensinya. Grafik juga dilengkapi 
dengan garis KDE untuk memperlihatkan pola distribusi yang lebih halus. 
""")

# Analisis hubungan antara cuaca dan penyewaan sepeda
st.subheader("Analisis Hubungan Cuaca dan Penyewaan Sepeda")
fig_weather, ax_weather = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=day_df_clean['temp'], y=day_df_clean['cnt'], ax=ax_weather)
ax_weather.set_title('Hubungan Suhu dengan Penyewaan Sepeda')
ax_weather.set_xlabel('Temperature (°C)')
ax_weather.set_ylabel('Total Rentals')
st.pyplot(fig_weather)

st.write("""
Grafik scatterplot ini menunjukkan hubungan antara suhu dan jumlah penyewaan sepeda. 
Semakin tinggi suhu, penyewaan sepeda cenderung meningkat, meskipun ada batas tertentu 
di mana suhu yang terlalu tinggi dapat menurunkan tingkat penyewaan.
""")

# Visualisasi penyewaan sepeda berdasarkan hari dalam seminggu
st.subheader("Penyewaan Sepeda Berdasarkan Hari dalam Seminggu")
fig_day_of_week, ax_day_of_week = plt.subplots(figsize=(10, 6))
sns.barplot(x=day_df_clean['weekday'], y=day_df_clean['cnt'], ax=ax_day_of_week)
ax_day_of_week.set_title('Total Penyewaan Sepeda Berdasarkan Hari dalam Seminggu')
ax_day_of_week.set_xlabel('Hari')
ax_day_of_week.set_ylabel('Total Rentals')
st.pyplot(fig_day_of_week)

st.write("""
Grafik bar ini menunjukkan jumlah penyewaan sepeda berdasarkan hari dalam seminggu. 
Data menunjukkan bahwa penyewaan sepeda cenderung lebih tinggi pada akhir pekan.
""")

# Menampilkan analisis waktu penyewaan sepeda berdasarkan jam
st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Jam dalam Sehari")
fig_hourly, ax_hourly = plt.subplots(figsize=(10, 6))
sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], ax=ax_hourly)
ax_hourly.set_title('Penyewaan Sepeda Berdasarkan Jam')
ax_hourly.set_xlabel('Jam dalam Sehari')
ax_hourly.set_ylabel('Total Rentals')
st.pyplot(fig_hourly)

st.write("""
Grafik lineplot ini menunjukkan pola penyewaan sepeda sepanjang hari. 
Penyewaan cenderung lebih tinggi pada jam sibuk, yaitu pagi hari saat berangkat kerja dan sore hari saat pulang kerja.
""")

# Ringkasan Akhir
st.subheader("Kesimpulan Analisis")
st.write("""
Dari analisis di atas, kita bisa melihat beberapa pola menarik dalam penyewaan sepeda:
1. **Distribusi Waktu:** Penyewaan sepeda meningkat pada jam-jam sibuk, dan lebih tinggi pada akhir pekan.
2. **Pengaruh Cuaca:** Suhu memiliki pengaruh terhadap jumlah penyewaan sepeda, namun cuaca ekstrem dapat mempengaruhi secara negatif.
3. **Outliers:** Data mengandung beberapa outliers, namun sudah kita tangani untuk membersihkan dataset.
""")
