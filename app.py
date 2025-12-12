import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# (Tambahan) AGAR SEMUA DATA TAMPIL PENUH
# ========================================
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
# ========================================
# 1. BACA DATA
# ========================================
df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")

# ========================================
# 2. NORMALISASI NAMA KOLOM
# ========================================
df.columns = df.columns.str.strip()
df.rename(columns={"Provinsi": "provinsi"}, inplace=True)

# ========================================
# 3. TENTUKAN JUMLAH TAHUN (2014–2024 = 11 tahun)
# ========================================
tahun = ['2014','2015','2016','2017','2018','2019','2020','2021','2022','2023','2024']

# ========================================
# 4. IDENTIFIKASI KOLOM BERDASARKAN URUTAN
# ========================================
# Asumsi format:
# Provinsi | 11 kolom PDRB | 11 kolom TPT | 11 kolom IPM

pdrb_cols = tahun
tpt_cols = df.columns[1+11 : 1+11+11].tolist()
ipm_cols = df.columns[1+22 : 1+22+11].tolist()

df_pdrb = df[['provinsi'] + pdrb_cols]
df_tpt  = df[['provinsi'] + tpt_cols]
df_ipm  = df[['provinsi'] + ipm_cols]

# ========================================
# 5. UBAH KE LONG FORMAT
# ========================================
df_pdrb_long = df_pdrb.melt(id_vars='provinsi', var_name='tahun', value_name='pdrb')
df_tpt_long  = df_tpt.melt(id_vars='provinsi', var_name='tahun', value_name='tpt')
df_ipm_long  = df_ipm.melt(id_vars='provinsi', var_name='tahun', value_name='ipm')

# ========================================
# 6. GABUNG SEMUA INDIKATOR MENJADI SATU DATAFRAME
# ========================================
df_all = df_pdrb_long.merge(df_tpt_long, on=['provinsi','tahun'])
df_all = df_all.merge(df_ipm_long, on=['provinsi','tahun'])

# ========================================
# 7. GRAFIK UNTUK 34 PROVINSI
# ========================================

provinsi_list = df_all['provinsi'].unique()

for prov in provinsi_list:
    d = df_all[df_all['provinsi'] == prov]

    plt.figure(figsize=(12,7))
    plt.plot(d['tahun'], d['pdrb'], marker='o', label='PDRB')
    plt.plot(d['tahun'], d['tpt'], marker='o', label='Tingkat Pengangguran')
    plt.plot(d['tahun'], d['ipm'], marker='o', label='IPM')
    
    plt.title(f"Tren PDRB, Pengangguran, dan IPM – {prov}")
    plt.xlabel("Tahun")
    plt.ylabel("Nilai")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
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
