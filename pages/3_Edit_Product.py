import streamlit as st
from modules.ui_helpers import init_app_state, save_all, display_products, render_nav_buttons
from modules.inventory_manager import update_product
from modules.category_tree import get_main_categories, get_sub_categories

st.set_page_config(page_title="แก้ไขสินค้า", layout="wide")
init_app_state()

st.title("✏️ แก้ไขสินค้า")

with st.sidebar:
    render_nav_buttons()

products = st.session_state.products


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

if "edit_search_results" not in st.session_state:
    st.session_state.edit_search_results = products.copy()

if st.button("ยืนยันการค้นหา", type="primary"):
    filtered_products = filter_by_category(
        products,
        main_category=selected_main_filter,
        sub_category=selected_sub_filter
    )

    final_products = search_by_product_id(filtered_products, search_keyword)
    st.session_state.edit_search_results = final_products

st.divider()

st.subheader("ผลลัพธ์สินค้า")
final_products = st.session_state.edit_search_results
display_products(final_products)

st.divider()

if final_products:
    product_options = [
        f"{p['product_id']} | {p['name']} | {p['category']}"
        for p in final_products
    ]

    selected_product_label = st.selectbox("เลือกสินค้าที่ต้องการแก้ไข", product_options)

    selected_product = None
    selected_product_id = selected_product_label.split(" | ")[0]

    for product in final_products:
        if product["product_id"] == selected_product_id:
            selected_product = product
            break

    if selected_product:
        st.subheader("แก้ไขข้อมูลสินค้า")

        old_parts = selected_product["category"].split(">")
        old_main = old_parts[0].strip() if len(old_parts) > 0 else ""
        old_sub = old_parts[1].strip() if len(old_parts) > 1 else ""

        all_main_categories = get_main_categories(products)

        with st.form("edit_product_form"):
            new_name = st.text_input("ชื่อสินค้า", value=selected_product["name"])
            new_price = st.number_input(
                "ราคา",
                min_value=0.0,
                value=float(selected_product["price"]),
                format="%.2f"
            )
            new_quantity = st.number_input(
                "จำนวนคงเหลือ",
                min_value=0,
                value=int(selected_product["quantity"]),
                step=1
            )

            if old_main and old_main not in all_main_categories:
                all_main_categories.append(old_main)
                all_main_categories = sorted(all_main_categories)

            main_options_edit = all_main_categories + ["เพิ่มหมวดหลักใหม่"]

            default_main_index = 0
            if old_main in main_options_edit:
                default_main_index = main_options_edit.index(old_main)

            selected_main_edit = st.selectbox(
                "เลือกหมวดหลัก",
                main_options_edit,
                index=default_main_index
            )

            if selected_main_edit == "เพิ่มหมวดหลักใหม่":
                main_category_edit = st.text_input("กรอกหมวดหลักใหม่")
                sub_category_edit = st.text_input("กรอกหมวดย่อย")
            else:
                main_category_edit = selected_main_edit

                sub_categories_edit = get_sub_categories(products, main_category_edit)

                if old_sub and old_sub not in sub_categories_edit and main_category_edit == old_main:
                    sub_categories_edit.append(old_sub)
                    sub_categories_edit = sorted(sub_categories_edit)

                sub_options_edit = sub_categories_edit + ["เพิ่มหมวดย่อยใหม่"]

                default_sub_index = 0
                if old_sub in sub_options_edit:
                    default_sub_index = sub_options_edit.index(old_sub)

                selected_sub_edit = st.selectbox(
                    "เลือกหมวดย่อย",
                    sub_options_edit,
                    index=default_sub_index
                )

                if selected_sub_edit == "เพิ่มหมวดย่อยใหม่":
                    sub_category_edit = st.text_input("กรอกหมวดย่อยใหม่")
                else:
                    sub_category_edit = selected_sub_edit

            submitted = st.form_submit_button("บันทึกการแก้ไข")

        if submitted:
            main_category_edit = main_category_edit.strip()
            sub_category_edit = sub_category_edit.strip()

            if not all([new_name.strip(), main_category_edit, sub_category_edit]):
                st.error("กรุณากรอกข้อมูลให้ครบ")
            else:
                old_data = selected_product.copy()

                updated_data = {
                    "name": new_name.strip(),
                    "price": float(new_price),
                    "quantity": int(new_quantity),
                    "category": f"{main_category_edit}>{sub_category_edit}"
                }

                success, message = update_product(
                    st.session_state.products,
                    selected_product["product_id"],
                    updated_data
                )

                if success:
                    st.session_state.undo_stack.push({
                        "action": "update",
                        "old_data": old_data
                    })
                    save_all()
                    st.session_state.edit_search_results = st.session_state.products.copy()
                    st.success(message)
                else:
                    st.error(message)
else:
    st.warning("ไม่พบสินค้าที่ตรงกับเงื่อนไข")