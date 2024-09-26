# © 2024 Numantic Solutions
# https://github.com/Numantic-NMoroney
# MIT License
#

import time
import streamlit as st
import matplotlib.pyplot as plt
import zipfile


if 'zip_idx' not in st.session_state:
    st.session_state.zip_idx = 20000

zips, xs, ys = [], [], []
grays, alphas, rgbas = [], [], []

# https://docs.streamlit.io/develop/concepts/architecture/caching
#
@st.cache_data
def load_data():
    name_zip = "us-48_zip_codes-lat_lon-1f.tsv.zip"
    with zipfile.ZipFile(name_zip) as archive :
        i = 0
        item = archive.read(name_zip[:-4])
        s = item.decode()
        lines = s.split("\n")
        for line in lines:
            ts = line.split()
            if (i != 0) and (len(ts) > 0):
                zips.append(ts[0])
                xs.append(float(ts[2]))
                ys.append(float(ts[1]))
                grays.append(float(ts[0])/110000)
                alphas.append(0.2)
            i += 1
    rgbas = list(zip(grays, grays, grays, alphas))
    return zips, xs, ys, rgbas

zips, xs, ys, rgbas = load_data()

st.subheader("Zip Highlighter")
st.text('Highlight a given range of US zip codes using the slider below.')

xc = list(xs)
yc = list(ys)
colors = list(rgbas)

max_idx = len(zips)
step = 250
n1 = int(st.session_state.zip_idx) - step
n2 = int(st.session_state.zip_idx) + step
if n1 < 0:
    n1 = 0
if n2 > (max_idx - 2):
    n2 = max_idx - 2
for i in range(n1,n2):
    colors.append([0.95, 0.55, 0.1, 0.8])   # 242, 140, 25  or  #F28C19
    xc.append(xs[i])
    yc.append(ys[i])

time.sleep(0.1)     # 0.25

col1, col2 = st.columns([0.7, 0.3])

plt.scatter(xc, yc, c=colors)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Contiguous US States')
plt.axis('equal')


with col1:
    st.pyplot(plt.gcf())

    zip_range = str(zips[n1]) + " - " + str(zips[n2])
    st.subheader("Zip Codes : " + zip_range)

    _ = st.slider("Index : ", 0, max_idx, 20000, key='zip_idx')

    st.markdown("[About](https://numanticsolutions.com/#ziphighlighter) — [comments/questions?](https://www.linkedin.com/feed/update/urn:li:share:7244909595695980544/?actorCompanyId=104756822")

