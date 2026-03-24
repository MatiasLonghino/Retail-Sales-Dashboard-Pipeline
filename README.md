# 📊 ETL Pipeline – Excel to Power BI Dashboards

## 📌 Overview
Este proyecto implementa un pipeline ETL desarrollado en Python que procesa datos provenientes de un archivo Excel (`.xlsx`), los limpia, transforma y los exporta en múltiples archivos `.csv` optimizados para su consumo en dashboards de Power BI.

El objetivo principal es simular un flujo de datos real dentro de un entorno de analítica, asegurando calidad, trazabilidad y escalabilidad del procesamiento.


---

## 🔄 Flujo ETL

El pipeline sigue las siguientes etapas:

### 1. Extract
- Lectura del archivo `.xlsx`
- Identificación de hojas relevantes

### 2. Validate
- Validación de esquema y estructura de datos
- Control de integridad y tipos

### 3. Transform
- Limpieza de datos (nulos, duplicados, formatos)
- Normalización
- Modelado en esquema tipo estrella:
  - Tablas de dimensión
  - Tabla de hechos

### 4. Load
- Exportación a archivos `.csv`
- Generación de logs del proceso

---

## 📁 Outputs

El pipeline genera los siguientes datasets:

- `dim_customers.csv`
- `dim_products.csv`
- `dim_stores.csv`
- `fact_transactions.csv`

Estos archivos están diseñados para ser consumidos directamente por Power BI.

---

## 📊 Visualización

El proyecto incluye **3 dashboards en Power BI** que consumen los datos procesados:

- 📈 Análisis de ventas  
- 🏬 Performance por tienda  
- 👥 Segmentación de clientes  

Estos dashboards permiten explorar métricas clave y facilitar la toma de decisiones basada en datos.
