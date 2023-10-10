class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cart = []

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.products = []

def save_data(data, filename):
    with open(filename, 'w') as file:
        for item in data:
            file.write(f"{item}\n")


def load_data(filename):
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                data.append(line.strip())
    except FileNotFoundError:
        pass
    return data

def save_users(users):
    save_data([f"{user.username}:{user.password}" for user in users], 'users.txt')

def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                username, password = line.strip().split(':')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

def save_products(products):
    save_data([f"{product.name}:{product.price}" for product in products], 'products.txt')

def load_products():
    products = []
    try:
        with open('products.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, price = line.strip().split(':')
                products.append(Product(name, float(price)))
    except FileNotFoundError:
        pass
    return products

def save_admin(admin):
    with open('admin.txt', 'w') as file:
        file.write(f"{admin.username}:{admin.password}")

def load_admin():
    try:
        with open('admin.txt', 'r') as file:
            line = file.readline()
            username, password = line.strip().split(':')
            return Admin(username, password)
    except FileNotFoundError:
        pass
    return None

def find_user(username, password, users):
    for user in users:
        if user.username == username and user.password == password:
            return user
    return None

def show_products(products):
    print("\nСписок товарів:")
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} - {product.price} грн")

def add_to_cart(current_user, products):
    show_products(products)
    choice = input("Виберіть товар для додавання у кошик (введіть номер товару): ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(products):
            current_user.cart.append(products[choice - 1])
            print("Товар додано у кошик.")
        else:
            print("Невірний номер товару.")
    except ValueError:
        print("Введіть коректний номер товару.")

def show_cart(user):
    total_price = sum(product.price for product in user.cart)
    print("\nКошик:")
    for i, product in enumerate(user.cart, 1):
        print(f"{i}. {product.name} - {product.price} грн")
    print(f"Загальна сума до оплати: {total_price} грн")

def checkout(user):
    total_price = sum(product.price for product in user.cart)
    print(f"Загальна сума до оплати: {total_price} грн")
    user.cart.clear()
    print("Покупка успішно завершена.")

def add_product(products):
    name = input("Введіть назву товару: ")
    price = float(input("Введіть ціну товару: "))
    products.append(Product(name, price))
    save_products(products)
    print("Товар додано.")

def delete_product(products):
    show_products(products)
    choice = input("Виберіть товар для видалення (введіть номер товару): ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(products):
            del products[choice - 1]
            save_products(products)
            print("Товар видалено.")
        else:
            print("Невірний номер товару.")
    except ValueError:
        print("Введіть коректний номер товару.")

def update_product(products):
    show_products(products)
    choice = input("Виберіть товар для зміни (введіть номер товару): ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(products):
            product = products[choice - 1]
            new_name = input("Введіть нову назву товару: ")
            new_price = float(input("Введіть нову ціну товару: "))
            product.name = new_name
            product.price = new_price
            save_products(products)
            print("Інформацію про товар оновлено.")
        else:
            print("Невірний номер товару.")
    except ValueError:
        print("Введіть коректний номер товару.")

def user_menu(current_user, products):
    while True:
        print("\n1. Показати список товарів")
        print("2. Додати товар у кошик")
        print("3. Показати кошик")
        print("4. Закінчити покупку")
        print("5. Вийти")
        choice = input("Оберіть опцію: ")
        if choice == "1":
            show_products(products)
        elif choice == "2":
            add_to_cart(current_user, products)
        elif choice == "3":
            show_cart(current_user)
        elif choice == "4":
            checkout(current_user)
        elif choice == "5":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

def admin_menu(admin_user, products):
    while True:
        print("\n1. Додати товар")
        print("2. Видалити товар")
        print("3. Змінити інформацію про товар")
        print("4. Вийти")
        admin_choice = input("Оберіть опцію: ")
        if admin_choice == "1":
            add_product(products)
        elif admin_choice == "2":
            delete_product(products)
        elif admin_choice == "3":
            update_product(products)
        elif admin_choice == "4":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

def main():
    admin_user = load_admin()
    if admin_user is None:
        admin_user = Admin("Admin", "Admin")
        save_admin(admin_user)

    users = load_users()
    products = load_products()

    while True:
        print("\n1. Зареєструватись")
        print("2. Увійти як користувач")
        print("3. Увійти як адміністратор")
        print("4. Вийти")
        choice = input("Оберіть опцію: ")

        if choice == "1":
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            users.append(User(username, password))
            save_users(users)
            print("Користувач зареєстрований.")

        elif choice == "2":
            username = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            current_user = find_user(username, password, users)
            if current_user:
                user_menu(current_user, products)
            else:
                print("Невірне ім'я користувача або пароль.")

        elif choice == "3":
            username = input("Введіть ім'я адміністратора: ")
            password = input("Введіть пароль адміністратора: ")
            if username == admin_user.username and password == admin_user.password:
                admin_menu(admin_user, products)
            else:
                print("Невірне ім'я адміністратора або пароль.")

        elif choice == "4":
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
