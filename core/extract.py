import pandas as pd
import numpy as np
import os
import core.logs as log

from connectors.drive.operations import _get_service
from connectors.drive.operations import _get_file_id
from connectors.drive.operations import _download_file

#EXTRACT
def extract_excel_local(file_path):#estructura basica para pasar de df a un formato start schema

    DimCustomers = pd.read_excel(file_path, sheet_name="Customers", engine="openpyxl")
    DimProducts = pd.read_excel(file_path, sheet_name="Products", engine="openpyxl")
    DimStores = pd.read_excel(file_path, sheet_name="Stores", engine="openpyxl")
    FactTransactions = pd.read_excel(file_path, sheet_name="Transactions", engine="openpyxl")

    return DimCustomers, DimProducts, DimStores, FactTransactions

def extract(source="drive"):
    log.log_step("EXTRACT")
    filename="retail_sales_dataset.xlsx"
    credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")    
    EXTRACT_FOLDER_ID=os.getenv("EXTRACT_FOLDER_ID")
    
    service=_get_service(credentials_path)
    
    file_id = []
    file_id = _get_file_id(service,filename,EXTRACT_FOLDER_ID)
    
    buffer = _download_file(service, file_id)    
    
    return {
        "dim_customers": pd.read_excel(buffer, sheet_name="Customers"),        
        "dim_products": pd.read_excel(buffer, sheet_name="Products"),
        "dim_stores": pd.read_excel(buffer, sheet_name="Stores"),
        "fact_transactions": pd.read_excel(buffer, sheet_name="Transactions"),
    }# Se devuelve un dict donde la clave es dim o el fact y su value es el df correspondiente
