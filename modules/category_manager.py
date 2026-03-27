import os


def load_categories(file_path):
    categories = []

    if not os.path.exists(file_path):
        return categories

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                categories.append(line)

    return categories


def save_categories(file_path, categories):
    with open(file_path, "w", encoding="utf-8") as file:
        for category in categories:
            file.write(category.strip() + "\n")


def add_category(categories, main_category, sub_category):
    main_category = main_category.strip()
    sub_category = sub_category.strip()

    if not main_category or not sub_category:
        return False, "กรุณากรอกหมวดหลักและหมวดย่อยให้ครบ"

    full_category = f"{main_category}>{sub_category}"

    if full_category in categories:
        return False, "มีหมวดหมู่นี้อยู่แล้ว"

    categories.append(full_category)
    categories.sort()
    return True, "เพิ่มหมวดหมู่เรียบร้อย"


def update_category(categories, old_category, new_main, new_sub):
    new_main = new_main.strip()
    new_sub = new_sub.strip()

    if not new_main or not new_sub:
        return False, "กรุณากรอกข้อมูลใหม่ให้ครบ", None, None

    new_category = f"{new_main}>{new_sub}"

    if old_category not in categories:
        return False, "ไม่พบหมวดหมู่เดิม", None, None

    if new_category != old_category and new_category in categories:
        return False, "มีหมวดหมู่นี้อยู่แล้ว", None, None

    index = categories.index(old_category)
    categories[index] = new_category
    categories.sort()

    return True, "แก้ไขหมวดหมู่เรียบร้อย", old_category, new_category


def delete_category(categories, category):
    if category not in categories:
        return False, "ไม่พบหมวดหมู่"

    categories.remove(category)
    return True, "ลบหมวดหมู่เรียบร้อย"


def get_main_categories(categories):
    main_categories = set()

    for category in categories:
        parts = category.split(">")
        if len(parts) > 0:
            main_categories.add(parts[0].strip())

    return sorted(list(main_categories))


def get_sub_categories(categories, main_category):
    sub_categories = set()

    for category in categories:
        parts = category.split(">")
        if len(parts) > 1 and parts[0].strip() == main_category:
            sub_categories.add(parts[1].strip())

    return sorted(list(sub_categories))