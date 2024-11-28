##see how its works on console

import json

with open('menu.json', 'r') as file:
    data = json.load(file)

items = data.get('items', [])
reviews = data.get('reviews', {})

while True:
    print('-' * 30)
    print('Welcome to Restaurant Menu System')
    print('-' * 30)
    print('1. Show Menu')
    print('2. Order Food')
    print('3. Add Item to Menu')
    print('4. Update Menu Item')
    print('5. Add/View Reviews')
    print('6. Exit')
    print('-' * 30)

    print("Enter your choice:")
    try:
        choice = int(input())
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    if choice == 1:
        if not items:
            print("The menu is currently empty.")
        else:
            print('ID\tName\tPrice')
            for item in items:
                print(f"{item.get('id')}\t{item.get('name')}\t{item.get('price')}")
    elif choice == 2:
        if not items:
            print("The menu is empty. Please add items first.")
        else:
            print("Enter the item IDs you want to order (comma-separated):")
            try:
                order_item_ids = list(map(int, input().split(',')))
                print('ID\tName\tPrice')
                total_amount = 0
                for order_id in order_item_ids:
                    for item in items:
                        if item['id'] == order_id:
                            print(f"{item.get('id')}\t{item.get('name')}\t{item.get('price')}")
                            total_amount += float(item.get('price', 0))
                            break
                print('Total Amount: ₹', total_amount)
            except ValueError:
                print("Invalid input. Please enter valid item IDs.")
    elif choice == 3:
        print("Enter the details of the new item:")
        try:
            new_id = int(input("Enter ID: "))
            new_name = input("Enter Name: ").strip()
            new_price = float(input("Enter Price: "))
            items.append({'id': new_id, 'name': new_name, 'price': new_price})
            print(f"Item '{new_name}' added successfully!")
            with open('menu.json', 'w') as file:
                json.dump({'items': items, 'reviews': reviews}, file, indent=4)
        except ValueError:
            print("Invalid input. Please enter valid details for the item.")
    elif choice == 4:
        if not items:
            print("The menu is empty. Please add items first.")
        else:
            try:
                update_id = int(input("Enter the ID of the item to update: "))
                for item in items:
                    if item['id'] == update_id:
                        print(f"Current Details: ID: {item['id']}, Name: {item['name']}, Price: {item['price']}")
                        print("What would you like to update?")
                        print("1. Name")
                        print("2. Price")
                        print("3. Both Name and Price")
                        update_choice = int(input("Enter your choice: "))

                        if update_choice == 1:
                            new_name = input("Enter new name: ").strip()
                            item['name'] = new_name
                            print("Name updated successfully!")
                        elif update_choice == 2:
                            new_price = float(input("Enter new price: "))
                            item['price'] = new_price
                            print("Price updated successfully!")
                        elif update_choice == 3:
                            new_name = input("Enter new name: ").strip()
                            new_price = float(input("Enter new price: "))
                            item['name'] = new_name
                            item['price'] = new_price
                            print("Name and price updated successfully!")
                        else:
                            print("Invalid choice. No changes made.")
                        with open('menu.json', 'w') as file:
                            json.dump({'items': items, 'reviews': reviews}, file, indent=4)
                        break
                else:
                    print(f"No item found with ID {update_id}.")
            except ValueError:
                print("Invalid input. Please enter valid details.")
    elif choice == 5:
        if not items:
            print("The menu is empty. Please add items first.")
        else:
            print("1. Add a Review")
            print("2. View Reviews")
            review_choice = int(input("Enter your choice: "))
            if review_choice == 1:
                item_id = int(input("Enter the item ID to review: "))
                for item in items:
                    if item['id'] == item_id:
                        review = input(f"Enter your review for {item['name']}: ")
                        if item_id not in reviews:
                            reviews[item_id] = []
                        reviews[item_id].append(review)
                        print("Review added successfully!")
                        with open('menu.json', 'w') as file:
                            json.dump({'items': items, 'reviews': reviews}, file, indent=4)
                        break
                else:
                    print(f"No item found with ID {item_id}.")
            elif review_choice == 2:
                item_id = int(input("Enter the item ID to view reviews: "))
                if item_id in reviews and reviews[item_id]:
                    print(f"Reviews for item ID {item_id}:")
                    for idx, review in enumerate(reviews[item_id], start=1):
                        print(f"{idx}. {review}")
                else:
                    print(f"No reviews found for item ID {item_id}.")
            else:
                print("Invalid choice. Please select 1 or 2.")
    elif choice == 6:
        print('Thank you for using the Restaurant Menu System. Goodbye!')
        break
    else:
        print('Invalid choice. Please enter a number between 1 and 6.')
