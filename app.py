import streamlit as st
from urllib.parse import quote
import unicodedata
import re
from datetime import date 

# ==============================================================================
# 🔒 ZONA INTOCÁVEL (LÓGICA DO PIX E LIMPEZA)
# ==============================================================================

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
        f"000201"
        f"26{len(p_chave):02}{p_chave}"
        f"52040000"
        f"5303986"
        f"54{len(valor_formatado):02}{valor_formatado}"
        f"5802BR"
        f"59{len(nome_limpo):02}{nome_limpo}"
        f"60{len(cidade_limpa):02}{cidade_limpa}"
        f"62070503{txid}"
        f"6304"
    )
    crc = crc16_ccitt(payload)
    return f"{payload}{crc}"

# ==============================================================================
# 🎨 INTERFACE (DARK NEON MINIMALISTA - FIX PIX COPIA/COLA)
# ==============================================================================

st.set_page_config(page_title="ZapCopy Pro", page_icon="💸", layout="centered")

# --- DEFINIÇÃO DE CORES NEON (Cyber Green) ---
ACCENT_COLOR = "#00FFC0" # Verde Neon
BG_COLOR = "#101018" # Fundo Escuro Suave
SECONDARY_BG_COLOR = "#1A1A24" # Fundo para containers e sidebar
TEXT_COLOR = "#EAEAEA" # Texto Claro

st.markdown(f"""
<style>
    /* 1. CONFIGURAÇÃO DE TEMA BASE */
    html, body, .stApp {{ 
        background-color: {BG_COLOR} !important; 
        color: {TEXT_COLOR}; 
        font-family: 'Montserrat', sans-serif; 
    }}
    .block-container {{ padding-top: 1.5rem !important; }}

    /* FIXES NO HEADER E CHEVRON (MANTIDOS) */
    .stApp > header {{
        background-color: {BG_COLOR} !important; 
        box-shadow: none !important;
    }}
    .stApp > header > div {{
        background-color: {BG_COLOR} !important; 
    }}
    .stApp > header button, .stApp > header button svg {{
        visibility: visible !important; 
        fill: {TEXT_COLOR} !important; 
        color: {TEXT_COLOR} !important;
        opacity: 1 !important;
        filter: none !important; 
    }}
    
    /* NEGITO E ESTILIZAÇÃO */
    label, .stLabel {{
        font-weight: 700 !important; 
        color: {TEXT_COLOR} !important;
    }}

    /* 2. TITULO PRINCIPAL */
    h1 {{
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5em; 
        font-weight: 800; 
        color: {ACCENT_COLOR}; 
        letter-spacing: 0.12em; 
        text-align: center;
        text-shadow: 0 0 10px {ACCENT_COLOR}, 0 0 20px rgba(0, 255, 192, 0.5); 
    }}

    /* 3. ESTILO DOS TÍTULOS LATERAIS (HTML BYPASS) */
    .neon-sidebar-header {{ 
        font-size: 1.5em; 
        font-weight: 800; 
        color: {ACCENT_COLOR} !important;
        letter-spacing: 0.1em;
        text-shadow: 0 0 8px {ACCENT_COLOR}, 0 0 15px rgba(0, 255, 192, 0.5) !important;
        margin-top: 15px;
        margin-bottom: 5px;
        font-family: 'Montserrat', sans-serif;
    }}
    
    /* 4. RESET GERAL PARA CAPTIONS NA SIDEBAR */
    .stSidebar p, .stSidebar div[data-testid^="stTextContainer"] {{
        color: {TEXT_COLOR} !important; 
        font-weight: 400;
        font-size: 1em;
        text-shadow: none !important;
    }}


    /* ESTILO DO CONTÊINER PRINCIPAL ÚNICO (Elegante)*/
    .stContainer {{
        background-color: {SECONDARY_BG_COLOR};
        border: none !important; 
        border-radius: 18px; 
        padding: 30px; 
        margin-bottom: 25px;
        box-shadow: 
            0 2px 5px rgba(0, 0, 0, 0.4), 
            0 0 15px rgba(0, 255, 192, 0.2);
        transition: box-shadow 0.3s ease-in-out;
    }}
    .stContainer:hover {{
        box-shadow: 
            0 4px 8px rgba(0, 0, 0, 0.6), 
            0 0 25px rgba(0, 255, 192, 0.4); 
    }}
    [data-testid="stVerticalBlock"] {{
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}


    /* Sidebar Styles (MANTÉM O SECUNDÁRIO) */
    .stSidebar {{
        background-color: {SECONDARY_BG_COLOR};
        border-right: none; 
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.4); 
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

    /* TABS */
    .stTabs [aria-selected="true"] {{
        color: {ACCENT_COLOR};
        border-color: {ACCENT_COLOR};
        background-color: {BG_COLOR}; 
        box-shadow: 0 -2px 8px rgba(0, 255, 192, 0.3);
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="false"] {{
        font-weight: 400 !important;
    }}

    /* TITULOS DE SESSÃO (h2/subheader) */
    h2 {{
        color: {ACCENT_COLOR};
        font-weight: 700;
        letter-spacing: 0.05em;
        text-shadow: 0 0 3px rgba(0, 255, 192, 0.2);
    }}

    /* BOTÕES PRIMÁRIOS */
    .stButton > button {{
        background-color: {ACCENT_COLOR}; 
        color: {BG_COLOR} !important; 
        border-radius: 8px;
        font-weight: 600;
        box-shadow: 0 0 10px {ACCENT_COLOR}; 
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        box-shadow: 0 0 20px {ACCENT_COLOR};
        transform: translateY(-2px);
    }}
    
    /* Subtítulo */
    .premium-subtitle-text {{
        font-family: 'Montserrat', sans-serif;
        font-size: 1.3em; 
        font-weight: 600; 
        color: {TEXT_COLOR}; 
        letter-spacing: 0.08em; 
        text-align: center;
        margin-top: 0px !important; 
        margin-bottom: 25px !important; 
        text-shadow: 0 0 3px rgba(255,255,255,0.1); 
    }}

</style>
""", unsafe_allow_html=True)


# Substituindo a logo e o st.title por um cabeçalho coeso
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>ZapCopy Pro</h1>
        <p class="premium-subtitle-text">Sistema de Cobrança Otimizado para WhatsApp</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- SIDEBAR (CONFIGURAÇÕES GERAIS) ---
with st.sidebar:
    st.markdown('<h3 class="neon-sidebar-header">Configurar Pix</h3>', unsafe_allow_html=True)
    st.caption("Dados obrigatórios para o código funcionar.")
    meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email", value="") 
    meu_nome = st.text_input("Seu Nome Completo", value="", placeholder="Ex: Leonardo Dias") 
    minha_cidade = st.text_input("Sua Cidade", placeholder="Ex: São Paulo", value="") 
    
    st.divider()
    st.markdown('<h3 class="neon-sidebar-header">Personalização</h3>', unsafe_allow_html=True)
    tom_voz = st.selectbox("Tom de Voz da Mensagem:", ["Amigável 😊", "Profissional 👔", "Persuasivo 🔥"])

# --- ÁREA PRINCIPAL (CONTÊINER ÚNICO) ---
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
    # 📤 ZONA DE SAÍDA (FIX PIX PURO PARA COPIA/COLA)
    # ==============================================================================

    if script_final:
        st.divider()
        st.success("✅ Mensagem Pronta!")
        
        # 1. Visualizar e Copiar Script da Conversa
        with st.expander("👀 Ver texto da mensagem"):
            st.write(script_final)

        link_texto = ""
        link_pix_code = ""
        
        # --- ENCODING ---
        # Conversa: Usa script_final_clean (Mensagem + Aviso do Pix)
        script_final_clean = script_final.replace('\n', '%0A') 
        msg_texto_encoded = quote(script_final_clean)
        
        # PIX Puro: Usa SOMENTE o pix_gerado
        pix_payload_clean = pix_gerado.replace('\n', '%0A')
        msg_pix_encoded = quote(pix_payload_clean)

        
        # --- Lógica de Construção da URL ---
        if celular_cliente:
            nums = "".join(filter(str.isdigit, celular_cliente.strip()))
            if not nums.startswith("55"): nums = "55" + nums
            # Base com telefone
            base_link_sem_query = f"https://api.whatsapp.com/send?phone={nums}"
            
            link_texto = f"{base_link_sem_query}&text={msg_texto_encoded}" # Inicia com &text
            label_btn = f"Enviar Conversa para {nome_cliente}"
            
            # Link PIX Puro (Com telefone, usa &text)
            link_pix_code = f"{base_link_sem_query}&text={msg_pix_encoded}" 
            
        else:
            # Base SEM telefone
            base_link_sem_query = f"https://api.whatsapp.com/send"
            
            link_texto = f"{base_link_sem_query}?text={msg_texto_encoded}" # Inicia com ?text
            label_btn = "Abrir WhatsApp com Conversa"

            # Link PIX Puro (Sem telefone, usa ?text)
            link_pix_code = f"{base_link_sem_query}?text={msg_pix_encoded}" # Inicia com ?text
            
        label_pix_btn = "💲 Enviar Pix (Copia e Cola)"
        
        # Colunas: Conversa, Pagamento, Limpeza
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            st.markdown("**Passo 1: Conversa**")
            st.link_button(f"💬 {label_btn}", link_texto, type="secondary", use_container_width=True)
        
        with col_btn2:
            st.markdown("**Passo 2: Pagamento**")
            if pix_gerado:
                # O BOTÃO DE PIX AGORA ENVIA APENAS O CÓDIGO PURO
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
                    
