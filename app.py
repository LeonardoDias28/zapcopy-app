import streamlit as st
from urllib.parse import quote
import unicodedata
import re

# ==============================================================================
# ⚙️ CONFIGURAÇÃO DA PÁGINA (GLOBAL)
# ==============================================================================
st.set_page_config(page_title="ZapCopy Pro", page_icon="💸", layout="centered")

# --- CORES NEON (GLOBAL) ---
ACCENT_COLOR = "#00FFC0"  # Verde Neon
BG_COLOR = "#101018"      # Fundo Ultra Dark
TEXT_COLOR = "#EAEAEA"

# ==============================================================================
# 🔐 LÓGICA DE LOGIN (SESSÃO)
# ==============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Credenciais Simples
CREDENCIAIS = {
    "admin": "123",
    "cliente": "1234"
}

def verificar_login():
    # Pega os valores e remove espaços em branco extras (.strip())
    user = st.session_state.get("input_user", "").strip()
    pwd = st.session_state.get("input_pwd", "").strip()
    
    if user in CREDENCIAIS and CREDENCIAIS[user] == pwd:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error(f"Login falhou. Tente Usuário: 'admin' e Senha: '123'")

def fazer_logout():
    st.session_state.logged_in = False
    st.rerun()

# ==============================================================================
# 🖥️ TELA DE LOGIN (DESIGN ISOLADO)
# ==============================================================================

def tela_login():
    # CSS Apenas para o Login
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {BG_COLOR}; color: {TEXT_COLOR}; }}
        .stTextInput input {{
            background-color: #252530; color: white; border: 1px solid #333; border-radius: 8px;
        }}
        .stButton > button {{
            background-color: {ACCENT_COLOR}; color: #101018; font-weight: 800;
            border-radius: 8px; border: none; width: 100%; text-transform: uppercase;
        }}
        .login-card {{
            background-color: #18181C; padding: 40px; border-radius: 15px;
            border: 1px solid #333; box-shadow: 0 0 20px rgba(0,0,0,0.5);
            text-align: center; margin-top: 50px;
        }}
        [data-testid="stSidebar"] {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
            <div class="login-card">
                <h1 style="margin:0; font-family:'Montserrat',sans-serif; font-size: 2.5em;">ZapCopy <span style="color:{ACCENT_COLOR}; text-shadow: 0 0 10px {ACCENT_COLOR};">Pro</span></h1>
                <p style="color:#888; margin-bottom: 20px;">Área Exclusiva</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Campos de entrada
        st.text_input("Usuário", key="input_user", placeholder="Digite: admin")
        st.text_input("Senha", key="input_pwd", type="password", placeholder="Digite: 123")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ENTRAR", on_click=verificar_login)
        
        # Dica visual para garantir que você consiga logar
        st.markdown(f"""
            <div style="margin-top: 20px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; font-size: 0.8em; color: #aaa;">
                🔑 <b>Acesso Admin:</b><br>User: <code>admin</code> | Senha: <code>123</code>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 🚀 APLICATIVO ZAPCOPY PRO (CÓDIGO ORIGINAL INTACTO)
# ==============================================================================

def main_app():
    # --- 1. CSS ORIGINAL (Restaurado) ---
    st.markdown(f"""
    <style>
        html, body, .stApp {{ background-color: {BG_COLOR} !important; color: {TEXT_COLOR}; font-family: 'Montserrat', sans-serif; }}
        .block-container {{ padding-top: 1.5rem !important; }}
        .stApp > header {{ background-color: {BG_COLOR} !important; box-shadow: none !important; }}
        .stApp > header > div {{ background-color: {BG_COLOR} !important; }}
        h1 {{ font-family: 'Montserrat', sans-serif; font-size: 3.5em; font-weight: 800; color: {ACCENT_COLOR}; letter-spacing: 0.12em; text-align: center; text-shadow: 0 0 10px {ACCENT_COLOR}, 0 0 20px rgba(0, 255, 192, 0.5); }}
        .neon-sidebar-header {{ font-size: 1.5em; font-weight: 800; color: {ACCENT_COLOR} !important; letter-spacing: 0.1em; text-shadow: 0 0 8px {ACCENT_COLOR}, 0 0 15px rgba(0, 255, 192, 0.5) !important; margin-top: 15px; margin-bottom: 5px; font-family: 'Montserrat', sans-serif; }}
        .stSidebar {{ background-color: #1A1A24; border-right: none; box-shadow: 2px 0 5px rgba(0, 0, 0, 0.4); }}
        .stTextInput > div > div > input, .stSelectbox > div > div {{ background-color: #252530; color: {TEXT_COLOR}; border: 1px solid #444; border-radius: 8px; box-shadow: inset 0 0 5px rgba(0,0,0,0.3); }}
        .stTextInput > div > div > input:focus {{ border-color: {ACCENT_COLOR}; box-shadow: 0 0 5px {ACCENT_COLOR}, inset 0 0 5px rgba(0,0,0,0.5); }}
        .stTabs [aria-selected="true"] {{ color: {ACCENT_COLOR}; border-color: {ACCENT_COLOR}; background-color: {BG_COLOR}; box-shadow: 0 -2px 8px rgba(0, 255, 192, 0.3); font-weight: 700 !important; }}
        .stButton > button {{ background-color: #FF4B4B; color: #FFFFFF !important; border-radius: 8px; font-weight: 600; box-shadow: 0 0 10px #FF4B4B; transition: all 0.3s ease; }}
        .stButton:nth-child(3) > button {{ background-color: {ACCENT_COLOR} !important; color: {BG_COLOR} !important; box-shadow: 0 0 10px {ACCENT_COLOR} !important; }}
        [data-testid^="stLinkButton"]:first-child a {{ background-color: #1A1A24 !important; color: {ACCENT_COLOR} !important; border: 1px solid {ACCENT_COLOR} !important; border-radius: 8px !important; box-shadow: 0 0 10px rgba(0, 255, 192, 0.5) !important; font-weight: 600; text-decoration: none !important; }}
        [data-testid^="stLinkButton"]:first-child a:hover {{ background-color: #252530 !important; box-shadow: 0 0 20px {ACCENT_COLOR} !important; transform: translateY(-2px); }}
        [data-testid^="stLinkButton"]:first-child a svg {{ fill: {ACCENT_COLOR} !important; }}
        .premium-subtitle-text {{ font-family: 'Montserrat', sans-serif; font-size: 1.3em; font-weight: 600; color: {TEXT_COLOR}; letter-spacing: 0.08em; text-align: center; margin-top: 0px !important; margin-bottom: 25px !important; text-shadow: 0 0 3px rgba(255,255,255,0.1); }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>ZapCopy Pro</h1>
            <p class="premium-subtitle-text">Sistema de Cobrança Otimizado para WhatsApp</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()

    with st.sidebar:
        if st.button("🔒 Sair", key="logout_btn", help="Encerrar sessão"):
            fazer_logout()   
        st.markdown('<h3 class="neon-sidebar-header">Configurar Pix</h3>', unsafe_allow_html=True)
        st.caption("Dados obrigatórios para o código funcionar.")
        meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email", value="") 
        meu_nome = st.text_input("Seu Nome Completo", value="", placeholder="Ex: Leonardo Dias") 
        minha_cidade = st.text_input("Sua Cidade", placeholder="Ex: São Paulo", value="") 
        st.divider()
        st.markdown('<h3 class="neon-sidebar-header">Personalização</h3>', unsafe_allow_html=True)
        tom_voz = st.selectbox("Tom de Voz da Mensagem:", ["Amigável 😊", "Profissional 👔", "Persuasivo 🔥"])

    with st.container(border=True):
        st.subheader("👤 Quem é o Cliente?")
        col_cli1, col_cli2 = st.columns(2)
        with col_cli1:
            nome_cliente = st.text_input("Nome do Cliente", value="", placeholder="Ex: João Silva") 
        with col_cli2:
            celular_cliente = st.text_input("WhatsApp (Opcional)", placeholder="11999999999", value="")
        st.markdown("<br>", unsafe_allow_html=True) 
        st.divider()

        st.subheader("💬 Gerador de Mensagens")
        tab1, tab2, tab3, tab4 = st.tabs(["💸 Cobrar", "🛒 Vender", "📅 Agendar", "⭐ Feedback"])
        script_final = ""
        pix_gerado = ""
        
        def limpar_texto(texto): return re.sub(r'[^A-Z0-9 ]', '', "".join([c for c in unicodedata.normalize('NFKD', texto if texto else "") if not unicodedata.combining(c)]).upper()).strip()
        def formatar_valor(valor):
            try: return "{:.2f}".format(float(valor.replace("R$", "").replace(",", ".").strip()))
            except: return "0.00"
        def crc16_ccitt(payload):
            crc = 0xFFFF; polynomial = 0x1021
            for byte in payload.encode('utf-8'):
                crc ^= (byte << 8)
                for _ in range(8):
                    if (crc & 0x8000): crc = (crc << 1) ^ polynomial
                    else: crc = (crc << 1)
                crc &= 0xFFFF
            return "{:04X}".format(crc)
        def gerar_pix_payload(chave, nome, cidade, valor, txid="***"):
            c_l = chave.strip(); n_l = limpar_texto(nome)[:25]; cid_l = limpar_texto(cidade)[:15]; v_l = formatar_valor(valor)
            p_k = f"0014BR.GOV.BCB.PIX01{len(c_l):02}{c_l}"
            pay = f"00020126{len(p_k):02}{p_k}52040000530398654{len(v_l):02}{v_l}5802BR59{len(n_l):02}{n_l}60{len(cid_l):02}{cid_l}62070503{txid}6304"
            return f"{pay}{crc16_ccitt(pay)}"

        with tab1:
            cenario = st.selectbox("Cenário:", ["Enviar Pix (Padrão)", "Lembrete", "Atraso"])
            val = st.text_input("Valor (R$)", placeholder="150,00", value="")
            if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
                if cenario == "Enviar Pix (Padrão)": intro = f"Prezado(a) {nome_cliente}, segue dados para pagamento de R$ {val}." if tom_voz == "Profissional 👔" else f"Oi {nome_cliente}, tudo bem? Segue o Pix referente ao valor de R$ {val}."
                elif cenario == "Lembrete": intro = f"Olá {nome_cliente}. Lembramos que o vencimento da fatura de R$ {val} é hoje." if tom_voz == "Profissional 👔" else f"Opa {nome_cliente}! Passando pra lembrar que seu boleto de R$ {val} vence hoje, ok?"
                else: intro = f"{nome_cliente}, precisamos regularizar pendência de R$ {val}." if tom_voz == "Profissional 👔" else f"Oi {nome_cliente}, não vi o pagamento de R$ {val}. Conseguimos resolver?"
                if meu_pix and meu_nome:
                    pix_gerado = gerar_pix_payload(meu_pix, meu_nome, minha_cidade, val if val else "0.00")
                    script_final = intro + "\n\n👇 Segue o código 'Copia e Cola' na mensagem abaixo:"
                else: st.error("⚠️ Preencha os dados do Pix na barra lateral!")
        with tab2:
            cenario_v = st.selectbox("Objetivo:", ["Oferta Especial", "Recuperar Cliente", "Upsell"])
            prod = st.text_input("Produto", value="")
            if st.button("✨ Gerar Venda", type="primary", use_container_width=True):
                if cenario_v == "Oferta Especial": script_final = f"😱 {nome_cliente}, oportunidade única no {prod}!" if tom_voz == "Persuasivo 🔥" else f"Oi {nome_cliente}! Condição especial no {prod} pra você."
                elif cenario_v == "Recuperar Cliente": script_final = f"Ei {nome_cliente}, sumiu! Chegou novidade de {prod}."
                else: script_final = f"{nome_cliente}, quem leva {prod} costuma levar esse complemento."
        with tab3:
            d_ag = st.date_input("Dia", value=None); h_ag = st.time_input("Hora", value=None)
            if st.button("✨ Confirmar Agenda", type="primary", use_container_width=True):
                d_s = f" dia {d_ag.strftime('%d/%m')}" if d_ag else ""; h_s = str(h_ag)[0:5] if h_ag else "horário combinado"
                script_final = f"Olá {nome_cliente}. Confirmamos agendamento{d_s} às {h_s}." if tom_voz == "Profissional 👔" else f"Confirmadíssimo, {nome_cliente}! Te espero{d_s} às {h_s}. 👊"
        with tab4:
            if st.button("✨ Pedir Feedback", type="primary", use_container_width=True):
                script_final = f"Oi {nome_cliente}! De 0 a 10, quanto recomendaria nosso serviço? ⭐"

        if script_final:
            st.divider(); st.success("✅ Mensagem Pronta!")
            with st.expander("👀 Ver texto"): st.write(script_final)
            
            s_clean = script_final.replace('\n', '%0A'); m_enc = quote(s_clean)
            p_clean = pix_gerado.replace('\n', '%0A'); p_enc = quote(p_clean)
            
            if celular_cliente:
                nums = "".join(filter(str.isdigit, celular_cliente.strip())); nums = "55" + nums if not nums.startswith("55") else nums
                base = f"https://api.whatsapp.com/send?phone={nums}"; l_txt = f"{base}&text={m_enc}"; l_pix = f"{base}&text={p_enc}"; l_lbl = f"Enviar para {nome_cliente}"
            else:
                base = "https://api.whatsapp.com/send"; l_txt = f"{base}?text={m_enc}"; l_pix = f"{base}?text={p_enc}"; l_lbl = "Abrir WhatsApp"
            
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown("**Passo 1: Conversa**"); st.link_button(f"💬 {l_lbl}", l_txt, type="secondary", use_container_width=True)
            with c2: st.markdown("**Passo 2: Pagamento**"); st.link_button("💲 Enviar Pix (Copia e Cola)", l_pix, type="primary", use_container_width=True) if pix_gerado else st.info("Sem Pix")
            with c3: st.markdown("**Ações**"); st.button("🗑️ Limpar Formulário", type="secondary", use_container_width=True, on_click=st.rerun)

            if pix_gerado:
                st.markdown("---")
                with st.expander("📱 Testar ou Copiar Código PIX"):
                    st.text_area("Código PIX:", pix_gerado, height=3)
                    qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_gerado)}"
                    cq, ct = st.columns([1,3]); 
                    with cq: st.image(qr, width=120)
                    with ct: st.caption("Escaneie para testar.")

# ==============================================================================
# 🚦 CONTROLE DE ACESSO
# ==============================================================================
if st.session_state.logged_in:
    main_app()
else:
    tela_login()
