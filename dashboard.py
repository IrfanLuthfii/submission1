import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hour").agg({"count": ["sum"]}).reset_index()
  return hour_count_df

def sum_hour (hour_df):
    sum_hour_df = hour_df.groupby("hour")['count'].sum().sort_values(ascending=False).reset_index()
    return sum_hour_df

def get_category_AM_PM(hour_df):
    hourly_data = hour_df.groupby(by="hour").agg({
        "count": "sum"
    }).reset_index()

    category_labels = ['AM (00.00-11.59)', 'PM (12.00-23.59)']
    hourly_data['category'] = pd.cut(hourly_data['hour'], bins=[0, 11, 23], labels=category_labels, right=False)

    category_data = hourly_data.groupby(by="category").agg({
        "count": "sum"
    }).reset_index()
    return category_data

def count_by_day_df(day_df):
    day_df_count = day_df.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    day_df_count.rename(columns = {
        "count": "total_count"
    },inplace = True)
    return day_df_count

def total_registered_df(day_df):
   registered_df =  day_df.groupby(by="date").agg({
      "registered": "sum"
    })
   registered_df = registered_df.reset_index()
   registered_df.rename(columns={
        "registered": "total_register"
    }, inplace=True)
   return registered_df

def total_casual_df(day_df):
   casual_df =  day_df.groupby(by="date").agg({
      "casual": ["sum"]
    })
   casual_df = casual_df.reset_index()
   casual_df.rename(columns={
        "casual": "total_casual"
    }, inplace=True)
   return casual_df

def get_yearly_monthly_count(day_df,year):
    df_yearly = day_df[day_df['date'].dt.year == year]
    df_yearly_monthly = df_yearly.groupby(df_yearly['date'].dt.month).agg({'count': 'sum'})
    return df_yearly_monthly



days_df = pd.read_csv("day_clean.csv")
hours_df = pd.read_csv("hour_clean.csv")

datetime_columns = ["date"]
days_df.sort_values(by="date", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="date", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["date"].min()
max_date_days = days_df["date"].max()

min_date_hour = hours_df["date"].min()
max_date_hour = hours_df["date"].max()

with st.sidebar:
    
    st.subheader("Welcome to Bikers :bicyclist:")
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/family-weekend-outdoors_74855-4788.jpg?t=st=1709349713~exp=1709353313~hmac=30616e7c6abff146405973d3da94d51c0454a0ea3ab4f8f52b50e495698b0ad8&w=900")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["date"] >= str(start_date)) & 
                       (days_df["date"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["date"] >= str(start_date)) & 
                        (hours_df["date"] <= str(end_date))]

season_order = ['Spring', 'Summer', 'Fall', 'Winter']
main_df_days['season'] = pd.Categorical(main_df_days['season'], categories=season_order, ordered=True)

hour_count_df = get_total_count_by_hour_df(main_df_hour)
category_AM_PM_df = get_category_AM_PM(main_df_hour)
sum_hour_df = sum_hour(main_df_hour)
day_df_count = count_by_day_df(main_df_days)
registered_df = total_registered_df(main_df_days)
casual_df = total_casual_df(main_df_days)
df_2011_monthly = get_yearly_monthly_count(days_df, 2011)
df_2012_monthly = get_yearly_monthly_count(days_df, 2012)

#Membuat Header dan Subheader Pertama
st.header("Bikers :bicyclist:")
st.subheader('Daily rentals')

col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count.total_count.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = registered_df.total_register.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = casual_df.total_casual.sum()
    st.metric("Total Casual", value=total_sum)

#Membuat SubHeader ke 2
st.subheader("Pada musim apa penyewaan sepeda paling banyak dan paling sedikit dilakukan?")
colors = ["red", "blue", "yellow", "blue"]
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
        y="count",
        x="season",
        data=main_df_days.sort_values(by="season",),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Jumlah Penyewaan Tiap Musim", loc="center", fontsize=20)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)
st.pyplot(fig)

#Membuat SubHeader ketiga
st.subheader("Pada jam berapa penyewaan sepeda yang paling banyak dan paling sedikit Sepanjang Tahun 2011 dan 2012 ?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(36, 16))

#Karena warna belum bisa tepat berubah secara dinamis maka warna saat ini dibuat sama
sns.barplot(x="hour", y="count", data=sum_hour_df.head(5), palette=["blue", "blue", "blue", "blue", "blue"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jam (Format 24)", fontsize=25)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=30)

#Karena warna belum bisa tepat berubah secara dinamis maka warna saat ini dibuat sama
sns.barplot(x="hour", y="count", data=sum_hour_df.sort_values(by="hour", ascending=True).head(5), palette=["blue", "blue", "blue", "blue","blue"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jam (Format 24)",  fontsize=25)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Membuat SubHeader Ketiga
st.subheader("Bagaimana Perbandingan jumlah penyewaan sepeda antara jam 00.00-11.59 dengan jam 12.00-23.59 (AM dan PM)?")
# Membuat Pie Chart
fig1, ax1 = plt.subplots()
ax1.pie(category_AM_PM_df['count'], labels=category_AM_PM_df['category'], autopct='%1.1f%%', startangle=120, colors=['lightblue', 'yellow'])
ax1.set_title('Penyewaan Sepeda Berdasarkan waktu AM dan PM')
ax1.axis('equal')  
st.pyplot(fig1)

# Membuat SubHeader Ke empat
st.subheader("Bagaimana perbandingan jumlah antara pelanggan jenis registered dan casual ?")
labels = 'casual', 'registered'
sizes = [18.8, 81.2]
fig1, ax1 = plt.subplots()
ax1.set_title('Penyewaan Sepeda Berdasarkan Jenis Pengguna')
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',colors=["lightblue", "yellow"], startangle=90)
ax1.axis('equal')  
st.pyplot(fig1)

# Membuat SubHeader Ke Lima
st.subheader("Bagaimana performa penyewaan sepeda per bulan tiap tahunnya?")
# Membuat line chart untuk membandingkan total penyewaan tiap bulannya di tahun 2011 dan 2012 menggunakan seaborn
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=df_2011_monthly.index, y=df_2011_monthly['count'], label='2011', marker='o', ax=ax)
sns.lineplot(x=df_2012_monthly.index, y=df_2012_monthly['count'], label='2012', marker='o', ax=ax)
ax.legend()
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penyewaan')
ax.set_title('Penyewaan Sepeda Per Bulan (2011 vs 2012)')

st.pyplot(fig)

st.caption('Copyright Irfan Luthfi')
