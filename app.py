import streamlit as st
import pandas as pd

df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")

st.title("Dashboard Data Indikator Pembangunan")

# -------------------------
# 1. DEFINE TAHUN
# -------------------------
tahun_cols = [str(y) for y in range(2014, 2025)]

# -------------------------
# 2. SPLIT BLOK DATA
# -------------------------
# PDRB = kolom 1–11 (Provinsi + 2014–2024)
pdrb_cols = ['Provinsi'] + tahun_cols
df_pdrb = df[pdrb_cols].copy()
df_pdrb['indikator'] = 'PDRB ADHK 2010'

# TPT = kolom berikutnya
tpt_start = len(pdrb_cols)
tpt_cols = ['Provinsi'] + list(df.columns[tpt_start:tpt_start+len(tahun_cols)])
df_tpt = df[tpt_cols].copy()
df_tpt.columns = ['Provinsi'] + tahun_cols
df_tpt['indikator'] = 'Tingkat Pengangguran Terbuka'

# IPM = blok ketiga
ipm_start = tpt_start + len(tahun_cols)
ipm_cols = ['Provinsi'] + list(df.columns[ipm_start:ipm_start+len(tahun_cols)])
df_ipm = df[ipm_cols].copy()
df_ipm.columns = ['Provinsi'] + tahun_cols
df_ipm['indikator'] = 'Indeks Pembangunan Manusia'

# -------------------------
# 3. MELT SEMUA BLOK
# -------------------------
df_long_pdrb = df_pdrb.melt(
    id_vars=['Provinsi', 'indikator'],
    value_vars=tahun_cols,
    var_name='tahun',
    value_name='nilai'
)

df_long_tpt = df_tpt.melt(
    id_vars=['Provinsi', 'indikator'],
    value_vars=tahun_cols,
    var_name='tahun',
    value_name='nilai'
)

df_long_ipm = df_ipm.melt(
    id_vars=['Provinsi', 'indikator'],
    value_vars=tahun_cols,
    var_name='tahun',
    value_name='nilai'
)

# -------------------------
# 4. GABUNGKAN
# -------------------------
df_long = pd.concat([df_long_pdrb, df_long_tpt, df_long_ipm], ignore_index=True)

st.subheader("📄 Data Long Format")
st.dataframe(df_long)

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
