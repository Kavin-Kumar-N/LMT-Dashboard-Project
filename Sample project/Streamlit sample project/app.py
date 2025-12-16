import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Login", page_icon="🔐", layout="wide")

# LOGIN STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/1_Home.py")

# CREATE 2 COLUMNS
left, right = st.columns([3, 1])

# =====================================
# LEFT SIDE - HTML ANIMATION (COMPONENT)
# =====================================
with left:
    animation_html = """
    <html>
    <head>
    <style>
    body { background: transparent; }
    .container {
    display: flex;
    height: 100vh;
    align-items: center;
	}

    .stickman {
        position: relative;
        width: 120px;
        height: 220px;
    }
    .head {
        width: 80px;
        height: 80px;
        background: #ffffff;
        border-radius: 50%;
        position: relative;
        margin: 0 auto;
        border: 3px solid black;
    }
    .eye {
        width: 40px;
        height: 40px;
        background: white;
        border: 2px solid black;
        border-radius: 50%;
        position: absolute;
        top: 20px;
        left: 20px;
        overflow: hidden;
    }
    .pupil {
        width: 18px;
        height: 18px;
        background: black;
        border-radius: 50%;
        position: absolute;
        top: 11px;
        left: 11px;
        transition: transform 0.05s linear;
    }
    .body {
        width: 6px;
        height: 60px;
        background: black;
        margin: 10px auto;
    }
    .arms {
        width: 80px;
        height: 6px;
        background: black;
        margin: 10px auto;
    }
    .legs {
        width: 60px;
        height: 60px;
        position: relative;
        margin: 0 auto;
    }
    .legs::before,
    .legs::after {
        content: '';
        position: absolute;
        width: 6px;
        height: 60px;
        background: black;
    }
    .legs::before { left: 0; transform: rotate(20deg); }
    .legs::after { right: 0; transform: rotate(-20deg); }
    </style>
    </head>

    <body>
    <div class="container">
        <div class="stickman">
            <div class="head"><div class="eye"><div class="pupil"></div></div></div>
            <div class="body"></div><div class="arms"></div><div class="legs"></div>
        </div>
    </div>

    <script>
    window.addEventListener("mousemove", function(e) {

        const pupils = document.querySelectorAll(".pupil");

        pupils.forEach(pupil => {
            const rect = pupil.getBoundingClientRect();

            const pupilX = rect.left + rect.width / 2;
            const pupilY = rect.top + rect.height / 2;

            const mouseX = e.clientX;
            const mouseY = e.clientY;

            const angle = Math.atan2(mouseY - pupilY, mouseX - pupilX);

            const distance = 10;

            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;

            pupil.style.transform = `translate(${x}px, ${y}px)`;
        });

    });
    </script>

    </body>
    </html>
    """
    components.html(animation_html, height=420, scrolling=False)  # << This renders animation, no code shown!

# =====================================
# RIGHT SIDE - LOGIN FORM
# =====================================
with right:
    st.markdown("### Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "12345":
            st.session_state.logged_in = True
            st.success("Login Successful! Redirecting...")
            st.switch_page("pages/1_Home.py")
        else:
            st.error("Invalid username or password")