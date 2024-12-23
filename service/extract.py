import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))  # current folder


def extract_csv_file(file_name=f"{dir_path}/../data/etl_test_data.csv"):
    def extract_datas(df):
        rs = []
        for index, row in df.iterrows():
            price = float(row['price'] or 0)
            quantity = float(row['quantity'] or 0)
            total_value = price*quantity
            if total_value < 10:
                continue
            available_row = [
                row["transaction_id"] and row["transaction_id"].upper() or '',
                row["customer_id"] and row["customer_id"].upper() or '',
                row["product_id"] and row["product_id"].upper() or '',
                row["category"] and row["category"].lower() or '',
                price,
                quantity,
                row["transaction_date"] or '',
                row["country"] and row["country"].lower() or '',
                total_value
            ]
            #yield available_row
            rs.append(available_row)
        return rs

    columns_mapping = ["transaction_id", "customer_id", "product_id","category",
                       "price", "quantity", "transaction_date",	"country"]
    df = pd.read_csv(file_name, usecols=columns_mapping)
    extract_datas = extract_datas(df)
    return extract_datas


extract_datas = extract_csv_file()
