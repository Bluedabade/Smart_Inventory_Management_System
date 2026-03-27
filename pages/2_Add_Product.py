import streamlit as st
from modules.ui_helpers import init_app_state, save_all, render_nav_buttons
from modules.inventory_manager import add_product
from modules.category_tree import get_main_categories, get_sub_categories

st.set_page_config(page_title="เพิ่มสินค้า", layout="wide")
init_app_state()

st.title("➕ เพิ่มสินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products

main_categories = get_main_categories(products)

with st.form("add_product_form"):
    product_id = st.text_input("รหัสสินค้า")
    name = st.text_input("ชื่อสินค้า")
    price = st.number_input("ราคา", min_value=0.0, format="%.2f")
    quantity = st.number_input("จำนวนคงเหลือ", min_value=0, step=1)

    # เลือกหมวดหลัก
    if main_categories:
        main_options = main_categories + ["เพิ่มหมวดหลักใหม่"]
    else:
        main_options = ["เพิ่มหมวดหลักใหม่"]

    selected_main = st.selectbox("เลือกหมวดหลัก", main_options)

    if selected_main == "เพิ่มหมวดหลักใหม่":
        main_category = st.text_input("กรอกหมวดหลักใหม่")
        sub_options = []
        sub_category = st.text_input("กรอกหมวดย่อย")
    else:
        main_category = selected_main
        sub_categories = get_sub_categories(products, main_category)

        if sub_categories:
            sub_options = sub_categories + ["เพิ่มหมวดย่อยใหม่"]
        else:
            sub_options = ["เพิ่มหมวดย่อยใหม่"]

        selected_sub = st.selectbox("เลือกหมวดย่อย", sub_options)

        if selected_sub == "เพิ่มหมวดย่อยใหม่":
            sub_category = st.text_input("กรอกหมวดย่อยใหม่")
        else:
            sub_category = selected_sub

    submitted = st.form_submit_button("เพิ่มสินค้า")

if submitted:
    main_category = main_category.strip()
    sub_category = sub_category.strip()

    if not all([product_id.strip(), name.strip(), main_category, sub_category]):
        st.error("กรุณากรอกข้อมูลให้ครบ")
    else:
        category = f"{main_category}>{sub_category}"

        new_product = {
            "product_id": product_id.strip(),
            "name": name.strip(),
            "price": float(price),
            "quantity": int(quantity),
            "category": category
        }

        success, message = add_product(st.session_state.products, new_product)

        if success:
            st.session_state.undo_stack.push({
                "action": "add",
                "product": new_product
            })
            save_all()
            st.success(message)
        else:
            st.error(message)