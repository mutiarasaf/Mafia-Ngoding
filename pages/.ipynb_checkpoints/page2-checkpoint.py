import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("Data Visualization")

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)
# Plot data
# fig, ax = plt.subplots()
# ax.plot(x, y)
# Display the plot
# st.pyplot(fig)

df = pd.read_csv("data/dataindikatorpembangunan.csv")

st.write(df.head(10))
st.write(df.tail())
