import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# 1. BACA DATA (HARUS PALING ATAS)
# -----------------------------------
df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")

# -----------------------------------
# 2. TAMPILKAN DASHBOARD
# -----------------------------------
st.title("Dashboard Data Indikator Pembangunan")

st.subheader("📄 Seluruh Data")
st.dataframe(df)
# ------------------------
# DETEKSI KOLOM TAHUN
# ------------------------
tahun_cols = [col for col in df.columns if isinstance(col, int)]

# Pastikan urut
tahun_cols = sorted(tahun_cols)

st.write("Kolom tahun terdeteksi:", tahun_cols)

# ------------------------
# BAGI MENJADI 3 VARIABEL
# ------------------------
pdrb_cols = tahun_cols[0:11]     # 2014-2024 PDRB
tpt_cols  = tahun_cols[11:22]    # 2014-2024 TPT
ipm_cols  = tahun_cols[22:33]    # 2014-2024 IPM

# ------------------------
# MELT MASING-MASING VARIABEL
# ------------------------
df_pdrb = df.melt(
    id_vars=['Provinsi'],
    value_vars=pdrb_cols,
    var_name='tahun',
    value_name='pdrb'
)

df_tpt = df.melt(
    id_vars=['Provinsi'],
    value_vars=tpt_cols,
    var_name='tahun',
    value_name='tpt'
)

df_ipm = df.melt(
    id_vars=['Provinsi'],
    value_vars=ipm_cols,
    var_name='tahun',
    value_name='ipm'
)

# ------------------------
# GABUNG SEMUA DATA
# ------------------------
df_all = df_pdrb.merge(df_tpt, on=['Provinsi','tahun'])
df_all = df_all.merge(df_ipm, on=['Provinsi','tahun'])

st.subheader("📊 Data Long Format")
st.dataframe(df_all)

# ------------------------
# FILTER PROVINSI
# ------------------------
provinsi_list = df['Provinsi'].unique()
prov_select = st.selectbox("Pilih Provinsi", provinsi_list)

df_selected = df_all[df_all['Provinsi'] == prov_select]

# ------------------------
# GRAFIK
# ------------------------
st.subheader(f"📈 Grafik Pembangunan - {prov_select}")

fig, ax = plt.subplots()
ax.plot(df_selected['tahun'], df_selected['pdrb'], label="PDRB (Miliar Rp)")
ax.set_xlabel("Tahun")
ax.set_ylabel("Nilai PDRB")
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(df_selected['tahun'], df_selected['tpt'], label="Tingkat Pengangguran Terbuka (%)")
ax.set_xlabel("Tahun")
ax.set_ylabel("TPT (%)")
ax.legend()
st.pyplot(fig)

fig, ax = plt.subplots()
ax.plot(df_selected['tahun'], df_selected['ipm'], label="Indeks Pembangunan Manusia")
ax.set_xlabel("Tahun")
ax.set_ylabel("IPM")
ax.legend()
st.pyplot(fig)

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
