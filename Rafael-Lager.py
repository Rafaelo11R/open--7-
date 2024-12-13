import csv
import os
import locale


# Sätter locale för korrekt valutahantering
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


# Funktion för att ladda produkter från CSV
def load_products(filename):
    products = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file: # Öppnar filen i läsläge
            reader = csv.DictReader(file)
            for row in reader:
                products.append({
                    "id": int(row['id']),
                    "name": row['name'],
                    "desc": row['desc'],
                    "price": float(row['price'].replace(",", " ")),
                    "quantity": int(row['quantity'])
                })
    except FileNotFoundError:
        print(f"Filen '{filename}' hittades inte. En ny fil skapas vid sparning.") # Om filen inte hittas
    return products

# Funktion för att spara produkter till CSV
def save_products(filename, products):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        fieldnames = ["id", "name", "desc", "price", "quantity"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def add_product(products, filename):
    try:
        name = input("Skriv produktens namn: ").capitalize()
        os.system('cls')
        desc = input("Skriv produktbeskrivningen: ").capitalize()
        os.system('cls')
        
        while True:
            try:
                price = float(input("Ange produktens pris: "))
                break
            except ValueError:
                os.system('cls')
                print("Var god och ange med siffror")
        os.system('cls')

        while True:
            try:
                quantity = int(input("Ange antal: "))
                break
            except ValueError:
                os.system('cls')
                print("Var god och ange med endast heltal")

        os.system('cls')

        # Metod skapat till att hitta det största id-värdet inom alla produkterna.
        new_id = max((product['id'] for product in products), default=0) + 1 # 0 används för att säkerställer om listan är tom och 1 läggs till för att skapa nytt unikt ID för nya produkten.
        new_product = {
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
        }
        products.append(new_product)
        save_products(filename, products)
        print(f"{name} har lagts till i listan.")
        input("\nTryck på Enter för att fortsätta...")

    except ValueError:
        os.system('cls')
        print("Var god ange med siffror")
        input("\nTryck på Enter för att fortsätta...")
        os.system('cls')


def remove_product(products, filename):
    while True:  # Loop för att repetera tills ett giltigt ID matas in
        try:
            os.system('cls')
            remove_product_id = int(input("Ange ID på produkten du vill ta bort: "))
            os.system('cls')

            for product in products:
                if product['id'] == remove_product_id:
                    products.remove(product)
                    print(f"Produkten med ID: {remove_product_id} har tagits bort från listan.")
                    save_products(filename, products)
                    input("\nTryck Enter för att fortsätta...")
                    os.system('cls')
                    return 
            
          
            print("Produkt med detta ID hittades inte.")
            input("\nTryck Enter för att försöka igen...")
        except ValueError:
            os.system('cls')
            print("Var god ange ett giltigt nummer.")
            input("\nTryck Enter för att försöka igen...")

def view_products(products):
    if not products:
        return "Inga produkter tillgängliga."

    # Rubrik och separator

    header_color = '\033[92m' # Skapar färgen grön 
    reset_color = '\033[0m' # För att återställa färgen i menyn
    header = f"{header_color}{'ID':<5} | {'NAMN':<20} | {'BESKRIVNING':<40} | {'PRIS':>13} | {'ANTAL':>10}{reset_color}" # Rubrik meed skapade avstånd ifrån varandra
    separator = "-" * len(header) # Separator som separerar - tecknet gånger längden på rubriken för att skapa linjer

    

    rows = [] # Tom lista för att lagra information om en produkt
    for product in products:

        description = product['desc'][:37] + "..." if len(product['desc']) > 40 else product['desc'] # Gör att beskrivningen justeras på bredd på 40 tecken.
      
        row = f"{product['id']:<5} | {product['name']:<20} | {description:<40} | {product['price']:>10,.2f} kr | {product['quantity']:>8}" # Justerar bredd mellan produktens namn, beskrivning, pris och antal
        rows.append(row)

    
    return "\n".join([header, separator] + rows) # Returnerar header samt separator plus alla rows



def view_product(products):
    try:
        os.system('cls')
        view = int(input("Ange ID för produkten du vill se detaljer "))
        os.system('cls')
        for product in products:
            if product['id'] == view:
                print(f"ID # {product['id']}")
                print(f"Namn: {product['name']}")
                print(f"Beskrivning: {product['desc']}")
                print(f"Pris: {product['price']:>10,.2f}")
                print(f"Kvantitet: {product['quantity']}")
                input("\nTryck Enter för att fortsätta...")
                return
        print("Ingen produkt hittad med denna ID")
        input("\nTryck Enter för att fortsätta...")
        os.system('cls')

    except ValueError:
        os.system('cls')
        print("Var god ange ett giltigt nummer.")
        input("\nTryck på Enter och försök igen...")



def edit_product(products, filename): 
    while True:
        try:
            os.system('cls')
            selected_product_id = int(input("Ange ID på produkten du vill ändra: "))
            os.system('cls')

            for product in products:
                if product['id'] == selected_product_id:
                    name = input(f"Ändra namn för {product['name']}:\nTryck på Enter för att inte ändra ") or product['name']
                    os.system('cls')
                    description = input(f"Ändra beskrivning för {product['desc']}:\nTryck på Enter för att inte ändra ") or product['desc']
                    os.system('cls')
                    price = float(input(f"Ändra pris för {product['price']}:\nTryck på Enter för att inte ändra ") or product['price'])
                    os.system('cls')
                    quantity = int(input(f"Ändra antal för {product['quantity']}:\nTryck på Enter för att inte ändra ") or product['quantity'])
                    os.system('cls')

                    product['name'] = name
                    product['desc'] = description
                    product['price'] = price
                    product['quantity'] = quantity

                    save_products(filename, products)
                    os.system('cls')
                    print(f"Produkten {name} har uppdaterats.")
                    
                    

                    return
                os.system('cls')
            print("Produkten hittades inte.")
            input("\nTryck på Enter för att försöka igen...")
        
        except ValueError:
            os.system('cls')
            print("\nVar god ange giltiga värde.")
            input("\nTryck på Enter och försök igen...")


def most_expensive(products):
    if not products:
        print("Det finns inga produkter")
        input("\nTryck Enter för att fortsätta...")
        return
    
    expensive_product = max(products, key=lambda product: product['price']) # Använder max för att hitta det elementet produkt med det största pris ur listan.
    # key specifierar vilket attribut i varje produkt som ska användas inom jämförelsen som då är pris
    # lambda är en annonym funktion som ska returnera priset för varje produkt

    os.system('cls')
    print("Den dyraste produkten är:")
    print("\n ")
    print(f"ID # {expensive_product['id']}")
    print(f"Namn: {expensive_product['name']}")
    print(f"Beskrivning: {expensive_product['desc']}")
    print(f"Pris: {expensive_product['price']:,.2f} kr")
    print(f"Kvantitet: {expensive_product['quantity']}")
    input("\nTryck Enter för att fortsätta...")
        
 

def main():
    # Anger sökvägen till CSV-filen
    filename = os.path.join(os.path.dirname(__file__), 'C:\\Users\\rafael.alzohairy\\Documents\\tillämpad programmering\\open (7)\\db_inventory.csv')

    # Kontrollerar om katalogen för filen inte existerar ananrs skapas den för att få filen att sparas på rätt plats
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

  
    products = load_products(filename)
    while True:
        os.system('cls')
        print(view_products(products))
        
        print()
        print("1. Skapa produkt")
        print("2. Ta bort produkt")
        print("3. Visa produkt")
        print("4. Redigera produkt")
        print("5. Avsluta")
        print("6. Visa dyraste produkt")
        print()
        
        try:
            print("Vällkommen till Lager Shop!")
            choice = int(input("\nVälj ett alternativ: "))
            os.system('cls')
            
            if choice == 1:
                add_product(products, filename)
            elif choice == 2:
                remove_product(products, filename)
            elif choice == 3:
                print(view_product(products))
                
            elif choice == 4:
                edit_product(products, filename)
                input("\nTryck Enter för att fortsätta...")
            elif choice == 5:
                print("Avslutar programmet.")
                break  # Avsluta programmet

            elif choice == 6: # Återanvänder funktionen via input
                print(most_expensive(products))
                

            else:
                
                print("Ogiltigt val! Försök igen.")
                input("\nTryck Enter för att fortsätta...")

        except ValueError:
            print("\nAnge ett giltigt nummer!")
            input("\nTryck Enter för att fortsätta...")
        
if __name__ == "__main__": # Säkerställer att main körs när filen executes
    main()