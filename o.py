import csv
import os
import locale

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

# Clearar skärmen
os.system('cls') 


products = []

# Function to load products from CSV file
def load_products(filename):
    products = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            products.append({
                "id": id,
                "name": name,
                "desc": desc,
                "price": price,
                "quantity": quantity
            })
    return products

# Function to save products to CSV file
def save_products(filename, products):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        fieldnames = ["id", "name", "desc", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

# Function to add a product
def add_product(products, filename):
    try:
        name = input("Skriv produktens namn: ").capitalize()
        os.system('cls')
        desc = input("Skriv produktbeskrivningen: ").capitalize()
        os.system('cls')
        price = float(input("Ange produktens pris: "))
        os.system('cls')
        quantity = int(input("Ange antal: "))
        os.system('cls')

        # Add the new product to the list
        new_product = {
            "id": len(products) + 1,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
        }
        products.append(new_product)

        # Save the updated list to the CSV file
        save_products(filename, products)

        print(f"{name} har lagts till i listan.")

    except ValueError:
        os.system('cls')
        print("Var god ange ett giltigt pris och antal.")

# Function to remove a product
def remove_product(products, filename):
    remove_product_id = int(input("Ange ID: på produkten du vill ta bort: "))
    os.system('cls')
    try:
        found_product = False
        for product in products:
            if product['id'] == remove_product_id:
                products.remove(product)
                found_product = True
                print(f"Produkten med ID: {remove_product_id} har tagits bort från listan.")
                break

        if not found_product:
            print("Produkt med denna ID finns inte.")

    except ValueError:
        print("Ange endast siffror")
        
    save_products(filename, products) # Spara det uppdaterade listan till CSV filen

# Skapad funktion för att se all produkter
def view_products(products):
    if not products:
        return "Inga produkter tillgängliga."

    # Skapa rubriker
    header = f"{'ID':<5} | {'NAMN':<20} | {'BESKRIVNING':<30} | {'PRIS':<15} | {'ANTAL':<10}"
    separator = "-" * len(header)

    # Skapa rader
    rows = []
    for product in products:
        id = product['id']
        name = product['name']
        desc = product['desc']
        price = locale.currency(product['price'], grouping=True)
        quantity = product['quantity']

        row = f"{id:<5} | {name:<20} | {desc:<30} | {price:<15} | {quantity:<10}"
        rows.append(row)

    # Kombinera rubriker, separator och rader
    inventory_table = "\n".join([header, separator] + rows)
    return inventory_table

# Function to edit a product
def edit_product(products):
    try:
        selected_product_id = int(input("Skriv namnet på produkten du vill ändra: "))
        os.system('cls')

        found_product = False
        for product in products:
            if product['id'] == selected_product_id:
                found_product = True

                # 
                name = input(f"Ändra namn för {product['name']}: ") or product['name']
                description = input(f"Ändra beskrivning för {product['desc']}: ") or product['desc']
                price_input = input(f"Ändra pris för {product['price']}: ")
                price = float(price_input) if price_input else product['price']
                quantity_input = input(f"Ändra antal för {product['quantity']}: ")
                quantity = int(quantity_input) if quantity_input else product['quantity']

                # Uppdaterar produkterna 
                product['name'] = name
                product['desc'] = description
                product['price'] = price
                product['quantity'] = quantity

                print(f"Din produkt har uppdaterats\nNytt namn: {product['name']}\nNy beskrivning: {product['desc']}\nNytt pris: {product['price']}\nNytt antal: {product['quantity']}")
                break

        if not found_product:
            print("Denna produkt hittades inte.")

    except ValueError:
        os.system('cls')
        print("Var god ange ett giltigt pris och antal.")

def main():
    filename = 'db_products.csv'
    products = load_products(filename)

    while True:
        os.system('cls')
        print("\nVälkommen till Lager Shop!")
        print(view_products(products))
        print("\n(Välj ett alternativ)")
        print("1. Skapa produkt")
        print("2. Ta bort produkt")
        print("3. Visa produkter")
        print("4. Redigera produkt")
        print("5. Avsluta")

        choice = input("Välj ett alternativ: ")

        if choice == "1":
            add_product(products, filename)
        elif choice == "2":
            remove_product(products, filename)
        elif choice == "3":
            print(view_products(products))
            input("\nTryck Enter för att fortsätta...")
        elif choice == "4":
            edit_product(products)
            input("\nTryck Enter för att fortsätta...")
        elif choice == "5":
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val. Vänligen välj ett giltigt alternativ.")
            input("\nTryck Enter för att fortsätta...")

if __name__ == "__main__":
    main()
