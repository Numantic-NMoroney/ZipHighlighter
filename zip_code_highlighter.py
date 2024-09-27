# © 2024 Numantic Solutions
# https://github.com/Numantic-NMoroney
# MIT License
#

import time
from bisect import bisect_left
import streamlit as st
import matplotlib.pyplot as plt
import zipfile

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
                zips.append(int(ts[0]))
                # zips.append(ts[0])
                xs.append(float(ts[2]))
                ys.append(float(ts[1]))
                grays.append(float(ts[0])/110000)
                alphas.append(0.2)
            i += 1
    rgbas = list(zip(grays, grays, grays, alphas))
    return zips, xs, ys, rgbas

zips, xs, ys, rgbas = load_data()

max_idx = len(zips)
half_idx = int(max_idx / 2)

# https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value/12141511#12141511
#
def closest_index(list_, value):
    idx = bisect_left(list_, value)
    if idx == 0:
        return 0
    if idx == len(list_):
        return -1
    before = list_[idx - 1]
    after = list_[idx]
    if after - value < value - before:
        return idx
    else:
        return idx - 1

if 'current_zip' not in st.session_state:
    st.session_state.current_zip = zips[half_idx]

st.subheader("Zip Highlighter")
st.text('Highlight a given range of US zip codes using the slider below.')

xc, yc, colors = list(xs), list(ys), list(rgbas)

step = 250
zip_idx = closest_index(zips, int(st.session_state.current_zip))
n1 = int(zip_idx) - step
n2 = int(zip_idx) + step
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

    _ = st.slider("Current Zip : ", 
                  zips[0], zips[-1], zips[half_idx], 
                  key='current_zip', label_visibility="hidden")

    st.markdown("[About](https://numanticsolutions.com/#ziphighlighter) — [Source](https://github.com/Numantic-NMoroney/ZipHighlighter) — [Comments/Questions?](https://www.linkedin.com/feed/update/urn:li:share:7244909595695980544/?actorCompanyId=104756822)")

