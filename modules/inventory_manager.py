def build_hash_table(products):
    product_table = {}
    for product in products:
        product_table[product["product_id"]] = product
    return product_table


def add_product(products, new_product):
    for product in products:
        if product["product_id"] == new_product["product_id"]:
            return False, "มีรหัสสินค้านี้อยู่แล้ว"
    products.append(new_product)
    return True, "เพิ่มสินค้าเรียบร้อย"


def update_product(products, product_id, updated_data):
    for product in products:
        if product["product_id"] == product_id:
            product["name"] = updated_data["name"]
            product["price"] = updated_data["price"]
            product["quantity"] = updated_data["quantity"]
            product["category"] = updated_data["category"]
            return True, "แก้ไขข้อมูลเรียบร้อย"
    return False, "ไม่พบรหัสสินค้า"


def delete_product(products, product_id):
    for i, product in enumerate(products):
        if product["product_id"] == product_id:
            deleted_product = products.pop(i)
            return True, "ลบสินค้าเรียบร้อย", deleted_product
    return False, "ไม่พบรหัสสินค้า", None


def get_product_by_id_hash(product_table, product_id):
    return product_table.get(product_id, None)

def replace_category_in_products(products, old_category, new_category):
    for product in products:
        if product["category"] == old_category:
            product["category"] = new_category


def category_in_use(products, category):
    for product in products:
        if product["category"] == category:
            return True
    return False


def remove_category_from_products(products, category):
    for product in products:
        if product["category"] == category:
            product["category"] = ""