"""Atempo login screen - fully separate from the rest of the app.

Letters on this page are always white. They ignore the theme chosen in the app's Settings menu."""
import streamlit as st

W = "[data-testid=stVerticalBlockBorderWrapper]"
BTN = "[data-testid=stBaseButton-primary]"
BTN2 = "[data-testid=stBaseButton-secondary]"

# Everything here is fixed: white letters on the navy login page, whatever theme
# (light / dark / custom colours) is chosen in the app's Settings menu.
CSS = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Fraunces:opsz,wght@9..144,500;9..144,700&display=swap');
:root,.stApp{{color-scheme:dark!important}}
.stApp,.stApp *{{font-family:'Manrope',sans-serif}}
.stApp,[data-testid=stAppViewContainer],[data-testid=stMain]{{background:radial-gradient(circle at 10% 15%,rgba(63,184,175,.30) 0,transparent 34%),radial-gradient(circle at 92% 88%,rgba(79,124,255,.24) 0,transparent 38%),linear-gradient(135deg,#0B1F3A 0%,#14386A 60%,#1B4F7A 100%)!important}}
.stApp::before{{content:'';position:fixed;left:-130px;top:-110px;width:380px;height:380px;border-radius:58% 42% 55% 45%;background:rgba(63,184,175,.16);pointer-events:none}}
.stApp::after{{content:'';position:fixed;right:-150px;bottom:-130px;width:430px;height:430px;border-radius:45% 55% 40% 60%;background:rgba(255,255,255,.06);pointer-events:none}}
.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h3 *{{font-family:'Fraunces',Georgia,serif!important;font-weight:600!important}}
[data-testid=stSidebar],[data-testid=stSidebarCollapsedControl],[data-testid=stHeader]{{display:none}}
.stApp *{{color:#FFFFFF!important}}
[data-testid=stCaptionContainer] *{{opacity:.8}}
{W}{{background:rgba(255,255,255,.07)!important;border:1px solid rgba(255,255,255,.22)!important;border-radius:36px 36px 36px 90px;padding:18px 24px;backdrop-filter:blur(10px);box-shadow:0 20px 50px rgba(0,0,0,.35)}}
[data-baseweb=input],[data-baseweb=base-input],input{{background:rgba(255,255,255,.12)!important;-webkit-text-fill-color:#FFFFFF!important;caret-color:#FFFFFF;border-radius:16px}}
[data-baseweb=input]{{border:1px solid rgba(255,255,255,.35)!important}}
[data-testid=stTextInput] svg{{fill:#FFFFFF!important;color:#FFFFFF!important}}
{BTN}{{background:#1F9D94!important;border:0!important;border-radius:999px;padding:.75rem}}
{BTN}:hover{{background:#25B5AB!important}}
{BTN2}{{background:transparent!important;border:2px solid #FFFFFF!important;border-radius:999px;padding:.75rem}}
{BTN2}:hover{{background:rgba(255,255,255,.14)!important}}
{BTN} *,{BTN2} *{{font-weight:800}}
[data-baseweb=select]>div{{background:rgba(255,255,255,.12)!important;border:1px solid rgba(255,255,255,.35)!important;border-radius:16px}}
[data-baseweb=popover],[data-baseweb=popover] ul,[data-baseweb=menu]{{background:#14386A!important}}
[data-baseweb=popover] *{{color:#FFFFFF!important}}
[data-baseweb=popover] li:hover{{background:#1F4B86!important}}
.login-foot{{text-align:center;font-size:.8rem}}
</style>"""


ROLES = {"caretaker": "health professional", "family": "family member"}


def _set(**kw): st.session_state.update(**kw)


def _enter(on_pick, role):
    st.session_state.update(auth=None, login_role=None); on_pick(role)


def _chooser(verb):
    st.markdown("**Are you a health professional or a family member?**")
    a, b = st.columns(2)
    a.button("I'm a health professional", type="primary", use_container_width=True, on_click=_set, kwargs=dict(login_role="caretaker"))
    a.caption("Monitor residents or policyholders, manage alerts and follow-ups.")
    b.button("I'm a family member", use_container_width=True, on_click=_set, kwargs=dict(login_role="family"))
    b.caption("Follow how your loved one is doing and stay in touch with the care team.")
    st.button("← Back", type="tertiary", on_click=_set, kwargs=dict(auth=None), key="b0")


def _signin(role, on_pick):
    pro = role == "caretaker"
    st.markdown("### Health professional sign in" if pro else "### Family sign in")
    st.caption("Use your professional license number and password." if pro else "Use the email and password you registered with.")
    if pro:
        st.text_input("License number", "NH-204518", key="lic"); st.text_input("Password", "demo-password", type="password", key="pw_pro")
    else:
        st.text_input("Email", "demo@atempo.care", key="em"); st.text_input("Password", "demo-password", type="password", key="pw_fam")
    st.button("Sign in", type="primary", use_container_width=True, on_click=_enter, args=(on_pick, role))
    st.button("← Back", type="tertiary", on_click=_set, kwargs=dict(login_role=None), key="b1")


def _signup(role):
    pro = role == "caretaker"
    st.markdown("### Create your professional account" if pro else "### Create your family account")
    st.caption("We only ask for what we need to confirm who you are and what you may access.")
    k = "su_p" if pro else "su_f"
    name = st.text_input("Full name", key=k + "n"); email = st.text_input("Work email" if pro else "Email", key=k + "e")
    if pro:
        c1, c2 = st.columns(2)
        c1.selectbox("Profession", ["Nurse", "Physician", "Care assistant", "Physiotherapist", "Case manager", "Other"], key=k + "pr")
        lic = c2.text_input("License number", key=k + "l")
        st.selectbox("Type of organisation", ["Nursing home", "Insurance company"], key=k + "ot"); org = st.text_input("Organisation name", key=k + "o")
        extra = all([lic, org])
    else:
        st.text_input("Mobile number (optional, for urgent updates)", key=k + "ph")
        st.selectbox("Your relationship to the person", ["Daughter", "Son", "Spouse or partner", "Grandchild", "Other relative", "Legal representative"], key=k + "rel")
        code = st.text_input("Invitation code from the care team", placeholder="e.g. ATP-4821", key=k + "c")
        extra = bool(code)
    pw = st.text_input("Password", type="password", key=k + "pw"); pw2 = st.text_input("Confirm password", type="password", key=k + "pw2")
    if pw and pw2 and pw != pw2: st.markdown("Passwords do not match.")
    c1 = st.checkbox("I accept the Terms of Use and the Privacy Policy", key=k + "t")
    c2 = st.checkbox("I confirm I am authorised to access the health data of the people my organisation monitors" if pro else
                     "I confirm the person I follow (or their legal representative) agreed to share this information with me", key=k + "a")
    ready = bool(name and email and pw and pw == pw2 and extra and c1 and c2)
    st.button("Create account", type="primary", use_container_width=True, disabled=not ready, on_click=_set, kwargs=dict(auth="done"))
    st.button("← Back", type="tertiary", on_click=_set, kwargs=dict(login_role=None), key="b2")


def login_page(logo_b64, on_pick):
    """Welcome -> (sign in | sign up) -> choose role -> role-specific form. Demo only: nothing is verified or stored."""
    st.markdown(CSS, unsafe_allow_html=True)
    auth, role = st.session_state.get("auth"), st.session_state.get("login_role")
    _, mid, _ = st.columns([1, 1.7, 1])
    with mid:
        st.markdown(f"<img src='data:image/png;base64,{logo_b64}' style='width:300px;max-width:80%;display:block;margin:1.5rem auto 1rem'>", unsafe_allow_html=True)
        with st.container(border=True):
            if auth is None:
                st.markdown("### Welcome to Atempo"); st.caption("Care beyond the visit.")
                a, b = st.columns(2)
                a.button("I already have an account", type="primary", use_container_width=True, on_click=_set, kwargs=dict(auth="signin", login_role=None))
                a.caption("Sign in to continue.")
                b.button("I'm new here", use_container_width=True, on_click=_set, kwargs=dict(auth="signup", login_role=None))
                b.caption("Create your account in a few minutes.")
            elif auth == "done":
                st.markdown("### Account created ✓")
                st.caption("Demo: in the real product a health professional's license would be checked, and a family member's invitation code confirmed by the care team, before access is enabled.")
                st.button("Continue to Atempo", type="primary", use_container_width=True, on_click=_enter, args=(on_pick, role or "caretaker"))
            elif role is None:
                st.markdown("### Sign in" if auth == "signin" else "### Create an account"); _chooser(auth)
            elif auth == "signin": _signin(role, on_pick)
            else: _signup(role)
        st.markdown("<p class='login-foot'>Demo prototype · fictional data · nothing is verified or stored</p>", unsafe_allow_html=True)
