import streamlit as st
from modules.ui_helpers import init_app_state, display_products, render_nav_buttons
from modules.category_tree import get_main_categories, get_sub_categories
from modules.sort_manager import insertion_sort, merge_sort

st.set_page_config(page_title="ค้นหาสินค้า", layout="wide")
init_app_state()

st.title("🔍 ค้นหาและเรียงลำดับสินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products

if "search_results" not in st.session_state:
    st.session_state.search_results = products.copy()


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


def search_products(products, keyword, search_type):
    keyword = keyword.strip().lower()

    if not keyword:
        return products

    result = []

    for product in products:
        if search_type == "รหัสสินค้า":
            if keyword in product["product_id"].lower():
                result.append(product)
        elif search_type == "ชื่อสินค้า":
            if keyword in product["name"].lower():
                result.append(product)

    return result


st.subheader("เงื่อนไขการค้นหา")

main_categories = get_main_categories(products)
main_options = ["ทั้งหมด"] + main_categories

with st.form("search_form"):
    selected_main_filter = st.selectbox("เลือกหมวดหลัก", main_options)

    if selected_main_filter != "ทั้งหมด":
        sub_categories = get_sub_categories(products, selected_main_filter)
        sub_options = ["ทั้งหมด"] + sub_categories
    else:
        sub_options = ["ทั้งหมด"]

    selected_sub_filter = st.selectbox("เลือกหมวดย่อย", sub_options)

    search_type = st.radio(
        "ค้นหาจาก",
        ["รหัสสินค้า", "ชื่อสินค้า"],
        horizontal=True
    )

    search_keyword = st.text_input("กรอกคำค้นหา", placeholder="เช่น P001 หรือ น้ำดื่ม")

    col1, col2 = st.columns(2)
    search_submitted = col1.form_submit_button("ค้นหา", use_container_width=True)
    reset_submitted = col2.form_submit_button("ล้างเงื่อนไข", use_container_width=True)

if search_submitted:
    filtered_products = filter_by_category(
        products,
        main_category=selected_main_filter,
        sub_category=selected_sub_filter
    )

    final_products = search_products(filtered_products, search_keyword, search_type)
    st.session_state.search_results = final_products

if reset_submitted:
    st.session_state.search_results = products.copy()
    st.rerun()

st.divider()

st.subheader("เรียงลำดับผลลัพธ์")

result_products = st.session_state.search_results.copy()

sort_field = st.selectbox(
    "เลือกเงื่อนไขการเรียง",
    ["ไม่เรียง", "price", "quantity"],
    format_func=lambda x: {
        "ไม่เรียง": "ไม่เรียง",
        "price": "ราคา",
        "quantity": "จำนวนคงเหลือ"
    }[x]
)

sort_order = st.radio(
    "ลำดับการเรียง",
    ["น้อยไปมาก", "มากไปน้อย"],
    horizontal=True
)

if sort_field != "ไม่เรียง":
    if len(result_products) <= 10:
        sorted_products = insertion_sort(result_products, sort_field)
    else:
        sorted_products = merge_sort(result_products, sort_field)

    if sort_order == "มากไปน้อย":
        sorted_products.reverse()

    result_products = sorted_products

st.divider()

st.subheader("ผลลัพธ์การค้นหา")
display_products(result_products)