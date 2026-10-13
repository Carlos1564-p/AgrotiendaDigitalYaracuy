import streamlit as st
import pandas as pd
import urllib.parse
from fpdf import FPDF
import base64

# Configuración de la página
st.set_page_config(
    page_title="AgroYaracuy & Región | Mercado Agrícola Digital",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa
EMPRESA_NOMBRE = "COMPANIA HCHFA CA"
EMPRESA_RIF = "J404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# ----------------------------------------------------
# 1. RENDERIZADO DEL LOGO CORPORATIVO SVG
# ----------------------------------------------------
logo_svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 130" width="100%">
  <rect width="550" height="130" fill="#f4f6f8" rx="12"/>
  <circle cx="65" cy="65" r="45" fill="#2E7D32"/>
  <text x="65" y="78" font-family="Arial" font-size="38" text-anchor="middle">🌾</text>
  <text x="130" y="52" font-family="Arial" font-size="21" font-weight="bold" fill="#1565C0">{EMPRESA_NOMBRE}</text>
  <text x="130" y="75" font-family="Arial" font-size="12" font-weight="bold" fill="#2E7D32">MERCADO BURSÁTIL Y DIGITAL DE INSUMOS AGRÍCOLAS</text>
  <line x1="130" y1="85" x2="510" y2="85" stroke="#FBC02D" stroke-width="3"/>
  <text x="130" y="108" font-family="monospace" font-size="14" font-weight="bold" fill="#333333">RIF: {EMPRESA_RIF} | Cobertura: Yaracuy - Lara - Carabobo</text>
</svg>
"""
b64_logo = base64.b64encode(logo_svg.encode('utf-8')).decode("utf-8")
st.markdown(f'<div style="text-align: center;"><img src="data:image/svg+xml;base64,{b64_logo}"/></div>', unsafe_allow_html=True)
st.markdown("---")

# ----------------------------------------------------
# 2. INICIALIZACIÓN DE ESTADOS (Base de Datos en Memoria)
# ----------------------------------------------------
if "pedidos" not in st.session_state:
    st.session_state.pedidos = []
if "ofertas" not in st.session_state:
    st.session_state.ofertas = []
if "agrotiendas_registradas" not in st.session_state:
    st.session_state.agrotiendas_registradas = [
        {"nombre": "Agroinsumos San Felipe C.A.", "estado": "Yaracuy", "municipio": "San Felipe", "telefono": "584121234567"},
        {"nombre": "Agrotienda El Semillero Barquisimeto", "estado": "Lara", "municipio": "Iribarren", "telefono": "584149876543"},
        {"nombre": "Distribuidora Agropecuaria Carabobo", "estado": "Carabobo", "municipio": "Valencia", "telefono": "584167654321"}
    ]

# ----------------------------------------------------
# 3. MENÚ DE NAVEGACIÓN PRINCIPAL
# ----------------------------------------------------
menu = st.sidebar.selectbox("Seleccione el Módulo del Sistema:", [
    "📖 Reseña, Objetivos y Beneficios",
    "🚜 Menú de Requerimientos del Campo",
    "📝 Afiliación de Agrotiendas (Contrato)",
    "🛒 Subasta y Oferta (Productor)",
    "🏪 Panel de Cotización (Agrotiendas)",
    "💳 Pasarela de Pago Móvil BDV"
])

# ----------------------------------------------------
# MÓDULO 1: RESEÑA, OBJETIVOS Y BENEFICIOS
# ----------------------------------------------------
if menu == "📖 Reseña, Objetivos y Beneficios":
    st.header("📖 Reseña Corporativa e Institucional")
    st.markdown(f"""
    **{EMPRESA_NOMBRE}** (RIF: **{EMPRESA_RIF}**)[cite: 1] es una entidad jurídica constituida para transformar la comercialización de insumos del sector primario a través de la marca digital **AgroYaracuy y Región Central**. Operamos bajo un modelo de mercado de oferta y demanda y corretaje agrícola digital, interconectando de forma transparente los valles productivos de **Yaracuy, Lara y Carabobo**.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Objetivo Central")
        st.write("""
        Minimizar el tiempo de inactividad de los productores del campo, eliminar la intermediación abusiva y optimizar los costos logísticos (combustible y traslados innecesarios) mediante un sistema de subasta inversa donde las agrotiendas compiten abiertamente ofreciendo el mejor precio del mercado.
        """)
    with col2:
        st.subheader("🌟 Beneficios Clave")
        st.write("""
        * **Para el Productor:** Ahorro financiero, inmediatez en emergencias y el mejor precio sin recorrer múltiples municipios.
        * **Para la Agrotienda:** Canales de venta directos con clientes de alta intención de compra y optimización de inventario.
        * **Para la Región Central:** Dinamización transparente del agro-comercio interconectando Yaracuy, Lara y Carabobo.
        """)

# ----------------------------------------------------
# MÓDULO 2: MENÚ DE REQUERIMIENTOS MÁS IMPORTANTES DEL CAMPO
# ----------------------------------------------------
elif menu == "🚜 Menú de Requerimientos del Campo":
    st.header("📋 Directorio de Insumos y Urgencias Agrícolas")
    st.markdown("Seleccione o consulte las categorías críticas de alta demanda en el campo:")
    
    requerimientos = {
        "Fertilizantes y Nutrición de Suelos": "Urea, Nitrato de Amonio, NPK y enmiendas calcáreas esenciales para cultivos de maíz, caña y hortalizas.",
        "Sanidad y Vacunación Animal": "Vacunas contra Aftosa, Rabia Silvestre, complejos vitamínicos y antibióticos de uso veterinario bovino/porcino.",
        "Agroquímicos y Control de Plagas": "Herbicidas sistémicos (Glifosato), insecticidas y fungicidas para protección preventiva y curativa.",
        "Maquinaria y Repuestos Críticos": "Correas de transmisión, filtros de aceite/combustible, mangueras de alta presión y puntas de discos para tractores.",
        "Semillas Certificadas": "Material genético certificado de maíz, caraota, sorgo y leguminosas adaptadas al trópico venezolano."
    }
    
    for categoria, desc in requerimientos.items():
        with st.expander(f"📦 {categoria}"):
            st.write(desc)
            if st.button(f"Publicar urgencia de: {categoria}", key=f"btn_{categoria}"):
                st.info(f"Diríjase a la sección '🛒 Subasta y Oferta (Productor)' para cotizar {categoria}.")

# ----------------------------------------------------
# MÓDULO 3: AFILIACIÓN DE AGROTIENDAS Y CONTRATO LEGAL
# ----------------------------------------------------
elif menu == "📝 Afiliación de Agrotiendas (Contrato)":
    st.header("📝 Contrato de Adhesión y Corretaje Digital Mercantil")
    
    with st.expander("🔍 Leer Términos Legales del Contrato (Haz clic para expandir)", expanded=False):
        st.markdown(f"""
        **CONTRATO DE ADHESIÓN - {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF})**[cite: 1]
        
        **PRIMERA (PARTES):** Se celebra entre {EMPRESA_NOMBRE} y la Agrotienda adherente, rigiéndose por el Código de Comercio venezolano y la Ley de Mensajes de Datos y Firmas Electrónicas.
        **SEGUNDA (OBJETO):** La plataforma opera como un mercado digital de oferta y demanda agrícola en los estados Yaracuy, Lara y Carabobo.
        **TERCERA (CONDICIONES):** La agrotienda se compromete a mantener precios competitivos y veraces. Las transacciones financieras usan exclusivamente la cuenta de {EMPRESA_NOMBRE} ({EMPRESA_BANCO}, Pagomóvil: {EMPRESA_TELEFONO})[cite: 1].
        """)

    st.markdown("### ✍️ Formulario de Incorporación y Firma Digital")
    with st.form("form_afiliacion"):
        nombre_tienda = st.text_input("Nombre de la Agrotienda / Empresa:")
        rif_tienda = st.text_input("RIF de la Agrotienda:")
        estado_tienda = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_tienda = st.text_input("Municipio / Localidad:")
        telefono_tienda = st.text_input("Teléfono WhatsApp de Contacto:")
        
        acepta_contrato = st.checkbox("✅ Acepto de forma libre, consciente y legal los términos del Contrato de Adhesión y Corretaje Digital de COMPANIA HCHFA CA.")
        
        btn_afiliar = st.form_submit_button("Firmar Adhesión e Incorporarse al Sistema")
        
        if btn_afiliar:
            if acepta_contrato and nombre_tienda and rif_tienda and telefono_tienda:
                st.session_state.agrotiendas_registradas.append({
                    "nombre": nombre_tienda, "estado": estado_tienda,
                    "municipio": municipio_tienda, "telefono": telefono_tienda
                })
                st.success(f"¡Felicidades! {nombre_tienda} ha sido afiliada exitosamente al mercado digital con respaldo de {EMPRESA_NOMBRE}.")
            elif not acepta_contrato:
                st.error("Debe marcar la casilla de aceptación de condiciones para formalizar el contrato.")
            else:
                st.error("Por favor complete todos los datos requeridos.")

# ----------------------------------------------------
# MÓDULO 4: SUBASTA Y OFERTA (PRODUCTOR)
# ----------------------------------------------------
elif menu == "🛒 Subasta y Oferta (Productor)":
    st.header("🛒 Módulo de Demanda y Subasta del Productor")
    st.markdown("Publique su requerimiento para que todas las agrotiendas registradas en **Yaracuy, Lara y Carabobo** compitan por ofrecerle el mejor precio.")
    
    with st.form("form_productor_robusto"):
        nombre_prod = st.text_input("Nombre del Productor / Finca:")
        estado_prod = st.selectbox("Estado de Ubicación:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_prod = st.text_input("Municipio:")
        insumo_req = st.text_input("Insumo / Repuesto Requerido:")
        cant_req = st.text_input("Cantidad (Ej: 10 sacos, 2 filtros):")
        tel_prod = st.text_input("WhatsApp de Contacto:")
        
        if st.form_submit_button("🚀 Lanzar Subasta Regional") and nombre_prod and insumo_req and tel_prod:
            pid = len(st.session_state.pedidos) + 1
            st.session_state.pedidos.append({
                "id": pid, "nombre": nombre_prod, "estado": estado_prod,
                "municipio": municipio_prod, "insumo": insumo_req, "cantidad": cant_req, "telefono": tel_prod
            })
            st.success(f"¡Subasta #{pid} emitida con éxito a la red de agrotiendas!")

    st.divider()
    st.subheader("📊 Seguimiento de Ofertas y Precios Competitivos")
    if not st.session_state.pedidos:
        st.info("No hay solicitudes de compra activas en este momento.")
    else:
        for p in st.session_state.pedidos:
            st.markdown(f"**Solicitud #{p['id']} ({p['estado']} - {p['municipio']}):** {p['insumo']} ({p['cantidad']})")
            ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
            if not ofertas_p:
                st.caption("_Esperando cotizaciones de las agrotiendas de la región..._")
            else:
                for o in sorted(ofertas_p, key=lambda x: x["precio"]):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1: st.write(f"🏪 **{o['tienda']}** ({o['estado_tienda']})")
                    with c2: st.write(f"💲 **${o['precio']:.2f} USD** | {o['tiempo']}")
                    with c3:
                        msg = f"Hola {o['tienda']}, acepto su oferta de ${o['precio']:.2f} para el insumo {p['insumo']} a través de AgroYaracuy."
                        url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                        st.markdown(f"[💬 Comprar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
            st.divider()

# ----------------------------------------------------
# MÓDULO 5: PANEL DE COTIZACIÓN (AGROTIENDAS)
# ----------------------------------------------------
elif menu == "🏪 Panel de Cotización (Agrotiendas)":
    st.header("🏪 Panel de Competencia de Precios (Agrotiendas)")
    st.markdown("Agrotiendas afiliadas en **Yaracuy, Lara y Carabobo**: visualicen las solicitudes y envíen sus ofertas.")
    
    if not st.session_state.pedidos:
        st.warning("No hay solicitudes de productores activas actualmente.")
    else:
        for p in st.session_state.pedidos:
            with st.container():
                st.markdown(f"### 🔔 Requerimiento #{p['id']} - [{p['estado']}] Municipio {p['municipio']}")
                st.write(f"**Productor:** {p['nombre']} | **Insumo:** {p['insumo']} | **Cantidad:** {p['cantidad']}")
                
                with st.form(f"form_cotizar_{p['id']}"):
                    t_nombre = st.text_input("Nombre de su Agrotienda:", key=f"tn_{p['id']}")
                    t_estado = st.selectbox("Estado de su Tienda:", ["Yaracuy", "Lara", "Carabobo"], key=f"te_{p['id']}")
                    t_precio = st.number_input("Precio Total Ofertado (USD $):", min_value=0.0, format="%.2f", key=f"tp_{p['id']}")
                    t_tiempo = st.text_input("Disponibilidad / Entrega:", key=f"tt_{p['id']}")
                    t_tel = st.text_input("Su WhatsApp comercial:", key=f"tel_{p['id']}")
                    
                    if st.form_submit_button("💡 Enviar Oferta Competitiva") and t_nombre and t_precio > 0:
                        st.session_state.ofertas.append({
                            "pedido_id": p['id'], "tienda": t_nombre, "estado_tienda": t_estado,
                            "precio": t_precio, "tiempo": t_tiempo, "telefono_tienda": t_tel
                        })
                        st.success("¡Oferta publicada exitosamente en la red regional!")
                st.divider()

# ----------------------------------------------------
# MÓDULO 6: PASARELA DE PAGO MÓVIL BDV
# ----------------------------------------------------
elif menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial")
    st.markdown("Procesamiento seguro respaldado por los datos fiscales de la empresa operadora.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"""
        ### 🏦 Datos Bancarios Oficiales:
        * **Razón Social:** {EMPRESA_NOMBRE}
        * **RIF:** {EMPRESA_RIF}[cite: 1]
        * **Banco:** {EMPRESA_BANCO}[cite: 1]
        * **Teléfono Pago Móvil:** {EMPRESA_TELEFONO}[cite: 1]
        """)
    with col2:
        st.markdown("### 📋 Validar Pago o Reserva")
        with st.form("form_pago_robusto"):
            monto_p = st.number_input("Monto a pagar:", min_value=0.0, format="%.2f")
            ref_p = st.text_input("Número de Referencia Bancaria:")
            banco_orig = st.text_input("Banco de Origen:")
            
            if st.form_submit_button("Confirmar Transacción") and ref_p and monto_p > 0:
                st.success("¡Pago reportado y validado en el sistema!")
                msg_pago = f"Hola, he realizado un Pago Móvil a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por un monto de ${monto_p:.2f}. Referencia: {ref_p}."
                url_pago_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                st.markdown(f"[📲 Enviar Comprobante vía WhatsApp]({url_pago_wa})", unsafe_allow_html=True)
            elif st.form_submit_button("Confirmar Transacción"):
                st.error("Ingrese un monto válido y el número de referencia.")
