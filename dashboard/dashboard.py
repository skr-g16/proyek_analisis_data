#import library
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv('./dashboard/day.csv')
hour_df = pd.read_csv('./dashboard/hour.csv')

def create_plot_week(df):
    week_df = df.groupby('weekday').agg({'cnt':'sum'}).sort_values(by='cnt', ascending=True)
    return week_df

def create_plot_month(df):
    month_df = df.groupby('mnth').agg({'cnt':'sum'}).sort_values(by='cnt', ascending=True)
    return month_df

def plot_weather_scatter(df):
    weather_factors = ["temp", "atemp", "hum", "windspeed"]
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    for ax, factor in zip(axs.flatten(), weather_factors):
        sns.scatterplot(data=df, x=factor, y="cnt", alpha=0.5, ax=ax)
        ax.set_title(f'Pengaruh {factor.capitalize()} Terhadap Penyewaan Sepeda')
        ax.set_xlabel(factor.capitalize())
        ax.set_ylabel('Jumlah Penyewaan')
        ax.grid(True, linestyle='--', alpha=0.7)   
    plt.tight_layout()
    st.pyplot(fig)

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    selected_season = st.multiselect(
    label='Pilih Musim', options=day_df['season'].unique(), default=day_df['season'].unique()
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date)) &
                (day_df["season"].isin(selected_season))]

hourly_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                    (hour_df["dteday"] <= str(end_date))&
                    (hour_df["season"].isin(selected_season))]

week_df = create_plot_week(main_df)
month_df = create_plot_month(main_df)

st.title('Dashboard Penyewaan Sepeda')
total_rentals = main_df['cnt'].sum()
avg_temp = main_df['temp'].mean()
avg_humidity = main_df['hum'].mean()

st.metric(label="Total Penyewaan", value=f"{total_rentals:,}")
st.metric(label="Rata-Rata Suhu", value=f"{avg_temp:.2f} °C")
st.metric(label="Rata-Rata Kelembapan", value=f"{avg_humidity:.2f} %")

st.header("Pola Penyewaan Berdasarkan Hari dan Bulan")

tab1, tab2 = st.tabs(['Hari', 'Bulan'])
with tab1:
    plt.figure(figsize=(10, 6))
    colors = ["#D3D3D3"] * len(week_df)
    colors[-1] = "#90CAF9" 
    plt.barh(week_df.index, week_df['cnt'], color=colors)
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Hari')
    plt.xlabel('Jumlah Penyewaan')
    plt.ylabel('Hari')
    st.pyplot(plt)
    
with tab2:
    plt.figure(figsize=(10, 6))
    colors = ["#D3D3D3"] * len(month_df)
    colors[-1] = "#90CAF9" 
    plt.barh(month_df.index, month_df['cnt'], color=colors)
    plt.title('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
    plt.xlabel('Jumlah Penyewaan')
    plt.ylabel('Bulan')
    st.pyplot(plt)

# Pengaruh faktor cuaca
st.header("Pengaruh Faktor Cuaca Terhadap Penyewaan Sepeda")
with st.expander("Lihat Detail Pengaruh Cuaca"):
    plot_weather_scatter(main_df)

st.header("Tren Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan selama Musim yang Berbeda")
# Filter untuk hari kerja dan akhir pekan
weekday_data = day_df[day_df['workingday'] == 'Weekday']
weekend_data = day_df[day_df['workingday'] == 'Weekend']

# Kelompokkan hari kerja berdasarkan musim dan hitung rata-rata penyewaan
weekday_seasonal_rentals = weekday_data.groupby('season')['cnt'].mean().sort_values(ascending=False)

# Kelompokkan akhir pekan berdasarkan musim dan hitung rata-rata penyewaan
weekend_seasonal_rentals = weekend_data.groupby('season')['cnt'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(weekday_seasonal_rentals.index, weekday_seasonal_rentals.values, label='Hari Kerja', color='blue')
plt.bar(weekend_seasonal_rentals.index, weekend_seasonal_rentals.values, label='Akhir Pekan', alpha=0.7, color='orange')
plt.title('Tren Musiman Penyewaan Sepeda')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.legend()
st.pyplot(plt)

st.header("Distribusi Penyewaan Sepeda Berdasarkan Tipe Pengguna")
total_casual = main_df['casual'].sum()
total_registered = main_df['registered'].sum()
plt.figure(figsize=(10, 6))
explode = [0.1, 0]
plt.pie([total_casual, total_registered], labels=['Casual', 'Registered'], autopct='%1.1f%%', explode=explode)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Tipe Pengguna')
st.pyplot(plt)

st.header("Jam-jam Puncak Penyewaan Sepeda")
hourly_rentals = hourly_df.groupby('hr')['cnt'].sum().sort_values(ascending=True)
plt.figure(figsize=(10, 6))
colors = ["#D3D3D3"] * len(hourly_rentals)
colors[-1] = "#90CAF9"  # Warna biru untuk nilai maksimal
hourly_rentals.plot(kind='barh', color=colors)
plt.title('Penyewaan Sepeda Per Jam')
plt.xlabel('Jumlah Penyewaan')
plt.ylabel('Jam')
st.pyplot(plt)