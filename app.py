import streamlit as st
from urllib.parse import quote
import unicodedata
import re
from datetime import date 

# ==============================================================================
# ⚙️ CONFIGURAÇÃO INICIAL
# ==============================================================================
st.set_page_config(page_title="ZapCopy Pro", page_icon="💸", layout="centered")

# ==============================================================================
# 🔐 LÓGICA DE LOGIN (SESSÃO)
# ==============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Defina aqui seu usuário e senha
CREDENCIAIS = {
    "admin": "123",      # Login Admin
    "cliente": "1234"    # Login Cliente
}

def verificar_login():
    # .strip() remove espaços em branco que o usuário pode digitar sem querer
    user = st.session_state.get("input_user", "").strip()
    pwd = st.session_state.get("input_pwd", "").strip()
    
    if user in CREDENCIAIS and CREDENCIAIS[user] == pwd:
        st.session_state.logged_in = True
        st.rerun()
    else:
        st.error("Acesso negado. Verifique usuário e senha.")

def fazer_logout():
    st.session_state.logged_in = False
    st.rerun()

# ==============================================================================
# 🖥️ TELA DE LOGIN (DESIGN DARK NEON)
# ==============================================================================

def tela_login():
    # CSS Exclusivo para a tela de login
    st.markdown("""
    <style>
        /* Esconde cabeçalho e rodapé */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        .stApp { background-color: #101018; color: #EAEAEA; font-family: 'Montserrat', sans-serif; }
        
        /* ESTILO PARA DEIXAR 'USUÁRIO' E 'SENHA' EM NEGRITO */
        .stTextInput label p {
            font-weight: 800 !important;
            color: #EAEAEA !important;
            font-size: 16px !important;
        }
        
        /* Inputs do Login */
        .stTextInput input {
            background-color: #252530; color: white; 
            border: 1px solid #333; border-radius: 8px;
        }
        
        /* Botão de Entrar */
        .stButton > button {
            background-color: #00FFC0; color: #101018; font-weight: 800;
            border-radius: 8px; border: none; width: 100%; text-transform: uppercase;
            box-shadow: 0 0 15px rgba(0, 255, 192, 0.4);
        }
        .stButton > button:hover {
            box-shadow: 0 0 25px rgba(0, 255, 192, 0.6);
        }

        /* Cartão de Login */
        .login-card {
            background-color: #18181C; padding: 40px; border-radius: 15px;
            border: 1px solid #333; box-shadow: 0 0 30px rgba(0,0,0,0.5);
            text-align: center; margin-top: 50px;
        }
        
        /* Esconde a sidebar no login */
        [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="login-card">
                <h1 style="margin:0; font-family:'Montserrat',sans-serif; font-size: 2.5em; color: #00FFC0; text-shadow: 0 0 10px #00FFC0;">ZapCopy Pro</h1>
                <p style="color:#888; margin-bottom: 20px;">Área Exclusiva de Membros</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Usuário", key="input_user", placeholder="Digite seu usuário")
        st.text_input("Senha", key="input_pwd", type="password", placeholder="Digite sua senha")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("ENTRAR NO SISTEMA", on_click=verificar_login)
        
        # Dica visual (remova em produção se quiser)
        st.markdown("<div style='text-align:center; color:#555; font-size:0.8em;'>Admin: admin | Senha: 123</div>", unsafe_allow_html=True)

# ==============================================================================
# 🚀 SEU APP ORIGINAL (ENCAPSULADO AQUI)
# ==============================================================================

def main_app():
    # --- SUAS FUNÇÕES INTOCÁVEIS ---
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
                if (crc & 0x8000): crc = (crc << 1) ^ polynomial
                else: crc = (crc << 1)
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

    # --- DEFINIÇÃO DE CORES NEON (Cyber Green) ---
    ACCENT_COLOR = "#00FFC0" # Verde Neon
    BG_COLOR = "#101018" # Fundo Escuro Suave
    SECONDARY_BG_COLOR = "#1A1A24" # Fundo para containers e sidebar
    TEXT_COLOR = "#EAEAEA" # Texto Claro

    # --- CSS DO SEU APP + AS CORREÇÕES QUE VOCÊ PEDIU ---
    st.markdown(f"""
    <style>
        /* 1. REMOVER A FAIXA ESQUISITA (HEADER) */
        header {{visibility: hidden;}}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* 2. CONFIGURAÇÃO DE TEMA BASE */
        html, body, .stApp {{ 
            background-color: {BG_COLOR} !important; 
            color: {TEXT_COLOR}; 
            font-family: 'Montserrat', sans-serif; 
        }}
        .block-container {{ padding-top: 1.5rem !important; }}

        /* 3. CORRIGIR OS TEXTOS (BRANCO E NEGRITO) */
        /* Isso força labels e captions a ficarem brancos e negrito */
        label, .stLabel, .stCaption, .stMarkdown p {{
            color: {TEXT_COLOR} !important;
            font-weight: 700 !important;
        }}
        
        /* INPUTS DE TEXTO */
        .stTextInput > div > div > input, .stSelectbox > div > div {{
            background-color: #252530;
            color: {TEXT_COLOR};
            border: 1px solid #444;
            border-radius: 8px;
            box-shadow: inset 0 0 5px rgba(0,0,0,0.3);
        }}
        .stTextInput > div > div > input:focus {{
            border-color: {ACCENT_COLOR};
            box-shadow: 0 0 5px {ACCENT_COLOR}, inset 0 0 5px rgba(0,0,0,0.5);
        }}

        /* TITULO PRINCIPAL */
        h1 {{
            font-family: 'Montserrat', sans-serif;
            font-size: 3.5em; font-weight: 800; color: {ACCENT_COLOR}; 
            letter-spacing: 0.12em; text-align: center;
            text-shadow: 0 0 10px {ACCENT_COLOR}, 0 0 20px rgba(0, 255, 192, 0.5); 
        }}

        /* TÍTULOS LATERAIS */
        .neon-sidebar-header {{ 
            font-size: 1.5em; font-weight: 800; color: {ACCENT_COLOR} !important;
            letter-spacing: 0.1em;
            text-shadow: 0 0 8px {ACCENT_COLOR}, 0 0 15px rgba(0, 255, 192, 0.5) !important;
            margin-top: 15px; margin-bottom: 5px; font-family: 'Montserrat', sans-serif;
        }}
        
        /* CONTÊINER PRINCIPAL */
        .stContainer {{
            background-color: {SECONDARY_BG_COLOR};
            border: none !important; border-radius: 18px; 
            padding: 30px; margin-bottom: 25px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 255, 192, 0.2);
            transition: box-shadow 0.3s ease-in-out;
        }}
        .stContainer:hover {{
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 255, 192, 0.4); 
        }}
        
        /* SIDEBAR */
        .stSidebar {{
            background-color: {SECONDARY_BG_COLOR};
            border-right: none; box-shadow: 2px 0 5px rgba(0, 0, 0, 0.4); 
        }}

        /* TABS */
        .stTabs [aria-selected="true"] {{
            color: {ACCENT_COLOR}; border-color: {ACCENT_COLOR};
            background-color: {BG_COLOR}; 
            box-shadow: 0 -2px 8px rgba(0, 255, 192, 0.3);
            font-weight: 700 !important;
        }}
        
        /* BOTÕES */
        .stButton > button {{
            background-color: #FF4B4B; color: #FFFFFF !important; 
            border-radius: 8px; font-weight: 600;
            box-shadow: 0 0 10px #FF4B4B; transition: all 0.3s ease;
        }}
        
        /* BOTÃO LIMPAR (Corrigido) */
        .stButton:nth-child(3) > button {{
            background-color: {ACCENT_COLOR} !important;
            color: {BG_COLOR} !important; 
            box-shadow: 0 0 10px {ACCENT_COLOR} !important; 
        }}

        /* LINK BUTTONS */
        [data-testid^="stLinkButton"]:first-child a {{
            background-color: {SECONDARY_BG_COLOR} !important;
            color: {ACCENT_COLOR} !important;
            border: 1px solid {ACCENT_COLOR} !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 255, 192, 0.5) !important;
            font-weight: 600; text-decoration: none !important; 
        }}
        [data-testid^="stLinkButton"]:first-child a:hover {{
            background-color: #252530 !important;
            box-shadow: 0 0 20px {ACCENT_COLOR} !important;
            transform: translateY(-2px);
        }}
        [data-testid^="stLinkButton"]:first-child a svg {{
            fill: {ACCENT_COLOR} !important;
        }}
        
        /* SUBTITULO */
        .premium-subtitle-text {{
            font-family: 'Montserrat', sans-serif;
            font-size: 1.3em; font-weight: 600; color: {TEXT_COLOR}; 
            letter-spacing: 0.08em; text-align: center;
            margin-top: 0px !important; margin-bottom: 25px !important; 
            text-shadow: 0 0 3px rgba(255,255,255,0.1); 
        }}
    </style>
    """, unsafe_allow_html=True)

    # --- CABEÇALHO DO APP ---
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h1>ZapCopy Pro</h1>
            <p class="premium-subtitle-text">Sistema de Cobrança Otimizado para WhatsApp</p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- SIDEBAR ---
    with st.sidebar:
        # Botão de Sair Discreto
        if st.button("🔒 Sair", key="logout_main", help="Encerrar sessão"):
            fazer_logout()
            
        st.markdown('<h3 class="neon-sidebar-header">Configurar Pix</h3>', unsafe_allow_html=True)
        st.caption("Dados obrigatórios para o código funcionar.")
        meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email", value="") 
        meu_nome = st.text_input("Seu Nome Completo", value="", placeholder="Ex: Leonardo Dias") 
        minha_cidade = st.text_input("Sua Cidade", placeholder="Ex: São Paulo", value="") 
        
        st.divider()
        st.markdown('<h3 class="neon-sidebar-header">Personalização</h3>', unsafe_allow_html=True)
        tom_voz = st.selectbox("Tom de Voz da Mensagem:", ["Amigável 😊", "Profissional 👔", "Persuasivo 🔥"])

    # --- ÁREA PRINCIPAL ---
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
        msg_pix_aviso = ""

        # === ABA 1: COBRANÇA ===
        with tab1:
            cenario_cobranca = st.selectbox("Cenário:", ["Enviar Pix (Padrão)", "Lembrete de Vencimento", "Cobrança Atrasada"])
            valor_cobranca = st.text_input("Valor (R$)", placeholder="Ex: 150,00", value="")
            
            if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
                if cenario_cobranca == "Enviar Pix (Padrão)":
                    if tom_voz == "Profissional 👔":
                        intro = f"Prezado(a) {nome_cliente}, segue os dados bancários para a quitação do valor de R$ {valor_cobranca}."
                    else:
                        intro = f"Oi {nome_cliente}, tudo bem? Segue o Pix referente ao valor de R$ {valor_cobranca} conforme combinamos."
                elif cenario_cobranca == "Lembrete de Vencimento":
                    if tom_voz == "Profissional 👔":
                        intro = f"Olá {nome_cliente}. Lembramos que o vencimento da fatura de R$ {valor_cobranca} é hoje."
                    else:
                        intro = f"Opa {nome_cliente}! Passando pra lembrar que seu boleto de R$ {valor_cobranca} vence hoje, ok?"
                else: # Atrasada
                    if tom_voz == "Amigável 😊":
                        intro = f"Oi {nome_cliente}, acho que você esqueceu da gente rs. Não vi o pagamento de R$ {valor_cobranca}. Conseguimos resolver hoje?"
                    else:
                        intro = f"{nome_cliente}, não identificamos o pagamento de R$ {valor_cobranca}. Precisamos regularizar para evitar pendências."

                if meu_pix and meu_nome:
                    valor_para_pix = valor_cobranca if valor_cobranca else "0,00"
                    pix_gerado = gerar_pix_payload(meu_pix, meu_nome, minha_cidade, valor_para_pix)
                    msg_pix_aviso = "\n\n👇 Segue o código 'Copia e Cola' na mensagem abaixo:"
                    script_final = intro + msg_pix_aviso
                else:
                    st.error("⚠️ Preencha os dados do Pix na barra lateral!")

        # === ABA 2: VENDAS ===
        with tab2:
            cenario_venda = st.selectbox("Objetivo:", ["Oferta Especial", "Recuperar Cliente", "Upsell (Oferecer mais)"])
            produto = st.text_input("Nome do Produto", value="", placeholder="Ex: Serviço Premium")
            
            if st.button("✨ Gerar Venda", type="primary", use_container_width=True):
                if cenario_venda == "Oferta Especial":
                    if tom_voz == "Persuasivo 🔥":
                        script_final = f"😱 {nome_cliente}, oportunidade única! Liberamos uma condição surreal para o {produto}. Restam poucas vagas. Quer ver?"
                    else:
                        script_final = f"Oi {nome_cliente}! Preparei uma condição especial no {produto} pra você. Tem um minutinho pra eu te mostrar?"
                elif cenario_venda == "Recuperar Cliente":
                    script_final = f"Ei {nome_cliente}, faz tempo que a gente não se fala! Chegou novidade de {produto} que é a sua cara."
                else:
                    script_final = f"{nome_cliente}, quem leva {produto} costuma ter muito resultado com esse complemento aqui. Posso adicionar no seu pacote?"

        # === ABA 3: AGENDAMENTO ===
        with tab3:
            data_agendamento = st.date_input("Dia do Agendamento (Opcional)", value=None)
            horario = st.time_input("Horário do Agendamento", value=None)
            
            if st.button("✨ Confirmar Agenda", type="primary", use_container_width=True):
                data_str = ""
                if data_agendamento:
                    data_str = f" no dia {data_agendamento.strftime('%d/%m')}"
                
                hora_str = str(horario)[0:5] if horario else "horário combinado"
                
                if tom_voz == "Profissional 👔":
                    script_final = f"Olá {nome_cliente}. Confirmamos seu agendamento{data_str} para às {hora_str}. Solicitamos pontualidade. Obrigado."
                else:
                    script_final = f"Confirmadíssimo, {nome_cliente}! Te espero{data_str} às {hora_str}. Até lá! 👊"

        # === ABA 4: FEEDBACK ===
        with tab4:
            if st.button("✨ Pedir Feedback", type="primary", use_container_width=True):
                script_final = f"Oi {nome_cliente}! Foi um prazer te atender. De 0 a 10, quanto você recomendaria nosso serviço? Sua opinião ajuda muito! ⭐"

        # ==============================================================================
        # 📤 ZONA DE SAÍDA (BOTÕES)
        # ==============================================================================

        if script_final:
            st.divider()
            st.success("✅ Mensagem Pronta!")
            
            with st.expander("👀 Ver texto da mensagem"):
                st.write(script_final)

            link_texto = ""
            link_pix_code = ""
            
            # ENCODING
            script_final_clean = script_final.replace('\n', '%0A') 
            msg_texto_encoded = quote(script_final_clean)
            
            pix_payload_clean = pix_gerado.replace('\n', '%0A')
            msg_pix_encoded = quote(pix_payload_clean)

            if celular_cliente:
                nums = "".join(filter(str.isdigit, celular_cliente.strip()))
                if not nums.startswith("55"): nums = "55" + nums
                base_link_sem_query = f"https://api.whatsapp.com/send?phone={nums}"
                link_texto = f"{base_link_sem_query}&text={msg_texto_encoded}"
                label_btn = f"Enviar Conversa para {nome_cliente}"
                link_pix_code = f"{base_link_sem_query}&text={msg_pix_encoded}" 
            else:
                base_link_sem_query = f"https://api.whatsapp.com/send"
                link_texto = f"{base_link_sem_query}?text={msg_texto_encoded}"
                label_btn = "Abrir WhatsApp com Conversa"
                link_pix_code = f"{base_link_sem_query}?text={msg_pix_encoded}" 
                
            label_pix_btn = "💲 Enviar Pix (Copia e Cola)"
            
            # Colunas: Conversa, Pagamento, Limpeza
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                st.markdown("**Passo 1: Conversa**")
                st.link_button(f"💬 {label_btn}", link_texto, type="secondary", use_container_width=True)
            
            with col_btn2:
                st.markdown("**Passo 2: Pagamento**")
                if pix_gerado:
                    st.link_button(label_pix_btn, link_pix_code, type="primary", use_container_width=True)
                else:
                    st.info("Nenhum Pix gerado.")

            with col_btn3:
                st.markdown("**Ações**")
                if st.button("🗑️ Limpar Formulário", type="secondary", use_container_width=True):
                    st.rerun()

            if pix_gerado:
                st.markdown("---")
                with st.expander("📱 Testar ou Copiar Código PIX"):
                    st.markdown("##### Código PIX (Para copiar e colar no app do banco)")
                    st.text_area("Código PIX:", pix_gerado, height=3, key='pix_payload_output', help="Clique no código para copiar para a área de transferência.")
                    
                    st.markdown("---")
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_gerado)}"
                    col_qr, col_txt = st.columns([1,3])
                    with col_qr:
                        st.image(qr_url, width=120)
                    with col_txt:
                        st.caption("Aponte o app do seu banco aqui para escanear o pagamento.")

# ==============================================================================
# 🚦 GATEKEEPER (CONTROLE DE ACESSO)
# ==============================================================================

if st.session_state.logged_in:
    main_app()
else:
    tela_login()
