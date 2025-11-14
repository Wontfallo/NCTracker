"""
Authentication Components for NCTracker
Login forms and auth-related UI
"""

from base64 import b64encode
from pathlib import Path

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

from database import db


def show_login_form():
    """Display the streamlined login layout."""
    background_layers = (
        "linear-gradient(130deg, rgba(14, 20, 37, 0.95) 0%, "
        "rgba(10, 16, 30, 0.92) 60%, rgba(9, 14, 26, 0.94) 100%)"
    )
    background_extras = "background-size: cover; background-position: center;"

    background_path = Path("assets/login_background.png")
    if background_path.exists():
        try:
            encoded = b64encode(background_path.read_bytes()).decode()
            background_layers = f"url('data:image/png;base64,{encoded}')"
            background_extras = (
                "background-size: contain;"
                "background-repeat: no-repeat;"
                "background-position: center center;"
            )
        except Exception:  # pragma: no cover - guard missing file edge cases
            pass

    st.markdown("""
    <style>
        .stApp {
            background: none !important;
            overflow: hidden !important;
        }
        [data-testid="stAppViewContainer"] {
            background: none !important;
            padding: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create full screen container
    with stylable_container(
        key="login_shell",
        css_styles=f"""
            {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                margin: 0;
                padding: 0;
                border-radius: 0;
                border: none;
                box-shadow: none;
                background: {background_layers};
                {background_extras}
                background-color: rgba(6, 12, 24, 0.85);
                backdrop-filter: blur(6px);
                display: flex;
                justify-content: center;
                align-items: center;
            }}
        """,
    ):
        # Center the content area
        with stylable_container(
            key="login_content",
            css_styles="""
                {
                    width: min(70vw, 800px);
                    height: auto;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    padding: 2rem;
                    margin-left: 8vw; /* Move content 38% from left edge */
                }
            """,
        ):
            with stylable_container(
                key="login_hero",
                css_styles="""
                    {
                        max-width: 400px;
                        margin: 0 auto 1.6rem;
                        padding: 1.35rem 1.25rem;
                        border-radius: 14px;
                        background: rgba(10, 18, 34, 0.1);
                        border: 1px solid rgba(148, 163, 184, 0.1);
                        text-align: center;
                        width: 100%;
                    }
                    h1 {
                        color: #f8fafc;
                        font-size: 1.82rem;
                        letter-spacing: 0.06em;
                        margin-bottom: 0.35rem;
                        font-weight: 700;
                    }
                    p {
                        color: rgba(226, 232, 240, 0.82);
                        font-size: 0.82rem;
                        letter-spacing: 0.08em;
                        text-transform: uppercase;
                    }
                """,
            ):
                st.markdown("<h1>NCTracker</h1>", unsafe_allow_html=True)
                st.markdown(
                    "<p>Quality Non-Conformance Report System</p>",
                    unsafe_allow_html=True,
                )

            with stylable_container(
                key="login_card",
                css_styles="""
                    {
                        max-width: 400px;
                        margin: 0 auto;
                        padding: 1.8rem 1.6rem 1.45rem;
                        border-radius: 16px;
                        background: rgba(8, 15, 30, 0.1);
                        border: 1px solid rgba(59, 130, 246, 0.1);
                        box-shadow: none;
                        width: 100%;
                    }
                    h2 {
                        margin: 0;
                        text-align: center;
                        color: var(--color-text);
                        font-size: 1.55rem;
                        font-weight: 700;
                    }
                    p.subtitle {
                        text-align: center;
                        color: var(--color-text-muted);
                        font-size: 0.88rem;
                        margin: 0.3rem 0 1.25rem;
                        letter-spacing: 0.02em;
                    }
                    div[data-testid="stTextInput"] label {
                        font-size: 0.75rem;
                        letter-spacing: 0.12em;
                        text-transform: uppercase;
                        color: rgba(226, 232, 240, 0.78);
                        font-weight: 600;
                    }
                    div[data-testid="stTextInput"] input {
                        background: #0f172a !important;
                        border-radius: 10px !important;
                        border: 1px solid rgba(148, 163, 184, 0.45) !important;
                        color: var(--color-text) !important;
                        height: 44px;
                        font-size: 0.95rem !important;
                    }
                    div[data-testid="stTextInput"] input:focus {
                        border-color: rgba(129, 140, 248, 0.75) !important;
                        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
                    }
                    button[kind="primary"] {
                        width: 100%;
                        border-radius: 10px !important;
                        padding: 0.75rem !important;
                        font-weight: 600 !important;
                        font-size: 0.95rem !important;
                        background: linear-gradient(135deg, #565ad8 0%, #4f46e5 100%) !important;
                        border: none !important;
                        box-shadow: 0 16px 28px rgba(72, 76, 200, 0.32) !important;
                    }
                    button[kind="primary"]:hover {
                        filter: brightness(1.05) !important;
                    }
                """,
            ):
                st.markdown(
                    '<h2>Sign in</h2><p class="subtitle">Access your NCR dashboard</p>',
                    unsafe_allow_html=True,
                )

                with st.form("login_form", clear_on_submit=False):
                    username = st.text_input(
                        "Username",
                        placeholder="Enter your username",
                        key="login_username",
                        help="Use your assigned username",
                    )

                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter your password",
                        key="login_password",
                        autocomplete="current-password",
                        help="Enter your secure password",
                    )

                    submitted = st.form_submit_button("Sign In", type="primary")

                    if submitted:
                        if username and password:
                            user = db.authenticate_user(username, password)
                            if user:
                                st.session_state.user = user
                                st.success(f"✅ Welcome back, {user['full_name']}!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password. Please try again.")
                        else:
                            st.warning("⚠️ Please enter both username and password")

            with stylable_container(
                key="login_credentials",
                css_styles="""
                    {
                        max-width: 400px;
                        margin: 1.45rem auto 0;
                        padding: 1.35rem 1.4rem;
                        border-radius: 14px;
                        background: rgba(8, 15, 30, 0.1);
                        border: 1px solid rgba(59, 130, 246, 0.1);
                        box-shadow: none;
                        width: 100%;
                    }
                    h3 {
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        color: #facc15;
                        font-size: 0.98rem;
                        margin: 0 0 0.85rem;
                        font-weight: 700;
                    }
                    p {
                        margin: 0.3rem 0;
                        color: var(--color-text);
                    }
                    code {
                        background: rgba(15, 23, 42, 0.9);
                        border-radius: 6px;
                        padding: 3px 8px;
                        border: 1px solid rgba(148, 163, 184, 0.3);
                        color: #38bdf8;
                    }
                    small {
                        display: block;
                        margin-top: 0.8rem;
                        color: var(--color-text-muted);
                        font-style: italic;
                    }
                """,
            ):
                st.markdown("<h3>🔑 Default Admin Account</h3>", unsafe_allow_html=True)
                st.markdown(
                    "<p><strong>Username:</strong> <code>admin</code></p>"
                    "<p><strong>Password:</strong> <code>admin123</code></p>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<small>🔒 Please change the password after first login for security.</small>",
                    unsafe_allow_html=True,
                )


def logout():
    """Handle user logout"""
    if 'user' in st.session_state:
        del st.session_state.user
    if 'ncr_form_data' in st.session_state:
        del st.session_state.ncr_form_data
    if 'current_ncr' in st.session_state:
        del st.session_state.current_ncr
    st.success("✅ You have been logged out successfully")
    st.rerun()
