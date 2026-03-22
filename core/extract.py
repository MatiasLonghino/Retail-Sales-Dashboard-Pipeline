import pandas as pd
import numpy as np

#EXTRACT
def extract_excel_local(file_path):

    DimCustomers = pd.read_excel(file_path, sheet_name="Customers", engine="openpyxl")
    DimProducts = pd.read_excel(file_path, sheet_name="Products", engine="openpyxl")
    DimStores = pd.read_excel(file_path, sheet_name="Stores", engine="openpyxl")
    FactTransactions = pd.read_excel(file_path, sheet_name="Transactions", engine="openpyxl")

    return DimCustomers, DimProducts, DimStores, FactTransactions