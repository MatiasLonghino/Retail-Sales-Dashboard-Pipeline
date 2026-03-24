import core.logs as log
import core.validate_schema as schema
from core.extract import extract
from core.transform import transform
from core.load import load
import os
from dotenv import load_dotenv


from  connectors.drive.operations import get_badId
from  connectors.drive.operations import delete_badId
from  connectors.drive.operations import clean_service_account_storage


def main():
    load_dotenv()
    log.log_step("ETL START")
    # =========================
    # EXTRACT
    # =========================
    raw_data  = extract("drive")        
    log.log_info("Customers extracted", raw_data["dim_customers"])
    log.log_info("Products extracted", raw_data["dim_products"])
    log.log_info("Stores extracted", raw_data["dim_stores"])
    log.log_info("Transactions extracted", raw_data["fact_transactions"])
    # =========================
    # VALIDATE SCHEMA
    # =========================
    log.log_step("SCHEMA VALIDATION")

    all_warnings = []

    results = schema.validate_schemas(raw_data)

    for table_name, issues in results.items():
        if issues:
            # Agregamos un prefijo para identificar la fuente
            formatted_issues = [f"[{table_name}] {msg}" for msg in issues]
            all_warnings.extend(formatted_issues)

    if all_warnings:
        log.log_warning("Se encontraron problemas de esquema:\n" + "\n".join(all_warnings))
    # =========================
    # TRANSFORM
    # =========================
    log.log_step("TRANSFORM")

    data_transformed =  transform(raw_data)

    log.log_info("Customers cleaned", data_transformed["dim_customers"])
    log.log_info("Products cleaned", data_transformed["dim_products"])
    log.log_info("Stores cleaned", data_transformed["dim_stores"])
    log.log_info("Transactions cleaned", data_transformed["fact_transactions"])

    # =========================
    # LOAD
    # =========================
    log.log_step("LOAD")
    load(data_transformed)
   
   
    log.log_step("ETL FINISHED")

def test():
    load_dotenv()
    #get_badId()
    #delete_badId()
    clean_service_account_storage()
    

if __name__ == "__main__":
    main()
    #test()
  