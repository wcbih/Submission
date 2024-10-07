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

# Menampilkan jumlah nilai hilang
st.write("Jumlah missing value day: ", day_df.isna().sum())
st.write("Jumlah missing value hour: ", hour_df.isna().sum())

# Menghapus duplikat dan nilai hilang
day_df.dropna(inplace=True)
day_df.drop_duplicates(inplace=True)
hour_df.dropna(inplace=True)
hour_df.drop_duplicates(inplace=True)

# Menampilkan boxplot untuk mendeteksi outlier
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

# Menampilkan ringkasan statistik
st.write(day_df_clean.describe())

# Visualisasi distribusi total rental sepeda
fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
sns.histplot(day_df_clean['cnt'], kde=True, ax=ax_hist)
ax_hist.set_title('Total Distribusi Rental Sepeda')
ax_hist.set_xlabel('Total Rentals')
st.pyplot(fig_hist)


st.write("Grafik histogram ini menunjukkan distribusi total penyewaan sepeda per jam, dengan sumbu horizontal menampilkan jumlah total penyewaan dan sumbu vertikal menunjukkan frekuensinya. Grafik juga dilengkapi dengan garis KDE untuk memperlihatkan pola distribusi yang lebih halus. Dari visualisasi ini, kita bisa melihat rentang penyewaan yang paling sering terjadi dan memahami tren umum perilaku pengguna dalam menyewa sepeda sepanjang hari, yang bisa digunakan untuk pengambilan keputusan terkait pengelolaan sepeda.")