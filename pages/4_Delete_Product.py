import streamlit as st
from modules.ui_helpers import init_app_state, save_all, display_products, render_nav_buttons
from modules.inventory_manager import delete_product
from modules.category_tree import get_main_categories, get_sub_categories

st.set_page_config(page_title="ลบสินค้า", layout="wide")
init_app_state()

st.title("🗑️ ลบสินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products

if "delete_search_results" not in st.session_state:
    st.session_state.delete_search_results = products.copy()

if "confirm_delete_id" not in st.session_state:
    st.session_state.confirm_delete_id = None


def filter_by_category(products, main_category=None, sub_category=None):
    result = []

    for product in products:
        parts = product["category"].split(">")
        product_main = parts[0].strip() if len(parts) > 0 else ""
        product_sub = parts[1].strip() if len(parts) > 1 else ""

        if main_category and main_category != "ทั้งหมด" and product_main != main_category:
            continue

        if sub_category and sub_category != "ทั้งหมด" and product_sub != sub_category:
            continue

        result.append(product)

    return result


def search_by_product_id(products, keyword):
    keyword = keyword.strip().lower()

    if not keyword:
        return products

    result = []
    for product in products:
        if keyword in product["product_id"].lower():
            result.append(product)

    return result


st.subheader("เลือกเงื่อนไขการค้นหา")

main_categories = get_main_categories(products)
main_options = ["ทั้งหมด"] + main_categories
selected_main_filter = st.selectbox("เลือกหมวดหลัก", main_options)

if selected_main_filter != "ทั้งหมด":
    sub_categories = get_sub_categories(products, selected_main_filter)
    sub_options = ["ทั้งหมด"] + sub_categories
else:
    sub_options = ["ทั้งหมด"]

selected_sub_filter = st.selectbox("เลือกหมวดย่อย", sub_options)
search_keyword = st.text_input("กรอกรหัสสินค้า")

if st.button("ยืนยันการค้นหา", type="primary"):
    filtered_products = filter_by_category(
        products,
        main_category=selected_main_filter,
        sub_category=selected_sub_filter
    )
    st.session_state.delete_search_results = search_by_product_id(filtered_products, search_keyword)
    st.session_state.confirm_delete_id = None

st.divider()

st.subheader("ผลลัพธ์สินค้า")
final_products = st.session_state.delete_search_results
display_products(final_products)

st.divider()

if final_products:
    product_options = [
        f"{p['product_id']} | {p['name']} | {p['category']}"
        for p in final_products
    ]

    selected_product_label = st.selectbox("เลือกสินค้าที่ต้องการลบ", product_options)
    selected_product_id = selected_product_label.split(" | ")[0]

    selected_product = None
    for product in final_products:
        if product["product_id"] == selected_product_id:
            selected_product = product
            break

    if selected_product:
        st.subheader("รายละเอียดสินค้า")
        st.dataframe([selected_product], use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("ลบสินค้า", type="primary"):
                st.session_state.confirm_delete_id = selected_product["product_id"]

        with col2:
            if st.session_state.confirm_delete_id == selected_product["product_id"]:
                if st.button("ยกเลิก", type="secondary"):
                    st.session_state.confirm_delete_id = None

        if st.session_state.confirm_delete_id == selected_product["product_id"]:
            st.warning(f"คุณแน่ใจหรือไม่ว่าต้องการลบสินค้า {selected_product['product_id']} - {selected_product['name']} ?")

            confirm_check = st.checkbox(
                "ฉันยืนยันว่าต้องการลบสินค้านี้",
                key=f"confirm_checkbox_{selected_product['product_id']}"
            )

            if st.button("ยืนยันการลบถาวร", type="primary", disabled=not confirm_check):
                success, message, deleted_product = delete_product(
                    st.session_state.products,
                    selected_product["product_id"]
                )

                if success:
                    st.session_state.undo_stack.push({
                        "action": "delete",
                        "product": deleted_product
                    })
                    save_all()
                    st.session_state.delete_search_results = st.session_state.products.copy()
                    st.session_state.confirm_delete_id = None
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
else:
    st.warning("ไม่พบสินค้าที่ตรงกับเงื่อนไข")