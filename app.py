import streamlit as st
from urllib.parse import quote
import unicodedata
import re
import time

# ==============================================================================
# ⚙️ CONFIGURAÇÃO INICIAL E ESTILO (LOGIN + APP)
# ==============================================================================

st.set_page_config(page_title="ZapCopy Pro", page_icon="🚀", layout="centered")

# --- CORES NEON ---
ACCENT_COLOR = "#00FFC0"  # Verde Neon
BG_COLOR = "#0E0E12"      # Fundo Ultra Dark
CARD_BG = "#18181C"       # Fundo dos Cards/Login
TEXT_COLOR = "#EAEAEA"

# --- CSS GLOBAL (Aplica tanto ao Login quanto ao App) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

    /* Reset Geral */
    html, body, .stApp {{
        background-color: {BG_COLOR} !important;
        font-family: 'Montserrat', sans-serif;
        color: {TEXT_COLOR};
    }}

    /* Estilo dos Inputs (Login e App) */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input {{
        background-color: #252530 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    .stTextInput input:focus {{
        border-color: {ACCENT_COLOR} !important;
        box-shadow: 0 0 8px rgba(0, 255, 192, 0.3) !important;
    }}

    /* Botões Primários (Neon Green) */
    .stButton > button {{
        background-color: {ACCENT_COLOR} !important;
        color: {BG_COLOR} !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 20px rgba(0, 255, 192, 0.6) !important;
        transform: scale(1.02);
    }}

    /* Estilo Específico do Container de Login */
    .login-box {{
        background-color: {CARD_BG};
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 50px;
        margin-bottom: 50px;
    }}

    /* Títulos Neon */
    .neon-text {{
        color: {ACCENT_COLOR};
        text-shadow: 0 0 10px {ACCENT_COLOR};
    }}
    
    /* Esconder elementos padrão do Streamlit na tela de login */
    [data-testid="stSidebar"] {{
        display: {'none' if 'logged_in' not in st.session_state or not st.session_state.logged_in else 'block'};
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🔐 SISTEMA DE AUTENTICAÇÃO (SESSÃO E LÓGICA)
# ==============================================================================

# 1. Inicializar Estado da Sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 2. Banco de Dados Simulado (Para o MVP)
# No futuro, isso virá da integração com Hotmart/Kiwify via API ou Webhook
CREDENCIAIS_VALIDAS = {
    "admin@zapcopy.com": "admin123", # Usuário Admin
    "cliente": "1234",               # Usuário Teste
}

def fazer_login():
    """Verifica as credenciais inseridas."""
    user = st.session_state.get("login_user", "")
    senha = st.session_state.get("login_pass", "")
    
    if user in CREDENCIAIS_VALIDAS and CREDENCIAIS_VALIDAS[user] == senha:
        st.session_state.logged_in = True
        st.success("Login realizado com sucesso!")
        time.sleep(0.5)
        st.rerun() # Recarrega a página para entrar no app
    else:
        st.error("❌ E-mail ou senha incorretos.")

def fazer_logout():
    """Encerra a sessão."""
    st.session_state.logged_in = False
    st.rerun()

# ==============================================================================
# 🖥️ TELA DE LOGIN (DESIGN DARK NEON)
# ==============================================================================

def tela_login():
    # Centralizando o formulário usando colunas
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div class="login-box">
                <h1 style="margin:0; font-size: 2.5em;">ZapCopy <span class="neon-text">Pro</span></h1>
                <p style="color:#888; margin-bottom: 30px; font-size: 0.9em;">Acesso Exclusivo para Membros</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulário
        st.text_input("E-mail de Acesso", placeholder="exemplo@email.com", key="login_user")
        st.text_input("Senha", type="password", placeholder="••••••", key="login_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botão de Login (Chama a função fazer_login)
        st.button("🔐 ENTRAR NO SISTEMA", on_click=fazer_login, use_container_width=True)
        
        # Footer do Login
        st.markdown("""
            <div style="text-align: center; margin-top: 20px; font-size: 0.8em; color: #666;">
                Esqueceu sua senha? Contate o suporte.<br>
                © 2025 ZapCopy Pro
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 🚀 APLICATIVO PRINCIPAL (SÓ CARREGA SE LOGADO)
# ==============================================================================

def main_app():
    # --- FUNÇÕES AUXILIARES DO APP ---
    def limpar_texto(texto):
        if not texto: return ""
        nfkd = unicodedata.normalize('NFKD', texto)
        sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return re.sub(r'[^A-Z0-9 ]', '', sem_acento.upper()).strip()

    def formatar_valor(valor):
        try:
            val_float = float(valor.replace("R$", "").replace(",", ".").strip())
            return "{:.2f}".format(val_float)
        except:
            return "0.00"

    def crc16_ccitt(payload):
        crc = 0xFFFF
        polynomial = 0x1021
        for byte in payload.encode('utf-8'):
            crc ^= (byte << 8)
            for _ in range(8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
            crc &= 0xFFFF
        return "{:04X}".format(crc)

    def gerar_pix_payload(chave, nome, cidade, valor, txid="***"):
        chave_limpa = chave.strip()
        nome_limpo = limpar_texto(nome)[:25]
        cidade_limpa = limpar_texto(cidade)[:15]
        valor_formatado = formatar_valor(valor)
        p_chave = f"0014BR.GOV.BCB.PIX01{len(chave_limpa):02}{chave_limpa}"
        payload = (
            f"00020126{len(p_chave):02}{p_chave}52040000530398654{len(valor_formatado):02}{valor_formatado}"
            f"5802BR59{len(nome_limpo):02}{nome_limpo}60{len(cidade_limpa):02}{cidade_limpa}"
            f"62070503{txid}6304"
        )
        crc = crc16_ccitt(payload)
        return f"{payload}{crc}"

    # --- CSS ESPECÍFICO PARA O APP INTERNO ---
    st.markdown(f"""
    <style>
        .neon-sidebar-header {{ 
            font-size: 1.5em; font-weight: 800; color: {ACCENT_COLOR} !important;
            letter-spacing: 0.1em; text-shadow: 0 0 8px {ACCENT_COLOR}, 0 0 15px rgba(0, 255, 192, 0.5) !important;
            margin-top: 15px; margin-bottom: 5px; font-family: 'Montserrat', sans-serif;
        }}
        /* Restaurando botão branco/neon para links */
        [data-testid^="stLinkButton"]:first-child a {{
            background-color: #1A1A24 !important; color: {ACCENT_COLOR} !important;
            border: 1px solid {ACCENT_COLOR} !important; border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 255, 192, 0.5) !important; font-weight: 600; text-decoration: none !important; 
        }}
        [data-testid^="stLinkButton"]:first-child a:hover {{
            background-color: #252530 !important; box-shadow: 0 0 20px {ACCENT_COLOR} !important; transform: translateY(-2px);
        }}
        /* Botão de Limpar (Secundário) */
        .stButton:nth-child(3) > button {{
            background-color: {ACCENT_COLOR} !important; color: {BG_COLOR} !important; box-shadow: 0 0 10px {ACCENT_COLOR} !important; 
        }}
        /* Botão de Pix (Vermelho) */
        .stButton:nth-child(2) > button {{
             background-color: #FF4B4B !important; color: #FFFFFF !important; box-shadow: 0 0 10px #FF4B4B !important; 
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER DO APP ---
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="text-shadow: 0 0 10px {ACCENT_COLOR};">ZapCopy <span style="color:{ACCENT_COLOR}">Pro</span></h1>
            <p style="font-weight: 600; color: {TEXT_COLOR}; margin-top: -10px;">Sistema de Cobrança Otimizado para WhatsApp</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown(f"👤 Logado como: **{st.session_state.get('login_user', 'Usuário')}**")
        if st.button("🚪 SAIR (LOGOUT)", use_container_width=True):
            fazer_logout()
            
        st.divider()
        st.markdown('<h3 class="neon-sidebar-header">Configurar Pix</h3>', unsafe_allow_html=True)
        meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email") 
        meu_nome = st.text_input("Seu Nome Completo", placeholder="Ex: Leonardo Dias") 
        minha_cidade = st.text_input("Sua Cidade", placeholder="Ex: São Paulo") 
        st.divider()
        st.markdown('<h3 class="neon-sidebar-header">Personalização</h3>', unsafe_allow_html=True)
        tom_voz = st.selectbox("Tom de Voz da Mensagem:", ["Amigável 😊", "Profissional 👔", "Persuasivo 🔥"])

    # --- ÁREA PRINCIPAL (MANTENDO SUA ESTRUTURA ANTERIOR) ---
    with st.container(border=True):
        st.subheader("👤 Quem é o Cliente?")
        c1, c2 = st.columns(2)
        with c1: nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: João Silva") 
        with c2: celular_cliente = st.text_input("WhatsApp (Opcional)", placeholder="11999999999")

        st.markdown("<br>", unsafe_allow_html=True) 
        st.divider()

        st.subheader("💬 Gerador de Mensagens")
        tab1, tab2, tab3, tab4 = st.tabs(["💸 Cobrar", "🛒 Vender", "📅 Agendar", "⭐ Feedback"])

        script_final = ""
        pix_gerado = ""
        
        # Lógica da Aba 1 (Cobrança) - Exemplo Simplificado para manter foco no Login
        with tab1:
            cenario = st.selectbox("Cenário:", ["Enviar Pix (Padrão)", "Lembrete", "Atraso"])
            valor = st.text_input("Valor (R$)", placeholder="150,00")
            if st.button("✨ Gerar Cobrança", key="btn_cob", use_container_width=True):
                # Lógica de texto (Resumida)
                if tom_voz == "Profissional 👔": intro = f"Prezado(a) {nome_cliente}, segue dados para pagamento de R$ {valor}."
                else: intro = f"Oi {nome_cliente}! Segue o Pix de R$ {valor} conforme combinado."
                
                if meu_pix:
                    pix_gerado = gerar_pix_payload(meu_pix, meu_nome, minha_cidade, valor if valor else "0.00")
                    script_final = intro + "\n\n👇 Segue o código 'Copia e Cola' na mensagem abaixo:"
                else:
                    st.error("⚠️ Preencha o Pix na lateral!")

        # (As outras abas seguem a mesma lógica do seu código anterior, omitidas aqui para brevidade, mas funcionariam igual)

        # --- ZONA DE SAÍDA ---
        if script_final:
            st.divider()
            st.success("✅ Mensagem Pronta!")
            with st.expander("👀 Ver texto"): st.write(script_final)

            # Preparar Links
            msg_enc = quote(script_final.replace('\n', '%0A'))
            pix_enc = quote(pix_gerado.replace('\n', '%0A'))
            
            nums = "".join(filter(str.isdigit, celular_cliente)) if celular_cliente else ""
            base = f"https://api.whatsapp.com/send?phone=55{nums}" if nums else "https://api.whatsapp.com/send"
            
            link_msg = f"{base}&text={msg_enc}" if nums else f"{base}?text={msg_enc}"
            link_pix = f"{base}&text={pix_enc}" if nums else f"{base}?text={pix_enc}"

            # BOTÕES ALINHADOS E ESTILIZADOS
            b1, b2, b3 = st.columns(3)
            with b1:
                st.markdown("**Passo 1: Conversa**")
                st.link_button(f"💬 Enviar Conversa", link_msg, type="secondary", use_container_width=True)
            with b2:
                st.markdown("**Passo 2: Pagamento**")
                if pix_gerado: st.link_button("💲 Enviar Pix", link_pix, type="primary", use_container_width=True)
                else: st.info("Sem Pix")
            with b3:
                st.markdown("**Ações**")
                if st.button("🗑️ Limpar", type="secondary", use_container_width=True): st.rerun()
            
            if pix_gerado:
                st.markdown("---")
                st.text_area("Código Pix Copia e Cola:", pix_gerado)


# ==============================================================================
# 🚦 CONTROLE DE ACESSO (GATEKEEPER)
# ==============================================================================

if st.session_state.logged_in:
    main_app()
else:
    tela_login()
