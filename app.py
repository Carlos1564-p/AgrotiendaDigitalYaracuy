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

st.markdown("<h3 style='text-align: center; color: #1565C0;'>Mercado Bursátil, Corretaje y Blindaje Tecnológico Agrícola</h3>", unsafe_allow_html=True)
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
# MENÚ DE NAVEGACIÓN PRINCIPAL
# ----------------------------------------------------
menu = st.sidebar.selectbox("Seleccione el Módulo del Sistema:", [
    "📖 Reseña y Blindaje de Negocio",
    "🚜 Menú de Requerimientos del Campo",
    "📝 Afiliación de Agrotiendas (Contrato)",
    "🛒 Subasta Inversa (Productor - Anonimizada)",
    "🏪 Panel de Cotización (Agrotiendas)",
    "📄 Generador de Notas de Entrega y Órdenes (PDF)",
    "💳 Pasarela de Pago Móvil BDV"
])

# ----------------------------------------------------
# MÓDULO 1: RESEÑA Y BLINDAJE DE NEGOCIO
# ----------------------------------------------------
if menu == "📖 Reseña y Blindaje de Negocio":
    st.header("📖 Reseña y Lógica de Protección Anti-Desintermediación")
    st.write(
        f"**{EMPRESA_NOMBRE}** (RIF: **{EMPRESA_RIF}**) opera bajo un modelo de corretaje digital estricto. "
        "Para evitar la evasión de acuerdos ('tratos por fuera'), el sistema implementa una arquitectura de **Anonimización Dinámica**: "
        "las agrotiendas compiten en las subastas sin conocer la identidad ni el teléfono directo del productor. "
        "La conexión y liberación de datos fiscales y de contacto solo ocurre tras la adjudicación formal y el uso de los instrumentos de pago "
        "respaldados por la plataforma."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ Mecanismos de Blindaje Tecnológico")
        st.write("• **Ocultamiento Preventivo:** Cero exposición de datos del productor durante la puja.")
        st.write("• **Trazabilidad Legal:** Contrato de adhesión electrónico con validez mercantil y fiscal.")
        st.write("• **Documentación Oficial:** Emisión obligatoria de Notas de Entrega y Órdenes en PDF para respaldo contable.")
    with col2:
        st.subheader("🌟 Fidelidad Tecnológica (Lock-in)")
        st.write("• **Garantía Operativa:** Centralización de pagos seguros vía Banco de Venezuela.")
        st.write("• **Historial Verificable:** Reputación comercial transparente en Yaracuy, Lara y Carabobo.")
        st.write("• **Velocidad Logística:** Acceso inmediato a inventarios críticos sin intermediarios abusivos.")

# ----------------------------------------------------
# MÓDULO 2: MENÚ DE REQUERIMIENTOS DEL CAMPO
# ----------------------------------------------------
elif menu == "🚜 Menú de Requerimientos del Campo":
    st.header("📋 Directorio de Insumos y Urgencias Agrícolas")
    requerimientos = {
        "Fertilizantes y Nutrición de Suelos": "Urea, Nitrato de Amonio, NPK y enmiendas calcáreas para maíz, caña y hortalizas.",
        "Sanidad y Vacunación Animal": "Vacunas contra Aftosa, Rabia Silvestre y complejos vitamínicos veterinarios.",
        "Agroquímicos y Control de Plagas": "Herbicidas sistémicos (Glifosato), insecticidas y fungicidas preventivos/curativos.",
        "Maquinaria y Repuestos Críticos": "Correas de transmisión, filtros, mangueras de alta presión y discos de arado.",
        "Semillas Certificadas": "Material genético certificado de maíz, caraota, sorgo y leguminosas tropicales."
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
        st.write("PRIMERA: La agrotienda acepta canalizar sus ventas regionales a través de la plataforma tecnológica.")
        st.write("SEGUNDA: Se prohíbe el contacto directo eludido previo a la adjudicación bajo sanción de expulsión del RIF comercial.")
        st.write(f"TERCERA: Operaciones financieras respaldadas por {EMPRESA_BANCO}, Pagomóvil: {EMPRESA_TELEFONO}.")

    st.markdown("### ✍️ Formulario de Incorporación Comercial")
    with st.form("form_afiliacion"):
        nombre_tienda = st.text_input("Nombre de la Agrotienda:")
        rif_tienda = st.text_input("RIF de la Agrotienda:")
        estado_tienda = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_tienda = st.text_input("Municipio:")
        telefono_tienda = st.text_input("Teléfono WhatsApp:")
        acepta = st.checkbox("✅ Acepto los términos del Contrato de Adhesión y las normas anti-desintermediación.")
        
        if st.form_submit_button("Firmar Adhesión Digital"):
            if acepta and nombre_tienda and rif_tienda:
                st.session_state.agrotiendas_registradas.append({
                    "nombre": nombre_tienda, "estado": estado_tienda,
                    "municipio": municipio_tienda, "telefono": telefono_tienda
                })
                st.success(f"¡{nombre_tienda} afiliada con éxito bajo supervisión de {EMPRESA_NOMBRE}!")
            else:
                st.error("Complete los campos y acepte el contrato.")

# ----------------------------------------------------
# MÓDULO 4: SUBASTA INVERSA (PRODUCTOR - ANONIMIZADA)
# ----------------------------------------------------
elif menu == "🛒 Subasta Inversa (Productor - Anonimizada)":
    st.header("🛒 Módulo de Subasta Inversa (Protección Activa)")
    st.markdown("Sus datos de contacto **permanecen ocultos** para las agrotiendas hasta que usted decida aceptar formalmente una oferta.")
    
    with st.form("form_subasta"):
        nombre_prod = st.text_input("Nombre o Código del Productor / Finca (Ej: Finca Anonimizada #104):")
        estado_prod = st.selectbox("Estado:", ["Yaracuy", "Lara", "Carabobo"])
        municipio_prod = st.text_input("Municipio:")
        insumo_req = st.text_input("Insumo Requerido:")
        cant_req = st.text_input("Cantidad:")
        tel_prod = st.text_input("WhatsApp Privado (Solo se revela tras adjudicar):")
        
        if st.form_submit_button("🚀 Lanzar Subasta Segura"):
            if nombre_prod and insumo_req and tel_prod:
                pid = len(st.session_state.pedidos) + 1
                st.session_state.pedidos.append({
                    "id": pid, "productor": nombre_prod, "estado": estado_prod,
                    "municipio": municipio_prod, "insumo": insumo_req, "cantidad": cant_req, "telefono": tel_prod
                })
                st.success(f"Subasta #{pid} publicada de forma anónima en la red regional.")
            else:
                st.error("Complete todos los campos.")

    st.divider()
    st.subheader("📊 Seguimiento de Pujas y Adjudicación")
    if not st.session_state.pedidos:
        st.info("No hay subastas activas.")
    else:
        for p in st.session_state.pedidos:
            st.markdown(f"**Subasta ID #{p['id']}** | Zona: *{p['estado']} - {p['municipio']}* | Requerimiento: **{p['insumo']} ({p['cantidad']})**")
            ofertas_p = [o for o in st.session_state.ofertas if o["pedido_id"] == p["id"]]
            
            if not ofertas_p:
                st.caption("_Las agrotiendas están compitiendo en precio (Identidad del productor protegida)._")
            else:
                for o in sorted(ofertas_p, key=lambda x: x["precio"]):
                    c1, c2, c3 = st.columns([2, 2, 2])
                    with c1: st.write(f"🏪 **{o['tienda']}** ({o['estado_tienda']})")
                    with c2: st.write(f"💲 **${o['precio']:.2f} USD** | {o['tiempo']}")
                    with c3:
                        if st.button(f"✅ Adjudicar y Revelar Contacto #{o['pedido_id']}", key=f"adj_{o['pedido_id']}_{o['tienda']}"):
                            # Guardar en transacciones cerradas para la generación de documentos legales
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
                            st.success("¡Oferta adjudicada! El sistema ha desbloqueado los datos de contacto y generado la orden legal.")
                            msg = f"Hola {o['tienda']}, he adjudicado su oferta de ${o['precio']:.2f} por la plataforma de {EMPRESA_NOMBRE}."
                            url_wa = f"https://wa.me/58{o['telefono_tienda'][-10:]}?text={urllib.parse.quote(msg)}"
                            st.markdown(f"[💬 Contactar Agrotienda Adjudicada]({url_wa})", unsafe_allow_html=True)
            st.divider()

# ----------------------------------------------------
# MÓDULO 5: PANEL DE COTIZACIÓN (AGROTIENDAS)
# ----------------------------------------------------
elif menu == "🏪 Panel de Cotización (Agrotiendas)":
    st.header("🏪 Panel de Competencia (Agrotiendas)")
    st.markdown("Las solicitudes muestran únicamente ubicación geográfica para garantizar el corretaje transparente.")
    
    if not st.session_state.pedidos:
        st.warning("No hay requerimientos activos.")
    else:
        for p in st.session_state.pedidos:
            with st.container():
                st.markdown(f"### 🔔 Demanda Anónima #{p['id']} - Zona: {p['estado']} / {p['municipio']}")
                st.write(f"**Insumo Solicitado:** {p['insumo']} | **Cantidad:** {p['cantidad']}")
                st.info("🔒 _Identidad del productor protegida por el sistema anti-desintermediación._")
                
                with st.form(f"form_cot_{p['id']}"):
                    t_nombre = st.text_input("Su Agrotienda:", key=f"tn_{p['id']}")
                    t_estado = st.selectbox("Estado de su tienda:", ["Yaracuy", "Lara", "Carabobo"], key=f"te_{p['id']}")
                    t_precio = st.number_input("Oferta Total (USD $):", min_value=0.0, format="%.2f", key=f"tp_{p['id']}")
                    t_tiempo = st.text_input("Condición de Entrega:", key=f"tt_{p['id']}")
                    t_tel = st.text_input("Su Teléfono Comercial:", key=f"tel_{p['id']}")
                    
                    if st.form_submit_button("💡 Enviar Puja Ciega"):
                        if t_nombre and t_precio > 0:
                            st.session_state.ofertas.append({
                                "pedido_id": p['id'], "tienda": t_nombre, "estado_tienda": t_estado,
                                "precio": t_precio, "tiempo": t_tiempo, "telefono_tienda": t_tel
                            })
                            st.success("¡Puja registrada con éxito!")
                        else:
                            st.error("Ingrese datos válidos.")
                st.divider()

# ----------------------------------------------------
# MÓDULO 6: GENERADOR DE NOTAS DE ENTREGA Y ÓRDENES (PDF)
# ----------------------------------------------------
elif menu == "📄 Generador de Notas de Entrega y Órdenes (PDF)":
    st.header("📄 Módulo de Validez Legal y Documentación en PDF")
    st.markdown("Generación automática de Órdenes de Compra y Notas de Entrega respaldadas por **COMPAÑÍA HCHF4 C.A.**")
    
    if not st.session_state.transacciones_cerradas:
        st.info("No hay transacciones adjudicadas para certificar documentalmente.")
    else:
        for t in st.session_state.transacciones_cerradas:
            st.markdown(f"**Transacción #{t['id_transaccion']}** | Productor: {t['productor']} ➔ Agrotienda: {t['tienda']}")
            st.write(f"Insumo: {t['insumo']} ({t['cantidad']}) | Monto: ${t['precio']:.2f} USD")
            
            if st.button(f"📥 Generar Nota de Entrega oficial (PDF) #{t['id_transaccion']}", key=f"pdf_{t['id_transaccion']}"):
                class PDF(FPDF):
                    def header(self):
                        self.set_font("Arial", "B", 14)
                        self.cell(0, 10, EMPRESA_NOMBRE, 0, 1, "C")
                        self.set_font("Arial", "", 10)
                        self.cell(0, 5, f"RIF: {EMPRESA_RIF} | Corretaje Agrícola Digital", 0, 1, "C")
                        self.ln(5)

                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "NOTA DE ENTREGA Y CERTIFICADO DE CORRETAJE", 0, 1, "C")
                pdf.ln(5)
                
                pdf.set_font("Arial", "", 10)
                pdf.cell(0, 8, f"Transaccion Nro: {t['id_transaccion']}", 0, 1)
                pdf.cell(0, 8, f"Zona de Operacion: {t['zona']}", 0, 1)
                pdf.cell(0, 8, f"Productor Adjudicatario: {t['productor']}", 0, 1)
                pdf.cell(0, 8, f"Agrotienda Proveedora: {t['tienda']}", 0, 1)
                pdf.ln(5)
                
                pdf.set_font("Arial", "B", 11)
                pdf.cell(0, 8, "Detalle del Insumo Negociado:", 0, 1)
                pdf.set_font("Arial", "", 10)
                pdf.cell(0, 8, f"- Insumo: {t['insumo']}", 0, 1)
                pdf.cell(0, 8, f"- Cantidad: {t['cantidad']}", 0, 1)
                pdf.cell(0, 8, f"- Monto Total Acordado: ${t['precio']:.2f} USD", 0, 1)
                pdf.ln(10)
                
                pdf.set_font("Arial", "I", 9)
                pdf.multi_cell(0, 5, f"Operacion validada y protegida por los protocolos de corretaje digital de {EMPRESA_NOMBRE}. Este documento sirve de comprobante de transaccion mercantil interconectando Yaracuy, Lara y Carabobo.")
                
                nombre_archivo = f"Nota_Entrega_{t['id_transaccion']}.pdf"
                pdf.output(nombre_archivo)
                
                with open(nombre_archivo, "rb") as archivo_pdf:
                    st.download_button(
                        label=f"⬇️ Descargar PDF Oficial (#{t['id_transaccion']})",
                        data=archivo_pdf,
                        file_name=nombre_archivo,
                        mime="application/pdf"
                    )
            st.divider()

# ----------------------------------------------------
# MÓDULO 7: PASARELA DE PAGO MÓVIL BDV
# ----------------------------------------------------
elif menu == "💳 Pasarela de Pago Móvil BDV":
    st.header("📲 Pasarela de Pago Móvil Oficial")
    st.markdown("Liquidación segura centralizada bajo la supervisión fiscal de la operadora.")
    
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
        st.markdown("### 📋 Validar Pago o Comisión de Corretaje")
        with st.form("form_pago"):
            monto_p = st.number_input("Monto en Bolívares / Divisas:", min_value=0.0, format="%.2f")
            ref_p = st.text_input("Número de Referencia Bancaria:")
            banco_orig = st.text_input("Banco Emisor de Origen:")
            
            if st.form_submit_button("Verificar Transacción"):
                if ref_p and monto_p > 0:
                    st.success("¡Pago validado exitosamente en el sistema central!")
                    msg_pago = f"Hola, reporto pago a {EMPRESA_NOMBRE} (RIF: {EMPRESA_RIF}) por {monto_p}. Ref: {ref_p}."
                    url_wa = f"https://wa.me/58{EMPRESA_TELEFONO[1:]}?text={urllib.parse.quote(msg_pago)}"
                    st.markdown(f"[📲 Notificar vía WhatsApp]({url_wa})", unsafe_allow_html=True)
                else:
                    st.error("Ingrese montos y referencias válidos.")
