import src.etl as etl
import src.logs as lg

import src.validate_schema as vs


FILE_PATH = "dataset/retail_sales_dataset.xlsx"


def main():

    lg.log_step("ETL START")

    # =========================
    # EXTRACT
    # =========================
    lg.log_step("EXTRACT")

    DimCustomers, DimProducts, DimStores, FactTransactions = etl.extract_excel(FILE_PATH)

    lg.log_info("Customers extracted", DimCustomers)
    lg.log_info("Products extracted", DimProducts)
    lg.log_info("Stores extracted", DimStores)
    lg.log_info("Transactions extracted", FactTransactions)

    # =========================
    # VALIDATE SCHEMA
    # =========================
    lg.log_step("SCHEMA VALIDATION")

    warnings = []

    validations = [
        vs.validate_customers_schema(DimCustomers),
        vs.validate_products_schema(DimProducts),
        vs.validate_stores_schema(DimStores),
        vs.validate_transactions_schema(FactTransactions)
    ]

    for result in validations:
            warnings.extend(result)

    if warnings:
        lg.log_warning("\n".join(warnings))

    # =========================
    # TRANSFORM
    # =========================
    lg.log_step("TRANSFORM")

    DimCustomers_clean = etl.clean_customers(DimCustomers)
    DimProducts_clean = etl.clean_products(DimProducts)
    DimStores_clean = etl.clean_stores(DimStores)
    FactTransactions_clean = etl.clean_transactions(FactTransactions)

    lg.log_info("Customers cleaned", DimCustomers_clean)
    lg.log_info("Products cleaned", DimProducts_clean)
    lg.log_info("Stores cleaned", DimStores_clean)
    lg.log_info("Transactions cleaned", FactTransactions_clean)

    # =========================
    # LOAD
    # =========================
    lg.log_step("LOAD")

    etl.save_csv(DimCustomers_clean, "dataset/clean_dataset/dim_customers.csv")
    etl.save_csv(DimProducts_clean, "dataset/clean_dataset/dim_products.csv")
    etl.save_csv(DimStores_clean, "dataset/clean_dataset/dim_stores.csv")
    etl.save_csv(FactTransactions_clean, "dataset/clean_dataset/fact_transactions.csv")

    lg.log_step("ETL FINISHED")


if __name__ == "__main__":
    main()