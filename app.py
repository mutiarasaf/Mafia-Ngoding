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
    else:
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
# TAB 1 – PENDAHULUAN
# =====================================================
with tab1:
    st.markdown("""
### *Pendahuluan*

Pembangunan ekonomi dan sosial di Indonesia merupakan isu krusial yang mencerminkan
kemajuan suatu negara dalam meningkatkan kesejahteraan masyarakatnya.
Indonesia sebagai negara kepulauan dengan 34 provinsi menunjukkan disparitas regional
yang signifikan dalam pertumbuhan ekonomi, kesempatan kerja, dan kualitas hidup manusia.

Analisis ini berfokus pada tiga indikator utama:
- **PDRB harga konstan**
- **Tingkat Pengangguran Terbuka (TPT)**
- **Indeks Pembangunan Manusia (IPM)**

Aplikasi ini memungkinkan eksplorasi interaktif data periode **2014–2024**
untuk mendukung kebijakan publik, investasi, dan penelitian menuju
**Indonesia Emas 2045**.
    """)

    st.markdown("""
### *Deskripsi Data*

- **Provinsi**: 34 provinsi Indonesia  
- **PDRB (Harga Konstan)**: Mengukur pertumbuhan ekonomi riil  
- **TPT**: Indikator kesehatan pasar tenaga kerja  
- **IPM**: Indikator komposit pembangunan manusia  

Sumber data: **BPS (diolah)**  
    """)

# =====================================================
# FUNCTION ANALISIS OTOMATIS PER PROVINSI
# =====================================================
def analisis_provinsi(df, indikator):
    hasil = []
    for p in df["Provinsi"].unique():
        d = df[(df["Provinsi"] == p) & (df["Indikator"] == indikator)]
        if len(d) < 2:
            continue

        awal, akhir = d["Tahun"].min(), d["Tahun"].max()
        growth = d.sort_values("Tahun")["Nilai"].pct_change().mean() * 100

        hasil.append({
            "Provinsi": p,
            "Periode": f"{awal}-{akhir}",
            "Rata-rata": d["Nilai"].mean(),
            "Growth (%)": growth
        })
    return pd.DataFrame(hasil)

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
        x="Provinsi", y="Nilai"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =====================================================
# TAB 3 – ANALISIS PER PROVINSI (RINCI)
# =====================================================
with tab3:
    indikator = st.selectbox(
        "Pilih indikator untuk analisis provinsi",
        ["PDRB", "TPT", "IPM"],
        key="prov"
    )

def analisis_provinsi(df, indikator):
    hasil = []

    for provinsi, d in df.groupby("Provinsi"):
        d = d.copy()

        # PASTIKAN numerik
        d["Nilai"] = pd.to_numeric(d["Nilai"], errors="coerce")

        growth = (
            d.sort_values("Tahun")["Nilai"]
             .pct_change()
             .mean() * 100
        )

        hasil.append({
            "Provinsi": provinsi,
            "Rata-rata Pertumbuhan (%)": growth
        })

    return pd.DataFrame(hasil)

    st.markdown("""
**Interpretasi:**
- Nilai rata-rata menunjukkan posisi relatif provinsi
- Growth (%) menunjukkan dinamika pembangunan
- Provinsi dengan growth tinggi tetapi level rendah perlu perhatian khusus
    """)

# =====================================================
# TAB 4 – HEATMAP & DATA KESELURUHAN
# =====================================================
with tab4:
    st.subheader("📊 Heatmap Antar Indikator")

df_filt["Nilai"] = (
    df_filt["Nilai"]
    .astype(str)
    .str.replace(",", "", regex=False)   # hapus koma ribuan
)

df_filt["Nilai"] = pd.to_numeric(df_filt["Nilai"], errors="coerce")

    fig_heat = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="RdBu"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("📄 Tabel Keseluruhan Data")
    st.dataframe(df_filt, use_container_width=True)