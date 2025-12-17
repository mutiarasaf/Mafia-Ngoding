import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Indikator Pembangunan", layout="wide")

st.title("📊 Analisis Indikator Pembangunan 34 Provinsi (2014–2024)")

# ================================
# 1. LOAD DATA
# ================================
df = pd.read_csv("C:/Mafia-Ngoding/data/data-indikator-pembangunan.csv")

st.subheader("📄 Data Mentah (CSV)")
st.dataframe(df, use_container_width=True)

# ================================
# 2. RESHAPE DATA (WIDE → LONG)
# ================================
pdrb_cols = df.columns[1:12]
tpt_cols  = df.columns[12:23]
ipm_cols  = df.columns[23:34]

pdrb_long = df.melt(
    id_vars="Provinsi",
    value_vars=pdrb_cols,
    var_name="Tahun",
    value_name="PDRB"
)

tpt_long = df.melt(
    id_vars="Provinsi",
    value_vars=tpt_cols,
    var_name="Tahun",
    value_name="TPT"
)

ipm_long = df.melt(
    id_vars="Provinsi",
    value_vars=ipm_cols,
    var_name="Tahun",
    value_name="IPM"
)

data_long = (
    pdrb_long
    .merge(tpt_long, on=["Provinsi", "Tahun"])
    .merge(ipm_long, on=["Provinsi", "Tahun"])
)

data_long["Tahun"] = data_long["Tahun"].astype(int)

# ================================
# 3. FILTER INPUT USER
# ================================
st.sidebar.header("🔍 Filter Data")

provinsi = st.sidebar.selectbox(
    "Pilih Provinsi:",
    sorted(data_long["Provinsi"].unique())
)

indikator = st.sidebar.selectbox(
    "Pilih Indikator:",
    ["PDRB", "TPT", "IPM"]
)

tahun_range = st.sidebar.slider(
    "Pilih Rentang Tahun:",
    2014, 2024, (2014, 2024)
)

# ================================
# 4. FILTER DATA SESUAI INPUT
# ================================
df_filtered = data_long[
    (data_long["Provinsi"] == provinsi) &
    (data_long["Tahun"] >= tahun_range[0]) &
    (data_long["Tahun"] <= tahun_range[1])
][["Tahun", indikator]].sort_values("Tahun")

# ================================
# 5. TAMPILKAN DATA
# ================================
st.subheader(f"📌 Data {indikator} – {provinsi}")
st.dataframe(df_filtered, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.write("### Lima Data Pertama")
    st.dataframe(df_filtered.head())

with col2:
    st.write("### Lima Data Terakhir")
    st.dataframe(df_filtered.tail())

# ================================
# 6. VISUALISASI GRAFIK
# ================================
st.subheader(f"📈 Grafik {indikator} ({provinsi})")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    df_filtered["Tahun"],
    df_filtered[indikator],
    marker="o"
)

ax.set_xlabel("Tahun")
ax.set_ylabel(indikator)
ax.set_title(f"{indikator} Provinsi {provinsi} ({tahun_range[0]}–{tahun_range[1]})")
ax.grid(True)

st.pyplot(fig)
