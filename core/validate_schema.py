def check_columns(df, expected_columns, table_name):

    actual_columns = set(df.columns)
    expected_columns = set(expected_columns)

    missing = expected_columns - actual_columns
    extra = actual_columns - expected_columns

    issues = []

    if missing:
        issues.append(f"{table_name}: faltan columnas {missing}")

    if extra:
        issues.append(f"{table_name}: columnas extra detectadas {extra}")

    return issues
        
        
def validate_customers_schema(df):

    expected_columns = [
        "CustomerID",
        "FirstName",
        "LastName",
        "Gender",
        "BirthDate",
        "City",
        "JoinDate"
    ]

    return check_columns(df, expected_columns, "Customers")
    
def validate_products_schema(df):

    expected_columns = [
        "ProductID",
        "ProductName",
        "Category",
        "Subcategory",
        "UnitPrice",
        "CostPrice"
    ]
    return check_columns(df, expected_columns, "Products")
    
def validate_stores_schema(df):

    expected_columns = [
        "StoreID",
        "StoreName",
        "City",
        "Region"
    ]

    return check_columns(df, expected_columns, "Stores") 

def validate_transactions_schema(df):

    expected_columns = [
        "TransactionID",
        "Date",
        "CustomerID",
        "ProductID",
        "StoreID",
        "Quantity",
        "Discount",
        "PaymentMethod"
    ]

    return check_columns(df, expected_columns, "Transactions")

def validate_schemas(data: dict):
    return {
        "dim_customers": validate_customers_schema(data["dim_customers"]),
        "dim_products": validate_products_schema(data["dim_products"]),
        "dim_stores": validate_stores_schema(data["dim_stores"]),
        "fact_transactions": validate_transactions_schema(data["fact_transactions"]),
    }