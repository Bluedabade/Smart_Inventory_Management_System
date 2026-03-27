def insertion_sort(products, key):
    arr = products.copy()

    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1

        while j >= 0 and arr[j][key] > current[key]:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = current

    return arr


def merge_sort(products, key):
    if len(products) <= 1:
        return products

    mid = len(products) // 2
    left = merge_sort(products[:mid], key)
    right = merge_sort(products[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i][key] <= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result