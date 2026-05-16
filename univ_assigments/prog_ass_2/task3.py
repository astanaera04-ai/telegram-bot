inventory = {"Apple": 0.50, "Banana": 0.30, "Milk": 2.50}

inventory["Bread"] = 1.20

inventory["Apple"] = 0.65
del inventory["Banana"]
 
print("--- Updated Product List ---")
for product, price in inventory.items():
    print(f"Product: {product:10} | Price: ${price:.2f}")