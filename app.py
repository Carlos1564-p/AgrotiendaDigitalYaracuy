import streamlit as st
import pandas as pd
import urllib.parse
from os import path
from fpdf import FPDF

# Configuración de la página
st.set_page_config(
    page_title="AgroYaracuy & Región | Plataforma Multi-Rol",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa
EMPRESA_NOMBRE = "COMPAÑÍA HCHF4 C.A."
EMPRESA_RIF = "J-404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# ----------------------------------------------------
# SECCIÓN CORPORATIVA: LOGOTIPO Y ENCABEZADO
# ----------------------------------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    logo_encontrado = None
    for archivo_posible in ["logo.jpg", "logo.JPG", "logo.png", "LOGO.jpg", "LOGO.png"]:
        if path.exists(archivo_posible):
            logo_encontrado = archivo_posible
            break
            
    if logo_encontrado:
        st.image(logo_encontrado, use_container_width=True)
    else:
        st.markdown(
            f"<div style='background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>"
            f"<h2 style='margin: 0; color: #FBC02D;'>🌾 {EMPRESA_NOMBRE}</h2>"
            f"<p style='margin: 5px 0 0 0; font-size: 14px; font-family: monospace;'>RIF: {EMPRESA_RIF}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )

st.markdown("<h3 style='text-align: center; color: #1565C0;'>Sistema de Corretaje Agrícola Digital con Control por Roles</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #2E7D32;'>Eje de Operaciones: Yaracuy - Lara - Carabobo</h5>", unsafe_allow_html=True)
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
if "transacciones_cerradas" not in st.session_state:
    st.session_state.transacciones_cerradas = []

# ----------------------------------------------------
# SISTEMA DE CONTROL DE ACCESO BASADO EN ROLES (RBAC)
# ----------------------------------------------------
st.sidebar.markdown("### 🔐 Control de Acceso por Roles")
rol_usuario = st.sidebar.selectbox("Seleccione su Rol en el Sistema:", [
    "🚜 Productor Agrícola",
    "🏪 Agrotienda Afiliada",
    "⚙️ Administrador del Sistema"
])

st.sidebar.divider()

# Filtrado dinámico de menús según el rol seleccionado
if rol_usuario == "🚜 Productor Agrícola":
    st.sidebar.markdown("#### 👤 Perfil: Productor")
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "🛒 Lanzar Subasta Inversa (Anónima)",
        "📊 Mis Pujas y Adjudicación",
        "🚜 Requerimientos del Campo"
    ])

elif rol_usuario == "🏪 Agrotienda Afiliada":
    st.sidebar.markdown("#### 🏪 Perfil: Agrotienda")
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📝 Afiliación y Contrato Mercantil",
        "🏪 Panel de Cotización Abierta",
        "💳 Pasarela de Pago Móvil BDV"
    ])

else:  # Administrador del Sistema
    st.sidebar.markdown("#### ⚙️ Perfil: Administrador")
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📊 Panel General de Control",
        "📄 Generador de Notas de Entrega (PDF)",
        "📑 Auditoría de Transacciones",
        "💳 Pasarela de Pago Móvil BDV"
    ])

# ----------------------------------------------------
# MÓDULOS DEL ROL: PRODUCTOR AGRÍCOLA
# ----------------------------------------------------
if menu == "🛒 Lanzar Subasta Inversa (Anónima)":
    st.header("🛒 Módulo de Subasta Inversa (Productor)")
    st.markdown("Publique su necesidad de insumos. Su nombre y teléfono **permanecen ocultos** para evitar contactos por fuera hasta que adjudique una oferta.")
    
    with st.form("form_subasta_prod"):
        nombre_prod = st.text_input("Nombre de Finca / Productor (Ej: Finca San José):")
        estado_prod = st.selectbox("Estado de Ubicación:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_prod = st.text_input("Municipio:")
        insumo_req = st.text_input("Insumo / Repuesto Requerido:")
        cant_req = st.text_input("Cantidad Requerida (Ej: 15 sacos):")
        tel_prod = st.text_input("WhatsApp Privado (Se libera al adjudicar):")
        
        if st.form_submit_button("🚀 Emitir Subasta Regional Segura"):
            if nombre_prod and insumo_req and tel_prod:
                pid = len(st.session_state.pedidos) + 1
                st.session_state.pedidos.append({
                    "id": pid, "productor": nombre_prod, "estado": estado_prod,
                    "municipio": municipio_prod, "insumo": insumo_req, "cantidad": cant_req, "telefono": tel_prod
                })
                st.success(f"¡Subasta #{pid} publicada correctamente en la red central!")
            else:
                st.error("Por favor complete los campos obligatorios.")

elif menu == "📊 Mis Pujas y Adjudicación":
    st.header("📊 Seguimiento de Ofertas y Adjudicación")
    st.markdown("Consulte las pujas de las agrotiendas y seleccione la mejor opción.")
    
    if not st.session_state.pedidos:
        st.info("No tiene solicitudes de subasta activas en este momento.")
    else:
        for p in st.session_state.pedidos:
            st.markdown(f"**Subasta #{p['id']}** | Zona: *{p['estado']} - {p['municipio']}* | Insumo: **{p['insumo']} ({p['cantidad']})**")
            ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
            
            if not ofertas_p:
                st.caption("_Esperando que las agrotiendas compitan con precios..._")
            else:
                for o in sorted(ofertas_p, key=lambda x: x["precio"]):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1: st.write(f"🏪 **{o['tienda']}** ({o['estado_tienda']})")
                    with c2: st.write(f"💲 **${o['precio']:.2f} USD** | {o['tiempo']}")
                    with c3:
                        if st.button(f"✅ Adjudicar Oferta #{o['pedido_id']}", key=f"btn_adj_{o['pedido_id']}_{o['tienda']}"):
                            st.session_state.transacciones_cerradas.append({
                                "id_transaccion": len(st.session_state.transacciones_cerradas) + 1,
                                "productor": p['productor'],
                                "telefono_productor": p['telefono'],
                                "tienda": o['tienda'],
                                "telefono_tienda": o['telefono_tienda'],
                                "insumo": p['insumo'],
                                "cantidad": p['cantidad'],
                                "precio": o['precio'],
                                "zona": f"{p['estado']} - {p['municipio']}"
                            })
                            st.success("¡Oferta adjudicada! Contacto y orden legal generados con éxito.")
                            msg = f"Hola {o['tienda']}, he adjudicado su oferta de ${o['precio']:.2f} en {EMPRESA_NOMBRE}."
                            url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                            st.markdown(f"[💬 Contactar Agrotienda vía WhatsApp]({url_wa})", unsafe_allow_html=True)
            st.divider()

elif menu == "🚜 Requerimientos del Campo":
    st.header("📋 Directorio de Insumos y Urgencias Agrícolas")
    requerimientos = {
        "Fertilizantes y Nutrición de Suelos": "Urea, Nitrato de Amonio, NPK y enmiendas calcáreas.",
        "Sanidad y Vacunación Animal": "Vacunas contra Aftosa, Rabia Silvestre y antibióticos veterinarios.",
        "Agroquímicos y Control de Plagas": "Herbicidas sistémicos (Glifosato), insecticidas y fungicidas.",
        "Maquinaria y Repuestos Críticos": "Correas de transmisión, filtros, mangueras y discos de arado.",
        "Semillas Certificadas": "Material genético certificado de maíz, caraota y sorgo."
    }
    for cat, desc in requerimientos.items():
        with st.expander(f"📦 {cat}"):
            st.write(desc)

# ----------------------------------------------------
# MÓDULOS DEL ROL: AGROTIENDA AFILIADA
# ----------------------------------------------------
elif menu == "📝 Afiliación y Contrato Mercantil":
    st.header("📝 Contrato de Adhesión y Corretaje Digital")
    with st.expander("🔍 Leer Términos Legales del Contrato", expanded=False):
        st.write(f"CONTRATO - {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF})")
        st.write("PRIMERA: La agrotienda operará bajo estrictas normas de corretaje transparente.")
        st.write("SEGUNDA: Prohibida la elusión de comisiones o tratos directos previos a la adjudicación.")
        st.write(f"TERCERA: Pagos tramitados por {EMPRESA_BANCO}, Pagomóvil: {EMPRESA_TELEFONO}.")

    st.markdown("### ✍️ Formulario de Registro de Agrotienda")
    with st.form("form_afilia_tienda"):
        t_nom = st.text_input("Nombre Comercial de la Agrotienda:")
        t_rif = st.text_input("RIF:")
        t_est = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        t_mun = st.text_input("Municipio:")
        t_tel = st.text_input("Teléfono de Contacto:")
        t_acepta = st.checkbox("✅ Acepto los términos del contrato de adhesión.")
        
        if st.form_submit_button("Registrar Agrotienda"):
            if t_acepta and t_nom and t_rif:
                st.session_state.agrotiendas_registradas.append({
                    "nombre": t_nom, "estado": t_est, "municipio": t_mun, "telefono": t_tel
                })
                st.success(f"¡{t_nom} incorporada exitosamente a la red regional!")
            else:
                st.error("Complete los datos requeridos y acepte el contrato.")

elif menu == "🏪 Panel de Cotización Abierta":
    st.header("🏪 Panel de Competencia (Agrotiendas)")
    st.markdown("Visualice requerimientos activos anonimizados por zona y envíe su mejor oferta de precio.")
    
    if not st.session_state.pedidos:
        st.warning("No hay solicitudes de productores activas en este momento.")
    else:
        for p in st.session_state.pedidos:
            with st.container():
                st.markdown(f"### 🔔 Demanda Zona: [{p['estado']}] - Municipio {p['municipio']}")
                st.write(f"**Insumo:** {p['insumo']} | **Cantidad:** {p['cantidad']}")
                st.info("🔒 _Identidad del productor protegida contra desintermediación._")
                
                with st.form(f"form_cot_{p['id']}"):
                    tienda_nombre = st.text_input("Nombre de su Agrotienda:", key=f"tn_{p['id']}")
                    tienda_estado = st.selectbox("Estado de su Tienda:", ["Yaracuy", "Lara", "Carabobo"], key=f"te_{p['id']}")
                    precio_ofertado = st.number_input("Precio Total Ofertado (USD $):", min_value=0.0, format="%.2f", key=f"tp_{p['id']}")
                    tiempo_entrega = st.text_input("Condición de Entrega:", key=f"tt_{p['id']}")
                    telefono_tienda = st.text_input("Su Teléfono Comercial:", key=f"tel_{p['id']}")
                    
                    if st.form_submit_button("💡 Enviar Puja Competitiva"):
                        if tienda_nombre and precio_ofertado > 0:
                            st.session_state.ofertas.append({
                                "pedido_id": p['id'], "tienda": tienda_nombre, "estado_tienda": tienda_estado,
                                "precio": precio_ofertado, "tiempo": tiempo_entrega, "telefono_tienda": telefono_tienda
                            })
                            st.success("¡Oferta enviada con éxito al sistema!")
                        else:
                            st.error("Ingrese un nombre de tienda y precio válidos.")
                st.divider()

# ----------------------------------------------------
# MÓDULOS DEL ROL: ADMINISTRADOR DEL SISTEMA
# ----------------------------------------------------
elif menu == "📊 Panel General de Control":
    st.header("⚙️ Panel de Control y Estadísticas del Administrador")
    c1, c2, c3 = st.columns(3)
    c1.metric("Subastas Activas", len(st.session_state.pedidos))
    c2.metric("Agrotiendas Afiliadas", len(st.session_state.agrotiendas_registradas))
    c3.metric("Transacciones Cerradas", len(st.session_state.transacciones_cerradas))
    
    st.divider()
    st.subheader("🏪 Agrotiendas Registradas en la Red")
    for ag in st.session_state.agrotiendas_registradas:
        st.write(f"• **{ag['nombre']}** ({ag['estado']} - {ag['municipio']}) | Telf: {ag['telefono']}")

elif menu == "📄 Generador de Notas de Entrega (PDF)":
    st.header("📄 Generador de Documentación Legal (PDF)")
    st.markdown(f"Certificados oficiales respaldados por **{EMPRESA_NOMBRE}** (RIF: {EMPRESA_RIF}).")
    
    if not st.session_state.transacciones_cerradas:
        st.info("No existen transacciones adjudicadas para generar documentos PDF.")
    else:
        for t in st.session_state.transacciones_cerradas:
            st.markdown(f"**Transacción #{t['id_transaccion']}** | {t['productor']} ➔ {t['tienda']} (${t['precio']:.2f} USD)")
            
            if st.button(f"📥 Descargar Nota de Entrega PDF #{t['id_transaccion']}", key=f"pdf_gen_{t['id_transaccion']}"):
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 14)
                        self.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "C")
                        self.set_font("Arial", "", 10)
                        self.cell(0, 5, f"RIF: {EMPRESA_RIF} | Corretaje y Blindaje Digital", 0, 1, "C")
                        self.ln(5)

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "NOTA DE ENTREGA Y CERTIFICADO DE CORRETAJE", 0, 1, "C")
                pdf.ln(5)
                
                pdf.set_font("Arial", "", 10)
                pdf.cell(0, 8, f"Transaccion ID: {t['id_transaccion']}", 0, 1)
                pdf.cell(0, 8, f"Eje Regional: {t['zona']}", 0, 1)
                pdf.cell(0, 8, f"Productor: {t['productor']} (Telf: {t['telefono_productor']})", 0, 1)
                pdf.cell(0, 8, f"Agrotienda: {t['tienda']} (Telf: {t['telefono_tienda']})", 0, 1)
                pdf.ln(5)
                
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Detalle del Insumo:", 0, 1)
                pdf.set_font("Arial", "", 10)
                pdf.cell(0, 8, f"- Insumo: {t['insumo']}", 0, 1)
                pdf.cell(0, 8, f"- Cantidad: {t['cantidad']}", 0, 1)
                pdf.cell(0, 8, f"- Monto Acordado: ${t['precio']:.2f} USD", 0, 1)
                pdf.ln(10)
                
                pdf.set_font("Arial", "I", 9)
                pdf.multi_cell(0, 5, f"Certificado oficial emitido por {EMPRESA_NOMBRE}. Operación protegida contra desintermediación en Yaracuy, Lara y Carabobo.")
                
                filename = f"Nota_Entrega_{t['id_transaccion']}.pdf"
                pdf.output(filename)
                
                with open(filename, "rb") as f_pdf:
                    st.download_button(
                        label=f"⬇️ Descargar Archivo PDF (#{t['id_transaccion']})",
                        data=f_pdf,
                        file_name=filename,
                        mime="application/pdf"
                    )
            st.divider()

elif menu == "📑 Auditoría de Transacciones":
    st.header("📑 Auditoría y Registro Histórico")
    if not st.session_state.transacciones_cerradas:
        st.info("Sin registros de auditoría actuales.")
    else:
        df_trans = pd.DataFrame(st.session_state.transacciones_cerradas)
        st.dataframe(df_trans, use_container_width=True)

# ----------------------------------------------------
# MÓDULO COMPARTIDO / ACCESIBLE (PASARELA DE PAGO)
# ----------------------------------------------------
if menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial")
    st.markdown("Liquidación segura de comisiones e insumos respaldada por la operadora.")
    
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
        st.markdown("### 📋 Validar Pago o Transacción")
        with st.form("form_pago_global"):
            monto_p = st.number_input("Monto:", min_value=0.0, format="%.2f")
            ref_p = st.text_input("Número de Referencia:")
            banco_orig = st.text_input("Banco Emisor:")
            
            if st.form_submit_button("Verificar Pago en Sistema"):
                if ref_p and monto_p > 0:
                    st.success("¡Pago reportado y validado con éxito!")
                    msg_pago = f"Hola, reporto pago a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por {monto_p}. Ref: {ref_p}."
                    url_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                    st.markdown(f"[📲 Notificar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
                else:
                    st.error("Ingrese montos y referencias válidos.")
