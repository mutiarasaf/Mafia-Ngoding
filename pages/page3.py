import streamlit as st

st.title("Settings")
st.write("This page allows you gto cuztomize your preferences.")

df = pd.read_csv('data/dataindikatorpembangunan.csv')
st.write(df.tail())

st.write("Simulasi error")
