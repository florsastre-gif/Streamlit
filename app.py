import base64
from pathlib import Path
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. CONFIGURACIÓN Y CARGA DE IA
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="SPRING AI SHIFT™", page_icon="🧠", layout="wide")

# ----------------------------
# HELPERS Y CSS
# ----------------------------
def file_to_base64(path: str) -> str:
    if Path(path).exists():
        data = Path(path).read_bytes()
        return base64.b64encode(data).decode("utf-8")
    return None

def inject_global_css():
    st.markdown(
        """
        <style>
          :root { color-scheme: dark; }
          .stApp { background: #000; color: #fff; }
          header, footer { visibility: hidden; }
          .block-container { padding-top: 1.5rem; padding-bottom: 4rem; }
          
          /* Glassmorphism Cards */
          .glass {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(12px);
            margin-bottom: 20px;
          }

          /* Buttons */
          div.stButton > button {
            background: rgba(255,255,255,0.1);
            color: white;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 12px;
            width: 100%;
            transition: 0.3s;
          }
          div.stButton > button:hover {
            background: #fff;
            color: #000;
          }

          /* Hero Video */
          .hero-wrap {
            position: relative;
            width: 100%;
            height: 400px;
            border-radius: 24px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.1);
          }
          .hero-video {
            position: absolute;
            top: 50%; left: 50%;
            min-width: 100%; min-height: 100%;
            transform: translate(-50%, -50%);
            opacity: 0.35;
          }
          .hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%);
          }
          .hero-content {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 40px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------
# COMPONENTES VISUALES
# ----------------------------
def render_hero():
    video_b64 = file_to_base64("assets/hero.mp4")
    video_html = f'<video class="hero-video" autoplay muted loop playsinline><source src="data:video/mp4;base64,{video_b64}" type="video/mp4"></video>' if video_b64 else '<div style="position:absolute;inset:0;background:radial-gradient(circle, #222 0%, #000 100%);"></div>'
    
    st.markdown(f"""
        <div class="hero-wrap">
          {video_html}
          <div class="hero-overlay"></div>
          <div class="hero-content">
            <h1 style="font-size:3rem; font-weight:800; line-height:1;">SPRING AI SHIFT™</h1>
            <p style="font-size:1.2rem; opacity:0.8; max-width:600px; margin-top:10px;">
                Transformamos la IA en claridad accionable. Sin hype ni tecnicismos. 
            </p>
          </div>
        </div>
    """, unsafe_allow_html=True)

# ----------------------------
# LOGICA DE APLICACIÓN
# ----------------------------
inject_global_css()
render_hero()

st.markdown("### ⚡ Clarity Engine")
st.markdown("""
    **No dejes que la complejidad detenga tu crecimiento**. Ingresá tu idea, problema o dolor actual y obtené claridad estratégica inmediata.
""")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    perfil = st.selectbox("¿Cuál es tu enfoque?", ["Soy emprendedor","Soy Empresa y quiero apoyar la causa", "Tengo negocio y quiero crecer"])
    input_text = st.text_area("Pega el texto técnico aquí:", placeholder="Ej: LLM, RAG, Webhooks, Governance...", height=150)
    run_button = st.button("Generar Claridad Accionable")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if run_button and input_text:
        with st.spinner("Procesando capas cognitivas..."):
            # PROMPT ESTRUCTURADO SEGÚN PERFIL
            prompt = f"""
            Actúa como el motor de claridad de SPRING AI SHIFT™.
            El usuario es del perfil: {perfil}.
            Toma este texto y genera una respuesta en 4 capas estrictas:
            1. Versión humana: Explica qué es sin jerga.
            2. Ejemplo cotidiano: Una analogía física según su perfil ({perfil}).
            3. Checklist accionable: 3 pasos concretos para aplicar esto.
            4. Verificación: Una pregunta para confirmar entendimiento.
            
            Texto: {input_text}
            """
            try:
                response = model.generate_content(prompt)
                st.markdown(f'<div class="glass" style="border-left: 4px solid #fff;">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error("Error al conectar con la IA. Revisa tu API Key.")
    else:
        st.markdown('<div class="glass" style="height:310px; display:flex; align-items:center; justify-content:center; opacity:0.5;">Esperando interacción...</div>', unsafe_allow_html=True)

# ----------------------------
# SERVICIOS Y CONTACTO
# ----------------------------
st.divider()
st.markdown("### Servicios & Impacto")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="glass"><b>Strategy Systems</b><br/><small>Gobernanza y velocidad ejecutiva.</small></div>', unsafe_allow_html=True)
    st.button("Ver Strategy")
with c2:
    st.markdown('<div class="glass"><b>Education</b><br/><small>Formación práctica para líderes.</small></div>', unsafe_allow_html=True)
    st.button("Ver Cursos")
with c3:
    st.markdown('<div class="glass"><b>Impact Partnerships</b><br/><small>Cerrando brechas con ONGs.</small></div>', unsafe_allow_html=True)
    st.button("Ver Alianzas")

# Newsletter simplificado
st.divider()
email = st.text_input("Quiero que se contacten conmigo: Tu email")
if st.button("Allí voy"):
    st.toast("¡Suscrito con éxito!")
