# import library
import streamlit as st 
import numpy as np
import pandas as pd


# menambahkan text untuk streamlit
st.title('Uber Pickup')
st.subheader('Bab 1')
st.write('here is the text')

# make dataframe
# df = pd.DataFrame({
#   '1st_column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })
#tampilkan data frame di streamlit
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# cache fetched data so we not reload data
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')


st.subheader('Raw data Uber Pickup in NYC')
st.write(data)

st.subheader('jumlah ')
angka_hist = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]# np.histogram(data[DATE_COLUMN].dt.hour,bin=24,range=(0.24))[0]
st.bar_chart(angka_hist)

# plotting map
# st.subheader('Peta penjemputan')
# st.map(data)


# slider UI
jam_jemput = st.slider('hour',0,23,17) #

# map spesifik
st.subheader('Peta penjemputan sesuai jam')
st.text('Peta penjemputan pada pukul 15')
# jam_penjemputan = 2
filtered_data = data[data[DATE_COLUMN].dt.hour==jam_jemput]

# plotting map
st.subheader('Peta penjemputan')
st.map(filtered_data)