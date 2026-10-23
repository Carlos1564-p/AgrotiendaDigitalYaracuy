import streamlit as st
import pandas as pd
import urllib.parse
from os import path
from fpdf import FPDF

# Configuración de la página
st.set_page_config(
    page_title="AgroYaracuy & Región | Acceso Seguro por Roles",
    page_icon="🌾",
    layout="wide"
)

# Datos oficiales de la empresa
EMPRESA_NOMBRE = "COMPAÑÍA HCHF4 C.A."
EMPRESA_RIF = "J-404509216"
EMPRESA_BANCO = "Banco de Venezuela (0102)"
EMPRESA_TELEFONO = "04120582064"

# ----------------------------------------------------
# INICIALIZACIÓN DE ESTADOS GLOBALES
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

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "rol_actual" not in st.session_state:
    st.session_state.rol_actual = None
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

# ----------------------------------------------------
# SECCIÓN CORPORATIVA: LOGOTIPO Y ENCABEZADO
# ----------------------------------------------------
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    logo_encontrado = None
    for archivo_posible in ["logo.png", "logo agrodigitalvenezueladefinitivo.png"]:
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

st.markdown("<h3 style='text-align: center; color: #1565C0;'>Plataforma Segura con Autenticación y Control de Roles</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: #2E7D32;'>Eje de Operaciones: Yaracuy - Lara - Carabobo</h5>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------------------------------
# CONTROL DE ACCESO: PANTALLA DE LOGIN OBLIGATORIO
# ----------------------------------------------------
if not st.session_state.autenticado:
    st.sidebar.markdown("### 🔐 Iniciar Sesión en el Sistema")
    st.sidebar.info("Ingrese sus credenciales corporativas o de productor para acceder al módulo correspondiente.")
    
    with st.sidebar.form("form_login"):
        input_usuario = st.text_input("Usuario o Cédula/RIF:")
        input_clave = st.text_input("Contraseña:", type="password")
        btn_login = st.form_submit_button("Entrar al Sistema")
        
        if btn_login:
            # Base de datos simulada de usuarios y roles estrictos
            # En producción, esto se conecta a una base de datos segura
            credenciales = {
                "admin": {"rol": "⚙️ Administrador", "nombre": "Administrador Central"},
                "agrotienda": {"rol": "🏪 Agrotienda", "nombre": "Agrotienda Afiliada"},
                "productor": {"rol": "🚜 Productor", "nombre": "Productor Agrícola"}
            }
            
            if input_usuario in credenciales and input_clave == "123456": # Clave de demostración segura
                st.session_state.autenticado = True
                st.session_state.rol_actual = credenciales[input_usuario]["rol"]
                st.session_state.usuario_actual = credenciales[input_usuario]["nombre"]
                st.rerun()
            else:
                st.sidebar.error("Usuario o contraseña incorrectos.")
    
    st.warning("⚠️ **Acceso Restringido:** Debe iniciar sesión en el panel lateral para utilizar las herramientas de subasta, cotización y gestión de la red.")
    st.stop()  # Detiene la ejecución del resto de la app si no está autenticado

# ----------------------------------------------------
# SESIÓN ACTIVA: PANEL LATERAL Y RESTRICCIÓN DE MENÚS
# ----------------------------------------------------
st.sidebar.markdown(f"### 👤 Sesión Activa")
st.sidebar.success(f"**Usuario:** {st.session_state.usuario_actual}\n\n**Rol:** {st.session_state.rol_actual}")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.rol_actual = None
    st.session_state.usuario_actual = ""
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("### 🧭 Menú Autorizado")

# Definición estricta de menús segmentados por rol (Blindaje contra cruce de accesos)
if st.session_state.rol_actual == "🚜 Productor":
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "🛒 Lanzar Subasta Inversa (Anónima)",
        "📊 Mis Pujas y Adjudicación",
        "🚜 Requerimientos del Campo"
    ])

elif st.session_state.rol_actual == "🏪 Agrotienda":
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📝 Afiliación y Contrato Mercantil",
        "🏪 Panel de Cotización Abierta",
        "💳 Pasarela de Pago Móvil BDV"
    ])

else:  # Administrador
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📊 Panel General de Control",
        "📄 Generador de Notas de Entrega (PDF)",
        "📑 Auditoría de Transacciones",
        "💳 Pasarela de Pago Móvil BDV"
    ])

# ----------------------------------------------------
# EJECUCIÓN DE MÓDULOS SEGÚN EL ROL VERIFICADO
# ----------------------------------------------------

# MÓDULOS DE PRODUCTOR
if menu == "🛒 Lanzar Subasta Inversa (Anónima)":
    st.header("🛒 Módulo de Subasta Inversa (Productor)")
    st.markdown("Publique su necesidad de insumos. Sus datos de contacto permanecen estrictamente ocultos hasta la adjudicación.")
    
    with st.form("form_subasta_prod"):
        nombre_prod = st.text_input("Nombre de Finca / Productor:")
        estado_prod = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_prod = st.text_input("Municipio:")
        insumo_req = st.text_input("Insumo / Repuesto Requerido:")
        cant_req = st.text_input("Cantidad Requerida:")
        tel_prod = st.text_input("WhatsApp Privado:")
        
        if st.form_submit_button("🚀 Emitir Subasta Segura"):
            if nombre_prod and insumo_req and tel_prod:
                pid = len(st.session_state.pedidos) + 1
                st.session_state.pedidos.append({
                    "id": pid, "productor": nombre_prod, "estado": estado_prod,
                    "municipio": municipio_prod, "insumo": insumo_req, "cantidad": cant_req, "telefono": tel_prod
                })
                st.success(f"¡Subasta #{pid} emitida correctamente!")
            else:
                st.error("Complete todos los campos obligatorios.")

elif menu == "📊 Mis Pujas y Adjudicación":
    st.header("📊 Seguimiento de Ofertas y Adjudicación")
    if not st.session_state.pedidos:
        st.info("No tiene solicitudes de subasta activas.")
    else:
        for p in st.session_state.pedidos:
            st.markdown(f"**Subasta #{p['id']}** | Zona: *{p['estado']} - {p['municipio']}* | Insumo: **{p['insumo']} ({p['cantidad']})**")
            ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
            
            if not ofertas_p:
                st.caption("_Esperando ofertas de las agrotiendas de la región..._")
            else:
                for o in sorted(ofertas_p, key=lambda x: x["precio"]):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1: st.write(f"🏪 **{o['tienda']}** ({o['estado_tienda']})")
                    with c2: st.write(f"💲 **${o['precio']:.2f} USD** | {o['tiempo']}")
                    with c3:
                        if st.button(f"✅ Adjudicar #{o['pedido_id']}", key=f"adj_{o['pedido_id']}_{o['tienda']}"):
                            st.session_state.transacciones_cerradas.append({
                                "id_transaccion": len(st.session_state.transacciones_cerradas) + 1,
                                "productor": p['productor'], "telefono_productor": p['telefono'],
                                "tienda": o['tienda'], "telefono_tienda": o['telefono_tienda'],
                                "insumo": p['insumo'], "cantidad": p['cantidad'], "precio": o['precio'],
                                "zona": f"{p['estado']} - {p['municipio']}"
                            })
                            st.success("¡Adjudicación exitosa! Contacto desbloqueado.")
                            msg = f"Hola {o['tienda']}, he adjudicado su oferta de ${o['precio']:.2f} en {EMPRESA_NOMBRE}."
                            url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                            st.markdown(f"[💬 Contactar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
            st.divider()

elif menu == "🚜 Requerimientos del Campo":
    st.header("📋 Directorio de Insumos Agrícolas")
    st.write("• Fertilizantes y Nutrición de Suelos (Urea, NPK)\n• Sanidad y Vacunación Animal\n• Agroquímicos y Control de Plagas\n• Maquinaria y Repuestos Críticos\n• Semillas Certificadas")


# MÓDULOS DE AGROTIENDA
elif menu == "📝 Afiliación y Contrato Mercantil":
    st.header("📝 Contrato de Adhesión y Corretaje Digital")
    with st.expander("🔍 Leer Términos Legales", expanded=False):
        st.write(f"CONTRATO - {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF})\nProhibida la desintermediación comercial. Pagos centralizados en {EMPRESA_BANCO}.")

    with st.form("form_afilia_t"):
        t_nom = st.text_input("Nombre de la Agrotienda:")
        t_rif = st.text_input("RIF:")
        t_est = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        t_mun = st.text_input("Municipio:")
        t_tel = st.text_input("Teléfono:")
        t_acepta = st.checkbox("✅ Acepto los términos del contrato de adhesión.")
        
        if st.form_submit_button("Registrar Agrotienda"):
            if t_acepta and t_nom:
                st.session_state.agrotiendas_registradas.append({"nombre": t_nom, "estado": t_est, "municipio": t_mun, "telefono": t_tel})
                st.success("¡Agrotienda afiliada con éxito!")
            else:
                st.error("Complete los datos y acepte el contrato.")

elif menu == "🏪 Panel de Cotización Abierta":
    st.header("🏪 Panel de Competencia de Precios (Agrotiendas)")
    if not st.session_state.pedidos:
        st.warning("No hay solicitudes de productores activas.")
    else:
        for p in st.session_state.pedidos:
            with st.container():
                st.markdown(f"### 🔔 Demanda Zona: [{p['estado']}] - Municipio {p['municipio']}")
                st.write(f"**Insumo:** {p['insumo']} | **Cantidad:** {p['cantidad']}")
                st.info("🔒 _Identidad del productor protegida._")
                
                with st.form(f"form_cot_{p['id']}"):
                    tienda_nombre = st.text_input("Nombre de su Agrotienda:", key=f"tn_{p['id']}")
                    tienda_estado = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"], key=f"te_{p['id']}")
                    precio_ofertado = st.number_input("Precio Total Ofertado (USD $):", min_value=0.0, format="%.2f", key=f"tp_{p['id']}")
                    tiempo_entrega = st.text_input("Disponibilidad:", key=f"tt_{p['id']}")
                    telefono_tienda = st.text_input("WhatsApp Comercial:", key=f"tel_{p['id']}")
                    
                    if st.form_submit_button("💡 Enviar Puja"):
                        if tienda_nombre and precio_ofertado > 0:
                            st.session_state.ofertas.append({
                                "pedido_id": p['id'], "tienda": tienda_nombre, "estado_tienda": tienda_estado,
                                "precio": precio_ofertado, "tiempo": tiempo_entrega, "telefono_tienda": telefono_tienda
                            })
                            st.success("¡Puja enviada exitosamente!")
                        else:
                            st.error("Ingrese un precio válido.")
                st.divider()


# MÓDULOS DE ADMINISTRADOR
elif menu == "📊 Panel General de Control":
    st.header("⚙️ Panel de Control del Administrador")
    c1, c2, c3 = st.columns(3)
    c1.metric("Subastas Activas", len(st.session_state.pedidos))
    c2.metric("Agrotiendas Afiliadas", len(st.session_state.agrotiendas_registradas))
    c3.metric("Transacciones Cerradas", len(st.session_state.transacciones_cerradas))

elif menu == "📄 Generador de Notas de Entrega (PDF)":
    st.header("📄 Generador de Documentación Legal (PDF)")
    if not st.session_state.transacciones_cerradas:
        st.info("No hay transacciones cerradas para certificar.")
    else:
        for t in st.session_state.transacciones_cerradas:
            st.markdown(f"**Transacción #{t['id_transaccion']}** | {t['productor']} ➔ {t['tienda']} (${t['precio']:.2f} USD)")
            if st.button(f"📥 Descargar PDF #{t['id_transaccion']}", key=f"pdf_gen_{t['id_transaccion']}"):
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 14)
                        self.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "C")
                        self.set_font("Arial", "", 10)
                        self.cell(0, 5, f"RIF: {EMPRESA_RIF}", 0, 1, "C")
                        self.ln(5)

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "NOTA DE ENTREGA Y CERTIFICADO", 0, 1, "C")
                pdf.ln(5)
                pdf.set_font("Arial", "", 10)
                pdf.cell(0, 8, f"Transaccion ID: {t['id_transaccion']}", 0, 1)
                pdf.cell(0, 8, f"Zona: {t['zona']}", 0, 1)
                pdf.cell(0, 8, f"Productor: {t['productor']}", 0, 1)
                pdf.cell(0, 8, f"Agrotienda: {t['tienda']}", 0, 1)
                pdf.cell(0, 8, f"Insumo: {t['insumo']} ({t['cantidad']}) - ${t['precio']:.2f} USD", 0, 1)
                
                filename = f"Nota_Entrega_{t['id_transaccion']}.pdf"
                pdf.output(filename)
                
                with open(filename, "rb") as f_pdf:
                    st.download_button(label=f"⬇️ Descargar Archivo", data=f_pdf, file_name=filename, mime="application/pdf")
            st.divider()

elif menu == "📑 Auditoría de Transacciones":
    st.header("📑 Auditoría y Registro Histórico")
    if not st.session_state.transacciones_cerradas:
        st.info("Sin registros de auditoría actuales.")
    else:
        df_trans = pd.DataFrame(st.session_state.transacciones_cerradas)
        st.dataframe(df_trans, use_container_width=True)


# MÓDULO COMPARTIDO (PASARELA DE PAGO)
if menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"🏦 Datos Bancarios:\n\n• Razón Social: {EMPRESA_NOMBRE}\n• RIF: {EMPRESA_RIF}\n• Banco: {EMPRESA_BANCO}\n• Teléfono: {EMPRESA_TELEFONO}")
    with col2:
        with st.form("form_pago"):
            monto_p = st.number_input("Monto:", min_value=0.0, format="%.2f")
            ref_p = st.text_input("Número de Referencia:")
            if st.form_submit_button("Validar Pago"):
                if ref_p and monto_p > 0:
                    st.success("¡Pago reportado con éxito!")
                else:
                    st.error("Ingrese referencia y monto.")
