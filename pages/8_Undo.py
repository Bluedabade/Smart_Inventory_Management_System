import streamlit as st
from modules.ui_helpers import init_app_state, save_all, render_nav_buttons

st.set_page_config(page_title="Undo", layout="wide")
init_app_state()

st.title("↩️ ประวัติการทำงานและย้อนกลับ")

with st.sidebar:
    render_nav_buttons()


def get_action_description(action):
    action_type = action.get("action", "")

    if action_type == "add":
        product = action.get("product", {})
        return f"เพิ่มสินค้า: {product.get('product_id', '')} - {product.get('name', '')}"

    elif action_type == "delete":
        product = action.get("product", {})
        return f"ลบสินค้า: {product.get('product_id', '')} - {product.get('name', '')}"

    elif action_type == "update":
        old_data = action.get("old_data", {})
        return f"แก้ไขสินค้า: {old_data.get('product_id', '')} - {old_data.get('name', '')}"

    elif action_type == "add_category":
        return f"เพิ่มหมวดหมู่: {action.get('category', '')}"

    elif action_type == "update_category":
        return f"แก้ไขหมวดหมู่: {action.get('old_category', '')} → {action.get('new_category', '')}"

    elif action_type == "delete_category":
        return f"ลบหมวดหมู่: {action.get('category', '')}"

    return "รายการไม่ทราบประเภท"


history = st.session_state.undo_stack.get_all()

st.subheader("ประวัติการทำงาน")

if history:
    history_data = []

    # แสดงจากล่าสุด -> เก่าสุด
    for i, action in enumerate(reversed(history), start=1):
        history_data.append({
            "ลำดับ": i,
            "เวลา": action.get("timestamp", "-"),
            "รายการ": get_action_description(action)
        })

    st.dataframe(history_data, use_container_width=True)

    st.divider()

    latest_action = st.session_state.undo_stack.peek()

    if latest_action:
        st.subheader("รายการล่าสุดที่สามารถย้อนกลับได้")
        st.info(get_action_description(latest_action))

        confirm_undo = st.checkbox("ฉันยืนยันว่าต้องการย้อนกลับรายการล่าสุด")

        if st.button("Undo ล่าสุด", type="primary", disabled=not confirm_undo):
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
                    st.rerun()

                elif action_type == "delete":
                    st.session_state.products.append(last_action["product"])
                    save_all()
                    st.success("Undo การลบสินค้าเรียบร้อย")
                    st.rerun()

                elif action_type == "update":
                    old_data = last_action["old_data"]
                    for i, product in enumerate(st.session_state.products):
                        if product["product_id"] == old_data["product_id"]:
                            st.session_state.products[i] = old_data
                            break
                    save_all()
                    st.success("Undo การแก้ไขสินค้าเรียบร้อย")
                    st.rerun()

                elif action_type == "add_category":
                    category = last_action["category"]
                    if category in st.session_state.categories:
                        st.session_state.categories.remove(category)
                    save_all()
                    st.success("Undo การเพิ่มหมวดหมู่เรียบร้อย")
                    st.rerun()

                elif action_type == "update_category":
                    old_category = last_action["old_category"]
                    new_category = last_action["new_category"]

                    for i, category in enumerate(st.session_state.categories):
                        if category == new_category:
                            st.session_state.categories[i] = old_category
                            break

                    for product in st.session_state.products:
                        if product["category"] == new_category:
                            product["category"] = old_category

                    save_all()
                    st.success("Undo การแก้ไขหมวดหมู่เรียบร้อย")
                    st.rerun()

                elif action_type == "delete_category":
                    category = last_action["category"]
                    if category not in st.session_state.categories:
                        st.session_state.categories.append(category)
                        st.session_state.categories.sort()
                    save_all()
                    st.success("Undo การลบหมวดหมู่เรียบร้อย")
                    st.rerun()
else:
    st.warning("ยังไม่มีประวัติการทำงาน")