
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF

# --- Funciones para cálculos ---
def calcular_punto_equilibrio(costo_fijo, costo_variable, precio_venta):
    return costo_fijo / (precio_venta - costo_variable)

def calcular_ingreso(cantidad, precio_venta):
    return cantidad * precio_venta

def calcular_costo_total(costo_fijo, costo_variable, cantidad):
    return costo_fijo + costo_variable * cantidad

def calcular_utilidad(ingreso, costo_total):
    return ingreso - costo_total

# --- Función para crear reporte PDF ---
def crear_reporte_pdf(costo_fijo, costo_variable, precio_venta, punto_eq, max_cantidad):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "📊 Reporte de Punto de Equilibrio - Panadería Artesanal 🥖", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, f"🏷️ Costo fijo mensual: ${costo_fijo:,.0f}", ln=True)
    pdf.cell(0, 10, f"🥐 Costo variable por unidad: ${costo_variable:,.0f}", ln=True)
    pdf.cell(0, 10, f"💰 Precio de venta por unidad: ${precio_venta:,.0f}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"📈 Punto de equilibrio en unidades: {punto_eq:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "🧮 Resumen de ingresos, costos y utilidades:", ln=True)
    pdf.ln(5)

    # Tabla simple
    pdf.cell(40, 10, "Cantidad", border=1)
    pdf.cell(50, 10, "Ingreso ($)", border=1)
    pdf.cell(50, 10, "Costo total ($)", border=1)
    pdf.cell(50, 10, "Utilidad ($)", border=1)
    pdf.ln()

    for cantidad in range(0, max_cantidad+1, max(1, int(max_cantidad/5))):
        ingreso = calcular_ingreso(cantidad, precio_venta)
        costo_total = calcular_costo_total(costo_fijo, costo_variable, cantidad)
        utilidad = calcular_utilidad(ingreso, costo_total)

        pdf.cell(40, 10, f"{cantidad}", border=1)
        pdf.cell(50, 10, f"{ingreso:,.0f}", border=1)
        pdf.cell(50, 10, f"{costo_total:,.0f}", border=1)
        pdf.cell(50, 10, f"{utilidad:,.0f}", border=1)
        pdf.ln()

    # Guardar PDF en bytes
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

# --- Título y descripción ---
st.title("🥖 Calculadora Punto de Equilibrio - Panadería Artesanal 🥐")
st.write("""
Esta calculadora 📊 permite analizar la viabilidad económica de tu panadería artesanal 🥖, 
calculando el punto de equilibrio 📈 y mostrando gráficos interactivos y tablas resumen 🧾.
""")

# --- Entradas interactivas ---
costo_fijo = st.number_input("🏷️ Costo fijo mensual (COP)", min_value=0, value=500000, step=10000)
costo_variable = st.number_input("🥐 Costo variable por unidad (COP)", min_value=0, value=1000, step=100)
precio_venta = st.number_input("💰 Precio de venta por unidad (COP)", min_value=0, value=2000, step=100)
max_cantidad = st.slider("📊 Cantidad máxima para análisis", min_value=1000, max_value=20000, value=10000, step=500)

if precio_venta <= costo_variable:
    st.error("⚠️ El precio de venta debe ser mayor que el costo variable para calcular el punto de equilibrio.")
else:
    # --- Cálculos ---
    punto_eq = calcular_punto_equilibrio(costo_fijo, costo_variable, precio_venta)

    st.subheader("📈 Resultados")
    st.write(f"📌 **Punto de equilibrio:** {punto_eq:.2f} unidades")

    # --- Análisis de sensibilidad ---
    st.subheader("🔍 Análisis de sensibilidad")

    variacion_precio = np.arange(precio_venta*0.8, precio_venta*1.2, (precio_venta*0.4)/10)
    variacion_costo = np.arange(costo_variable*0.8, costo_variable*1.2, (costo_variable*0.4)/10)

    sensibilidad_precio = [calcular_punto_equilibrio(costo_fijo, costo_variable, p) for p in variacion_precio]
    sensibilidad_costo = [calcular_punto_equilibrio(costo_fijo, c, precio_venta) for c in variacion_costo]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=variacion_precio, y=sensibilidad_precio, mode='lines+markers', name='Variación Precio 💰'))
    fig.add_trace(go.Scatter(x=variacion_costo, y=sensibilidad_costo, mode='lines+markers', name='Variación Costo Variable 🥐'))
    fig.update_layout(
        title="Análisis de sensibilidad del Punto de Equilibrio 🧮",
        xaxis_title="Precio de Venta o Costo Variable (COP)",
        yaxis_title="Punto de Equilibrio (unidades)",
        legend_title="Parámetros",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Tabla resumen ---
    st.subheader("🧾 Tabla resumen de ingresos, costos y utilidades")

    cantidades = np.arange(0, max_cantidad+1, max(1, int(max_cantidad/20)))
    data = {
        "Cantidad": cantidades,
        "Ingreso (COP)": [calcular_ingreso(q, precio_venta) for q in cantidades],
        "Costo Total (COP)": [calcular_costo_total(costo_fijo, costo_variable, q) for q in cantidades],
        "Utilidad (COP)": [calcular_utilidad(calcular_ingreso(q, precio_venta), calcular_costo_total(costo_fijo, costo_variable, q)) for q in cantidades]
    }
    df = pd.DataFrame(data)
    st.dataframe(df.style.format("{:,.0f}"))

    # --- Gráfico ingresos, costos y utilidades ---
    st.subheader("📊 Gráficos de Ingresos, Costos y Utilidades")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Cantidad"], y=df["Ingreso (COP)"], mode='lines', name='Ingreso 💰'))
    fig2.add_trace(go.Scatter(x=df["Cantidad"], y=df["Costo Total (COP)"], mode='lines', name='Costo Total 🥐'))
    fig2.add_trace(go.Scatter(x=df["Cantidad"], y=df["Utilidad (COP)"], mode='lines', name='Utilidad 📈'))
    fig2.add_vline(x=punto_eq, line_dash="dash", line_color="red", annotation_text="Punto de Equilibrio ⚖️", annotation_position="top right")
    fig2.update_layout(xaxis_title="Cantidad de panes 🥖", yaxis_title="COP", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

    # --- Explicaciones ---
    st.subheader("❓ ¿Qué es el Punto de Equilibrio?")
    st.write("""
    El punto de equilibrio ⚖️ es la cantidad mínima de unidades que debes vender para cubrir todos tus costos (fijos y variables).
    A partir de ese punto, tu negocio comienza a generar ganancias 💵.
    """)

    st.subheader("💡 ¿Por qué es importante?")
    st.write("""
    Entender el punto de equilibrio te ayuda a tomar decisiones informadas sobre precios, costos y metas de venta.
    Así puedes garantizar la rentabilidad y sostenibilidad de tu panadería artesanal 🥖.
    """)

    # --- Botón para descargar reporte ---
    st.subheader("📥 Descarga tu reporte")
    if st.button("Generar y descargar reporte PDF"):
        pdf_file = crear_reporte_pdf(costo_fijo, costo_variable, precio_venta, punto_eq, max_cantidad)
        st.download_button(
            label="Descargar reporte PDF 📄",
            data=pdf_file,
            file_name="Reporte_Punto_Equilibrio_Panaderia.pdf",
            mime="application/pdf"
        )
