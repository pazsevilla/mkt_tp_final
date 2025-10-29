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

## 🧱 Arquitectura del Proyecto

