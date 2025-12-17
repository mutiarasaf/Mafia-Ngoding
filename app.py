import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Dashboard Indikator Pembangunan",
    layout="wide"
)

st.title("📊 Dashboard Indikator Pembangunan Provinsi")
st.caption("PDRB, Tingkat Pengangguran Terbuka (TPT), dan Indeks Pembangunan Manusia (IPM)")

# =====================================
# UPLOAD DATA (CSV / EXCEL)
# =====================================
uploaded_file = st.file_uploader(
    "Upload data indikator pembangunan (CSV / Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is None:
    st.warning("Silakan upload file data terlebih dahulu")
    st.stop()

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

df = load_data(uploaded_file)

# =====================================
# TRANSFORM WIDE → LONG
# =====================================
data = df.melt(
    id_vars=["Provinsi"],
    var_name="Variabel",
    value_name="Nilai"
)

data["Indikator"] = data["Variabel"].str.extract(r"(PDRB|TPT|IPM)")
data["Tahun"] = data["Variabel"].str.extract(r"(\d{4})").astype(int)
data = data.dropna()

# =====================================
# SIDEBAR FILTER
# =====================================
st.sidebar.header("🔎 Filter Data")

provinsi = st.sidebar.multiselect(
    "Pilih Provinsi",
    options=sorted(data["Provinsi"].unique()),
    default=sorted(data["Provinsi"].unique())[:6]
)

tahun = st.sidebar.slider(
    "Rentang Tahun",
    int(data["Tahun"].min()),
    int(data["Tahun"].max()),
    (2018, int(data["Tahun"].max()))
)

df_filt = data[
    (data["Provinsi"].isin(provinsi)) &
    (data["Tahun"].between(tahun[0], tahun[1]))
]

# =====================================
# FUNCTION ANALISIS OTOMATIS
# =====================================
def analisis_otomatis(df, indikator):
    df_i = df[df["Indikator"] == indikator]

    awal = df_i["Tahun"].min()
    akhir = df_i["Tahun"].max()

    mean_growth = (
        df_i.groupby("Provinsi")
        .apply(lambda x: x.sort_values("Tahun")["Nilai"].pct_change().mean() * 100)
        .mean()
    )

    df_last = df_i[df_i["Tahun"] == akhir]
    tertinggi = df_last.loc[df_last["Nilai"].idxmax()]
    terendah = df_last.loc[df_last["Nilai"].idxmin()]

    return f"""
    Berdasarkan data tahun {awal}–{akhir}, indikator **{indikator}**
    menunjukkan rata-rata pertumbuhan tahunan sekitar **{mean_growth:.2f}%**.
    Pada tahun {akhir}, nilai tertinggi dicapai oleh **{tertinggi['Provinsi']}**
    dengan nilai **{tertinggi['Nilai']:.2f}**, sedangkan nilai terendah
    tercatat di **{terendah['Provinsi']}** sebesar **{terendah['Nilai']:.2f}**.
    """

# =====================================
# FUNCTION VIEW PER INDIKATOR
# =====================================
def indikator_view(indikator, judul):
    df_i = df_filt[df_filt["Indikator"] == indikator]

    if df_i.empty:
        st.warning("Data tidak tersedia untuk filter yang dipilih")
        return

    # KPI
    c1, c2, c3 = st.columns(3)
    c1.metric("Rata-rata", f"{df_i['Nilai'].mean():,.2f}")
    c2.metric("Tertinggi", f"{df_i['Nilai'].max():,.2f}")
    c3.metric("Terendah", f"{df_i['Nilai'].min():,.2f}")

    # Narasi
    st.markdown("### 📝 Analisis Otomatis")
    st.write(analisis_otomatis(df_filt, indikator))

    # Tren waktu
    st.markdown("### 📈 Tren Waktu")
    fig_line = px.line(
        df_i,
        x="Tahun",
        y="Nilai",
        color="Provinsi",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # Ranking
    st.markdown("### 🏆 Ranking Provinsi (Tahun Terakhir)")
    tahun_akhir = df_i["Tahun"].max()
    ranking = (
        df_i[df_i["Tahun"] == tahun_akhir]
        .sort_values("Nilai", ascending=False)
        .reset_index(drop=True)
    )
    ranking["Peringkat"] = ranking.index + 1

    st.dataframe(
        ranking[["Peringkat", "Provinsi", "Nilai"]],
        use_container_width=True
    )

    # Growth
    st.markdown("### 📈 Laju Pertumbuhan Tahunan (%)")
    df_i = df_i.sort_values(["Provinsi", "Tahun"])
    df_i["Growth (%)"] = df_i.groupby("Provinsi")["Nilai"].pct_change() * 100

    st.dataframe(
        df_i[["Provinsi", "Tahun", "Nilai", "Growth (%)"]],
        use_container_width=True
    )

# =====================================
# TABS
# =====================================
tab1, tab2, tab3 = st.tabs(["📈 PDRB", "👷 TPT", "🎓 IPM"])

with tab1:
    indikator_view("PDRB", "Produk Domestik Regional Bruto")

with tab2:
    indikator_view("TPT", "Tingkat Pengangguran Terbuka")

with tab3:
    indikator_view("IPM", "Indeks Pembangunan Manusia")