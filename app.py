
import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import gdown
import os

st.set_page_config(layout="wide")
st.title("🌧️ Visualisasi Curah Hujan Bulanan (2011–2020) dari Google Drive")

# Input Google Drive file ID
file_id = st.text_input("🔗 Masukkan Google Drive File ID:", value="")

if file_id:
    filename = "data.nc"

    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        st.info("🔽 Mengunduh file dari Google Drive...")
        gdown.download(url, filename, quiet=False)
        st.success("✅ File berhasil diunduh!")

    if os.path.exists(filename):
        # Buka dataset tanpa decode waktu karena menggunakan kalender julian
        ds = xr.open_dataset(filename, decode_times=False)

        st.subheader("📋 Metadata")
        st.write("**Dimensi:**", ds.dims)
        st.write("**Koordinat:**", list(ds.coords))
        st.write("**Variabel:**", list(ds.data_vars))

        var_name = list(ds.data_vars)[0]
        var_data = ds[var_name]

        time_len = ds.dims["time"]
        time_index = st.slider("🗓️ Pilih indeks waktu (0–119):", 0, time_len - 1, 0)

        selected_slice = var_data.isel(time=time_index)

        st.subheader(f"🗺️ Peta Curah Hujan (indeks waktu: {time_index})")
        fig, ax = plt.subplots(figsize=(8, 4))
        selected_slice.plot(ax=ax, cmap="Blues", cbar_kwargs={'label': 'mm/bulan'})
        ax.set_title(f"Curah Hujan Bulanan (Indeks Waktu: {time_index})")
        st.pyplot(fig)

        st.subheader("📈 Grafik Waktu di Lokasi Tertentu")
        lat = st.number_input("Latitude (misalnya -6.5):", value=-6.5)
        lon = st.number_input("Longitude (misalnya 107.5):", value=107.5)

        lat_idx = np.abs(ds["lat"].values - lat).argmin()
        lon_idx = np.abs(ds["lon"].values - lon).argmin()

        time_series = var_data[:, lat_idx, lon_idx]
        st.write(f"Time series di lat={ds['lat'].values[lat_idx]}, lon={ds['lon'].values[lon_idx]}")

        fig2, ax2 = plt.subplots()
        ax2.plot(np.arange(time_len), time_series, marker="o")
        ax2.set_xlabel("Indeks Bulan (0–119)")
        ax2.set_ylabel("Curah Hujan (mm/bulan)")
        ax2.set_title("Time Series Curah Hujan")
        st.pyplot(fig2)
