import os
import random
from datetime import datetime, timedelta, timezone

import pandas as pd


def ensure_folders(base_dir: str) -> dict:
    """Create output folders and return paths."""
    paths = {
        "dimensions_dir": os.path.join(base_dir, "data", "dimensions"),
        "transactions_dir": os.path.join(base_dir, "data", "transactions"),
    }
    os.makedirs(paths["transactions_dir"], exist_ok=True)
    return paths


def load_dimensions(dimensions_dir: str):
    """Load dimension tables and return lists of IDs."""
    products_path = os.path.join(dimensions_dir, "products.csv")
    stores_path = os.path.join(dimensions_dir, "stores.csv")
    customers_path = os.path.join(dimensions_dir, "customers.csv")

    if not (os.path.exists(products_path) and os.path.exists(stores_path) and os.path.exists(customers_path)):
        raise FileNotFoundError(
            "Missing dimension files. Make sure you have:\n"
            " - data/dimensions/products.csv\n"
            " - data/dimensions/stores.csv\n"
            " - data/dimensions/customers.csv\n"
        )

    products = pd.read_csv(products_path)
    stores = pd.read_csv(stores_path)
    customers = pd.read_csv(customers_path)

    product_ids = products["product_id"].dropna().astype(str).tolist()
    store_ids = stores["store_id"].dropna().astype(str).tolist()
    customer_ids = customers["customer_id"].dropna().astype(str).tolist()

    return product_ids, store_ids, customer_ids


def random_timestamp_within_days(days_back: int = 30) -> str:
    """Create an ISO timestamp within last N days (UTC)."""
    now = datetime.now(timezone.utc)
    seconds_back = random.randint(0, days_back * 24 * 3600)
    ts = now - timedelta(seconds=seconds_back)
    return ts.isoformat()


def generate_transactions_batch(
    batch_size: int,
    product_ids: list,
    store_ids: list,
    customer_ids: list,
    start_txn_num: int,
    bad_rate: float = 0.02,
    dup_rate: float = 0.01,
    late_rate: float = 0.01,
) -> pd.DataFrame:
    """
    Generate one batch of transaction rows.

    bad_rate  = % rows that will have invalid values (missing ids, negative qty/price)
    dup_rate  = % rows that will duplicate an earlier transaction_id (simulate duplicates)
    late_rate = % rows with old timestamps (simulate late-arriving events)
    """
    channels = ["online", "store"]
    payment_methods = ["card", "cash", "wallet"]
    currencies = ["EUR"]

    rows = []
    txn_ids_so_far = []

    for i in range(batch_size):
        txn_num = start_txn_num + i
        transaction_id = f"TXN_{txn_num:012d}"

        transaction_ts = random_timestamp_within_days(days_back=30)

        store_id = random.choice(store_ids)
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)

        qty = random.randint(1, 5)
        unit_price = round(random.uniform(2.0, 250.0), 2)

        channel = random.choice(channels)
        payment_method = random.choice(payment_methods)
        currency = random.choice(currencies)

        rows.append(
            {
                "transaction_id": transaction_id,
                "transaction_ts": transaction_ts,
                "store_id": store_id,
                "customer_id": customer_id,
                "product_id": product_id,
                "qty": qty,
                "unit_price": unit_price,
                "currency": currency,
                "channel": channel,
                "payment_method": payment_method,
            }
        )
        txn_ids_so_far.append(transaction_id)

    df = pd.DataFrame(rows)

    # --- Introduce duplicates (dup_rate) ---
    n_dup = int(batch_size * dup_rate)
    if n_dup > 0 and len(txn_ids_so_far) > 10:
        dup_indices = random.sample(range(batch_size), n_dup)
        # duplicate IDs by copying IDs from earlier in THIS batch
        for idx in dup_indices:
            df.loc[idx, "transaction_id"] = random.choice(txn_ids_so_far[: max(10, batch_size // 2)])

    # --- Introduce bad records (bad_rate) ---
    n_bad = int(batch_size * bad_rate)
    if n_bad > 0:
        bad_indices = random.sample(range(batch_size), n_bad)
        for idx in bad_indices:
            bad_type = random.choice(["missing_product", "missing_customer", "missing_store", "neg_qty", "neg_price"])

            if bad_type == "missing_product":
                df.loc[idx, "product_id"] = None
            elif bad_type == "missing_customer":
                df.loc[idx, "customer_id"] = None
            elif bad_type == "missing_store":
                df.loc[idx, "store_id"] = None
            elif bad_type == "neg_qty":
                df.loc[idx, "qty"] = -random.randint(1, 3)
            elif bad_type == "neg_price":
                df.loc[idx, "unit_price"] = -round(random.uniform(1.0, 80.0), 2)

    # --- Introduce late-arriving events (late_rate) ---
    n_late = int(batch_size * late_rate)
    if n_late > 0:
        late_indices = random.sample(range(batch_size), n_late)
        for idx in late_indices:
            now = datetime.now(timezone.utc)
            days_back = random.randint(120, 365)  # 4–12 months old
            ts = now - timedelta(days=days_back, seconds=random.randint(0, 86400))
            df.loc[idx, "transaction_ts"] = ts.isoformat()

    return df


def main():
    random.seed(42)  # repeatable results

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paths = ensure_folders(base_dir)

    # ---------------- CONFIG ----------------
    # Recommended with 100k customers:
    total_transactions = 500_000      # change to 300_000 or 1_000_000 if you want
    batch_file_size = 10_000          # 10k rows per file -> 50 files for 500k
    bad_rate = 0.02                   # 2% bad rows
    dup_rate = 0.01                   # 1% duplicate transaction_ids
    late_rate = 0.01                  # 1% late timestamps
    # ----------------------------------------

    product_ids, store_ids, customer_ids = load_dimensions(paths["dimensions_dir"])

    num_files = (total_transactions + batch_file_size - 1) // batch_file_size
    txn_counter = 1

    print(f"Generating {total_transactions:,} transactions into {num_files} files...")
    print(f"Each file size: ~{batch_file_size:,} rows")
    print(f"Bad rows: {bad_rate*100:.1f}% | Duplicate IDs: {dup_rate*100:.1f}% | Late events: {late_rate*100:.1f}%")
    print("Output folder:", paths["transactions_dir"])
    print("-" * 60)

    for file_idx in range(1, num_files + 1):
        remaining = total_transactions - (txn_counter - 1)
        current_batch = min(batch_file_size, remaining)

        df = generate_transactions_batch(
            batch_size=current_batch,
            product_ids=product_ids,
            store_ids=store_ids,
            customer_ids=customer_ids,
            start_txn_num=txn_counter,
            bad_rate=bad_rate,
            dup_rate=dup_rate,
            late_rate=late_rate,
        )

        ts_label = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_file = f"transactions_{ts_label}_part{file_idx:03d}.csv"
        out_path = os.path.join(paths["transactions_dir"], out_file)

        df.to_csv(out_path, index=False)

        print(f"✅ [{file_idx:03d}/{num_files:03d}] Wrote {len(df):,} rows -> {out_file}")

        txn_counter += current_batch

    print("-" * 60)
    print("🎉 Done. Transaction files created in: data/transactions/")


if __name__ == "__main__":
    main()
