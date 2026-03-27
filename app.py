import streamlit as st
from modules.file_manager import load_products, save_products
from modules.inventory_manager import (
    build_hash_table,
    add_product,
    update_product,
    delete_product,
    get_product_by_id_hash
)
from modules.search_manager import sequential_search_by_name, binary_search_by_id
from modules.sort_manager import insertion_sort, merge_sort
from modules.category_tree import build_category_tree, get_products_by_category, get_all_categories
from modules.undo_stack import UndoStack

FILE_PATH = "data/products.txt"


# session state เริ่มต้น
if "products" not in st.session_state:
    st.session_state.products = load_products(FILE_PATH)

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = UndoStack()


def save_all():
    save_products(FILE_PATH, st.session_state.products)


def display_products(products):
    if not products:
        st.warning("ไม่พบข้อมูลสินค้า")
        return

    st.table(products)


# UI
st.set_page_config(page_title="Smart Inventory", layout="wide")
st.title("📦 Smart Inventory Management System")

menu = st.sidebar.selectbox(
    "เลือกเมนู",
    [
        "แสดงสินค้าทั้งหมด",
        "เพิ่มสินค้า",
        "แก้ไขสินค้า",
        "ลบสินค้า",
        "ค้นหาสินค้า",
        "เรียงลำดับสินค้า",
        "หมวดหมู่สินค้า",
        "Undo"
    ]
)

products = st.session_state.products
product_table = build_hash_table(products)


# แสดงทั้งหมด
if menu == "แสดงสินค้าทั้งหมด":
    st.subheader("รายการสินค้าทั้งหมด")
    display_products(products)


# เพิ่มสินค้า
elif menu == "เพิ่มสินค้า":
    st.subheader("เพิ่มสินค้า")

    product_id = st.text_input("รหัสสินค้า")
    name = st.text_input("ชื่อสินค้า")
    price = st.number_input("ราคา", min_value=0.0, format="%.2f")
    quantity = st.number_input("จำนวนคงเหลือ", min_value=0, step=1)
    category = st.text_input("หมวดหมู่", placeholder="เช่น อาหาร>เครื่องดื่ม")

    if st.button("เพิ่มสินค้า"):
        new_product = {
            "product_id": product_id.strip(),
            "name": name.strip(),
            "price": float(price),
            "quantity": int(quantity),
            "category": category.strip()
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


# แก้ไขสินค้า
elif menu == "แก้ไขสินค้า":
    st.subheader("แก้ไขสินค้า")

    product_id = st.text_input("กรอกรหัสสินค้าที่ต้องการแก้ไข")

    if product_id:
        product = get_product_by_id_hash(product_table, product_id)

        if product:
            new_name = st.text_input("ชื่อสินค้า", value=product["name"])
            new_price = st.number_input("ราคา", min_value=0.0, value=float(product["price"]), format="%.2f")
            new_quantity = st.number_input("จำนวนคงเหลือ", min_value=0, value=int(product["quantity"]), step=1)
            new_category = st.text_input("หมวดหมู่", value=product["category"])

            if st.button("บันทึกการแก้ไข"):
                old_data = product.copy()

                updated_data = {
                    "name": new_name.strip(),
                    "price": float(new_price),
                    "quantity": int(new_quantity),
                    "category": new_category.strip()
                }

                success, message = update_product(st.session_state.products, product_id, updated_data)

                if success:
                    st.session_state.undo_stack.push({
                        "action": "update",
                        "old_data": old_data
                    })
                    save_all()
                    st.success(message)
                else:
                    st.error(message)
        else:
            st.error("ไม่พบรหัสสินค้า")


# ลบสินค้า
elif menu == "ลบสินค้า":
    st.subheader("ลบสินค้า")

    product_id = st.text_input("กรอกรหัสสินค้าที่ต้องการลบ")

    if st.button("ลบสินค้า"):
        success, message, deleted_product = delete_product(st.session_state.products, product_id)

        if success:
            st.session_state.undo_stack.push({
                "action": "delete",
                "product": deleted_product
            })
            save_all()
            st.success(message)
        else:
            st.error(message)


# ค้นหา
elif menu == "ค้นหาสินค้า":
    st.subheader("ค้นหาสินค้า")

    search_type = st.radio("เลือกประเภทการค้นหา", ["ค้นหาด้วยชื่อ (Sequential Search)", "ค้นหาด้วยรหัส (Binary Search)"])

    if search_type == "ค้นหาด้วยชื่อ (Sequential Search)":
        keyword = st.text_input("กรอกชื่อสินค้าที่ต้องการค้นหา")
        if st.button("ค้นหา"):
            result = sequential_search_by_name(products, keyword)
            display_products(result)

    else:
        product_id = st.text_input("กรอกรหัสสินค้าที่ต้องการค้นหา")
        if st.button("ค้นหา"):
            sorted_products = sorted(products, key=lambda x: x["product_id"])
            result = binary_search_by_id(sorted_products, product_id)

            if result:
                display_products([result])
            else:
                st.warning("ไม่พบสินค้า")


# เรียงลำดับ
elif menu == "เรียงลำดับสินค้า":
    st.subheader("เรียงลำดับสินค้า")

    sort_field = st.selectbox("เลือกข้อมูลที่ต้องการเรียง", ["price", "quantity"])
    sort_method = st.radio("เลือกอัลกอริทึม", ["Insertion Sort", "Merge Sort"])

    if st.button("เรียงลำดับ"):
        if sort_method == "Insertion Sort":
            sorted_products = insertion_sort(products, sort_field)
        else:
            sorted_products = merge_sort(products, sort_field)

        display_products(sorted_products)


# 7 หมวดหมู่
elif menu == "หมวดหมู่สินค้า":
    st.subheader("หมวดหมู่สินค้าแบบ Tree")

    tree = build_category_tree(products)
    categories = get_all_categories(products)

    st.write("โครงสร้างหมวดหมู่")
    st.json(tree)

    selected_category = st.selectbox("เลือกหมวดหมู่", categories)

    if st.button("แสดงสินค้าในหมวดหมู่"):
        result = get_products_by_category(products, selected_category)
        display_products(result)


# 8) Undo
elif menu == "Undo":
    st.subheader("ย้อนกลับการทำงานล่าสุด")

    if st.button("Undo ล่าสุด"):
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