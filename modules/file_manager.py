import os


def load_products(file_path):
    products = []

    if not os.path.exists(file_path):
        return products

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 5:
                    product = {
                        "product_id": parts[0],
                        "name": parts[1],
                        "price": float(parts[2]),
                        "quantity": int(parts[3]),
                        "category": parts[4]
                    }
                    products.append(product)

    return products


def save_products(file_path, products):
    with open(file_path, "w", encoding="utf-8") as file:
        for product in products:
            line = f"{product['product_id']},{product['name']},{product['price']},{product['quantity']},{product['category']}\n"
            file.write(line)