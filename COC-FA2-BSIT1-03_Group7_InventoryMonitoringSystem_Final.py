"""
INVENTORY MONITORING SYSTEM
Python Console-Based Program

Based on the user's project instructions:
1. Add Product
2. Search Product
3. Stock In
4. Sales
5. View Inventory
6. View Sales
0. Exit

No JSON, database, or file-saving/loading feature is used.
Records exist only while this program is running.
"""

from datetime import datetime

CATEGORIES = {
    "C001": "KITCHEN APPLIANCES",
    "C002": "SCHOOL SUPPLIES",
    "C003": "MILK & DAIRY",
    "C004": "DETERGENTS",
    "C005": "RTW",
}

# Product ID prefixes follow the examples in the project instructions.
CATEGORY_PREFIX = {
    "C001": "P",
    "C002": "SP",
    "C003": "MK",
    "C004": "D",
    "C005": "RTW",
}

products = []
stock_history = []
sales = []
MONTHS = [
    "JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE",
    "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"
]


def line(char="=", width=112):
    print(char * width)


def pause():
    input("\nPress ENTER to return to the main menu...")


def money(value):
    return f"{value:,.2f}" if value % 1 else f"{value:,.0f}"


def get_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_quantity(prompt, allow_zero=False):
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 0 or (value == 0 and not allow_zero):
                print("Enter a valid whole number.")
                continue
            return value
        except ValueError:
            print("Invalid quantity. Enter a whole number, such as 10.")


def get_price(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Price cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid price. Enter a number, such as 1000 or 50.50.")


def show_categories():
    line()
    print(f"{'CATEGORY ID':<22}{'CATEGORY NAME'}")
    line("-")
    for category_id, category_name in CATEGORIES.items():
        print(f"{category_id:<22}{category_name}")
    line()


def find_product(product_id):
    product_id = product_id.strip().upper()
    for product in products:
        if product["product_id"] == product_id:
            return product
    return None


def next_product_id(category_id):
    prefix = CATEGORY_PREFIX[category_id]
    highest = 0

    for product in products:
        if product["category_id"] == category_id:
            product_id = product["product_id"]
            suffix = product_id[len(prefix):]
            if product_id.startswith(prefix) and suffix.isdigit():
                highest = max(highest, int(suffix))

    return f"{prefix}{highest + 1:03d}"


def print_products(rows):
    if not rows:
        print("No matching products found.")
        return

    line()
    print(
        f"{'CATEGORY ID':<12} {'CATEGORY NAME':<22} {'PRODUCT ID':<10} "
        f"{'PRODUCT CATEGORY':<19} {'PRODUCT NAME':<22} "
        f"{'QUANTITY':>10} {'PRICE EACH':>12} {'TOTAL':>12}"
    )
    line("-")
    for p in rows:
        total = p["quantity"] * p["price"]
        print(
            f"{p['category_id']:<12} {p['category_name'][:21]:<22} "
            f"{p['product_id']:<10} {p['product_category'][:18]:<19} "
            f"{p['product_name'][:21]:<22} {p['quantity']:>10} "
            f"{money(p['price']):>12} {money(total):>12}"
        )
    line()



def add_product(): # 1. ADD PRODUCT
    print("\n" + "=" * 60)
    print("                     ADD PRODUCT")
    print("=" * 60)

    # The user manually enters the product and category information.
    product_id = get_text("ENTER PRODUCT ID: ").upper()

    # Prevent duplicate product IDs.
    if find_product(product_id):
        print("ERROR: This PRODUCT ID already exists.")
        pause()
        return

    category_id = get_text("ENTER CATEGORY ID: ").upper()
    category_name = get_text("ENTER CATEGORY NAME: ").upper()
    product_category = get_text("ENTER PRODUCT CATEGORY: ").upper()
    product_name = get_text("ENTER PRODUCT NAME: ").upper()

    quantity = get_quantity("ENTER QUANTITY: ", allow_zero=True)
    price = get_price("ENTER PRICE EACH: ")

    # Create the product using the details entered by the user.
    product = {
        "product_id": product_id,
        "category_id": category_id,
        "category_name": category_name,
        "product_category": product_category,
        "product_name": product_name,
        "quantity": quantity,
        "price": price
    }

    products.append(product)

    print("\n" + "=" * 60)
    print("             PRODUCT ADDED SUCCESSFULLY")
    print("=" * 60)

    print(f"PRODUCT ID:        {product_id}")
    print(f"CATEGORY ID:       {category_id}")
    print(f"CATEGORY NAME:     {category_name}")
    print(f"PRODUCT CATEGORY:  {product_category}")
    print(f"PRODUCT NAME:      {product_name}")
    print(f"QUANTITY:          {quantity}")
    print(f"PRICE EACH:        {money(price)}")
    print(f"TOTAL:             {money(quantity * price)}")
    now = datetime.now()
    print(f"DATE/TIME:         {now.strftime('%m/%d/%Y  %I:%M %p')}")

    print("=" * 60)
    pause()



def search_product(): # 2. SEARCH PRODCUCT
    while True:
        print("\nSEARCH PRODUCT")
        print("1. SEARCH BY CATEGORY NAME")
        print("2. SEARCH BY PRODUCT ID")
        print("0. BACK")

        choice = input("Select option (0-2): ").strip()

        if choice == "1":
            name = get_text("SEARCH BY CATEGORY NAME: ").upper()
            matches = [
                p for p in products
                if name in p["category_name"]
            ]
            print_products(matches)

        elif choice == "2":
            product_id = get_text("SEARCH BY PRODUCT ID: ").upper()
            product = find_product(product_id)
            print_products([product] if product else [])

        elif choice == "0":
            break

        else:
            print("Invalid option. Select 1, 2, or 0.")


def choose_month():
    month = input("ENTER MONTH (e.g. DECEMBER, or EXIT to cancel): ").strip().upper()
    if month == "EXIT":
        return None
    if month not in MONTHS:
        print("Invalid month name.")
        return None
    return month



def record_stock_in(): # 3. STOCK IN
    while True:
        print("\n" + "=" * 40)
        print("              STOCK IN")
        print("=" * 40)
        print("1. ENTER PRODUCT ID")
        print("2. ENTER MONTH")
        print("3. UPDATE PRODUCT PRICE")
        print("0. BACK")
        print("=" * 40)

        choice = input("Select option: ").strip()

        if choice == "1":
            product_id = input(
                "ENTER PRODUCT ID (or EXIT to return): "
            ).strip().upper()

            if product_id == "EXIT":
                continue

            product = find_product(product_id)

            if not product:
                print("Product ID not found.")
                pause()
                continue

            month = choose_month()

            if month is None:
                continue

            quantity = get_quantity("ENTER QUANTITY: ")
            now = datetime.now()

            product["quantity"] += quantity

            stock_history.append({
                "product_id": product_id,
                "month": month,
                "quantity": quantity,
                "date_time": now
            })

            print("\nSTOCK IN RECORDED SUCCESSFULLY!")
            print(f"PRODUCT ID: {product_id}")
            print(f"PRODUCT NAME: {product['product_name']}")
            print(f"QUANTITY ADDED: {quantity}")
            print(f"NEW QUANTITY: {product['quantity']}")
            print(
                "DATE/TIME:",
                now.strftime("%B %d, %Y - %I:%M %p")
            )

            show_stock_history(product_id, month)
            pause()

        elif choice == "2":
            month = choose_month()

            if month is None:
                continue

            matching_products = [
                p for p in products
                if any(
                    r["product_id"] == p["product_id"]
                    and r["month"] == month
                    for r in stock_history
                )
            ]

            if not matching_products:
                print(f"No stock-in records found for {month}.")
                pause()
                continue

            print(f"\nPRODUCTS WITH STOCK-IN RECORDS FOR {month}")
            print("-" * 60)

            for p in matching_products:
                print(
                    f"{p['product_id']} - {p['product_name']} "
                    f"(Current quantity: {p['quantity']})"
                )

            product_id = input(
                "\nENTER PRODUCT ID TO ADD STOCK (or EXIT): "
            ).strip().upper()

            if product_id == "EXIT":
                continue

            product = find_product(product_id)

            if not product:
                print("Product ID not found.")
                pause()
                continue

            quantity = get_quantity("ENTER QUANTITY: ")
            now = datetime.now()

            product["quantity"] += quantity

            stock_history.append({
                "product_id": product_id,
                "month": month,
                "quantity": quantity,
                "date_time": now
            })

            print("\nSTOCK IN RECORDED SUCCESSFULLY!")
            print(f"PRODUCT ID: {product_id}")
            print(f"PRODUCT NAME: {product['product_name']}")
            print(f"MONTH: {month}")
            print(f"QUANTITY ADDED: {quantity}")
            print(f"NEW QUANTITY: {product['quantity']}")
            print(
                "DATE/TIME:",
                now.strftime("%B %d, %Y - %I:%M %p")
            )

            show_stock_history(product_id, month)
            pause()

        elif choice == "3":
            product_id = input(
                "ENTER PRODUCT ID TO UPDATE PRICE (or EXIT to cancel): "
            ).strip().upper()

            if product_id == "EXIT":
                continue

            product = find_product(product_id)

            if not product:
                print("Product ID not found.")
                pause()
                continue

            print("\\nPRODUCT FOUND")
            print(f"PRODUCT ID: {product['product_id']}")
            print(f"PRODUCT NAME: {product['product_name']}")
            print(f"CURRENT PRICE: {money(product['price'])}")

            new_price = get_price("ENTER NEW PRICE EACH: ")
            old_price = product["price"]
            now = datetime.now()
            product["price"] = new_price

            print("\nPRODUCT PRICE UPDATED SUCCESSFULLY!")
            print(f"PRODUCT ID: {product['product_id']}")
            print(f"PRODUCT NAME: {product['product_name']}")
            print(f"OLD PRICE EACH: {money(old_price)}")
            print(f"NEW PRICE EACH: {money(new_price)}")
            print(f"CURRENT QUANTITY: {product['quantity']}")
            print(f"DATE/TIME: {now.strftime('%m/%d/%Y  %I:%M %p')}")
            pause()

        elif choice == "0":
            break

        else:
            print("Invalid option. Please select 0, 1, 2, or 3.")



def show_stock_history(product_id, month):
    records = [
        r for r in stock_history
        if r["product_id"] == product_id and r["month"] == month
    ]
    print(f"\nSTOCK IN HISTORY - {month}")
    line()
    print(f"{'STOCK IN DATE':<25}{'PRODUCT ID':<14}{'PRODUCT CATEGORY':<22}{'QUANTITY STOCK IN':>20}")
    line("-")
    total_in = 0
    for r in records:
        p = find_product(product_id)
        dt = r["date_time"]
        print(
            f"{dt.strftime('%B %d, %Y %I:%M %p'):<25}{product_id:<14}"
            f"{p['product_category'][:21]:<22}{r['quantity']:>20}"
        )
        total_in += r["quantity"]
    line("-")
    print(f"{'TOTAL STOCK IN':<61}{total_in:>20}")
    line()



def record_sale(): # 4 SALES
    while True:
        print("\nSALES")
        product_id = input(
            "ENTER PRODUCT ID (or EXIT to return): "
        ).strip().upper()

        if product_id == "EXIT":
            break

        product = find_product(product_id)
        if not product:
            print("Product ID not found. Please try again.")
            continue

        print(f"PRODUCT NAME: {product['product_name']}")
        print(f"AVAILABLE STOCK: {product['quantity']}")

        quantity = get_quantity("ENTER QUANTITY SOLD: ")

        if quantity > product["quantity"]:
            print("Not enough stock. Sale was not recorded.")
            continue

        now = datetime.now()
        total = quantity * product["price"]
        product["quantity"] -= quantity

        sales.append({
            "product_id": product_id,
            "quantity": quantity,
            "price_each": product["price"],
            "total": total,
            "month": now.strftime("%B").upper(),
            "date_time": now,
        })

        line()
        print(
            f"{'PRODUCT ID':<15}{'PRODUCT NAME':<25}"
            f"{'TOTAL STOCK OUT':>18}{'PRICE EACH':>15}"
            f"{'TOTAL SALES':>16}"
        )
        line("-")

        print(
            f"{product_id:<15}{product['product_name'][:24]:<25}"
            f"{quantity:>18}{money(product['price']):>15}"
            f"{money(total):>16}"
        )

        line()
        print(f"DATE/TIME: {now.strftime('%B %d, %Y %I:%M %p')}")
        print(f"REMAINING STOCK: {product['quantity']}")
        line()




def view_inventory(): # 5 VIEW INVENTORY
    while True:
        print("\nVIEW INVENTORY")
        print("1. VIEW BY PRODUCT ID")
        print("2. VIEW BY MONTH")
        print("0. BACK")
        choice = input("Select option (0-2, or ENTER to go back): ").strip()

        if choice == "" or choice == "0":
            break

        elif choice == "1":
            product_id = input("ENTER PRODUCT ID: ").strip().upper()
            product = find_product(product_id)

            if product:
                print_products([product])
            else:
                print("Product ID not found.")

        elif choice == "2":
            month = choose_month()

            if month:
                # Show every registered product in the inventory.
                # The selected month is the report label; quantities and prices
                # shown here are the current values, not historical month-end values.
                rows = products.copy()

                print(f"\nINVENTORY FOR {month} {datetime.now().year} (CURRENT QUANTITIES)")
                print_products(rows)

        else:
            print("Invalid option. Select 1, 2, 0, or press ENTER.")





def view_sales(): # 6. VIEW SALES
    while True:
        print("\nVIEW SALES")
        print("1. VIEW BY PRODUCT ID")
        print("2. VIEW BY MONTH")
        print("0. BACK")
        choice = input("Select option (0-2, or ENTER to go back): ").strip()

        if choice == "" or choice == "0":
            break

        elif choice == "1":
            product_id = input("ENTER PRODUCT ID: ").strip().upper()

            if not find_product(product_id):
                print("Product ID not found.")
            else:
                rows = [
                    s for s in sales
                    if s["product_id"] == product_id
                ]
                print_sales(rows, f"SALES FOR PRODUCT {product_id}")

        elif choice == "2":
            month = choose_month()

            if month:
                rows = [
                    s for s in sales
                    if s["month"] == month
                ]
                print_sales(rows, f"SALES FOR {month}")

        else:
            print("Invalid option. Select 1, 2, 0, or press ENTER.")




def print_sales(rows, title):
    print(f"\n{title}")
    line()
    print(
       f"{'DATE/TIME':<27}{'CATEGORY NAME':<22}{'PRODUCT ID':<12}"
        f"{'PRODUCT NAME':<22}{'QTY SOLD':>10}{'PRICE EACH':>13}{'TOTAL SALES':>14}"
    )
    line("-")

    if not rows:
        print("No sales records found.")
        line()
        return

    total_quantity = 0
    grand_total = 0
    for sale in sorted(rows, key=lambda r: r["date_time"]):
        product = find_product(sale["product_id"])
        dt = sale["date_time"]
        print(
           f"{dt.strftime('%B %d, %Y %I:%M %p'):<27}{product['category_name'][:21]:<22}"
            f"{sale['product_id']:<12}{product['product_name'][:21]:<22}"
            f"{sale['quantity']:>10}{money(sale['price_each']):>13}"
            f"{money(sale['total']):>14}"
        )
        total_quantity += sale["quantity"]
        grand_total += sale["total"]

    line("-")
    print(f"TOTAL QUANTITY SOLD: {total_quantity}")
    print(f"TOTAL SALES: {money(grand_total)}")
    line()


def main():
    while True:
        print()
        line()
        print("                         INVENTORY MONITORING SYSTEM")
        line()
        show_categories()
        print("1. ADD PRODUCT")
        print("2. SEARCH PRODUCT")
        print("3. STOCK IN")
        print("4. SALES")
        print("5. VIEW INVENTORY")
        print("6. VIEW SALES")
        print("0. EXIT")
        line()
        choice = input("Select option (0-6): ").strip()

        if choice == "1":
            add_product()
        elif choice == "2":
            search_product()
        elif choice == "3":
            record_stock_in()
        elif choice == "4":
            record_sale()
        elif choice == "5":
            view_inventory()
        elif choice == "6":
            view_sales()
        elif choice == "0":
            print("\nThank you for using the Inventory Management System.")
            print("Program closed.")
            break
        else:
            print("Invalid choice. Please select 0 to 6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
