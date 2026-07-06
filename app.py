import streamlit as st
from google import genai
from google.genai import types


#  STREAMLIT PAGE CONFIGURATION

st.set_page_config(page_title="EcoRoute Agentic System", page_icon="🤖", layout="wide")
st.title("🤖 EcoRoute: SDG 12 Agentic Logistics System")
st.caption("AI Driven Optimization")
st.markdown("---")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Provide an optimization requirement (e.g., *'Route 100kg of surplus food from Mumbai markets to local centers'*), and I will coordinate my backend system to optimize it."}
    ]

# Production Secret/Key Configuration
# Strict cloud configuration for production deployment
api_key = st.secrets["GEMINI_API_KEY"]

with st.sidebar:
    st.header("⚙️ System Control Panel")
    st.success("✅ System Credentials Loaded Securely from Cloud.")
    
    st.markdown("---")
    st.info("**Goal:** UN SDG 12 (Responsible Consumption & Production)\n\n**Framework:** Streamlit UI + Google GenAI Python API")

# Render historical messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#  CHAT ENGINE & AGENT SIMULATION

if user_prompt := st.chat_input("Enter logistics detail or transit query..."):
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("assistant"):
        with st.spinner("EcoRoute system analyzing parameters and generating green transit alternatives..."):
            try:
                client = genai.Client(api_key=api_key)
                
                system_instruction = (
                    "You act as a multi-agent orchestration system named EcoRoute. "
                    "First, assume the persona of a 'Supply Chain Waste Analyzer' to evaluate the input cargo for material waste and deterioration vectors under UN SDG 12. "
                    "Second, pass that analysis to a 'Green Logistics Route Optimizer' persona to map out an eco-friendly routing blueprint, highlighting fuel alternatives and carbon reduction scoring. "
                    "Present your final answer cleanly separated into these two stages using markdown headers."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3
                    )
                )
                
                final_output = response.text
                st.markdown(final_output)
                st.session_state.messages.append({"role": "assistant", "content": final_output})

            except Exception as sys_error:
                st.error(f"Execution Error: {str(sys_error)}")