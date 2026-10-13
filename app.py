import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
import base64

# Configuración de la página
st.set_page_config(
    page_title="AgroYaracuy | Mercado Digital",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa
EMPRESA_NOMBRE = "COMPANIA HCHFA CA"
EMPRESA_RIF = "J404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# Renderizado seguro del logo corporativo
logo_svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 120" width="380">
  <rect width="500" height="120" fill="#f8f9fa" rx="10"/>
  <circle cx="50" cy="60" r="35" fill="#2E7D32"/>
  <text x="50" y="70" font-family="Arial" font-size="30" fill="#ffffff" text-anchor="middle">🌾</text>
  <text x="100" y="50" font-family="Arial" font-size="20" font-weight="bold" fill="#1565C0">{EMPRESA_NOMBRE}</text>
  <text x="100" y="70" font-family="Arial" font-size="12" font-weight="bold" fill="#2E7D32">SECTOR AGROALIMENTARIO - AGROYARACUY</text>
  <line x1="100" y1="78" x2="460" y2="78" stroke="#FBC02D" stroke-width="2"/>
  <text x="100" y="98" font-family="monospace" font-size="14" font-weight="bold" fill="#333333">RIF: {EMPRESA_RIF}</text>
</svg>
"""

b64_logo = base64.b64encode(logo_svg.encode('utf-8')).decode("utf-8")
st.markdown(f'<div style="text-align: center;"><img src="data:image/svg+xml;base64,{b64_logo}"/></div>', unsafe_allow_html=True)
st.markdown("---")

# Base de datos en sesión
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []
if "ofertas" not in st.session_state:
    st.session_state.ofertas = []

# Menú lateral
menu = st.sidebar.selectbox("Seleccione su Rol:", [
    "🚜 Productor (Publicar Solicitud)", 
    "🏪 Agrotienda (Cotizar y Competir)", 
    "💳 Pasarela de Pago Móvil BDV"
])

# 1. MODULO PRODUCTOR
if menu == "🚜 Productor (Publicar Solicitud)":
    st.header("🚜 Publicar Requerimiento de Insumo")
    with st.form("form_productor"):
        nombre = st.text_input("Nombre del Productor / Finca:")
        municipio = st.selectbox("Municipio:", ["San Felipe", "Independencia", "Cocorote", "Bruzual", "Nirgua", "Urachiche", "Páez", "Veroes"])
        insumo = st.text_input("Insumo Requerido (Ej: Urea 50kg, Vacuna Aftosa):")
        cantidad = st.text_input("Cantidad necesaria:")
        telefono = st.text_input("WhatsApp de Contacto (Ej: 04121234567):")
        
        if st.form_submit_button("🚀 Lanzar Subasta") and nombre and insumo and telefono:
            nuevo_id = len(st.session_state.pedidos) + 1
            st.session_state.pedidos.append({
                "id": nuevo_id, "nombre": nombre, "municipio": municipio,
                "insumo": insumo, "cantidad": cantidad, "telefono": telefono
            })
            st.success(f"¡Solicitud #{nuevo_id} creada!")

    st.divider()
    st.subheader("📊 Cotizaciones Recibidas")
    for p in st.session_state.pedidos:
        st.markdown(f"**Solicitud #{p['id']}:** {p['insumo']} ({p['cantidad']}) - *{p['municipio']}*")
        ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
        for o in sorted(ofertas_p, key=lambda x: x["precio"]):
            c1, c2, c3 = st.columns([2, 2, 2])
            with c1: st.write(f"🏪 **{o['tienda']}**")
            with c2: st.write(f"💲 **${o['precio']:.2f} USD**")
            with c3:
                msg = f"Hola {o['tienda']}, acepto la oferta de ${o['precio']:.2f} para {p['insumo']}."
                url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                st.markdown(f"[💬 Contactar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
        st.divider()

# 2. MODULO AGROTIENDA
elif menu == "🏪 Agrotienda (Cotizar y Competir)":
    st.header("🏪 Panel para Agrotiendas")
    if not st.session_state.pedidos:
        st.info("No hay solicitudes activas por el momento.")
    else:
        for p in st.session_state.pedidos:
            with st.expander(f"🔔 Solicitud #{p['id']}: {p['insumo']} en {p['municipio']}"):
                with st.form(f"form_oferta_{p['id']}"):
                    tienda = st.text_input("Nombre de tu Agrotienda:")
                    precio = st.number_input("Precio Oferta USD ($):", min_value=0.0, format="%.2f")
                    tiempo = st.text_input("Tiempo de Entrega:")
                    tel_tienda = st.text_input("Tu WhatsApp (Ej: 04149998877):")
                    
                    if st.form_submit_button("💡 Enviar Cotización") and tienda and precio > 0:
                        st.session_state.ofertas.append({
                            "pedido_id": p['id'], "tienda": tienda,
                            "precio": precio, "tiempo": tiempo, "telefono_tienda": tel_tienda
                        })
                        st.success("¡Cotización enviada!")

# 3. PASARELA DE PAGO MÓVIL
elif menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil BDV")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"""
        ### 🏦 Datos Oficiales:
        * **Comercio:** {EMPRESA_NOMBRE}
        * **RIF:** {EMPRESA_RIF}
        * **Banco:** {EMPRESA_BANCO}
        * **Teléfono:** {EMPRESA_TELEFONO}
        """)
    with col2:
        with st.form("form_pago"):
            monto = st.number_input("Monto Pagado:", min_value=0.0, format="%.2f")
            referencia = st.text_input("Número de Referencia:")
            if st.form_submit_button("Confirmar Pago") and referencia and monto > 0:
                st.success("¡Pago registrado!")
                msg_pago = f"Hola, he realizado un Pago Móvil a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por ${monto:.2f}. Ref: {referencia}."
                url_pago_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                st.markdown(f"[📲 Enviar Comprobante]({url_pago_wa})", unsafe_allow_html=True)
