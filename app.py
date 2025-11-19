import streamlit as st
from urllib.parse import quote

# --- FUNÇÃO GERAÇÃO PIX (MANTIDA E VERIFICADA) ---
def gerar_payload_pix(chave, nome, cidade, valor):
    nome = nome[0:25].upper().ljust(25)
    cidade = cidade[0:15].upper().ljust(15)
    valor_str = "{:.2f}".format(float(valor.replace(",", ".")))
    
    # Payload padrão do Banco Central
    payload = f"00020126330014BR.GOV.BCB.PIX0114{chave}520400005303986540{len(valor_str)}{valor_str}5802BR59{len(nome)}{nome}60{len(cidade)}{cidade}62070503***6304"
    
    # Cálculo CRC16 (Obrigatório)
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

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="ZapCopy Pro", page_icon="🚀", layout="centered")

# Título
st.title("🚀 ZapCopy Pro")
st.markdown("##### Ferramenta de Cobrança e Vendas Rápida")
st.divider()

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Seus Dados Pix")
    st.info("Preencha APENAS SE quiser gerar QR Code.")
    meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Celular ou Email")
    meu_nome = st.text_input("Seu Nome", placeholder="Ex: Leonardo Dias")
    minha_cidade = st.text_input("Sua Cidade", value="Osasco")

# --- ÁREA PRINCIPAL ---
with st.container(border=True):
    st.subheader("👤 Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome", value="Fulano")
    with col2:
        # DICA VISUAL PARA O USUÁRIO
        celular_cliente = st.text_input("WhatsApp do Cliente", placeholder="DDD + 9 + Número")
    
    st.write("") 
    
    st.subheader("💬 Criar Mensagem")
    tab1, tab2, tab3 = st.tabs(["💸 Cobrar", "🛒 Vender", "📅 Agendar"])
    
    script_final = ""
    pix_copia_cola = ""

    # --- ABA COBRANÇA ---
    with tab1:
        situacao = st.selectbox("Cenário:", ["Lembrete Amigável", "Cobrança com Pix", "Negociação"])
        valor_cobranca = st.text_input("Valor (R$)", value="100,00")
        
        if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
            if situacao == "Lembrete Amigável":
                script_final = f"Oi {nome_cliente}, tudo bem? 👋\nPassando pra lembrar que seu boleto de R$ {valor_cobranca} vence amanhã. Já quer deixar agendado?"
            elif situacao == "Cobrança com Pix":
                if meu_pix:
                    pix_copia_cola = gerar_payload_pix(meu_pix, meu_nome, minha_cidade, valor_cobranca)
                    # O texto foca no Copia e Cola que é o que funciona no zap
                    script_final = f"Olá {nome_cliente}.\nO valor de R$ {valor_cobranca} está em aberto.\nPara facilitar, copie o código abaixo e pague no app do seu banco (Opção Pix Copia e Cola):\n\n{pix_copia_cola}\n\nMe envia o comprovante?"
                else:
                    st.error("⚠️ Preencha sua Chave Pix na barra lateral esquerda!")
            else:
                script_final = f"{nome_cliente}, precisamos regularizar a pendência de R$ {valor_cobranca}. Podemos dividir? Me chame para negociar."

    # --- ABA VENDAS ---
    with tab2:
        venda_tipo = st.selectbox("Tipo:", ["Oferta Relâmpago", "Recuperação"])
        produto = st.text_input("Produto", value="Serviço Premium")
        if st.button("✨ Gerar Venda", type="primary", use_container_width=True):
            if venda_tipo == "Oferta Relâmpago":
                script_final = f"Opa {nome_cliente}! \nLiberamos uma condição especial para o {produto} hoje.\nTem interesse em ver?"
            else:
                script_final = f"Oi {nome_cliente}, vi que você se interessou pelo {produto}.\nFicou alguma dúvida? Posso te ajudar a fechar?"

    # --- ABA AGENDA ---
    with tab3:
        horario = st.time_input("Horário", value=None)
        if st.button("✨ Gerar Confirmação", type="primary", use_container_width=True):
            hora_str = str(horario)[0:5]
            script_final = f"Confirmado, {nome_cliente}! \nTe aguardo às {hora_str}. Até lá! 👊"

# --- RESULTADO ---
if script_final:
    st.divider()
    st.markdown("### ✅ Mensagem Pronta:")
    st.code(script_final, language=None)
    
    # MOSTRAR QR CODE (Apenas visualmente na tela)
    if pix_copia_cola:
        col_qr, col_txt = st.columns([1, 3])
        with col_qr:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_copia_cola)}"
            st.image(qr_url, width=150, caption="Escanear com App do Banco")
        with col_txt:
            st.warning("⚠️ O WhatsApp não permite enviar a imagem do QR Code automaticamente. O código 'Copia e Cola' já está no texto da mensagem!")

    # BOTÃO WHATSAPP BLINDADO (FIX)
    texto_encoded = quote(script_final)
    
    if celular_cliente:
        # Limpeza agressiva do número (remove traços, espaços, parenteses)
        nums = "".join(filter(str.isdigit, celular_cliente))
        
        # Garante o código do Brasil (55) se o usuário não digitou
        if not nums.startswith("55"):
            nums = "55" + nums
            
        # Usa link API oficial (mais robusto)
        link_zap = f"https://api.whatsapp.com/send?phone={nums}&text={texto_encoded}"
        btn_texto = f"Enviar para {nome_cliente} ({nums}) 📲"
    else:
        link_zap = f"https://api.whatsapp.com/send?text={texto_encoded}"
        btn_texto = "Abrir no WhatsApp (Selecionar Contato) 📲"

    st.link_button(btn_texto, link_zap, type="primary", use_container_width=True)
