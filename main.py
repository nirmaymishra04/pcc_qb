import os
import json
import streamlit as st
import base64
from groq import Groq

# Streamlit page configuration (Must be first Streamlit command)
st.set_page_config(
    page_title="PCC",
    page_icon="🧑‍🎓",
    layout="wide"
)


#  Function to encode image to Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string


# Path to your local image
image_path = "background.jpeg"

try:
    # Convert image to Base64
    base64_image = get_base64_image(image_path)

    # Inject CSS with Base64 image
    background_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """

    # Apply the background CSS
    st.markdown(background_css, unsafe_allow_html=True)

    # Add text styling for bold and larger text
    text_style_css = """
    <style>
    .stMarkdown p, .stChat p, .stChatMessage div p {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-weight: bold;
        font-size: 120%;
    }
    .stChatInput textarea::placeholder {
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    """
    st.markdown(text_style_css, unsafe_allow_html=True)

except Exception as e:
    st.sidebar.error(f"Error loading background image: {e}")

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# Save the API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize chat sessions in session state
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"New Chat": []}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# Sidebar navigation
st.sidebar.title("💬 Chat Sessions")
selected_chat = st.sidebar.radio("Select a chat", list(st.session_state.chat_sessions.keys()))

# Button to start a new chat
if st.sidebar.button("➕ New Chat"):
    new_chat_name = f"Chat {len(st.session_state.chat_sessions)}"
    st.session_state.chat_sessions[new_chat_name] = []
    st.session_state.current_chat = new_chat_name
    st.rerun()

st.session_state.current_chat = selected_chat

# Streamlit page title
st.title("👨‍️  PCC QUESTION BANK GPT 2.0 ")
st.subheader(" made by -NM")
st.sidebar.success("If you don't build your dreams, someone will hire you to help build theirs")

# Display chat history for the selected session
chat_history = st.session_state.chat_sessions[st.session_state.current_chat]
for message in chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message:
user_prompt = st.chat_input("HOW CAN I HELP YOU  ...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    chat_history.append({"role": "user", "content": user_prompt})

    # Send user's message to the LLM and get a response
    messages = [
        {"role": "system",
         "content": "You are MADDY whose task is to help students to understand a topic and will tell what will be the probable question that can come into my university semester exam with probable marks and will also provide a cheatcode for remembering that topic  and will provide a diagramatic approach to understand in exam , here are the details for chapters -This course covers fundamental concepts in communication systems, divided into six modules "
                    "MODULE 1: ANALOG COMMUNICATION -Communication system components: transmitter, channel, receiver,Signal types: analog vs digital,Modulation fundamentals: need, benefits (signal strength, preventing interference, antenna size),Amplitude Modulation (AM): principles, modulation index, waveforms,AM transmitters and receivers: block diagrams, components, functions,Frequency Modulation (FM): principles, waveforms, advantages, FM transmitters and receivers: block diagrams, components, functions,Demodulation techniques for AM and FM"
                    "MODULE 2: DIGITAL COMMUNICATION- Digital communication system block diagram and components, Sampling theorem: Nyquist rate (fs ≥ 2fm), Pulse Code Modulation (PCM): process, waveforms, applications,  Digital modulation techniques: Amplitude Shift Keying (ASK): principles, waveforms, Frequency Shift Keying (FSK): principles, waveforms,Frequency Shift Keying (FSK): principles, waveforms, Phase Shift Keying (PSK): principles, waveforms,Advantages of digital over analog communication,Phase Shift Keying (PSK): principles, waveforms,Advantages of digital over analog communication,Disadvantages of digital communication: bandwidth requirements, complexity"
                    "MODULE 3: COMPUTER COMMUNICATION NETWORKS-  Computer network basics: components, nodes, protocols,Network components: message, sender, receiver, transmission media, protocol,Network topologies:Mesh topology, Star topology, Bus topology,Ring topology,Tree topology,Hybrid topology ,TCP/IP model:Network Access Layer,Internet/Network Layer,Transport Layer,Application Layer,OSI model seven layers: Physical Layer,Data Link Layer,Network Layer,Transport Layer,Session Layer,Presentation Layer,Application Layer,Data communication types:Simplex communication,Half-duplex communication,Full-duplex communication,Transmission media:Guided (wired) media: twisted pair, coaxial cable, optical fiber, stripline, microstripline,Unguided (wireless) media: radio waves, microwaves, infrared"
                    "MODULE 4: MOBILE COMMUNICATION- Wireless communication fundamentals,Mobile telephony: principles, components, operation,Mobile communication system elements:Mobile Station (MS): User Equipment, Transceiver, SIM Card,Mobile Switching Center (MSC): call routing, handoff management,Base Stations: functionality, components,Core Network: infrastructure connections,Channel types: control, forward, reverse,Cellular network principles: cell structure, frequency reuse,Mobile wireless generations:1G: analog systems, FM transmission,2G: digital signals, TDMA/CDMA,2.5G: GPRS, EDGE, CDMA2000,3G: WCDMA, CDMA2000, TD-SCDMA,4G: LTE, WiMAX,5G: millimeter wave, massive MIMO, beamforming, edge computing "
                    "MODULE 5: FIBER OPTICAL COMMUNICATION- Fiber optic communication principles,Total internal reflection,Optical fiber structure and components,Types of optical fibers,Advantages and disadvantages,Applications of fiber optic communication"
                    "MODULE 6: SATELLITE COMMUNICATION- Satellite communication fundamentals,Types of satellites,Applications of satellite communication systems,Frequency bands: C-band, Ku-band, Ka-band,Components of satellite communication systems"},
        *chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
