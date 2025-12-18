import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Dashboard Pembangunan Indonesia",
    layout="wide"
)

st.title("📊 Dashboard Pembangunan Ekonomi & Sosial Indonesia")
st.caption("Analisis PDRB, TPT, dan IPM Provinsi Indonesia 2014–2024")

# =====================================================
# UPLOAD DATA
# =====================================================
uploaded_file = st.file_uploader(
    "Upload data (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.stop()

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file)

df = load_data(uploaded_file)

# =====================================================
# TRANSFORM DATA (WIDE → LONG)
# =====================================================
data = df.melt(
    id_vars=["Provinsi"],
    var_name="Variabel",
    value_name="Nilai"
)

data["Indikator"] = data["Variabel"].str.extract(r"(PDRB|TPT|IPM)")
data["Tahun"] = data["Variabel"].str.extract(r"(\d{4})").astype(int)
data = data.dropna()

data["Nilai"] = (
    data["Nilai"]
    .astype(str)
    .str.replace(",", "", regex=False)
)
data["Nilai"] = pd.to_numeric(data["Nilai"], errors="coerce")

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.header("🔎 Filter")

provinsi_filter = st.sidebar.multiselect(
    "Pilih Provinsi",
    sorted(data["Provinsi"].unique()),
    default=sorted(data["Provinsi"].unique())
)

tahun_filter = st.sidebar.slider(
    "Rentang Tahun",
    int(data["Tahun"].min()),
    int(data["Tahun"].max()),
    (2014, int(data["Tahun"].max()))
)

df_filt = data[
    (data["Provinsi"].isin(provinsi_filter)) &
    (data["Tahun"].between(tahun_filter[0], tahun_filter[1]))
]

# =====================================================
# TAB UTAMA
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Pendahuluan",
    "📈 Analisis Indikator",
    "🧠 Analisis Per Provinsi",
    "📊 Heatmap & Data Lengkap"
])

# =====================================================
# TAB 1 – PENDAHULUAN & DESKRIPSI DATA
# =====================================================
with tab1:
    st.markdown("""
### *Pendahuluan*

Pembangunan ekonomi dan sosial di Indonesia merupakan isu krusial yang mencerminkan
kemajuan suatu negara dalam meningkatkan kesejahteraan masyarakatnya.
Indonesia sebagai negara kepulauan dengan 34 provinsi menunjukkan adanya
disparitas regional dalam pertumbuhan ekonomi, kesempatan kerja,
dan kualitas hidup manusia.

Analisis ini berfokus pada tiga indikator utama:
- **PDRB harga konstan**
- **Tingkat Pengangguran Terbuka (TPT)**
- **Indeks Pembangunan Manusia (IPM)**

Periode analisis mencakup tahun **2014–2024**.
    """)

    st.markdown("""
### *Deskripsi Data*

- **Provinsi**: 34 provinsi Indonesia  
- **PDRB (Harga Konstan)**: Indikator pertumbuhan ekonomi riil  
- **TPT**: Indikator ketenagakerjaan  
- **IPM**: Indikator pembangunan manusia  

Sumber data: **BPS (diolah)**
    """)

# =====================================================
# TAB 2 – ANALISIS INDIKATOR
# =====================================================
with tab2:
    indikator = st.selectbox("Pilih Indikator", ["PDRB", "TPT", "IPM"])
    df_i = df_filt[df_filt["Indikator"] == indikator]

    st.subheader("📈 Tren Waktu")
    fig = px.line(df_i, x="Tahun", y="Nilai", color="Provinsi")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Distribusi Tahun Terakhir")
    tahun_akhir = df_i["Tahun"].max()

    fig2 = px.bar(
        df_i[df_i["Tahun"] == tahun_akhir],
        x="Provinsi",
        y="Nilai"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ================= INTERPRETASI =================
    st.markdown("""
### 📝 Interpretasi Hasil Analisis

Berdasarkan data tahun terakhir, PDRB tertinggi masih didominasi oleh provinsi di Pulau Jawa, 
yaitu DKI Jakarta (±2.151.041), Jawa Timur (±1.935.810), dan Jawa Barat (±1.752.071), 
yang juga terlihat jelas pada grafik Distribusi Tahun Terakhir dan tren peningkatan yang stabil 
pada grafik Tren Waktu. Sebaliknya, PDRB terendah tercatat di Papua (±24.874), Gorontalo (±32.950), 
dan Sulawesi Barat (±37.088).

Dari sisi ketenagakerjaan, TPT tertinggi justru terdapat di provinsi dengan ekonomi besar 
seperti Jawa Barat (6,75%), Banten (6,68%), dan DKI Jakarta (6,21%), sedangkan TPT terendah 
berada di Sulawesi Barat (2,68%) dan NTB (2,73%).

Sementara itu, IPM tertinggi dicapai oleh DKI Jakarta (83,08) dan DI Yogyakarta (81,55), 
sedangkan IPM terendah masih berada di Papua Barat (67,02) dan NTT (67,39).

Temuan ini menunjukkan bahwa pertumbuhan ekonomi yang tinggi belum sepenuhnya diikuti oleh 
pemerataan kesempatan kerja dan kualitas pembangunan manusia, sehingga ketimpangan antarwilayah 
masih bersifat struktural.
    """)

# =====================================================
# FUNCTION ANALISIS PROVINSI
# =====================================================
def analisis_provinsi(df, indikator):
    hasil = []

    for provinsi, d in df[df["Indikator"] == indikator].groupby("Provinsi"):
        if len(d) < 2:
            continue

        growth = (
            d.sort_values("Tahun")["Nilai"]
             .pct_change()
             .mean() * 100
        )

        hasil.append({
            "Provinsi": provinsi,
            "Rata-rata Nilai": d["Nilai"].mean(),
            "Rata-rata Growth (%)": growth
        })

    return pd.DataFrame(hasil)

# =====================================================
# TAB 3 – ANALISIS PER PROVINSI
# =====================================================
with tab3:
    indikator_p = st.selectbox(
        "Pilih indikator untuk analisis provinsi",
        ["PDRB", "TPT", "IPM"],
        key="prov"
    )

    hasil_prov = analisis_provinsi(df_filt, indikator_p)
    st.dataframe(hasil_prov, use_container_width=True)

# =====================================================
# TAB 4 – HEATMAP & DATA KESELURUHAN
# =====================================================
with tab4:
    st.subheader("📊 Heatmap Antar Provinsi dan Tahun")

    pivot = df_filt.pivot_table(
        index="Provinsi",
        columns="Tahun",
        values="Nilai",
        aggfunc="mean"
    )

    fig_heat = px.imshow(
        pivot,
        aspect="auto",
        text_auto=True
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("📄 Tabel Keseluruhan Data")
    st.dataframe(df_filt, use_container_width=True)
