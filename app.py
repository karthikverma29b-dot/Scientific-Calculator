import math
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx() is None:
    print('Run this app with: streamlit run "your_file_name.py"')
    raise SystemExit(0)

# --- CONFIG ---
st.set_page_config(page_title="Pro Calculator", page_icon="🧮", layout="wide")

# --- CUSTOM CSS (The "Beauty" Logic) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Main Calculator Container */
    .calc-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }

    /* Display Area */
    .display-screen {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        text-align: right;
    }

    .expression-text {
        font-family: 'JetBrains Mono', monospace;
        color: #94a3b8;
        font-size: 1.1rem;
        min-height: 1.5rem;
    }

    .result-text {
        font-family: 'JetBrains Mono', monospace;
        color: #38bdf8;
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    /* Button Styling Overrides */
    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        height: 3.5rem !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: #38bdf8 !important;
        transform: translateY(-2px);
    }

    /* Special Button Colors */
    /* We use data-testid or just logical grouping in the loop below */
    </style>
    """, unsafe_allow_html=True)

# --- CALCULATOR LOGIC ---
if "expression" not in st.session_state: st.session_state.expression = ""
if "result" not in st.session_state: st.session_state.result = "0"
if "last_answer" not in st.session_state: st.session_state.last_answer = 0
if "history" not in st.session_state: st.session_state.history = []
if "angle_mode" not in st.session_state: st.session_state.angle_mode = "Degrees"

def safe_functions():
    use_degrees = st.session_state.angle_mode == "Degrees"
    return {
        "sin": lambda x: math.sin(math.radians(x)) if use_degrees else math.sin(x),
        "cos": lambda x: math.cos(math.radians(x)) if use_degrees else math.cos(x),
        "tan": lambda x: math.tan(math.radians(x)) if use_degrees else math.tan(x),
        "log": math.log10,
        "sqrt": math.sqrt,
        "pi": math.pi,
        "e": math.e,
        "Ans": st.session_state.last_answer,
    }

def handle_input(value):
    if value == "AC":
        st.session_state.expression = ""
        st.session_state.result = "0"
    elif value == "DEL":
        st.session_state.expression = st.session_state.expression[:-1]
    elif value == "=":
        try:
            # Simple sanitization
            expr = st.session_state.expression.replace('×', '*').replace('÷', '/')
            result = eval(expr, {"__builtins__": {}}, safe_functions())
            st.session_state.history.insert(0, f"{st.session_state.expression} = {result}")
            st.session_state.result = str(round(result, 4))
            st.session_state.last_answer = result
            st.session_state.expression = str(result)
        except Exception:
            st.error("Invalid Syntax")
    else:
        st.session_state.expression += str(value)

# --- UI LAYOUT ---
st.title("✨ Scientific Calculator")
st.write("Scientific computing with a modern touch.")

main_col, side_col = st.columns([2, 1], gap="large")

with main_col:
    st.markdown('<div class="calc-container">', unsafe_allow_html=True)
    
    # Display
    st.markdown(f"""
        <div class="display-screen">
            <div class="expression-text">{st.session_state.expression if st.session_state.expression else "0"}</div>
            <div class="result-text">{st.session_state.result}</div>
        </div>
    """, unsafe_allow_html=True)

    # Angle Mode & Controls
    m1, m2 = st.columns([1, 1])
    with m1:
        st.radio("Mode", ["Degrees", "Radians"], horizontal=True, key="angle_mode", label_visibility="collapsed")
    
    # Grid
    BUTTONS = [
        ["AC", "DEL", "(", ")", "/"],
        ["sin(", "cos(", "tan(", "log(", "sqrt("],
        ["7", "8", "9", "*", "**"],
        ["4", "5", "6", "-", "%"],
        ["1", "2", "3", "+", "pi"],
        ["0", ".", "e", "Ans", "="],
    ]

    for row in BUTTONS:
        cols = st.columns(len(row))
        for i, label in enumerate(row):
            # Applying different logic based on button type
            button_type = "secondary"
            if label in ["AC", "DEL"]: color = "rgba(239, 68, 68, 0.2)"
            elif label == "=": color = "rgba(56, 189, 248, 0.3)"
            elif label.isalpha() or "(" in label: color = "rgba(139, 92, 246, 0.1)"
            else: color = "rgba(255, 255, 255, 0.05)"

            if cols[i].button(label, key=f"btn_{label}_{row.index(label)}", use_container_width=True):
                handle_input(label)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

with side_col:
    st.markdown("### 🕒 History")
    if st.session_state.history:
        for entry in st.session_state.history[:8]:
            st.info(entry)
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No recent calculations")