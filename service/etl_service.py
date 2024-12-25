import pandas as pd
import os
import sys
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.model.transaction import TransactionModel

dir_path = os.path.dirname(os.path.realpath(__file__))  # current folder


def extract_csv_file(file_name=f"{dir_path}/../data/etl_test_data.csv"):
    def extract_datas(df):
        rs = []
        for index, row in df.iterrows():
            price = float(row['price'] or 0)
            quantity = float(row['quantity'] or 0)
            total_price = price*quantity
            if total_price < 10:
                continue
            available_row = {
                "transaction_id": row["transaction_id"] and row["transaction_id"].upper() or '',
                "customer_id": row["customer_id"] and row["customer_id"].upper() or '',
                "product_id": row["product_id"] and row["product_id"].upper() or '',
                "category": row["category"] and row["category"].lower() or '',
                "price": price,
                "quantity": quantity,
                "transaction_date": row["transaction_date"] or '',
                "country": row["country"] and row["country"].lower() or '',
                "total_price": total_price
            }
            #yield available_row
            rs.append(available_row)
        return rs

    try:
        columns_mapping = [
            "transaction_id", "customer_id", "product_id","category", "price", "quantity", "transaction_date",	"country"]
        df = pd.read_csv(file_name, usecols=columns_mapping)
        extract_datas = extract_datas(df)
        return extract_datas
    except Exception as e:
        print(f"[EXTRACT][ERROR]: {str(e)}")

def transform_datas(extract_datas=[]):
    try:
        print(f"[EXTRACT][RUNNING]: ============= >>>>>>")
        if not extract_datas:
            extract_datas = extract_csv_file()
        assert extract_datas, "Not found any data"
        print(f"[EXTRACT][INFO]: extract_datas {extract_datas}")
        transaction_model = TransactionModel()
        transaction_model.create_multi(extract_datas)
        print(f"[EXTRACT][DONE]: <<<< =============")
    except Exception as e:
        print(f"[TRANSFORM][ERROR]: {str(e)}")


extract_datas = transform_datas()
