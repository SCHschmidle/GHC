from get_menus import get_menus

menus = get_menus()
for name, desc, sort in menus:
    print("Menü Name:", name)
    print("Beschreibung:", desc)
    print("Type:", sort)
    print("-" * 40)
