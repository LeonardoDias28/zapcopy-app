import streamlit as st
from urllib.parse import quote

# --- FUNÇÃO PIX (MANTIDA) ---
def gerar_payload_pix(chave, nome, cidade, valor):
    nome = nome[0:25].upper().ljust(25)
    cidade = cidade[0:15].upper().ljust(15)
    valor_str = "{:.2f}".format(float(valor.replace(",", ".")))
    payload = f"00020126330014BR.GOV.BCB.PIX0114{chave}520400005303986540{len(valor_str)}{valor_str}5802BR59{len(nome)}{nome}60{len(cidade)}{cidade}62070503***6304"
    
    polinomio = 0x1021
    resultado = 0xFFFF
    if type(payload) is str:
        payload = payload.encode()
    for byte in payload:
        resultado ^= (byte << 8)
        for _ in range(8):
            if (resultado & 0x8000):
                resultado = (resultado << 1) ^ polinomio
            else:
                resultado = resultado << 1
        resultado &= 0xFFFF
    crc16 = "{:04X}".format(resultado)
    return f"{payload.decode()}{crc16}"

# --- CONFIGURAÇÃO VISUAL (CLEAN) ---
# Mudei para "centered" para não ficar esticado
st.set_page_config(page_title="ZapCopy Pro", page_icon="🚀", layout="centered")

# Cabeçalho Limpo
st.title("🚀 ZapCopy Pro")
st.markdown("##### O jeito mais rápido de responder clientes no WhatsApp.")
st.divider()

# --- BARRA LATERAL (CONFIGURAÇÕES DO USUÁRIO) ---
with st.sidebar:
    st.header("⚙️ Seus Dados (Pix)")
    st.caption("Preencha para gerar o QR Code de pagamento.")
    
    meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Email ou Celular")
    meu_nome = st.text_input("Seu Nome", placeholder="Ex: Leonardo Dias")
    minha_cidade = st.text_input("Sua Cidade", value="Sao Paulo")
    
    st.success("Configurações salvas automaticamente!")

# --- ÁREA PRINCIPAL (EM CARTÃO) ---
# Container para agrupar e ficar bonito visualmente
with st.container(border=True):
    st.subheader("👤 Quem é o cliente?")
    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome", value="Fulano")
    with col2:
        celular_cliente = st.text_input("WhatsApp (Opcional)", placeholder="DDD + Número")
    
    st.write("") # Espaço
    
    st.subheader("💬 O que você quer fazer?")
    # Abas Limpas
    tab1, tab2, tab3 = st.tabs(["💸 Cobrar", "🛒 Vender", "📅 Agendar"])
    
    script_final = ""
    pix_copia_cola = ""

    # --- ABA COBRANÇA ---
    with tab1:
        situacao = st.selectbox("Situação:", ["Lembrete Amigável", "Atraso + Pix", "Negociação Urgente"])
        valor_cobranca = st.text_input("Valor (R$)", value="100,00")
        
        if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
            if situacao == "Lembrete Amigável":
                script_final = f"Oi {nome_cliente}, tudo bem? 👋\nSó lembrando que o vencimento de R$ {valor_cobranca} é amanhã. Já quer agendar?"
            elif situacao == "Atraso + Pix":
                if meu_pix:
                    pix_copia_cola = gerar_payload_pix(meu_pix, meu_nome, minha_cidade, valor_cobranca)
                    script_final = f"Olá {nome_cliente}.\nNão identificamos o pagamento de R$ {valor_cobranca}.\nSegue o Pix Copia e Cola pra facilitar:\n\n{pix_copia_cola}\n\nMe avisa quando pagar?"
                else:
                    st.warning("⚠️ Preencha sua Chave Pix na barra lateral!")
            else:
                script_final = f"{nome_cliente}, precisamos resolver a pendência de R$ {valor_cobranca} para evitar bloqueio. Vamos negociar?"

    # --- ABA VENDAS ---
    with tab2:
        tipo_venda = st.selectbox("Tipo:", ["Oferta Especial", "Recuperar Cliente"])
        produto = st.text_input("Produto/Serviço", value="Consultoria")
        
        if st.button("✨ Gerar Venda", type="primary", use_container_width=True):
            if tipo_venda == "Oferta Especial":
                script_final = f"Opa {nome_cliente}! \nSeparei uma condição exclusiva pra você fechar a {produto} hoje.\nTem interesse em ver?"
            else:
                script_final = f"Oi {nome_cliente}, sumiu! \nChegou novidade de {produto} que é a sua cara. Posso mandar foto?"

    # --- ABA AGENDA ---
    with tab3:
        horario = st.time_input("Horário", value=None)
        if st.button("✨ Gerar Confirmação", type="primary", use_container_width=True):
            hora = str(horario)[0:5]
            script_final = f"Confirmadíssimo, {nome_cliente}! \nTe espero às {hora}. Endereço você já tem né? Até lá! 👊"

# --- RESULTADO (FORA DO CARTÃO DE INPUTS) ---
if script_final:
    st.divider()
    st.markdown("### ✅ Sua Mensagem:")
    
    st.code(script_final, language=None)
    
    if pix_copia_cola:
        col_qr, col_info = st.columns([1, 3])
        with col_qr:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_copia_cola)}"
            st.image(qr_url, width=150)
        with col_info:
            st.info("⬅️ O cliente pode ler este QR Code agora, ou copiar o código que está na mensagem acima!")

    # BOTÃO WHATSAPP
    texto_encoded = quote(script_final)
    if celular_cliente:
        nums = "".join(filter(str.isdigit, celular_cliente))
        link_zap = f"https://wa.me/55{nums}?text={texto_encoded}"
        btn_label = f"Enviar para {nome_cliente} 📲"
    else:
        link_zap = f"https://wa.me/?text={texto_encoded}"
        btn_label = "Abrir no WhatsApp 📲"

    st.link_button(btn_label, link_zap, type="primary", use_container_width=True)
