import pandas as pd
import numpy as np

#TRANSFORM

def clean_customers(df):
    # 1. Copia profunda para evitar SettingWithCopyWarning
    df = df.drop_duplicates().copy()

    # 2. Manejo de nulos antes de convertir a string (evita que NaN se vuelva la palabra "nan")
    for col in ["FirstName", "LastName"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip().str.title()

    # 3. Limpieza de Género corregida
    df["Gender"] = df["Gender"].astype(str).str.strip().str.upper()
    df.loc[~df["Gender"].isin(["M", "F"]), "Gender"] = "Unknown"

    # 4. Fechas con coerce para evitar errores por formatos extraños
    df["BirthDate"] = pd.to_datetime(df["BirthDate"], errors='coerce')
    df["JoinDate"] = pd.to_datetime(df["JoinDate"], errors='coerce')

    return df

def clean_products(df):
    df = df.drop_duplicates().copy()

    # Usamos .title() para nombres de productos (mejor que .capitalize() para nombres compuestos)
    cols_to_fix = ["ProductName", "Category", "SubCategory"]
    for col in cols_to_fix:
        df[col] = df[col].fillna("Other").astype(str).str.strip().str.title()

    # 5. to_numeric es más seguro que .astype(float) si hay textos accidentales
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors='coerce')
    df["CostPrice"] = pd.to_numeric(df["CostPrice"], errors='coerce')

    return df

def clean_stores(df):
    df = df.drop_duplicates().copy()

    for col in ["StoreName", "City", "Region"]:
        df[col] = df[col].fillna("N/A").astype(str).str.strip().str.title()

    return df

def clean_transactions(df):
    df = df.drop_duplicates().copy()

    # 6. Conversión robusta de tipos
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")

    # 7. Lógica de negocio: Cantidades lógicas
    # Si la cantidad es <= 0 o nula, podrías querer eliminar la fila o poner un default
    df = df[df["Quantity"] > 0].copy() 

    # 8. Normalización de Descuento (Asegurar que sea entre 0 y 1)
    df["Discount"] = df["Discount"].abs()
    # Si el descuento es > 1 (ej: 15%), lo convertimos a decimal (0.15)
    df.loc[df["Discount"] > 1, "Discount"] = df["Discount"] / 100
    # Si aún así es ilógico (> 1), lo marcamos como 0
    df.loc[df["Discount"] > 1, "Discount"] = 0

    df["PaymentMethod"] = df["PaymentMethod"].fillna("Other").astype(str).str.strip().str.title()

    return df

