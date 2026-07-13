import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from google import genai
from google.genai import types

# Page Config
st.set_page_config(
    page_title="PulseArena 2026 - FIFA World Cup Smart Stadium Copilot",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glass Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .kpi-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 255, 204, 0.4);
        box-shadow: 0 12px 40px 0 rgba(0, 255, 204, 0.15);
    }
    
    .kpi-title {
        color: #9CA3AF;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }
    
    .kpi-value-green {
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(135deg, #00FFCC 0%, #33FF33 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-value-purple {
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(135deg, #A855F7 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-value-gold {
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(135deg, #F59E0B 0%, #10B981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .alert-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 16px;
        color: #F87171;
        margin-bottom: 20px;
    }
    
    .ai-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        padding: 20px;
        color: #E0E7FF;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function: Check Gemini availability and call API
def call_gemini_api(api_key, prompt, system_instruction=None):
    if not api_key:
        return None
    try:
        # Configure the official GenAI Client
        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig()
        if system_instruction:
            config.system_instruction = system_instruction
            
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

# High-fidelity mock AI answers
def get_mock_fan_response(query, language):
    q = query.lower()
    if "wheelchair" in q or "access" in q or "ramp" in q or "elevator" in q:
        res = {
            "English": "👨‍🦽 **Accessibility Support**:\nWheelchair-accessible seating is located on Level 1 in Sections 105, 112, and 124. Level 2 has elevators situated near Gates A and C. Elevators have tactile lettering and audio announcements. You can request a stadium wheelchair escort at any help desk.",
            "Spanish": "👨‍🦽 **Soporte de Accesibilidad**:\nLos asientos accesibles para sillas de ruedas se encuentran en el Nivel 1 en las Secciones 105, 112 y 124. El Nivel 2 cuenta con ascensores situados cerca de las Puertas A y C. Los ascensores cuentan con letras táctiles y anuncios de audio. Puede solicitar asistencia en silla de ruedas en cualquier mesa de ayuda.",
            "French": "👨‍🦽 **Assistance Accessibilité**:\nLes sièges accessibles aux fauteuils roulants sont situés au niveau 1 dans les sections 105, 112 et 124. Le niveau 2 dispose d'ascenseurs situés près des portes A et C. Les ascenseurs disposent de lettrage tactile et d'annonces audio. Vous pouvez demander un accompagnement en fauteuil roulant à n'importe quel bureau d'assistance."
        }
        return res.get(language, res["English"])
    elif "shuttle" in q or "bus" in q or "transit" in q or "metro" in q or "train" in q:
        res = {
            "English": "🚌 **Transportation Guide**:\nShuttle buses leave from Gate B every 5 minutes connecting directly to the Central Metro Station. Metro Line 2 is accessible via the West Exit. Rideshares can pick up at Zone 4. Using public transit saves 1.8kg of CO2 per trip!",
            "Spanish": "🚌 **Guía de Transporte**:\nLos autobuses lanzadera salen de la Puerta B cada 5 minutos y conectan directamente con la estación central de metro. La línea 2 del metro es accesible a través de la salida oeste. Los viajes compartidos se recogen en la Zona 4. ¡El transporte público ahorra 1.8kg de CO2 por viaje!",
            "French": "🚌 **Guide des Transports**:\nDes navettes partent de la porte B toutes les 5 minutes et relient directement la station de métro centrale. La ligne 2 du métro est accessible par la sortie ouest. Les trajets partagés peuvent être récupérés dans la zone 4. L'utilisation des transports en commun permet d'économiser 1,8 kg de CO2 par trajet!"
        }
        return res.get(language, res["English"])
    elif "eco" in q or "sustain" in q or "point" in q or "recycle" in q:
        res = {
            "English": "♻️ **Sustainability Center**:\nYou can earn Eco-Points by scanning the QR codes at recycling bins in the concourse, or by logging your transit journey in the Sustainability tab. Swap 100 points for a discount at the FIFA Fan Shop!",
            "Spanish": "♻️ **Centro de Sostenibilidad**:\nPuedes ganar Puntos Ecológicos escaneando los códigos QR en los contenedores de reciclaje del pasillo, o registrando tu viaje en transporte público en la pestaña de Sostenibilidad. ¡Canjea 100 puntos por un descuento en la Tienda Oficial de la FIFA!",
            "French": "♻️ **Centre de Durabilité**:\nVous pouvez gagner des éco-points en scannant les codes QR sur les bacs de recyclage dans le hall, ou en enregistrant votre trajet en transport en commun dans l'onglet Durabilité. Échangez 100 points contre une réduction à la boutique officielle de la FIFA!"
        }
        return res.get(language, res["English"])
    elif "gate" in q or "find" in q or "navig" in q:
        res = {
            "English": "📍 **Navigation Assist**:\nGate A is on the north side, Gate B is on the east side, Gate C is on the south side. If your ticket says 'Section 100-115', Gate A is your closest entrance. If you are arriving from the metro station, follow the blue pathway to Gate B.",
            "Spanish": "📍 **Asistente de Navegación**:\nLa Puerta A está en el lado norte, la Puerta B en el lado este, la Puerta C en el lado sur. Si su boleto indica 'Sección 100-115', la Puerta A es su entrada más cercana. Si llega desde la estación de metro, siga el camino azul hacia la Puerta B.",
            "French": "📍 **Aide à la Navigation**:\nLa porte A est du côté nord, la porte B du côté est, la porte C du côté sud. Si votre billet indique 'Section 100-115', la porte A est votre entrée la plus proche. Si vous arrivez de la station de métro, suivez le chemin bleu vers la porte B."
        }
        return res.get(language, res["English"])
    else:
        res = {
            "English": "👋 Welcome to the **FIFA World Cup 2026 PulseArena Assistant**! I am your GenAI copilot. Ask me anything about stadium gates, accessibility support, concessions, or public transport.",
            "Spanish": "👋 ¡Bienvenido al **Asistente PulseArena de la Copa Mundial de la FIFA 2026**! Soy su copiloto de GenAI. Pregúnteme cualquier cosa sobre las puertas del estadio, accesibilidad, comida o transporte público.",
            "French": "👋 Bienvenue dans **l'Assistant PulseArena de la Coupe du Monde de la FIFA 2026**! Je suis votre copilote GenAI. Posez-moi des questions sur les portes du stade, l'accessibilité, la nourriture ou les transports."
        }
        return res.get(language, res["English"])

def calculate_eco_points(journey_mode, journey_distance):
    co2_factors = {
        "Walking / Running": 0.25,
        "Cycling": 0.22,
        "Metro Train": 0.15,
        "Shuttle Bus": 0.10,
        "Rideshare / Car": 0.0
    }
    factor = co2_factors.get(journey_mode, 0.0)
    co2_saved = journey_distance * factor
    points_earned = int(co2_saved * 10)
    return points_earned, co2_saved

def parse_incident_report(ai_response):
    if not ai_response:
        return "", "Medium"
    try:
        parts = ai_response.split('|')
        summary = parts[0].replace("Summary:", "").strip()
        severity = parts[1].replace("Severity:", "").strip()
        if severity not in ["High", "Medium", "Low"]:
            severity = "Medium"
        return summary, severity
    except Exception:
        return ai_response.strip(), "Medium"

# Initialize session state variables
if "incidents" not in st.session_state:
    st.session_state.incidents = pd.DataFrame(columns=["Incident ID", "Category", "Zone", "Details", "Summary", "Severity"])
if "eco_points" not in st.session_state:
    st.session_state.eco_points = 50

# App Branding Sidebar
st.sidebar.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='background: linear-gradient(135deg, #00FFCC 0%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; font-weight: 800; margin-bottom: 0;'>PULSEARENA</h1>
        <p style='color: #9CA3AF; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px;'>Stadium Copilot 2026</p>
    </div>
    """, unsafe_allow_html=True
)

# Sidebar API Key Input
st.sidebar.markdown("---")
st.sidebar.subheader("🔌 AI Configuration")
gemini_key = st.sidebar.text_input("Google Gemini API Key", type="password", help="Input your Gemini API key to activate real generative capabilities. Leave blank to run in simulated mode.")

if gemini_key:
    st.sidebar.success("Gemini API Key Loaded!")
else:
    st.sidebar.info("Simulated Mode (Mock AI Active)")

# Sidebar Navigation Mode
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 View Mode")
view_mode = st.sidebar.radio("Select Interface", ["🏟️ Fan Portal", "📋 Staff Operations Hub"])

st.sidebar.markdown("---")
st.sidebar.subheader("♿ Accessibility Settings")
access_mode = st.sidebar.checkbox("High Contrast & Text Zoom Mode", help="Enhances text contrast and enlarges elements for screen readers and visually impaired users.")

if access_mode:
    st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-size: 18px !important;
        }
        .kpi-card {
            background: #000000 !important;
            border: 2px solid #FFFFFF !important;
            color: #FFFFFF !important;
        }
        .kpi-title {
            color: #FFFFFF !important;
            font-size: 16px !important;
            font-weight: 700 !important;
        }
        .kpi-value-green, .kpi-value-purple, .kpi-value-gold {
            background: none !important;
            -webkit-text-fill-color: initial !important;
            color: #FFFF00 !important;
            font-size: 44px !important;
        }
        .alert-box {
            background: #000000 !important;
            border: 2px solid #FF0000 !important;
            color: #FF6666 !important;
        }
        .ai-box {
            background: #000000 !important;
            border: 2px solid #00FFFF !important;
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Main Header
col_logo, col_header = st.columns([1, 10])
with col_logo:
    if os.path.exists("stadium_banner.png"):
        st.image("stadium_banner.png", width=120)
    else:
        st.write("🏆")
with col_header:
    st.title("PulseArena 2026 — Smart Venue Operations & Experience")
    st.write("Leveraging Generative AI to optimize stadium logistics, accessibility, and fan operations for the FIFA World Cup 2026.")

# =========================================================================
# FAN PORTAL VIEW
# =========================================================================
if view_mode == "🏟️ Fan Portal":
    # Banner
    if os.path.exists("stadium_banner.png"):
        st.image("stadium_banner.png", width="stretch")
        
    st.markdown('## <span role="img" aria-label="stadium">🏟️</span> Fan Assistance & Accessibility Hub', unsafe_allow_html=True)
    
    col_chat, col_info = st.columns([3, 2])
    
    with col_chat:
        st.markdown('### <span role="img" aria-label="speech balloon">💬</span> Ask the PulseArena Fan Copilot', unsafe_allow_html=True)
        st.write("Our AI assistant supports multilingual text. Type your query below.")
        
        fan_lang = st.selectbox("Preferred Language", ["English", "Spanish", "French"])
        fan_query = st.text_input("What would you like assistance with? (e.g. finding wheelchair ramps, shuttle schedules, eco-points)", key="fan_query_input")
        
        if st.button("Ask Copilot"):
            if fan_query:
                with st.spinner("GenAI Copilot thinking..."):
                    if gemini_key:
                        prompt = f"The fan asks in {fan_lang}: '{fan_query}'. Answer them concisely and helper-fully. Include emojis."
                        system_instruction = "You are the FIFA World Cup 2026 PulseArena Assistant. You help fans navigate the stadium, find food, transport, and accessibility options (elevators, wheelchair ramps). You reply in the fan's selected language."
                        answer = call_gemini_api(gemini_key, prompt, system_instruction)
                    else:
                        answer = get_mock_fan_response(fan_query, fan_lang)
                    
                    st.markdown(f"""
                    <div class="ai-box" role="region" aria-label="AI Copilot Response Box">
                        <strong><span role="img" aria-label="robot">🤖</span> AI Copilot Response:</strong><br><br>
                        {answer}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please type a question first.")
                
        # Quick actions
        st.write("**Quick Help Prompts:**")
        q_cols = st.columns(3)
        with q_cols[0]:
            if st.button("📍 Find Nearest Gate"):
                st.info(get_mock_fan_response("gate", fan_lang))
        with q_cols[1]:
            if st.button("♿ Wheelchair Access Routes"):
                st.info(get_mock_fan_response("wheelchair", fan_lang))
        with q_cols[2]:
            if st.button("🚌 Shuttle Metro Service"):
                st.info(get_mock_fan_response("shuttle", fan_lang))

    with col_info:
        st.subheader("🍔 Live Concession Queue Tracker")
        st.write("Avoid the rush! Real-time crowd sensors monitor concession stand queue wait-times.")
        
        stands = ["Hotdog & Burger Zone", "Taco Arena", "Soda & Refreshments Station", "FIFA Official Merchandise"]
        queues = [12, 28, 4, 35] # queue lengths
        waits = [5, 15, 2, 20] # in minutes
        
        stand_data = pd.DataFrame({"Stand": stands, "Queue Length": queues, "Avg Wait (Mins)": waits})
        
        # Plot concession queues
        fig_concessions = px.bar(
            stand_data,
            x="Avg Wait (Mins)",
            y="Stand",
            orientation="h",
            color="Avg Wait (Mins)",
            color_continuous_scale="RdYlGn_r",
            labels={"Avg Wait (Mins)": "Wait Time (Minutes)", "Stand": "Stand"},
            text="Avg Wait (Mins)"
        )
        fig_concessions.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E7EB',
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_concessions, width="stretch")

    # Transit & Eco Tracker Row
    st.markdown("---")
    st.subheader("♻️ Sustainability & Transport Hub")
    
    transit_col, eco_col = st.columns(2)
    
    with transit_col:
        st.markdown("#### 🚇 Sustainable Transit Schedule")
        st.write("World Cup 2026 encourages green travel. Check the latest transit status:")
        
        transports = ["Metro Line 1 (Northbound)", "Metro Line 2 (Westbound)", "Shuttle Bus Route A (Central Station)", "ECO Bike Share Dock"]
        status = ["On Time (Normal)", "On Time (Normal)", "2 Min Delay (High Demand)", "12 Bikes Available"]
        carbon_savings = ["-1.8 kg CO2", "-1.8 kg CO2", "-1.1 kg CO2", "-2.5 kg CO2"]
        
        transit_df = pd.DataFrame({"Transit Mode": transports, "Status": status, "CO2 Saved / Trip": carbon_savings})
        st.dataframe(transit_df, hide_index=True, width="stretch")

    with eco_col:
        st.markdown("#### ⚡ Log Your Journey & Earn Eco-Points")
        st.write(f"Your current Eco-Points: **{st.session_state.eco_points}** 🪙")
        
        journey_mode = st.selectbox("How did you get to the stadium today?", ["Walking / Running", "Cycling", "Metro Train", "Shuttle Bus", "Rideshare / Car"])
        journey_distance = st.slider("Travel distance (in km)", 1, 50, 5)
        
        if st.button("Log Green Trip & Claim Points"):
            points_earned, co2_saved = calculate_eco_points(journey_mode, journey_distance)
            if points_earned > 0:
                st.session_state.eco_points += points_earned
                st.success(f"🌱 Journey logged! You saved {co2_saved:.2f}kg of CO2! Earned **{points_earned} Eco-Points**.")
            else:
                st.info("Log a public transit or active journey to earn Eco-Points.")

# =========================================================================
# STAFF OPERATIONS HUB VIEW
# =========================================================================
else:
    st.markdown('## <span role="img" aria-label="clipboard">📋</span> Venue Operations & Decision Support', unsafe_allow_html=True)
    
    # KPI Row
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(
            """
            <div class="kpi-card" role="region" aria-label="Total Attendance Metric">
                <div class="kpi-title">Total Attendance</div>
                <div class="kpi-value-green">74,250</div>
            </div>
            """, unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            """
            <div class="kpi-card" role="region" aria-label="Active Gate Flow Metric">
                <div class="kpi-title">Active Gate Flow</div>
                <div class="kpi-value-purple">620 / min</div>
            </div>
            """, unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            f"""
            <div class="kpi-card" role="region" aria-label="Logged Incidents Count Metric">
                <div class="kpi-title">Logged Incidents</div>
                <div class="kpi-value-gold">{len(st.session_state.incidents)}</div>
            </div>
            """, unsafe_allow_html=True
        )
    with kpi_cols[3]:
        st.markdown(
            """
            <div class="kpi-card" role="region" aria-label="Venue Security Status Metric">
                <div class="kpi-title">Venue Status</div>
                <div class="kpi-value-green">SECURE</div>
            </div>
            """, unsafe_allow_html=True
        )

    # Crowd Control Row
    st.markdown("---")
    crowd_col, ai_plan_col = st.columns([3, 2])
    
    with crowd_col:
        st.subheader("📊 Live Crowd Density Simulation")
        st.write("Sensors monitor densities in key zones. Zoom & hover to inspect.")
        
        # Simulate density grid for stadium sectors
        sectors = ["North Gate A", "East Gate B", "South Gate C", "West Exit D", "Lower Concourse", "Upper Concourse", "VIP Concourse", "Food Arena"]
        x_coords = [1, 5, 1, 5, 2.5, 2.5, 3.0, 2.0]
        y_coords = [5, 5, 1, 1, 4.0, 2.0, 3.0, 3.0]
        densities = [45, 92, 38, 55, 62, 70, 48, 81] # simulated occupancy %
        
        density_df = pd.DataFrame({"Zone": sectors, "X": x_coords, "Y": y_coords, "Density (%)": densities})
        
        # Plot Heatmap Scatter
        fig_crowd = px.scatter(
            density_df,
            x="X",
            y="Y",
            size="Density (%)",
            color="Density (%)",
            hover_name="Zone",
            color_continuous_scale="Viridis",
            size_max=40,
            text="Zone"
        )
        fig_crowd.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E7EB',
            height=340,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_crowd.update_xaxes(showgrid=False, showticklabels=False)
        fig_crowd.update_yaxes(showgrid=False, showticklabels=False)
        st.plotly_chart(fig_crowd, width="stretch")

    with ai_plan_col:
        st.markdown('### <span role="img" aria-label="light bulb">💡</span> GenAI Crowd Control Action Plan', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="alert-box" role="alert" aria-live="assertive">
                <strong><span role="img" aria-label="warning">⚠️</span> Alert: East Gate B Density Exceeds 85% (Critical Bottleneck)</strong>
            </div>
            """, unsafe_allow_html=True
        )
        
        if st.button("Generate Re-routing Strategy"):
            with st.spinner("AI analyzing densities and generating strategy..."):
                if gemini_key:
                    prompt = (
                        "Generate a crowd re-routing strategy for stadium operations. "
                        "Current status: East Gate B is at 92% density (bottleneck), while South Gate C is at 38% "
                        "and North Gate A is at 45%. Concession food arena is at 81%. "
                        "Provide 3 clear, actionable operational steps for venue volunteers and safety staff."
                    )
                    ai_plan = call_gemini_api(gemini_key, prompt)
                else:
                    ai_plan = (
                        "🟢 **PulseArena AI Action Plan (Simulated)**:\n\n"
                        "1. **Spectator Re-routing**: Immediately activate concourse LED signage. "
                        "Direct arriving ticket holders from Gate B outer plaza to Gate C (only 38% occupied).\n"
                        "2. **Staff Redeployment**: Shift 8 concourse safety volunteers from VIP lounge "
                        "to Gate B to assist in queue structuring and manual ticket scan verifications.\n"
                        "3. **Broadcast Notification**: Trigger a location-based push alert in the Fan App: "
                        "*'Gate B is currently congested. Please proceed to Gate C for faster entry (est. wait 4 mins)'.*"
                    )
                st.markdown(f"""
                <div class="ai-box" role="region" aria-label="AI Generated Action Plan">
                    <strong><span role="img" aria-label="robot">🤖</span> GenAI Action Plan:</strong><br><br>
                    {ai_plan}
                </div>
                """, unsafe_allow_html=True)

    # Incident Management Row
    st.markdown("---")
    st.subheader("📋 GenAI Incident Logger & Summary Processor")
    
    log_col, list_col = st.columns([2, 3])
    
    with log_col:
        st.markdown("#### Log New Venue Incident")
        cat = st.selectbox("Category", ["Facilities", "Security", "Medical", "Ticketing"])
        zone = st.selectbox("Zone / Location", ["Zone A (Gate A Concourse)", "Zone B (Gate B Concourse)", "Zone C (Level 1 Seating)", "Zone D (Food Court)"])
        details = st.text_area("Detailed Incident Report (Type freely in any language)")
        
        if st.button("Submit & Process Incident"):
            if details:
                with st.spinner("AI processing report..."):
                    if gemini_key:
                        prompt = f"Analyze this incident: '{details}'. Categorize and output a 1-line summary in English, followed by a severity rating (High, Medium, Low) and suggested immediate operational response."
                        system_instruction = "You are a venue operations analyst. You classify stadium incident reports. You must output EXACTLY in this format: Summary: <summary> | Severity: <High/Medium/Low> | Response: <suggested action>"
                        ai_res = call_gemini_api(gemini_key, prompt, system_instruction)
                        
                        # Parse results
                        summary, severity = parse_incident_report(ai_res)
                    else:
                        # Simulated AI Processing
                        q = details.lower()
                        if "medical" in q or "hurt" in q or "fall" in q or "blood" in q or "chest" in q:
                            summary = "Spectator reporting physical distress/injury in logged zone."
                            severity = "High"
                        elif "fight" in q or "argument" in q or "drunk" in q or "stole" in q:
                            summary = "Security disturbance reported; intervention requested."
                            severity = "High"
                        elif "spill" in q or "leak" in q or "broken" in q or "trash" in q or "dirty" in q:
                            summary = "Facilities maintenance issue requiring cleaning crew."
                            severity = "Low"
                        else:
                            summary = "General incident report logged for dispatch check."
                            severity = "Medium"
                    
                    # Generate ID
                    inc_id = f"INC-{len(st.session_state.incidents) + 101}"
                    new_inc = pd.DataFrame([{
                        "Incident ID": inc_id,
                        "Category": cat,
                        "Zone": zone,
                        "Details": details,
                        "Summary": summary,
                        "Severity": severity
                    }])
                    st.session_state.incidents = pd.concat([st.session_state.incidents, new_inc], ignore_index=True)
                    st.success(f"Incident {inc_id} processed by GenAI and logged!")
            else:
                st.warning("Please input incident details first.")

    with list_col:
        st.markdown("#### Active Incidents Board")
        if not st.session_state.incidents.empty:
            # Highlight Severity with custom colors or dataframe display
            st.dataframe(
                st.session_state.incidents,
                column_config={
                    "Incident ID": "ID",
                    "Category": "Category",
                    "Zone": "Zone",
                    "Details": "Logged Detail",
                    "Summary": "GenAI Summary",
                    "Severity": "Severity Rating"
                },
                hide_index=True,
                width="stretch"
            )
            
            # Interactive action trigger
            st.write("---")
            st.markdown("##### ⚡ Dispatch Dispatcher Response")
            inc_to_dispatch = st.selectbox("Select Incident ID to dispatch crew for:", st.session_state.incidents["Incident ID"].unique())
            if st.button("Confirm Crew Dispatch"):
                st.success(f"Radio call dispatched to safety volunteers in selected zone for {inc_to_dispatch}!")
        else:
            st.info("No incidents logged in the system currently. All sectors are clear.")
