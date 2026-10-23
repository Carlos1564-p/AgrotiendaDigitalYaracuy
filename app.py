import streamlit as st
import pandas as pd
import urllib.parse
from os import path
from datetime import datetime
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
# INICIALIZACIÓN DE ESTADOS GLOBALES Y TASA BCV
# ----------------------------------------------------
if "tasa_bcv" not in st.session_state:
    st.session_state.tasa_bcv = 36.50
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
if "pagos_agrotiendas" not in st.session_state:
    st.session_state.pagos_agrotiendas = []

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "rol_actual" not in st.session_state:
    st.session_state.rol_actual = None
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

# ----------------------------------------------------
# SECCIÓN CORPORATIVA: DOBLE LOGOTIPO ENCABEZADO
# ----------------------------------------------------
col_l1, col_l2 = st.columns(2)
with col_l1:
    if path.exists("logo.png"):
        st.image("logo.png", width=220)
    elif path.exists("logo agrodigitalvenezueladeinitivo.png"):
        st.image("logo agrodigitalvenezueladeinitivo.png", width=220)
    else:
        st.markdown(f"### 🌾 {EMPRESA_NOMBRE}")

with col_l2:
    if path.exists("logo agrodigitalvenezueladeinitivo.png"):
        st.image("logo agrodigitalvenezueladeinitivo.png", width=220)
    elif path.exists("logo.png"):
        st.image("logo.png", width=220)
    else:
        st.markdown("### 💻 AgroDigital Venezuela")

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
            credenciales = {
                "admin": {"rol": "⚙️ Administrador", "nombre": "Administrador Central"},
                "agrotienda": {"rol": "🏪 Agrotienda", "nombre": "Agrotienda Afiliada"},
                "productor": {"rol": "🚜 Productor", "nombre": "Productor Agrícola"}
            }
            
            if input_usuario in credenciales and input_clave == "123456":
                st.session_state.autenticado = True
                st.session_state.rol_actual = credenciales[input_usuario]["rol"]
                st.session_state.usuario_actual = credenciales[input_usuario]["nombre"]
                st.rerun()
            else:
                st.sidebar.error("Usuario o contraseña incorrectos.")
    
    st.warning("⚠️ **Acceso Restringido:** Debe iniciar sesión en el panel lateral para utilizar las herramientas de subasta, cotización y gestión de la red.")
    st.stop()

# ----------------------------------------------------
# SESIÓN ACTIVA: PANEL LATERAL Y RESTRICCIÓN DE MENÚS
# ----------------------------------------------------
st.sidebar.markdown(f"### 👤 Sesión Activa")
st.sidebar.success(f"**Usuario:** {st.session_state.usuario_actual}\n\n**Rol:** {st.session_state.rol_actual}\n\n**Tasa BCV:** {st.session_state.tasa_bcv:.2f} VES")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.rol_actual = None
    st.session_state.usuario_actual = ""
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("### 🧭 Menú Autorizado")

if st.session_state.rol_actual == "🚜 Productor":
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "🛒 Lanzar Subasta Inversa (Anónima)",
        "📊 Mis Pujas y Adjudicación",
        "💳 Pagar Producto Adquirido",
        "🚜 Requerimientos del Campo"
    ])

elif st.session_state.rol_actual == "🏪 Agrotienda":
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📝 Afiliación y Contrato Mercantil",
        "🏪 Panel de Cotización Abierta",
        "💳 Pasarela de Pago Móvil BDV"
    ])

else: # Administrador
    menu = st.sidebar.selectbox("Seleccione Módulo:", [
        "📊 Panel General y Tasa BCV (24h)",
        "📑 Auditoría Detallada de Transacciones",
        "💸 Liquidación y Pagos a Agrotiendas",
        "💬 Gestión de Agradecimiento",
        "📄 Generador de Notas de Entrega (PDF)",
        "💳 Pasarela de Pago General BDV"
    ])

# ----------------------------------------------------
# EJECUCIÓN DE MÓDULOS SEGÚN EL ROL VERIFICADO
# ----------------------------------------------------

# --- MÓDULOS DE PRODUCTOR ---
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
                    with c2: st.write(f"💲 **${o['precio']:.2f} USD** (~{o['precio']*st.session_state.tasa_bcv:,.2f} VES) | {o['tiempo']}")
                    with c3:
                        if st.button(f"✅ Adjudicar #{o['pedido_id']}", key=f"adj_{o['pedido_id']}_{o['tienda']}"):
                            st.session_state.transacciones_cerradas.append({
                                "id_transaccion": len(st.session_state.transacciones_cerradas) + 1,
                                "productor": p['productor'], "telefono_productor": p['telefono'],
                                "tienda": o['tienda'], "telefono_tienda": o['telefono_tienda'],
                                "insumo": p['insumo'], "cantidad": p['cantidad'], "precio": o['precio'],
                                "zona": f"{p['estado']} - {p['municipio']}"
                            })
                            st.success("¡Adjudicación exitosa! Ya puede proceder al pago en su sección correspondiente.")
                            msg = f"Hola {o['tienda']}, he adjudicado su oferta de ${o['precio']:.2f} en {EMPRESA_NOMBRE}."
                            url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                            st.markdown(f"[💬 Contactar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
            st.divider()

elif menu == "💳 Pagar Producto Adquirido":
    st.header("💳 Pasarela de Pago del Producto Adquirido")
    st.markdown("Realice el pago de los insumos que ha decidido adquirir tras ganar o adjudicar la subasta en la red.")
    
    if not st.session_state.transacciones_cerradas:
        st.info("No tiene transacciones adjudicadas pendientes de pago actualmente.")
    else:
        for t in st.session_state.transacciones_cerradas:
            monto_ves_prod = t['precio'] * st.session_state.tasa_bcv
            with st.container():
                st.markdown(f"### 📦 Transacción Adjudicada #{t['id_transaccion']} - Insumo: {t['insumo']} ({t['cantidad']})")
                st.write(f"🏪 **Agrotienda Proveedora:** {t['tienda']} | 💲 **Monto USD:** ${t['precio']:.2f}")
                st.info(f"💱 **Monto equivalente en Bolívares (Tasa BCV {st.session_state.tasa_bcv:.2f}):** **{monto_ves_prod:,.2f} VES**")
                
                with st.form(f"form_pago_prod_{t['id_transaccion']}"):
                    st.markdown(f"🏦 **Datos de Pago Móvil BDV:** {EMPRESA_BANCO} | Teléfono: {EMPRESA_TELEFONO} | RIF: {EMPRESA_RIF}")
                    ref_pago_prod = st.text_input("Número de Referencia Bancaria (Pago Móvil):", key=f"ref_{t['id_transaccion']}")
                    banco_origen_prod = st.text_input("Banco de Origen:", key=f"banco_{t['id_transaccion']}")
                    
                    if st.form_submit_button("Confirmar Pago del Insumo"):
                        if ref_pago_prod:
                            st.success("¡Pago reportado con éxito al administrador y a la agrotienda!")
                            msg_pago_prod = f"Hola {t['tienda']}, he pagado el insumo {t['insumo']} por ${t['precio']:.2f} ({monto_ves_prod:,.2f} VES). Ref: {ref_pago_prod}."
                            url_wa_pago = f"https://wa.me/58{t['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg_pago_prod)}"
                            st.markdown(f"[📲 Notificar Pago a la Agrotienda vía WhatsApp]({url_wa_pago})", unsafe_allow_html=True)
                        else:
                            st.error("Por favor ingrese el número de referencia bancaria.")
                st.divider()

elif menu == "🚜 Requerimientos del Campo":
    st.header("📋 Directorio de Insumos Agrícolas")
    st.write("• Fertilizantes y Nutrición de Suelos (Urea, NPK)\n• Sanidad y Vacunación Animal\n• Agroquímicos y Control de Plagas\n• Maquinaria y Repuestos Críticos\n• Semillas Certificadas")


# --- MÓDULOS DE AGROTIENDA ---
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
                    st.caption(f"Equivalente en Bolívares BCV: ~{precio_ofertado * st.session_state.tasa_bcv:,.2f} VES")
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


# --- MÓDULOS DE ADMINISTRADOR ---
elif menu == "📊 Panel General y Tasa BCV (24h)":
    st.header("⚙️ Panel de Control del Administrador y Tasas BCV")
    
    col_adm1, col_adm2 = st.columns(2)
    with col_adm1:
        st.subheader("💱 Actualizador de Tasa BCV (24h)")
        nueva_tasa = st.number_input("Modificar Tasa USD/VES Referencial:", value=float(st.session_state.tasa_bcv), format="%.2f")
        if st.button("🔄 Guardar y Actualizar Tasa BCV"):
            st.session_state.tasa_bcv = nueva_tasa
            st.success(f"¡Tasa BCV actualizada a {nueva_tasa:.2f} VES/USD con vigencia de 24h!")
        st.caption(f"📅 Última sincronización registrada: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
    with col_adm2:
        st.subheader("📈 Resumen del Ecosistema")
        st.metric("Subastas Activas", len(st.session_state.pedidos))
        st.metric("Agrotiendas Afiliadas", len(st.session_state.agrotiendas_registradas))
        st.metric("Transacciones Cerradas", len(st.session_state.transacciones_cerradas))

elif menu == "📑 Auditoría Detallada de Transacciones":
    st.header("📑 Auditoría Detallada de Transacciones Cerradas")
    st.markdown("Visualice con precisión el productor adjudicatario, la agrotienda proveedora, el producto y la oferta de precio pujado.")
    
    if not st.session_state.transacciones_cerradas:
        st.info("No hay transacciones cerradas registradas actualmente en el sistema.")
    else:
        for t in st.session_state.transacciones_cerradas:
            monto_ves_audit = t['precio'] * st.session_state.tasa_bcv
            with st.container():
                st.markdown(f"### 📋 Transacción ID #{t['id_transaccion']}")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.write(f"**🚜 Productor:** {t['productor']}")
                    st.caption(f"Telf: {t['telefono_productor']}")
                with col_b:
                    st.write(f"**🏪 Agrotienda:** {t['tienda']}")
                    st.caption(f"Telf: {t['telefono_tienda']}")
                with col_c:
                    st.write(f"**📦 Producto / Insumo:** {t['insumo']}")
                    st.caption(f"Cantidad: {t['cantidad']}")
                
                st.markdown(f"💲 **Precio Pujado / Ofertado:** **${t['precio']:.2f} USD** (~{monto_ves_audit:,.2f} VES a Tasa BCV)")
                st.write(f"📍 **Zona Regional:** {t['zona']}")
                st.divider()

elif menu == "💸 Liquidación y Pagos a Agrotiendas":
    st.header("💸 Módulo de Liquidación y Pago a Agrotiendas")
    st.markdown("Calcule el margen de corretaje contractual de la empresa y procese la transferencia neta a la agrotienda.")
    
    if not st.session_state.transacciones_cerradas:
        st.info("No hay transacciones cerradas para liquidar.")
    else:
        # Porcentaje de comisión por defecto establecido en el contrato (ej. 3%)
        comision_porcentaje = st.slider("Margen / Comisión de Corretaje de la Empresa (%):", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
        
        st.divider()
        for t in st.session_state.transacciones_cerradas:
            monto_total_usd = t['precio']
            comision_empresa_usd = monto_total_usd * (comision_porcentaje / 100.0)
            monto_neto_agrotienda_usd = monto_total_usd - comision_empresa_usd
            
            monto_neto_ves = monto_neto_agrotienda_usd * st.session_state.tasa_bcv
            
            with st.container():
                st.markdown(f"### 🧾 Liquidación Transacción #{t['id_transaccion']} - Agrotienda: {t['tienda']}")
                st.write(f"• **Insumo:** {t['insumo']} ({t['cantidad']}) | **Productor:** {t['productor']}")
                st.write(f"• **Monto Ofertado Total:** ${monto_total_usd:.2f} USD")
                st.write(f"• **Margen de la Empresa ({comision_porcentaje}%):** ${comision_empresa_usd:.2f} USD")
                st.success(f"💰 **Monto Neto a Pagar a la Agrotienda:** **${monto_neto_agrotienda_usd:.2f} USD** (~{monto_neto_ves:,.2f} VES)")
                
                with st.form(f"form_liq_{t['id_transaccion']}"):
                    ref_pago_agro = st.text_input("Número de Referencia de Pago a la Agrotienda:")
                    banco_destino_agro = st.text_input("Banco de Destino de la Agrotienda:")
                    
                    if st.form_submit_button("Registrar Liquidación y Pago"):
                        if ref_pago_agro:
                            st.session_state.pagos_agrotiendas.append({
                                "id_transaccion": t['id_transaccion'],
                                "agrotienda": t['tienda'],
                                "monto_neto_usd": monto_neto_agrotienda_usd,
                                "referencia": ref_pago_agro,
                                "fecha": datetime.now().strftime('%d/%m/%Y %H:%M')
                            })
                            st.success(f"¡Pago a la agrotienda {t['tienda']} registrado con éxito en la contabilidad!")
                        else:
                            st.error("Ingrese el número de referencia de la transferencia.")
                st.divider()

elif menu == "💬 Gestión de Agradecimiento":
    st.header("💬 Gestión de Agradecimiento a Productores")
    st.markdown("Herramienta administrativa para enviar mensajes de agradecimiento institucional por WhatsApp a los productores de la red.")
    
    with st.form("form_agradecimiento_admin"):
        prod_telf_adm = st.text_input("Teléfono WhatsApp del Productor (Ej: 04121234567):")
        prod_nombre_adm = st.text_input("Nombre del Productor / Finca:")
        
        if st.form_submit_button("Generar Enlace de Agradecimiento"):
            if prod_telf_adm and prod_nombre_adm:
                msg_agradecimiento_adm = f"¡Estimado(a) {prod_nombre_adm}! De parte de la directiva y equipo técnico de {EMPRESA_NOMBRE} (AgroDigital Venezuela), le expresamos nuestro más sincero agradecimiento por la confianza depositada al utilizar nuestra plataforma para potenciar su producción agrícola en la región."
                url_wa_adm = f"https://wa.me/58{prod_telf_adm[-10:]}?text={urllib.parse.quote(msg_agradecimiento_adm)}"
                st.success("¡Enlace generado exitosamente!")
                st.markdown(f"[💬 Enviar mensaje de agradecimiento vía WhatsApp]({url_wa_adm})", unsafe_allow_html=True)
            else:
                st.error("Por favor complete el teléfono y el nombre del productor.")

elif menu == "📄 Generador de Notas de Entrega (PDF)":
    st.header("📄 Generador de Documentación Legal (PDF)")
    if not st.session_state.transacciones_cerradas:
        st.info("No hay transacciones cerradas para certificar.")
    else:
        for t in st.session_state.transacciones_cerradas:
            st.markdown(f"**Transacción #{t['id_transaccion']}** | Productor: {t['productor']} ➔ Agrotienda: {t['tienda']} (${t['precio']:.2f} USD)")
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

if menu == "💳 Pasarela de Pago General BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial (General)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"🏦 Datos Bancarios:\n\n• Razón Social: {EMPRESA_NOMBRE}\n• RIF: {EMPRESA_RIF}\n• Banco: {EMPRESA_BANCO}\n• Teléfono: {EMPRESA_TELEFONO}\n• Tasa BCV Actual: {st.session_state.tasa_bcv:.2f} VES")
    with col2:
        with st.form("form_pago_gen"):
            monto_p = st.number_input("Monto en USD:", min_value=0.0, format="%.2f")
            monto_ves = monto_p * st.session_state.tasa_bcv
            st.write(f"Equivalente a pagar: **{monto_ves:,.2f} VES**")
            ref_p = st.text_input("Número de Referencia:")
            if st.form_submit_button("Validar Pago"):
                if ref_p and monto_p > 0:
                    st.success("¡Pago reportado con éxito!")
                else:
                    st.error("Ingrese referencia y monto.")
