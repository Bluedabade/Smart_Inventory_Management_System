def sequential_search_by_name(products, keyword):
    result = []
    keyword = keyword.lower().strip()

    for product in products:
        if keyword in product["name"].lower():
            result.append(product)

    return result


def binary_search_by_id(sorted_products, target_id):
    left = 0
    right = len(sorted_products) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_id = sorted_products[mid]["product_id"]

        if mid_id == target_id:
            return sorted_products[mid]
        elif mid_id < target_id:
            left = mid + 1
        else:
            right = mid - 1

    return None