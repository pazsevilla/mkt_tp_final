# 💡 TP Final – Ecosistema de Datos Comercial (Data Warehouse + STAR Schema)

Trabajo Práctico Final de la materia **Introducción al Marketing Online y los Negocios Digitales** – Universidad Austral (2025).

---

## 🎯 Objetivo del Trabajo

Diseñar e implementar un **mini–ecosistema de datos comercial (online + offline)** para la empresa ficticia *EcoBottle*, construir un **pipeline ETL** en Python y generar un **Data Warehouse dimensional (STAR SCHEMA)** listo para análisis y visualización de KPIs clave del negocio:

- Ventas totales  
- Usuarios activos  
- Ticket promedio  
- Ventas por provincia  
- Ranking mensual por producto  
- NPS

Las fuentes de datos provienen de 13 archivos `.csv` con información de clientes, pedidos, productos, pagos, envíos, sesiones web y respuestas NPS.

Este repositorio contiene el código necesario para transformar los datos crudos en un Data Warehouse, exportado como CSV dentro de `warehouse/`, listo para su uso en herramientas BI como **Looker Studio o Power BI**.

---
## Diagrama Entidad Relación - OLTP
<img width="5286" height="4258" alt="DER (2)" src="https://github.com/user-attachments/assets/26f097e7-a66b-414c-9f70-372ca59da4e1" />

---
## 🧱 Arquitectura del Proyecto
```mkt_tp_final/
│
├── raw/ # Datos transaccionales crudos (.csv)
│
├── etl/
│ ├── extract/ # Lectura de fuentes raw
│ ├── transform/ # Limpieza + surrogate keys + joins
│ ├── load/ # Exportación al Data Warehouse
│
├── warehouse/ # ✅ Data Warehouse final
│ ├── dim/ # Dimensiones transformadas
│ └── fact/ # Tablas de hechos transformadas
│
└── main.py # Orquestador del pipeline ETL
```

---

## ⚙️ Descripción del Pipeline ETL

### ✅ 1) Extract
Lectura automática de los 13 archivos CSV desde `/raw/` usando Pandas.

### ✅ 2) Transform
- Limpieza de datos y estandarización  
- Conversión de fechas y tipos
- Generación de **surrogate keys (PK artificiales)**
- Reemplazo de IDs naturales por SK (en hechos)
- Desnormalización para STAR SCHEMA
- Construcción de dimensiones y hechos

### ✅ 3) Load
Exporta los resultados a:
warehouse/
├── dim/
└── fact/

Cada archivo CSV generado está listo para ser usado en una herramienta BI.

---

## 🌟 Modelo Estrella (STAR SCHEMA)

### 📌 Dimensiones generadas

| Tabla | Contenido | Primary Key |
|-------|-----------|-------------|
| `dim_date` | calendario (día, mes, año, trimestre, nombre del día) | `date_sk` |
| `dim_customer` | datos de clientes | `customer_sk` |
| `dim_product` | producto + categoría desnormalizada | `product_sk` |
| `dim_channel` | canales de venta | `channel_sk` |
| `dim_address` | direcciones + ciudad + provincia | `address_sk` |
| `dim_store` | tiendas físicas + dirección y provincia | `store_sk` |

---

### 📌 Tablas de Hechos
| Tabla | Grain | Primary Key (Surrogate) | Métricas principales |
|-------|-------|-------------------------|----------------------|
| `fact_sales_order` | una fila por orden | `sales_order_sk` | subtotal, impuestos, total, shipping_fee |
| `fact_sales_order_item` | una fila por producto dentro de una orden | `order_item_sk` | cantidad, precio unitario, descuentos, total línea |
| `fact_payment` | una fila por transacción | `payment_sk` | monto, método, estado |
| `fact_shipment` | una fila por envío | `shipment_sk` | estado, carrier, shipping cost, fechas |
| `fact_web_session` | una fila por sesión | `session_sk` | canal, dispositivo, fechas inicio/fin |
| `fact_nps_response` | una fila por respuesta NPS | `nps_sk` | score, comentario, canal |

---

## ✅ Ejecución

### 1️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2️⃣ Ejecutar el pipeline completo
```
python main.py
```

Al finalizar, la consola mostrará:

✅ DW (STAR SCHEMA) generado: dimensiones y hechos exportados a warehouse/


Las carpetas warehouse/dim/ y warehouse/fact/ contendrán todos los CSV transformados.

### 📊 Dashboard 

El modelo resultante permite analizar:

-Ventas totales ($)

-Usuarios activos

-Ticket promedio

-Ventas por provincia y canal

-Ranking mensual de productos

-Distribución y tendencia de NPS

-Métricas logísticas (envíos y pagos)

### ✅ Entregables de este repositorio

✔ Pipeline ETL completo (extract → transform → load)

✔ Modelo dimensional según Kimball (STAR SCHEMA)

✔ Tablas CSV finales listas para BI

✔ Código modular, limpio y reproducible

✔ Ejecución desde consola mediante main.py

### 🧾 Autoría

Proyecto desarrollado por Paz Sevilla, Licenciatura en Ciencia de Datos – Universidad Austral (2025).
Los archivos raw provienen del repositorio académico provisto por la cátedra y fueron utilizados únicamente con fines educativos.



