import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# READ FULL DATASET
# -----------------------------
df = os.chdir(r"C:\Mafia-Ngoding")
pd.read_csv(r"C:\Mafia-Ngoding\dataindikatorpembangunan.csv")


st.title("Dashboard Data Indikator Pembangunan")

# -----------------------------
# SHOW FULL DATA
# -----------------------------
st.subheader("📄 Seluruh Data")
st.dataframe(df)    # tampilkan seluruh data, bukan head/tail

# -----------------------------
# FILTER PROVINSI
# -----------------------------
st.subheader("🔍 Pilih Provinsi")
provinsi_list = df['provinsi'].unique()   # kolom harus bernama “provinsi”
pilihan_provinsi = st.selectbox("Pilih Provinsi:", provinsi_list)

df_selected = df[df['provinsi'] == pilihan_provinsi]

st.write(f"### Data untuk Provinsi: *{pilihan_provinsi}*")
st.dataframe(df_selected)

# -----------------------------
# VISUALISASI BAR CHART
# -----------------------------
st.subheader("📊 Visualisasi Bar Chart")

# SESUAIKAN kolom indikator yg mau ditampilkan
# contoh: 'tahun' sebagai x dan 'nilai' sebagai bar
plt.figure(figsize=(10, 5))
plt.bar(df_selected['tahun'], df_selected['nilai'])
plt.xlabel("Tahun")
plt.ylabel("Nilai Indikator")
plt.title(f"Bar Chart Indikator Pembangunan - {pilihan_provinsi}")

st.pyplot(plt)

pages = [
    st.Page(page="pages/page1.py", title="Home", icon="🏡"),
    st.Page(page="pages/page2.py", title="Visualisasi Data", icon="📊"),
    st.Page(page="pages/page3.py", title="Settings", icon="⚙️")
]

pg = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)
pg.run()
