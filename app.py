import streamlit as st
from urllib.parse import quote
import unicodedata
import re

# --- 1. FUNÇÕES DE LIMPEZA E CRIPTOGRAFIA (BLINDADAS) ---

def limpar_texto(texto):
    """Remove acentos e caracteres especiais, deixando apenas letras e números básicos."""
    if not texto: return ""
    # Normaliza (remove acentos)
    nfkd = unicodedata.normalize('NFKD', texto)
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # Mantém apenas letras, números e espaços, converte para maiúsculo
    return re.sub(r'[^A-Z0-9 ]', '', sem_acento.upper()).strip()

def formatar_valor(valor):
    """Garante que o valor esteja no formato 100.00"""
    try:
        # Troca vírgula por ponto e converte para float
        val_float = float(valor.replace("R$", "").replace(",", ".").strip())
        return "{:.2f}".format(val_float)
    except:
        return "0.00"

def crc16_ccitt(payload):
    """Calcula o CRC16 padrão exigido pelo Banco Central."""
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
    # Limpezas de Segurança
    chave_limpa = chave.strip() # Chave pix aceita caracteres, mas sem espaços nas pontas
    nome_limpo = limpar_texto(nome)[:25] # Max 25 chars
    cidade_limpa = limpar_texto(cidade)[:15] # Max 15 chars
    valor_formatado = formatar_valor(valor)
    
    # Montagem dos Campos (Padrão EMV QRCPS)
    # 00 - Payload Format
    # 26 - Merchant Account (GUI + Chave)
    # 52 - MCC (0000 ou 6012)
    # 53 - Moeda (986 = BRL)
    # 54 - Valor
    # 58 - País
    # 59 - Nome
    # 60 - Cidade
    # 62 - Additional Data (TxID)
    
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

# --- 2. INTERFACE DO APLICATIVO ---
st.set_page_config(page_title="ZapCopy Pro", page_icon="💸", layout="centered")

st.title("💸 ZapCopy Pro")
st.markdown("##### Sistema de Cobrança Otimizado para WhatsApp")
st.divider()

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Configurar Pix")
    st.warning("Preencha com atenção para evitar erros no Banco.")
    
    meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email")
    meu_nome = st.text_input("Nome do Beneficiário", help="Nome que aparece no comprovante")
    minha_cidade = st.text_input("Cidade", value="Sao Paulo")

# MAIN APP
with st.container(border=True):
    st.subheader("1. Dados da Cobrança")
    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome do Cliente", value="Cliente")
    with col2:
        valor = st.text_input("Valor (R$)", value="100,00")
    
    celular = st.text_input("WhatsApp do Cliente (Opcional)", placeholder="11999999999")

    st.subheader("2. Gerar")
    
    if st.button("✨ Criar Cobrança", type="primary", use_container_width=True):
        if not meu_pix or not meu_nome:
            st.error("❌ Erro: Preencha sua Chave Pix e Nome na barra lateral esquerda!")
        else:
            # Gera o Código
            pix_code = gerar_pix_payload(meu_pix, meu_nome, minha_cidade, valor)
            
            # Prepara os Links
            msg_texto = f"Olá {nome_cliente}, tudo bem? 👋\n\nConforme combinado, segue o código Pix para pagamento no valor de R$ {valor}.\n\nVou te mandar o código 'Copia e Cola' na mensagem abaixo para facilitar 👇"
            msg_texto_encoded = quote(msg_texto)
            
            msg_pix_encoded = quote(pix_code)
            
            # Tratamento do Número do Celular
            link_zap_texto = ""
            link_zap_pix = ""
            
            if celular:
                nums = "".join(filter(str.isdigit, celular))
                if not nums.startswith("55"): nums = "55" + nums
                link_zap_texto = f"https://api.whatsapp.com/send?phone={nums}&text={msg_texto_encoded}"
                link_zap_pix = f"https://api.whatsapp.com/send?phone={nums}&text={msg_pix_encoded}"
                label_destino = f"para {nome_cliente}"
            else:
                link_zap_texto = f"https://api.whatsapp.com/send?text={msg_texto_encoded}"
                link_zap_pix = f"https://api.whatsapp.com/send?text={msg_pix_encoded}"
                label_destino = "no WhatsApp"

            # --- EXIBIÇÃO DOS RESULTADOS ---
            st.divider()
            st.success("✅ Cobrança Gerada com Sucesso!")
            
            # Mostra QR Code para teste
            col_qr, col_info = st.columns([1,2])
            with col_qr:
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_code)}"
                st.image(qr_url, caption="Teste com seu banco")
            with col_info:
                st.info("🚀 **Estratégia de Envio:**\nPara facilitar a vida do cliente, envie em dois passos:")
            
            st.markdown("---")
            
            # BOTÕES MÁGICOS LADO A LADO
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown(f"**Passo 1: A Mensagem**")
                st.link_button(f"1️⃣ Enviar Texto {label_destino}", link_zap_texto, use_container_width=True)
            
            with c2:
                st.markdown(f"**Passo 2: O Código**")
                st.link_button(f"2️⃣ Enviar Pix Copia e Cola", link_zap_pix, type="primary", use_container_width=True)
            
            # Exibir o código na tela caso queira copiar manual
            with st.expander("Ver código Pix gerado"):
                st.code(pix_code, language=None)
