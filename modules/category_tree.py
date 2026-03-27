def build_category_tree(products):
    tree = {}

    for product in products:
        categories = product["category"].split(">")
        current = tree

        for cat in categories:
            cat = cat.strip()
            if cat not in current:
                current[cat] = {}
            current = current[cat]

    return tree


def get_main_categories(products):
    main_categories = set()

    for product in products:
        parts = product["category"].split(">")
        if len(parts) > 0:
            main_categories.add(parts[0].strip())

    return sorted(list(main_categories))


def get_sub_categories(products, main_category):
    sub_categories = set()

    for product in products:
        parts = product["category"].split(">")
        if len(parts) > 1 and parts[0].strip() == main_category:
            sub_categories.add(parts[1].strip())

    return sorted(list(sub_categories))


def get_products_by_main_and_sub_category(products, main_category, sub_category):
    result = []

    for product in products:
        parts = product["category"].split(">")

        if len(parts) > 1:
            product_main = parts[0].strip()
            product_sub = parts[1].strip()

            if product_main == main_category and product_sub == sub_category:
                result.append(product)

    return result