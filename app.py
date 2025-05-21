import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora Panadería", layout="centered")

st.title("🧁 Calculadora Interactiva - Punto de Equilibrio para Panadería Artesanal")

st.markdown("""
Esta calculadora te permite simular el comportamiento financiero de una panadería artesanal. 
Ajusta los valores a la izquierda para ver cómo varían los ingresos, costos, utilidad y punto de equilibrio.
""")

# Entradas del usuario
st.sidebar.header("🔧 Configura tu escenario")
costo_fijo = st.sidebar.number_input("Costo fijo mensual (COP)", value=500000, step=50000)
costo_variable = st.sidebar.number_input("Costo variable por pan (COP)", value=1000, step=100)
precio_venta = st.sidebar.number_input("Precio de venta por pan (COP)", value=2000, step=100)
cantidad = st.sidebar.slider("Cantidad de panes vendidos por mes", 0, 5000, 1000, step=100)

# Cálculos
ingresos = precio_venta * cantidad
costos_variables = costo_variable * cantidad
costos_totales = costos_variables + costo_fijo
utilidad = ingresos - costos_totales
margen_unitario = precio_venta - costo_variable
punto_equilibrio = costo_fijo / margen_unitario if margen_unitario > 0 else 0

# Resultados numéricos
st.subheader("📊 Resultados Financieros del Mes")
col1, col2 = st.columns(2)
with col1:
    st.metric("Ingresos", f"${ingresos:,.0f}")
    st.metric("Costos Totales", f"${costos_totales:,.0f}")
with col2:
    st.metric("Utilidad", f"${utilidad:,.0f}")
    st.metric("Punto de Equilibrio", f"{punto_equilibrio:.0f} panes")

# Mensaje visual
if cantidad < punto_equilibrio:
    st.warning("🚨 No has alcanzado el punto de equilibrio.")
else:
    st.success("✅ ¡Superaste el punto de equilibrio! La panadería es rentable.")

# Gráfico
st.subheader("📈 Análisis Visual")
cantidades = list(range(0, 5001, 100))
df = pd.DataFrame({
    "Cantidad vendida": cantidades,
    "Ingresos": [x * precio_venta for x in cantidades],
    "Costos totales": [costo_fijo + (x * costo_variable) for x in cantidades]
})
df["Utilidad"] = df["Ingresos"] - df["Costos totales"]

fig, ax = plt.subplots()
ax.plot(df["Cantidad vendida"], df["Ingresos"], label="Ingresos", color="green")
ax.plot(df["Cantidad vendida"], df["Costos totales"], label="Costos Totales", color="red")
ax.fill_between(df["Cantidad vendida"], df["Costos totales"], df["Ingresos"],
                where=(df["Ingresos"] > df["Costos totales"]),
                interpolate=True, color='green', alpha=0.2, label="Utilidad")
ax.axvline(punto_equilibrio, color="blue", linestyle="--", label=f"PE: {punto_equilibrio:.0f} panes")
ax.set_xlabel("Cantidad de Panes Vendidos")
ax.set_ylabel("Pesos (COP)")
ax.set_title("Ingresos vs Costos Totales")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("💡 *Puedes usar este gráfico en tu video para explicar el momento en que tu panadería comienza a generar ganancias.*")
