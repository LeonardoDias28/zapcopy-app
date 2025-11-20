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

# Credenciais (Pode alterar aqui depois ou conectar com banco)
CREDENCIAIS = {
    "admin": "123",
    "cliente": "1234"
}

def verificar_login():
    user = st.session_state.get("input_user", "")
    pwd = st.session_state.get("input_pwd", "")
    
    if user in CREDENCIAIS and CREDENCIAIS[user] == pwd:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos.")

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
        /* Esconde a sidebar na tela de login para ficar limpo */
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
        
        st.text_input("Usuário", key="input_user", placeholder="admin")
        st.text_input("Senha", key="input_pwd", type="password", placeholder="123")
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ENTRAR", on_click=verificar_login)

# ==============================================================================
# 🚀 APLICATIVO ZAPCOPY PRO (CÓDIGO ORIGINAL V12.15 INTACTO)
# ==============================================================================

def main_app():
    # --- 1. CSS ORIGINAL (Restaurado) ---
    st.markdown(f"""
    <style>
        /* CONFIGURAÇÃO DE TEMA BASE */
        html, body, .stApp {{ 
            background-color: {BG_COLOR} !important; 
            color: {TEXT_COLOR}; 
            font-family: 'Montserrat', sans-serif; 
        }}
        .block-container {{ padding-top: 1.5rem !important; }}

        /* HEADER E CHEVRON */
        .stApp > header {{ background-color: {BG_COLOR} !important; box-shadow: none !important; }}
        .stApp > header > div {{ background-color: {BG_COLOR} !important; }}
        
        /* TÍTULO PRINCIPAL */
        h1 {{
            font-family: 'Montserrat', sans-serif; font-size: 3.5em; font-weight: 800; 
            color: {ACCENT_COLOR}; letter-spacing: 0.12em; text-align: center;
            text-shadow: 0 0 10px {ACCENT_COLOR}, 0 0 20px rgba(0, 255, 192, 0.5); 
        }}

        /* TÍTULOS LATERAIS (NEON) */
        .neon-sidebar-header {{ 
            font-size: 1.5em; font-weight: 800; color: {ACCENT_COLOR} !important;
            letter-spacing: 0.1em; text-shadow: 0 0 8px {ACCENT_COLOR}, 0 0 15px rgba(0, 255, 192, 0.5) !important;
            margin-top: 15px; margin-bottom: 5px; font-family: 'Montserrat', sans-serif;
        }}

        /* SIDEBAR */
        .stSidebar {{ background-color: #1A1A24; border-right: none; box-shadow: 2px 0 5px rgba(0, 0, 0, 0.4); }}

        /* INPUTS */
        .stTextInput > div > div > input, .stSelectbox > div > div {{
            background-color: #252530; color: {TEXT_COLOR}; border: 1px solid #444;
            border-radius: 8px; box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
        }}
        .stTextInput > div > div > input:focus {{
            border-color: {ACCENT_COLOR}; box-shadow: 0 0 5px {ACCENT_COLOR}, inset 0 0 5px rgba(0,0,0,0.5);
        }}

        /* TABS */
        .stTabs [aria-selected="true"] {{
            color: {ACCENT_COLOR}; border-color: {ACCENT_COLOR}; background-color: {BG_COLOR}; 
            box-shadow: 0 -2px 8px rgba(0, 255, 192, 0.3); font-weight: 700 !important;
        }}
        
        /* BOTÕES GERAIS (Vermelho para o Pix) */
        .stButton > button {{
            background-color: #FF4B4B; color: #FFFFFF !important; border-radius: 8px;
            font-weight: 600; box-shadow: 0 0 10px #FF4B4B; transition: all 0.3s ease;
        }}
        
        /* BOTÃO LIMPAR (Neon Green - Fixado por posição) */
        .stButton:nth-child(3) > button {{
            background-color: {ACCENT_COLOR} !important; color: {BG_COLOR} !important; box-shadow: 0 0 10px {ACCENT_COLOR} !important; 
        }}

        /* LINK BUTTON (Conversa) */
        [data-testid^="stLinkButton"]:first-child a {{
            background-color: #1A1A24 !important; color: {ACCENT_COLOR} !important;
            border: 1px solid {ACCENT_COLOR} !important; border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 255, 192, 0.5) !important; font-weight: 600; text-decoration: none !important; 
        }}
        [data-testid^="stLinkButton"]:first-child a:hover {{
            background-color: #252530 !important; box-shadow: 0 0 20px {ACCENT_COLOR} !important; transform: translateY(-2px);
        }}
        [data-testid^="stLinkButton"]:first-child a svg {{ fill: {ACCENT_COLOR} !important; }}
        
        /* Subtítulo */
        .premium-subtitle-text {{
            font-family: 'Montserrat', sans-serif; font-size: 1.3em; font-weight: 600; color: {TEXT_COLOR}; 
            letter-spacing: 0.08em; text-align: center; margin-top: 0px !important; margin-bottom: 25px !important; 
            text-shadow: 0 0 3px rgba(255,255,255,0.1); 
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- 2. ESTRUTURA ORIGINAL ---
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>ZapCopy Pro</h1>
            <p class="premium-subtitle-text">Sistema de Cobrança Otimizado para WhatsApp</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    with st.sidebar:
        # LOGOUT DISCRETO (Pequeno link no topo, sem estragar o layout)
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
        
        # Lógica auxiliar
        def limpar_texto(texto):
            if not texto: return ""
            nfkd = unicodedata.normalize('NFKD', texto)
            sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
            return re.sub(r'[^A-Z0-9 ]', '', sem_acento.upper()).strip()
        def formatar_valor(valor):
            try: return "{:.2f}".format(float(valor.replace("R$", "").replace(",", ".").strip()))
            except: return "0.00"
        def crc16_ccitt(payload):
            crc = 0xFFFF
            polynomial = 0x1021
            for byte in payload.encode('utf-8'):
                crc ^= (byte << 8)
                for _ in range(8):
                    if (crc & 0x8000): crc = (crc << 1) ^ polynomial
                    else: crc = (crc << 1)
                crc &= 0xFFFF
            return "{:04X}".format(crc)
        def gerar_pix_payload(chave, nome, cidade, valor, txid="***"):
            chave_limpa = chave.strip(); nome_limpo = limpar_texto(nome)[:25]; cidade_limpa = limpar_texto(cidade)[:15]; valor_formatado = formatar_valor(valor)
            p_chave = f"0014BR.GOV.BCB.PIX01{len(chave_limpa):02}{chave_limpa}"
            payload = f"00020126{len(p_chave):02}{p_chave}52040000530398654{len(valor_formatado):02}{valor_formatado}5802BR59{len(nome_limpo):02}{nome_limpo}60{len(cidade_limpa):02}{cidade_limpa}62070503{txid}6304"
            return f"{payload}{crc16_ccitt(payload)}"

        with tab1:
            cenario_cobranca = st.selectbox("Cenário:", ["Enviar Pix (Padrão)", "Lembrete de Vencimento", "Cobrança Atrasada"])
            valor_cobranca = st.text_input("Valor (R$)", placeholder="Ex: 150,00", value="")
            if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
                if cenario_cobranca == "Enviar Pix (Padrão)":
                    intro = f"Prezado(a) {nome_cliente}, segue os dados bancários para a quitação do valor de R$ {valor_cobranca}." if tom_voz == "Profissional 👔" else f"Oi {nome_cliente}, tudo bem? Segue o Pix referente ao valor de R$ {valor_cobranca} conforme combinamos."
                elif cenario_cobranca == "Lembrete de Vencimento":
                    intro = f"Olá {nome_cliente}. Lembramos que o vencimento da fatura de R$ {valor_cobranca} é hoje." if tom_voz == "Profissional 👔" else f"Opa {nome_cliente}! Passando pra lembrar que seu boleto de R$ {valor_cobranca} vence hoje, ok?"
                else: 
                    intro = f"{nome_cliente}, não identificamos o pagamento de R$ {valor_cobranca}. Precisamos regularizar." if tom_voz == "Profissional 👔" else f"Oi {nome_cliente}, acho que você esqueceu da gente rs. Não vi o pagamento de R$ {valor_cobranca}."
                
                if meu_pix and meu_nome:
                    pix_gerado = gerar_pix_payload(meu_pix, meu_nome, minha_cidade, valor_cobranca if valor_cobranca else "0,00")
                    script_final = intro + "\n\n👇 Segue o código 'Copia e Cola' na mensagem abaixo:"
                else:
                    st.error("⚠️ Preencha os dados do Pix na barra lateral!")

        with tab2:
            cenario_venda = st.selectbox("Objetivo:", ["Oferta Especial", "Recuperar Cliente", "Upsell (Oferecer mais)"])
            produto = st.text_input("Nome do Produto", value="", placeholder="Ex: Serviço Premium")
            if st.button("✨ Gerar Venda", type="primary", use_container_width=True):
                if cenario_venda == "Oferta Especial":
                    script_final = f"😱 {nome_cliente}, oportunidade única! Liberamos uma condição surreal para o {produto}. Restam poucas vagas." if tom_voz == "Persuasivo 🔥" else f"Oi {nome_cliente}! Preparei uma condição especial no {produto} pra você."
                elif cenario_venda == "Recuperar Cliente":
                    script_final = f"Ei {nome_cliente}, faz tempo que a gente não se fala! Chegou novidade de {produto} que é a sua cara."
                else:
                    script_final = f"{nome_cliente}, quem leva {produto} costuma ter muito resultado com esse complemento aqui. Posso adicionar no seu pacote?"

        with tab3:
            data_agendamento = st.date_input("Dia do Agendamento (Opcional)", value=None)
            horario = st.time_input("Horário do Agendamento", value=None)
            if st.button("✨ Confirmar Agenda", type="primary", use_container_width=True):
                d_str = f" no dia {data_agendamento.strftime('%d/%m')}" if data_agendamento else ""
                h_str = str(horario)[0:5] if horario else "horário combinado"
                script_final = f"Olá {nome_cliente}. Confirmamos seu agendamento{d_str} para às {h_str}. Solicitamos pontualidade." if tom_voz == "Profissional 👔" else f"Confirmadíssimo, {nome_cliente}! Te espero{d_str} às {h_str}. Até lá! 👊"

        with tab4:
            if st.button("✨ Pedir Feedback", type="primary", use_container_width=True):
                script_final = f"Oi {nome_cliente}! Foi um prazer te atender. De 0 a 10, quanto você recomendaria nosso serviço? Sua opinião ajuda muito! ⭐"

        if script_final:
            st.divider()
            st.success("✅ Mensagem Pronta!")
            with st.expander("👀 Ver texto da mensagem"): st.write(script_final)

            script_clean = script_final.replace('\n', '%0A'); msg_enc = quote(script_clean)
            pix_clean = pix_gerado.replace('\n', '%0A'); pix_enc = quote(pix_clean)
            
            if celular_cliente:
                nums = "".join(filter(str.isdigit, celular_cliente.strip()))
                if not nums.startswith("55"): nums = "55" + nums
                base = f"https://api.whatsapp.com/send?phone={nums}"
                link_t, label_b, link_p = f"{base}&text={msg_enc}", f"Enviar Conversa para {nome_cliente}", f"{base}&text={pix_enc}"
            else:
                base = "https://api.whatsapp.com/send"
                link_t, label_b, link_p = f"{base}?text={msg_enc}", "Abrir WhatsApp com Conversa", f"{base}?text={pix_enc}"
            
            c_b1, c_b2, c_b3 = st.columns(3)
            with c_b1:
                st.markdown("**Passo 1: Conversa**")
                st.link_button(f"💬 {label_b}", link_t, type="secondary", use_container_width=True)
            with c_b2:
                st.markdown("**Passo 2: Pagamento**")
                if pix_gerado: st.link_button("💲 Enviar Pix (Copia e Cola)", link_p, type="primary", use_container_width=True)
                else: st.info("Nenhum Pix gerado.")
            with c_b3:
                st.markdown("**Ações**")
                if st.button("🗑️ Limpar Formulário", type="secondary", use_container_width=True): st.rerun()

            if pix_gerado:
                st.markdown("---")
                with st.expander("📱 Testar ou Copiar Código PIX"):
                    st.markdown("##### Código PIX")
                    st.text_area("Código PIX:", pix_gerado, height=3)
                    st.markdown("---")
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_gerado)}"
                    col_qr, col_txt = st.columns([1,3])
                    with col_qr: st.image(qr_url, width=120)
                    with col_txt: st.caption("Aponte o app do seu banco aqui para escanear o pagamento.")

# ==============================================================================
# 🚦 CONTROLE DE ACESSO
# ==============================================================================
if st.session_state.logged_in:
    main_app()
else:
    tela_login()
