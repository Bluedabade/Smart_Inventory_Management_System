import streamlit as st
from modules.ui_helpers import init_app_state, save_all, render_nav_buttons

st.set_page_config(page_title="Undo", layout="wide")
init_app_state()

st.title("↩️ Undo การทำงานล่าสุด")

with st.sidebar:
    render_nav_buttons()

if st.button("Undo ล่าสุด", type="primary"):
    last_action = st.session_state.undo_stack.pop()

    if last_action is None:
        st.warning("ไม่มีประวัติให้ย้อนกลับ")
    else:
        action_type = last_action["action"]

        if action_type == "add":
            product_id = last_action["product"]["product_id"]
            for i, product in enumerate(st.session_state.products):
                if product["product_id"] == product_id:
                    st.session_state.products.pop(i)
                    break
            save_all()
            st.success("Undo การเพิ่มสินค้าเรียบร้อย")

        elif action_type == "delete":
            st.session_state.products.append(last_action["product"])
            save_all()
            st.success("Undo การลบสินค้าเรียบร้อย")

        elif action_type == "update":
            old_data = last_action["old_data"]
            for i, product in enumerate(st.session_state.products):
                if product["product_id"] == old_data["product_id"]:
                    st.session_state.products[i] = old_data
                    break
            save_all()
            st.success("Undo การแก้ไขสินค้าเรียบร้อย")