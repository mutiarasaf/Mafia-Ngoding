import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Data Indikator Pembangunan")

# -----------------------------------------------------------
# 1. BACA DATASET SEKALI SAJA
# -----------------------------------------------------------
df = pd.read_csv(r"C:\Mafia-Ngoding\data\dataindikatorpembangunan.csv") st.write("📌 Daftar kolom di dataset:")
st.write(df.columns.tolist())

# Normalisasi kolom
df.columns = df.columns.str.lower().str.strip()

# -----------------------------------------------------------
# 2. TAMPILKAN SELURUH DATA (FULL, NO HEAD/TAIL)
# -----------------------------------------------------------
st.subheader("📄 Seluruh Data (Tanpa Dipotong)")
st.dataframe(df)

# -----------------------------------------------------------
# 3. CEK KATEGORI DATA
#    Jika format seperti Excel (tahun 2014–2024 jadi kolom)
# -----------------------------------------------------------
tahun_cols = [col for col in df.columns if col.isdigit()]

if not tahun_cols:
    st.error("Kolom tahun tidak ditemukan! Pastikan dataset memiliki kolom 2014–2024.")
else:
    tahun_cols = sorted(tahun_cols)

# -----------------------------------------------------------
# 4. UBAH DATASET KE BENTUK LONG AGAR MUDAH DIFILTER DAN DIGRAFIKKAN
# -----------------------------------------------------------
df_long = df.melt(
    id_vars=['Provinsi'],  # pake kolom yang benar
    var_name='Produk Domestik Bruto/Produk Domestik Regional Bruto Atas Dasar Harga Konstan 2010 (miliar rupiah) (Miliar Rp)', 'Data tingkat pengangguran di Indonesia (Per Agustus)', 'Indeks Pembangunan Manusia Menurut Provinsi',
    value_name='2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'
)


# Pastikan tahun menjadi angka
df_long["tahun"] = df_long["tahun"].astype(int)

# -----------------------------------------------------------
# 5. FILTER PROVINSI
# -----------------------------------------------------------
st.subheader("🔍 Pilih Provinsi")
provinsi_list = df_long["provinsi"].unique()
pilihan_provinsi = st.selectbox("Pilih Provinsi:", provinsi_list)

df_selected = df_long[df_long["provinsi"] == pilihan_provinsi]

st.write(f"### Data untuk Provinsi: *{pilihan_provinsi}*")
st.dataframe(df_selected)

# -----------------------------------------------------------
# 6. PILIH INDIKATOR
# -----------------------------------------------------------
st.subheader("📌 Pilih Indikator")
indikator_list = df_long["indikator"].unique()
pilihan_indikator = st.multiselect(
    "Pilih indikator:",
    indikator_list,
    default=[
        indikator_list[0]
    ]
)

df_plot = df_selected[df_selected["indikator"].isin(pilihan_indikator)]

# -----------------------------------------------------------
# 7. VISUALISASI BAR CHART
# -----------------------------------------------------------
st.subheader("📊 Visualisasi Bar Chart")

if df_plot.empty:
    st.warning("Tidak ada data untuk indikator yang dipilih.")
else:
    fig, ax = plt.subplots(figsize=(12, 5))

    for indikator in pilihan_indikator:
        subset = df_plot[df_plot["indikator"] == indikator]
        ax.bar(subset["tahun"], subset["nilai"], label=indikator)

    ax.set_title(f"Grafik Indikator untuk Provinsi {pilihan_provinsi}")
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Nilai")
    ax.legend()
    st.pyplot(fig)

# -----------------------------------------------------------
# 8. NAVIGASI HALAMAN
# -----------------------------------------------------------

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
