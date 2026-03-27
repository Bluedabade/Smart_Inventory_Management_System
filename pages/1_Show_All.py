import streamlit as st
from modules.ui_helpers import init_app_state, display_products, render_nav_buttons

st.set_page_config(page_title="แสดงสินค้าทั้งหมด", layout="wide")
init_app_state()

st.title("📋 แสดงสินค้าทั้งหมด")

with st.sidebar:
    render_nav_buttons()

display_products(st.session_state.products)