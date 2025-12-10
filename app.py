import streamlit as st
import pandas as pd

st.title("Analisis Indikator Pembangunan 34 Provinsi (2014–2024)")

# ================================
# 1. LOAD DATA CSV
# ================================
df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv")


# ================================
# 2. RESHAPE: UBAH WIDE → LONG
# ================================
# Deteksi otomatis kolom PDRB / TPT / IPM berdasarkan prefix
pdrb_cols = [col for col in df.columns if col.isdigit() and int(col) >= 2014 and int(col) <= 2024]

# PDRB kolom ada 2014–2024 pertama → ambil 11 pertama
pdrb_cols = df.columns[1:12]

# TPT kolom 2014–2024 kedua → ambil 11 berikutnya
tpt_cols = df.columns[12:23]

# IPM kolom 2014–2024 ketiga → ambil 11 berikutnya
ipm_cols = df.columns[23:34]

# Convert ke long format
pdrb_long = df.melt(id_vars="Provinsi", value_vars=pdrb_cols,
                    var_name="Tahun", value_name="PDRB")

tpt_long = df.melt(id_vars="Provinsi", value_vars=tpt_cols,
                   var_name="Tahun", value_name="TPT")

ipm_long = df.melt(id_vars="Provinsi", value_vars=ipm_cols,
                   var_name="Tahun", value_name="IPM")

# Gabungkan semuanya
data_long = pdrb_long.merge(tpt_long, on=["Provinsi", "Tahun"])
data_long = data_long.merge(ipm_long, on=["Provinsi", "Tahun"])

# Pastikan Tahun numerik
data_long["Tahun"] = data_long["Tahun"].astype(int)

# ================================
# 3. FILTER USER INPUT
# ================================
provinsi_list = sorted(df["Provinsi"].dropna().astype(str).unique())

provinsi_dipilih = st.selectbox("Pilih Provinsi:", provinsi_list)

indikator = st.selectbox("Pilih Indikator:", ["PDRB", "TPT", "IPM"])

tahun_mulai, tahun_akhir = st.slider(
    "Pilih rentang tahun:", 2014, 2024, (2014, 2024)
)

# Filter data
df_filtered = data_long[
    (data_long["Provinsi"] == provinsi_dipilih) &
    (data_long["Tahun"] >= tahun_mulai) &
    (data_long["Tahun"] <= tahun_akhir)
][["Tahun", indikator]]

# ================================
# 4. TAMPILKAN DATA
# ================================
st.write(f"### Data {indikator} - {provinsi_dipilih}")
st.dataframe(df_filtered)

st.write("### Lima Data Pertama")
st.write(df_filtered.head())

st.write("### Lima Data Terakhir")
st.write(df_filtered.tail())

# ================================
# 5. GRAFIK
# ================================
st.write(f"### Grafik {indikator} ({provinsi_dipilih})")
st.line_chart(df_filtered.set_index("Tahun"))

st.title("Data Indikator Pembangunan")

# Kamus Provinsi

kamus_provinsi = {
    "AC" : 'Aceh',
    "SUMUT" : 'Sumatera Utara',
    "SB" : 'Sumatera Barat',
    "RI" : 'Riau',
    "JB" : 'Jambi',
    "SUMSEL" : 'Sumatera Selatan',
    "BKL" : 'Bengkulu',
    "LPG" : 'Lampung',
    "KEPBB" : 'Kepulauan Bangka Belitung',
    "KEPRI" : 'Kepulauan Riau',
    "DKJ" : 'DKI Jakarta',
    "JABAR" : 'Jawa Barat',
    "JATENG" : 'Jawa Tengah',
    "DIY" : 'DI Yogyakarta',
    "JATIM" : 'Jawa Timur',
    "BTN" : 'Banten',
    "BL" : 'Bali',
    "NTB" : 'Nusa Tenggara Barat',
    "NTT" : 'Nusa Tenggara Timur',
    "KALBAR" : 'Kalimantan Barat',
    "KALTE" : 'Kalimantan Tengah',
    "KALSEL" : 'Kalimantan Selatan',
    "KALTIM" : 'Kalimantan Timur',
    "KALUT" : 'Kalimatan Utara',
    "SULUT" : 'Sulawesi Utara', 
    "SULTE" : 'Sulawesi Tengah',
    "SULSEL" : 'Sulawesi Selatan',
    "SULTENG" : 'Sulawesi Tenggara',
    "GOR" : 'Gorontalo',
    "SULBAR" : 'Sulawesi Barat',
    "MAL" : 'Maluku',
    "MALUT" : 'Maluku Utara',
    "PABAR" : 'Papua Barat',
    "PA" : 'Papua'
}

st.title ("Data Indikator Pembangunan")

# PILIH PROVINSI MENGGUNAKAN SORTED ()
provinsi_dipilih = 'AC'
provinsi_dipilih = st.selectbox(
    'Silahkan pilih provinsi:',
    sorted( kamus_provinsi.keys() )
)

kode_provinsi = kamus_provinsi[provinsi_dipilih]

# Masukan tanggal

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
