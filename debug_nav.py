import streamlit as st

p1 = st.Page(lambda: st.write("Page 1"), title="Page 1", url_path="p1")
p2 = st.Page(lambda: st.write("Page 2"), title="Page 2", url_path="p2")

pg = st.navigation([p1, p2])

st.write(f"pg object: {pg}")
st.write(f"pg.title: {pg.title}")
st.write(f"pg.url_path: {pg.url_path}")

pg.run()
