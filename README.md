# 💡 TP Final – Ecosistema de Datos Comercial EcoBottle

Trabajo Práctico Final de la materia Introducción al Marketing Online y los Negocios Digitales – Universidad Austral (2025).

---

## 🎯 Objetivo del Trabajo

Diseñar e implementar un mini–ecosistema de datos comercial (online + offline) para la empresa ficticia *EcoBottle*, construir un pipeline ETL en Python y generar un Data Warehouse dimensional (STAR SCHEMA) listo para análisis y visualización de KPIs clave del negocio:

- Ventas totales  
- Usuarios activos  
- Ticket promedio  
- Ventas por provincia  
- Ranking mensual por producto  
- NPS

Las fuentes de datos provienen de 13 archivos `.csv` con información de clientes, pedidos, productos, pagos, envíos, sesiones web y respuestas NPS.

Este repositorio contiene el código necesario para transformar los datos crudos en un Data Warehouse, exportado como CSV dentro de `warehouse/`, listo para su uso en herramientas BI como Power BI.

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
- Generación de surrogate keys
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
| `dim_channel` | canales de venta (Online/Offline) | `channel_sk` |
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
## 🌟 Diagramas Star Schema 

### Fact Sales Order

<img width="710" height="748" alt="Captura de pantalla (236)" src="https://github.com/user-attachments/assets/d96245e4-d63d-4c96-b85d-cd7be1cacdda" />

### Fact Sales Order Item

<img width="610" height="740" alt="stars_schema fact_sales_order_item" src="https://github.com/user-attachments/assets/e35fa284-9dd3-4a19-a360-71db714b4bcc" />

### Fact Web Session

<img width="968" height="733" alt="Captura de pantalla (232)" src="https://github.com/user-attachments/assets/645c2294-344f-49f7-8ecb-28de7c42d147" />

### Fact Payment

<img width="763" height="768" alt="Captura de pantalla (237)" src="https://github.com/user-attachments/assets/f0a37880-dbfe-4513-acf5-9a5c92ffabe5" />

### Fact Shipment

<img width="635" height="628" alt="star_schema fact_shipment" src="https://github.com/user-attachments/assets/5074d106-a23f-4960-a26d-0206a169dcba" />

### Fact Nps Response 

<img width="957" height="768" alt="Captura de pantalla (238)" src="https://github.com/user-attachments/assets/f1fe5fa6-1f01-4eac-8762-9c2f16af5dfe" />

---

## ✅ Ejecución

### 1️⃣ **Clonar el repositorio:**
  ```bash9
  git clone [https://github.com/pazsevilla/mkt_tp_final.git](https://github.com/Paz-Sevilla/mkt_tp_final.git)
  cd mkt_tp_final
  ```
    
### 2️⃣ **Crear y activar un entorno virtual**:
  ```bash
  # En Windows (cmd)
  python -m venv .venv
   .\.venv\Scripts\activate
  ```

### 3️⃣ **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Ejecutar el pipeline completo:**
```
python main.py
```

Al finalizar, la consola mostrará:

✅ DW (STAR SCHEMA) generado: dimensiones y hechos exportados a warehouse/


Las carpetas warehouse/dim/ y warehouse/fact/ contendrán todos los CSV transformados.

### 📊 Dashboard 
**Ver Dashboard Final intercativo (PowerBI):** [Click aqui para ver la Dashboard](https://app.powerbi.com/groups/me/reports/675366ca-9b80-4303-a7cb-570463e94976/592406c330bb7948db19?experience=power-bi)

El modelo resultante permite analizar:

-Ventas totales ($)

-Usuarios activos

-Ticket promedio

-Ventas por provincia y canal

-Ranking mensual de productos

-Distribución y tendencia de NPS

-Métricas de clientes (activos, recompra, top clientes)

### ✅ Entregables de este repositorio

✔ Pipeline ETL completo (extract → transform → load)

✔ Modelo dimensional según Kimball (STAR SCHEMA)

✔ Tablas CSV finales listas para BI

✔ Código modular, limpio y reproducible

✔ Ejecución desde consola mediante main.py

✔ Dashboard interactivo en Power BI

✔ Documentación del proyecto

### 🧾 Autoría

Proyecto desarrollado por Paz Sevilla, Licenciatura en Ciencia de Datos – Universidad Austral (2025).
Los archivos raw provienen del repositorio académico provisto por la cátedra y fueron utilizados únicamente con fines educativos.



