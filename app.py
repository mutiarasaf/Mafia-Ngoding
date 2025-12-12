import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# READ FULL DATASET
# -----------------------------
df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")


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
df.columns = df.columns.str.lower().str.strip()
provinsi_list = df['provinsi'].unique()
   # kolom harus bernama “provinsi”
pilihan_provinsi = st.selectbox("Pilih Provinsi:", provinsi_list)

df_selected = df[df['provinsi'] == pilihan_provinsi]

st.write(f"### Data untuk Provinsi: *{pilihan_provinsi}*")
st.dataframe(df_selected)

# -----------------------------
# VISUALISASI BAR CHART
# -----------------------------
st.subheader("📊 Visualisasi Bar Chart")

# Baca dataset
df = pd.read_csvprint(df.columns)
(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")

# Pilih indikator yang ingin ditampilkan
indikator_list = ['Produk Domestik Bruto/Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 (miliar rupiah) (Miliar Rp)', 'Data tingkat pengangguran di Indonesia (Per Agustus)', 'Indeks Pembangunan Manusia Menurut Provinsi']
df_selected = df = pd.read_csv("C:/Mafia-Ngoding/data/dataindikatorpembangunan.csv")

# Normalisasi nama kolom
df.columns = df.columns.str.lower().str.replace(" ", "_")

print(df.columns)  # cek dulu

df_selected = df[df['indikator'].isin(indikator_list)]

# Plot
plt.figure(figsize=(12,5))

for indikator in indikator_list:
    subset = df_selected[df_selected['indikator'] == indikator]
    plt.bar(subset['tahun'], subset['nilai'], label=indikator)

plt.title("Perbandingan PDB, TPT, dan IPM per Tahun")
plt.xlabel("Tahun")
plt.ylabel("Nilai Indikator")
plt.legend()
plt.tight_layout()
plt.show()

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
