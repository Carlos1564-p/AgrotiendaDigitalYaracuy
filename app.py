import streamlit as st
import pandas as pd
import urllib.parse
from os import path
from fpdf import FPDF

# Configuración de la página
st.set_page_config(
    page_title="AgroYaracuy & Región | Mercado Agrícola Digital",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa
EMPRESA_NOMBRE = "COMPAÑÍA HCHF4 C.A."
EMPRESA_RIF = "J-404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# ----------------------------------------------------
# SECCIÓN CORPORATIVA: LOGOTIPO OFICIAL Y ENCABEZADO
# ----------------------------------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    # Búsqueda segura del archivo de imagen en la raíz del proyecto
    logo_encontrado = None
    for archivo_posible in ["logo.jpg", "logo.JPG", "logo.png", "LOGO.jpg", "LOGO.png"]:
        if path.exists(archivo_posible):
            logo_encontrado = archivo_posible
            break
            
    if logo_encontrado:
        st.image(logo_encontrado, use_container_width=True)
    else:
        # Banner institucional de respaldo si la imagen aún no está cargada en el repositorio
        st.markdown(
            f"<div style='background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>"
            f"<h2 style='margin: 0; color: #FBC02D;'>🌾 {EMPRESA_NOMBRE}</h2>"
            f"<p style='margin: 5px 0 0 0; font-size: 14px; font-family: monospace;'>RIF: {EMPRESA_RIF}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )

st.markdown("<h3 style='text-align: center; color: #1565C0;'>Mercado Bursátil y Digital de Insumos Agrícolas</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #2E7D32;'>Cobertura Estratégica: Yaracuy - Lara - Carabobo</h5>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------------------------------
# INICIALIZACIÓN DE ESTADOS (BASE DE DATOS EN MEMORIA)
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
# MENÚ DE NAVEGACIÓN PRINCIPAL
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
    st.write(
        f"**{EMPRESA_NOMBRE}** (RIF: **{EMPRESA_RIF}**) es una entidad jurídica constituida para transformar la comercialización "
        "de insumos del sector primario a través del mercado digital. Operamos bajo un modelo de oferta y demanda y corretaje "
        "agrícola digital, interconectando de forma transparente los valles productivos de **Yaracuy, Lara y Carabobo**."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎯 Objetivo Central")
        st.write("Minimizar el tiempo de inactividad de los productores del campo, eliminar la intermediación abusiva y optimizar los costos logísticos mediante un sistema de subasta inversa donde las agrotiendas compiten abiertamente ofreciendo el mejor precio del mercado.")
    with col2:
        st.subheader("🌟 Beneficios Clave")
        st.write("• **Para el Productor:** Ahorro financiero, inmediatez en emergencias y el mejor precio sin recorrer múltiples municipios.")
        st.write("• **Para la Agrotienda:** Canales de venta directos con clientes de alta intención de compra y optimización de inventario.")
        st.write("• **Para la Región Central:** Dinamización transparente del agro-comercio interconectando Yaracuy, Lara y Carabobo.")

# ----------------------------------------------------
# MÓDULO 2: MENÚ DE REQUERIMIENTOS MÁS IMPORTANTES
# ----------------------------------------------------
elif menu == "🚜 Menú de Requerimientos del Campo":
    st.header("📋 Directorio de Insumos y Urgencias Agrícolas")
    st.markdown("Consulte las categorías críticas de alta demanda en el campo:")
    
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

# ----------------------------------------------------
# MÓDULO 3: AFILIACIÓN DE AGROTIENDAS Y CONTRATO
# ----------------------------------------------------
elif menu == "📝 Afiliación de Agrotiendas (Contrato)":
    st.header("📝 Contrato de Adhesión y Corretaje Digital Mercantil")
    
    with st.expander("🔍 Leer Términos Legales del Contrato", expanded=False):
        st.write(f"CONTRATO DE ADHESIÓN - {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF})")
        st.write("PRIMERA (PARTES): Se celebra entre la empresa y la Agrotienda adherente, rigiéndose por el Código de Comercio venezolano.")
        st.write("SEGUNDA (OBJETO): La plataforma opera como un mercado digital de oferta y demanda agrícola en los estados Yaracuy, Lara y Carabobo.")
        st.write(f"TERCERA (CONDICIONES): Las transacciones financieras usan exclusivamente la cuenta oficial de {EMPRESA_NOMBRE} ({EMPRESA_BANCO}, Pagomóvil: {EMPRESA_TELEFONO}).")

    st.markdown("### ✍️ Formulario de Incorporación y Firma Digital")
    with st.form("form_afiliacion"):
        nombre_tienda = st.text_input("Nombre de la Agrotienda / Empresa:")
        rif_tienda = st.text_input("RIF de la Agrotienda:")
        estado_tienda = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_tienda = st.text_input("Municipio / Localidad:")
        telefono_tienda = st.text_input("Teléfono WhatsApp de Contacto:")
        
        acepta_contrato = st.checkbox("✅ Acepto de forma libre, consciente y legal los términos del Contrato de Adhesión.")
        btn_afiliar = st.form_submit_button("Firmar Adhesión e Incorporarse al Sistema")
        
        if btn_afiliar:
            if acepta_contrato and nombre_tienda and rif_tienda and telefono_tienda:
                st.session_state.agrotiendas_registradas.append({
                    "nombre": nombre_tienda, "estado": estado_tienda,
                    "municipio": municipio_tienda, "telefono": telefono_tienda
                })
                st.success(f"¡Felicidades! {nombre_tienda} ha sido afiliada exitosamente con respaldo de {EMPRESA_NOMBRE}.")
            elif not acepta_contrato:
                st.error("Debe marcar la casilla de aceptación de condiciones para formalizar el contrato.")
            else:
                st.error("Por favor complete todos los datos requeridos.")

# ----------------------------------------------------
# MÓDULO 4: SUBASTA Y OFERTA (PRODUCTOR)
# ----------------------------------------------------
elif menu == "🛒 Subasta y Oferta (Productor)":
    st.header("🛒 Módulo de Demanda y Subasta del Productor")
    st.markdown("Publique su requerimiento para que las agrotiendas registradas en la región compitan por ofrecerle el mejor precio.")
    
    with st.form("form_productor_robusto"):
        nombre_prod = st.text_input("Nombre del Productor / Finca:")
        estado_prod = st.selectbox("Estado de Ubicación:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_prod = st.text_input("Municipio:")
        insumo_req = st.text_input("Insumo / Repuesto Requerido:")
        cant_req = st.text_input("Cantidad (Ej: 10 sacos, 2 filtros):")
        tel_prod = st.text_input("WhatsApp de Contacto:")
        
        btn_subasta = st.form_submit_button("🚀 Lanzar Subasta Regional")
        if btn_subasta:
            if nombre_prod and insumo_req and tel_prod:
                pid = len(st.session_state.pedidos) + 1
                st.session_state.pedidos.append({
                    "id": pid, "nombre": nombre_prod, "estado": estado_prod,
                    "municipio": municipio_prod, "insumo": insumo_req, "cantidad": cant_req, "telefono": tel_prod
                })
                st.success(f"¡Subasta #{pid} emitida con éxito a la red de agrotiendas!")
            else:
                st.error("Complete los campos obligatorios.")

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
                        msg = f"Hola {o['tienda']}, acepto su oferta de ${o['precio']:.2f} para el insumo {p['insumo']}."
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
                    
                    btn_oferta = st.form_submit_button("💡 Enviar Oferta Competitiva")
                    if btn_oferta:
                        if t_nombre and t_precio > 0:
                            st.session_state.ofertas.append({
                                "pedido_id": p['id'], "tienda": t_nombre, "estado_tienda": t_estado,
                                "precio": t_precio, "tiempo": t_tiempo, "telefono_tienda": t_tel
                            })
                            st.success("¡Oferta publicada exitosamente en la red regional!")
                        else:
                            st.error("Ingrese un nombre y un precio válido.")
                st.divider()

# ----------------------------------------------------
# MÓDULO 6: PASARELA DE PAGO MÓVIL BDV
# ----------------------------------------------------
elif menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial")
    st.markdown("Procesamiento seguro respaldado por los datos fiscales de la empresa operadora.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        texto_banco = (
            "🏦 Datos Bancarios Oficiales:\n\n"
            f"• Razón Social: {EMPRESA_NOMBRE}\n"
            f"• RIF: {EMPRESA_RIF}\n"
            f"• Banco: {EMPRESA_BANCO}\n"
            f"• Teléfono Pago Móvil: {EMPRESA_TELEFONO}"
        )
        st.info(texto_banco)
    with col2:
        st.markdown("### 📋 Validar Pago o Reserva")
        with st.form("form_pago_robusto"):
            monto_p = st.number_input("Monto a pagar:", min_value=0.0, format="%.2f")
            ref_p = st.text_input("Número de Referencia Bancaria:")
            banco_orig = st.text_input("Banco de Origen:")
            
            submitted_pago = st.form_submit_button("Confirmar Transacción")
            if submitted_pago:
                if ref_p and monto_p > 0:
                    st.success("¡Pago reportado y validado en el sistema!")
                    msg_pago = f"Hola, he realizado un Pago Móvil a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por un monto de ${monto_p:.2f}. Referencia: {ref_p}."
                    url_pago_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                    st.markdown(f"[📲 Enviar Comprobante vía WhatsApp]({url_pago_wa})", unsafe_allow_html=True)
                else:
                    st.error("Por favor, ingrese un monto válido y el número de referencia.")
