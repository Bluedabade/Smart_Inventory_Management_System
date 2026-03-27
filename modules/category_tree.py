def build_category_tree(products):
    tree = {}

    for product in products:
        categories = product["category"].split(">")
        current = tree

        for cat in categories:
            if cat not in current:
                current[cat] = {}
            current = current[cat]

    return tree


def get_products_by_category(products, selected_category):
    result = []
    for product in products:
        if selected_category in product["category"]:
            result.append(product)
    return result


def get_all_categories(products):
    categories = set()
    for product in products:
        categories.add(product["category"])
    return sorted(list(categories))