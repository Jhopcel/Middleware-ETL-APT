import pandas as pd
# import time

def get_data_invoice():
    data = pd.read_csv('src/assets/data_sources/customer_shopping.csv', usecols=['invoice_no','category','quantity','price','payment_method','invoice_date','shopping_mall','customer_id','Product Name'])
    data_store = pd.read_csv('src/assets/data_sources/local_name.csv')
    
    data["store_id"] = 0
    # for index, store_name in data["shopping_mall"].items():
    #     for _,row in data_store.iterrows():
    #         if store_name == row["shopping_mall"]:
    #             data.loc[index, "store_id"] = row["quantity"]
    
    store_dict = {row["shopping_mall"]: row["quantity"] for _, row in data_store.iterrows()}
    for index, store_name in data["shopping_mall"].items():
        data.loc[index, "store_id"] = store_dict.get(store_name, None) 
    
    structure = ['invoice_no','category','quantity','Product Name','price','payment_method','invoice_date','store_id', 'customer_id']
    change_columns = ['invoice_no','category','quantity','product_name','price','payment_method','invoice_date','store_id', 'customer_id']
    data = data[structure]
    data.columns = change_columns

    return data.to_json()