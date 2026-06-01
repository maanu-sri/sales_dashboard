import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sales_data():
    random.seed(42)
    np.random.seed(42)

    categories = ["Electronics", "Clothing", "Food & Beverage", "Books", "Sports"]
    regions = ["North", "South", "East", "West"]
    products = {
        "Electronics": ["Laptop", "Phone", "Headphones", "Tablet", "Smartwatch"],
        "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Saree"],
        "Food & Beverage": ["Coffee", "Tea", "Snacks", "Juice", "Chocolates"],
        "Books": ["Fiction", "Non-Fiction", "Textbook", "Comic", "Biography"],
        "Sports": ["Cricket Bat", "Football", "Yoga Mat", "Dumbbells", "Badminton Kit"]
    }

    rows = []
    start_date = datetime(2024, 1, 1)

    for _ in range(1000):
        category = random.choice(categories)
        product = random.choice(products[category])
        region = random.choice(regions)
        date = start_date + timedelta(days=random.randint(0, 364))
        quantity = random.randint(1, 10)
        price = round(random.uniform(100, 5000), 2)
        revenue = round(quantity * price, 2)

        rows.append({
            "date": date,
            "category": category,
            "product": product,
            "region": region,
            "quantity": quantity,
            "price": price,
            "revenue": revenue
        })

    df = pd.DataFrame(rows)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df