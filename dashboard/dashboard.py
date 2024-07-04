import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv('clean_day_df.csv')
hour_df = pd.read_csv('clean_hour_df.csv')



def plot_tren_mingguan(df):
    tren_mingguan = df.groupby('weekday')['cnt'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=tren_mingguan, x='weekday', y='cnt',order=tren_mingguan['weekday'])
    plt.title('Rata-Rata Harian Penyewaan sepeda dalam Mingguan')
    plt.xlabel('Hari\n0 = Minggu, 6 = Sabtu')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot(plt)

def plot_tren_bulanan(df):
    tren_bulanan = df.groupby('mnth')['cnt'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(data=tren_bulanan, x='mnth', y='cnt', order=tren_bulanan['mnth'])
    plt.title('Rata-Rata Harian Penyewaan sepeda dalam bulanan')
    plt.xlabel('Bulan\n 1 = Januari, 12 = Desember')
    plt.ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot(plt)
    
def ensure_all_weathersit_categories(df):
    # Buat DataFrame dengan semua kategori weathersit dan cnt = 0
    all_weathersit = pd.DataFrame({'weathersit': [1, 2, 3, 4], 'cnt': [0, 0, 0, 0]})
    
    # Hitung rata-rata penyewaan per kategori weathersit
    weather_counts = df.groupby('weathersit')['cnt'].mean().reset_index()

    # Gabungkan dengan data asli untuk memastikan semua kategori ada
    combined_df = pd.concat([weather_counts, all_weathersit]).drop_duplicates('weathersit', keep='first').sort_values('weathersit').reset_index(drop=True)

    return combined_df

def plot_kondisi_cuaca(df):
    df = ensure_all_weathersit_categories(df)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='weathersit', y='cnt', estimator='mean', palette='Blues')
    plt.title('Rata-Rata harian Penyewa berdasarkan kondisi cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-Rata Penyewa Sepeda')
    plt.legend()
    plt.xticks(ticks=[0, 1, 2, 3])
    st.pyplot(plt)

def plot_musiman(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='season', y='cnt', estimator='mean')
    plt.title('Rata-Rata Harian Penyewa Sepeda Berdasarkan Musim')
    plt.xlabel('Musim')
    plt.ylabel('Rata-Rata Penyewa Sepeda')
    st.pyplot(plt)

def plot_tipe_pengguna(df):
    explode=[0,0.1]
    total_pengguna = df[['casual', 'registered']].sum()
    labels = [f'Casual: {total_pengguna["casual"]}', f'Registered: {total_pengguna["registered"]}']
    plt.figure(figsize=(8, 8))
    plt.pie(total_pengguna, labels=labels, autopct='%1.1f%%', startangle=140, colors=['green', 'red'],explode=explode)
    plt.title('Distribusi Penyewa Sepeda Berdasarkan Tipe Pengguna')
    plt.axis('equal') 
    st.pyplot(plt)

def plot_jam_penyewaan(df):
    Hitung_jam = df.groupby('hr')['cnt'].sum().reset_index().sort_values(by='cnt', ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(data=Hitung_jam, x='cnt', y='hr', order=Hitung_jam['hr'], orient='h')
    plt.title('Total Penyewa Sepeda Berdasarkan Jam')
    plt.xlabel('Total Penyewa')
    plt.ylabel('Jam Per Hari')
    st.pyplot(plt)


st.title("Bike Rentals Analysis")
st.header("Pola Penyewaan Berdasarkan Hari dan Bulan")
tab1, tab2 = st.tabs(['Hari', 'Bulan'])
with tab1:
    plot_tren_mingguan(day_df)
    
with tab2:
    plot_tren_bulanan(day_df)

st.header("Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
plot_kondisi_cuaca(day_df)
with st.expander("Penjelasan"):
    st.write('''
        - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
		\n- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
		\n- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
		\n- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'''
    )

st.header("Tren Musiman dalam Penyewaan Sepeda")
plot_musiman(day_df)

st.header("Distribusi Penyewaan Sepeda Berdasarkan Tipe Pengguna")
plot_tipe_pengguna(day_df)

st.header("Penyewaan Sepeda Berdasarkan Jam")
plot_jam_penyewaan(hour_df)