import streamlit as st

st.write(f"Streamlit Version: {st.__version__}")
try:
    st.write(f"st.context.url_path: '{st.context.url_path}'")
    st.write(f"st.context.cookies: {st.context.cookies}")
    st.write(f"st.context.headers: {st.context.headers.get('Host')}")
except Exception as e:
    st.write(f"Error accessing st.context: {e}")

st.write("---")
st.write("Query Params:")
st.write(st.query_params)
