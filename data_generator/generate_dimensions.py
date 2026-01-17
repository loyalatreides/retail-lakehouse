import os
import random
from datetime import datetime, timedelta

import pandas as pd


def ensure_folders(base_dir: str) -> dict:
    """Create output folders and return paths."""
    paths = {
        "dimensions_dir": os.path.join(base_dir, "data", "dimensions"),
    }
    os.makedirs(paths["dimensions_dir"], exist_ok=True)
    return paths


def generate_products(n_products: int = 2000) -> pd.DataFrame:
    categories = {
        "Electronics": ["Logitech", "Samsung", "Apple", "Sony", "Anker", "Xiaomi"],
        "Grocery": ["Tesco", "Dunnes", "Kerrygold", "Heinz", "Nestle", "Lidl"],
        "Home": ["IKEA", "Philips", "Dyson", "Bosch", "Tefal", "Kenwood"],
        "Fashion": ["Zara", "H&M", "Nike", "Adidas", "Puma", "Levi's"],
        "Books": ["Penguin", "HarperCollins", "O'Reilly", "Pearson", "Oxford", "Pan Macmillan"],
    }

    rows = []
    for i in range(1, n_products + 1):
        category = random.choice(list(categories.keys()))
        brand = random.choice(categories[category])

        product_id = f"P_{i:06d}"
        product_name = f"{category} Item {i:06d}"

        # Cost price is used later to compute margin (Gold/Silver enrichment)
        cost_price = round(random.uniform(2.0, 120.0), 2)

        rows.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "brand": brand,
                "cost_price": cost_price,
            }
        )

    return pd.DataFrame(rows)


def generate_stores(n_physical_stores: int = 50) -> pd.DataFrame:
    # Keep it Ireland-themed but scalable
    cities_regions = [
        ("Dublin", "Leinster"),
        ("Cork", "Munster"),
        ("Galway", "Connacht"),
        ("Limerick", "Munster"),
        ("Waterford", "Munster"),
        ("Kilkenny", "Leinster"),
        ("Drogheda", "Leinster"),
        ("Sligo", "Connacht"),
        ("Letterkenny", "Ulster"),
        ("Wexford", "Leinster"),
        ("Athlone", "Leinster"),
        ("Navan", "Leinster"),
        ("Ennis", "Munster"),
        ("Tralee", "Munster"),
        ("Dundalk", "Leinster"),
    ]

    rows = []
    for i in range(1, n_physical_stores + 1):
        city, region = random.choice(cities_regions)
        store_id = f"S_{i:04d}"

        rows.append(
            {
                "store_id": store_id,
                "city": city,
                "region": region,
                "store_type": "Physical",
            }
        )

    # Add one “Online” store to support channel analysis later
    rows.append(
        {
            "store_id": "S_9999",
            "city": "Online",
            "region": "Online",
            "store_type": "Online",
        }
    )

    return pd.DataFrame(rows)


def generate_customers(n_customers: int = 100000) -> pd.DataFrame:
    tiers = ["Bronze", "Silver", "Gold"]
    today = datetime.utcnow().date()

    rows = []
    for i in range(1, n_customers + 1):
        customer_id = f"C_{i:07d}"

        # Signup date within last 3 years
        days_back = random.randint(0, 365 * 3)
        signup_date = today - timedelta(days=days_back)

        # Realistic distribution: more Bronze than Gold
        loyalty_tier = random.choices(tiers, weights=[70, 22, 8], k=1)[0]

        rows.append(
            {
                "customer_id": customer_id,
                "signup_date": signup_date.isoformat(),
                "loyalty_tier": loyalty_tier,
            }
        )

    return pd.DataFrame(rows)


def main():
    random.seed(42)  # repeatable results

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paths = ensure_folders(base_dir)

    # Generate dimension datasets
    products = generate_products(n_products=2000)
    stores = generate_stores(n_physical_stores=50)
    customers = generate_customers(n_customers=100000)

    # Save to CSV
    products_path = os.path.join(paths["dimensions_dir"], "products.csv")
    stores_path = os.path.join(paths["dimensions_dir"], "stores.csv")
    customers_path = os.path.join(paths["dimensions_dir"], "customers.csv")

    products.to_csv(products_path, index=False)
    stores.to_csv(stores_path, index=False)
    customers.to_csv(customers_path, index=False)

    print("✅ Dimension files generated:")
    print(f" - {products_path}  (rows={len(products)})")
    print(f" - {stores_path}    (rows={len(stores)})")
    print(f" - {customers_path} (rows={len(customers)})")


if __name__ == "__main__":
    main()
