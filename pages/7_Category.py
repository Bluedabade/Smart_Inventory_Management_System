import streamlit as st
from modules.ui_helpers import init_app_state, save_all, render_nav_buttons
from modules.category_manager import (
    add_category,
    update_category,
    delete_category,
    get_main_categories,
    get_sub_categories
)
from modules.inventory_manager import (
    replace_category_in_products,
    category_in_use
)

st.set_page_config(page_title="จัดการหมวดหมู่สินค้า", layout="wide")
init_app_state()

st.title("📂 จัดการหมวดหมู่สินค้า")

with st.sidebar:
    render_nav_buttons()

categories = st.session_state.categories
products = st.session_state.products

tab1, tab2, tab3, tab4 = st.tabs([
    "แสดงหมวดหมู่",
    "เพิ่มหมวดหมู่",
    "แก้ไขหมวดหมู่",
    "ลบหมวดหมู่"
])

# แสดงหมวดหมู่
with tab1:
    st.subheader("รายการหมวดหมู่ทั้งหมด")

    if categories:
        main_categories = get_main_categories(categories)

        for main in main_categories:
            sub_categories = get_sub_categories(categories, main)

            st.markdown(f"###  {main}")
            if sub_categories:
                for sub in sub_categories:
                    st.markdown(f"- {sub}")
            else:
                st.write("ไม่มีหมวดย่อย")

            st.divider()
    else:
        st.warning("ยังไม่มีหมวดหมู่ในระบบ")

# เพิ่มหมวดหมู่
with tab2:
    st.subheader("เพิ่มหมวดหมู่ใหม่")

    add_type = st.radio(
        "เลือกรูปแบบการเพิ่มที่ต้องการ",
        ["เพิ่มหมวดหลักใหม่", "เพิ่มหมวดย่อยในหมวดหลักเดิม"],
        horizontal=True
    )

    main_categories = get_main_categories(categories)

    with st.form("add_category_form"):
        if add_type == "เพิ่มหมวดหลักใหม่":
            st.info("ใช้กรณีที่ต้องการสร้างหมวดหลักใหม่พร้อมหมวดย่อยแรก")
            main_category = st.text_input("ชื่อหมวดหลักใหม่", placeholder="เช่น อาหาร")
            sub_category = st.text_input("ชื่อหมวดย่อยแรก", placeholder="เช่น เครื่องดื่ม")

        else:
            st.info("ใช้กรณีที่ต้องการเพิ่มหมวดย่อยในหมวดหลักที่มีอยู่แล้ว")
            if main_categories:
                main_category = st.selectbox("เลือกหมวดหลัก", main_categories)
                sub_category = st.text_input("ชื่อหมวดย่อยใหม่", placeholder="เช่น ของหวาน")
            else:
                main_category = ""
                sub_category = ""
                st.warning("ยังไม่มีหมวดหลักในระบบ กรุณาเพิ่มหมวดหลักใหม่ก่อน")

        submitted = st.form_submit_button("เพิ่มหมวดหมู่")

    if submitted:
        success, message = add_category(
            st.session_state.categories,
            main_category,
            sub_category
        )

        if success:
            save_all()
            st.success(message)
        else:
            st.error(message)
# แก้ไขหมวดหมู่
with tab3:
    st.subheader("แก้ไขหมวดหมู่")

    if categories:
        main_categories = get_main_categories(categories)

        selected_old_main = st.selectbox(
            "เลือกหมวดหลักเดิม",
            main_categories,
            key="edit_old_main"
        )

        old_sub_categories = get_sub_categories(categories, selected_old_main)

        if old_sub_categories:
            selected_old_sub = st.selectbox(
                "เลือกหมวดย่อยเดิม",
                old_sub_categories,
                key="edit_old_sub"
            )

            old_category = f"{selected_old_main}>{selected_old_sub}"

            edit_type = st.radio(
                "ต้องการแก้ไขแบบไหน",
                [
                    "เปลี่ยนชื่อหมวดหลัก",
                    "เปลี่ยนชื่อหมวดย่อย",
                    "ย้ายหมวดย่อยไปหมวดหลักอื่น"
                ],
                horizontal=True,
                key="edit_type"
            )

            with st.form("edit_category_form"):
                if edit_type == "เปลี่ยนชื่อหมวดหลัก":
                    new_main = st.text_input(
                        "ชื่อหมวดหลักใหม่",
                        value=selected_old_main
                    )
                    new_sub = selected_old_sub

                    st.text_input(
                        "หมวดย่อย",
                        value=selected_old_sub,
                        disabled=True
                    )

                elif edit_type == "เปลี่ยนชื่อหมวดย่อย":
                    new_main = selected_old_main

                    st.text_input(
                        "หมวดหลัก",
                        value=selected_old_main,
                        disabled=True
                    )

                    new_sub = st.text_input(
                        "ชื่อหมวดย่อยใหม่",
                        value=selected_old_sub
                    )

                else:
                    target_main_options = main_categories + ["เพิ่มหมวดหลักใหม่"]

                    default_index = 0
                    if selected_old_main in target_main_options:
                        default_index = target_main_options.index(selected_old_main)

                    selected_target_main = st.selectbox(
                        "เลือกหมวดหลักใหม่",
                        target_main_options,
                        index=default_index
                    )

                    if selected_target_main == "เพิ่มหมวดหลักใหม่":
                        new_main = st.text_input("กรอกหมวดหลักใหม่")
                    else:
                        new_main = selected_target_main

                    new_sub = st.text_input(
                        "ชื่อหมวดย่อย",
                        value=selected_old_sub
                    )

                submitted_edit = st.form_submit_button("บันทึกการแก้ไข")

            if submitted_edit:
                new_main = new_main.strip()
                new_sub = new_sub.strip()

                success, message, old_category_value, new_category_value = update_category(
                    st.session_state.categories,
                    old_category,
                    new_main,
                    new_sub
                )

                if success:
                    replace_category_in_products(
                        st.session_state.products,
                        old_category_value,
                        new_category_value
                    )
                    save_all()
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("หมวดหลักนี้ยังไม่มีหมวดย่อย")
    else:
        st.warning("ยังไม่มีหมวดหมู่ให้แก้ไข")

# ลบหมวดหมู่
with tab4:
    st.subheader("ลบหมวดหมู่")

    if categories:
        main_categories = get_main_categories(categories)

        selected_delete_main = st.selectbox(
            "เลือกหมวดหลัก",
            main_categories,
            key="delete_main_category"
        )

        delete_sub_categories = get_sub_categories(categories, selected_delete_main)

        if delete_sub_categories:
            selected_delete_sub = st.selectbox(
                "เลือกหมวดย่อย",
                delete_sub_categories,
                key="delete_sub_category"
            )

            full_category = f"{selected_delete_main}>{selected_delete_sub}"

            used_products = [
                product for product in products
                if product["category"] == full_category
            ]

            st.info(f"หมวดหมู่ที่เลือก: {selected_delete_main} > {selected_delete_sub}")

            if used_products:
                st.warning(
                    f"ไม่สามารถลบหมวดหมู่นี้ได้ เพราะยังมีสินค้าใช้งานอยู่ {len(used_products)} รายการ"
                )

                st.write("สินค้าที่ใช้หมวดหมู่นี้:")
                st.dataframe(used_products, use_container_width=True)

            else:
                st.success("หมวดหมู่นี้ยังไม่มีสินค้าใช้งานอยู่ และสามารถลบได้")

                confirm_delete = st.checkbox(
                    f"ฉันยืนยันว่าต้องการลบหมวดหมู่ {selected_delete_main} > {selected_delete_sub}",
                    key="confirm_delete_category_checkbox"
                )

                if st.button("ลบหมวดหมู่", type="primary", disabled=not confirm_delete):
                    success, message = delete_category(
                        st.session_state.categories,
                        full_category
                    )

                    if success:
                        save_all()
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.warning("หมวดหลักนี้ยังไม่มีหมวดย่อย")
    else:
        st.warning("ยังไม่มีหมวดหมู่ให้ลบ")