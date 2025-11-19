import streamlit as st
from urllib.parse import quote

# --- FUNÇÃO GERADORA DE PIX (Payload CRC16) ---
# Esta função cria o código "Copia e Cola" padrão Banco Central sem precisar de bibliotecas extras
def gerar_payload_pix(chave, nome, cidade, valor):
    nome = nome[0:25].upper().ljust(25) # Limite 25 chars
    cidade = cidade[0:15].upper().ljust(15) # Limite 15 chars
    valor_str = "{:.2f}".format(float(valor.replace(",", ".")))
    
    payload = f"00020126330014BR.GOV.BCB.PIX0114{chave}520400005303986540{len(valor_str)}{valor_str}5802BR59{len(nome)}{nome}60{len(cidade)}{cidade}62070503***6304"
    
    # Cálculo do CRC16
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
st.set_page_config(page_title="ZapCopy Ultimate", page_icon="💎", layout="wide")

# CSS Customizado para visual "App Nativo"
st.markdown("""
<style>
    .stApp {background-color: #0E1117;}
    .main-card {background-color: #262730; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);}
    h1 {color: #00CC66;}
    .stButton button {
        background-color: #25D366 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        height: 50px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (DADOS DO USUÁRIO) ---
with st.sidebar:
    st.title("⚙️ Configurações")
    st.markdown("Preencha seus dados para gerar o Pix corretamente.")
    
    meu_pix = st.text_input("Sua Chave Pix (CPF/Email)", placeholder="Ex: seu@email.com")
    meu_nome = st.text_input("Seu Nome Completo", placeholder="Nome do Beneficiário Pix")
    minha_cidade = st.text_input("Sua Cidade", value="Sao Paulo")
    
    st.divider()
    st.info("💡 Dica: Preencha tudo para o QR Code funcionar!")

# --- ÁREA PRINCIPAL ---
col_esq, col_dir = st.columns([1, 1.5])

with col_esq:
    st.markdown("## 👤 Cliente")
    with st.container(border=True):
        nome_cliente = st.text_input("Nome do Cliente", value="Fulano")
        celular_cliente = st.text_input("WhatsApp (DDD + Número)", placeholder="Ex: 11999999999")
        tom_voz = st.select_slider("Tom da Mensagem", options=["😌 Sutil", "👔 Profissional", "🔥 Persuasivo"])

with col_dir:
    st.markdown("## 💬 Gerador de Script")
    
    # Abas de Categorias
    tab1, tab2, tab3, tab4 = st.tabs(["💸 Cobrança", "🛒 Vendas", "📅 Agendamento", "⭐ Feedback"])
    
    script_final = ""
    pix_copia_cola = ""
    
    # --- ABA COBRANÇA ---
    with tab1:
        situacao = st.selectbox("Situação:", ["Lembrete Antes do Vencimento", "Boleto Vencido (Leve)", "Cobrança Incisiva + Pix"])
        valor_cobranca = st.text_input("Valor (R$)", value="100,00")
        
        if st.button("Gerar Cobrança", key="btn_cob"):
            if situacao == "Lembrete Antes do Vencimento":
                script_final = f"Oi {nome_cliente}, tudo bem? 👋\nPassando pra lembrar que seu boleto de R$ {valor_cobranca} vence amanhã.\nJá quer deixar agendado?"
            
            elif situacao == "Boleto Vencido (Leve)":
                script_final = f"Olá {nome_cliente}! \nNão identificamos o pagamento de R$ {valor_cobranca}.\nAconteceu algo? Posso atualizar a data pra você?"
            
            elif situacao == "Cobrança Incisiva + Pix":
                if meu_pix and meu_nome:
                    pix_copia_cola = gerar_payload_pix(meu_pix, meu_nome, minha_cidade, valor_cobranca)
                    script_final = f"Oi {nome_cliente}.\nPrecisamos regularizar a pendência de R$ {valor_cobranca}.\nPara facilitar, segue o Pix Copia e Cola abaixo (é só copiar e pagar no app do banco):\n\n{pix_copia_cola}\n\nAguardo o comprovante."
                else:
                    st.error("⚠️ Preencha sua Chave Pix na barra lateral para gerar o código!")

    # --- ABA VENDAS ---
    with tab2:
        oferta = st.selectbox("Tipo:", ["Promoção Relâmpago", "Recuperação de Carrinho", "Upsell (Oferecer mais)"])
        produto = st.text_input("Produto", value="Mentoria")
        
        if st.button("Gerar Venda", key="btn_venda"):
            if oferta == "Promoção Relâmpago":
                script_final = f"😱 {nome_cliente}, você viu isso?\nLiberamos 3 vagas extras para a {produto} com desconto.\nDeu a louca no chefe! Quer o link?"
            elif oferta == "Recuperação de Carrinho":
                script_final = f"Ei {nome_cliente}, vi que você quase levou a {produto}!\nFicou alguma dúvida? Posso te dar um bônus pra fechar agora?"
            else:
                script_final = f"{nome_cliente}, quem leva {produto} geralmente adora esse complemento aqui...\nFaz total sentido pra você. Posso te mostrar?"

    # --- ABA AGENDAMENTO ---
    with tab3:
        acao = st.radio("Ação:", ["Confirmar Horário", "Reagendar", "Lembrete 1h antes"])
        horario = st.time_input("Horário", value=None)
        
        if st.button("Gerar Agendamento", key="btn_agenda"):
            hora_str = str(horario)[0:5] if horario else "combinado"
            if acao == "Confirmar Horário":
                script_final = f"Opa {nome_cliente}! Tudo confirmado para às {hora_str}?\nEstou separando seu material aqui. 👍"
            elif acao == "Reagendar":
                script_final = f"Oi {nome_cliente}, tive um imprevisto e vou precisar ajustar nosso horário das {hora_str}.\nVocê tem disponibilidade mais tarde?"
            else:
                script_final = f"⏰ Lembrete: Nosso encontro é daqui a pouco, às {hora_str}.\nO endereço você já tem, né? Até já!"

    # --- ABA FEEDBACK ---
    with tab4:
        if st.button("Gerar Pedido de Feedback", key="btn_feed"):
            script_final = f"{nome_cliente}, foi um prazer te atender!\n\nUma pergunta rápida: De 0 a 10, quanto você indicaria nosso serviço?\nSua opinião manda muito aqui! ⭐"

# --- RESULTADO FINAL ---
st.markdown("---")
if script_final:
    st.success("✅ Mensagem Pronta:")
    
    # Container do resultado
    with st.container(border=True):
        st.code(script_final, language=None)
        
        # SE TIVER PIX, MOSTRA O QR CODE
        if pix_copia_cola:
            st.markdown("### 📱 QR Code para Pagamento:")
            # Usa API pública para gerar a imagem do QR Code baseada no payload
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={quote(pix_copia_cola)}"
            st.image(qr_url, caption="Mostre isso pro cliente escanear")
            st.info("O código 'Copia e Cola' já está no texto da mensagem acima!")

        # BOTÃO DO WHATSAPP INTELIGENTE
        texto_encoded = quote(script_final)
        
        # Lógica: Se tem celular, link direto. Se não, link genérico.
        if celular_cliente:
            # Remove caracteres não numéricos
            celular_limpo = "".join(filter(str.isdigit, celular_cliente))
            link_zap = f"https://wa.me/55{celular_limpo}?text={texto_encoded}"
            label_btn = f"Enviar para {nome_cliente} 📲"
        else:
            link_zap = f"https://wa.me/?text={texto_encoded}"
            label_btn = "Abrir no WhatsApp (Escolher Contato) 📲"

        st.markdown(f"""
        <a href="{link_zap}" target="_blank" style="text-decoration:none;">
            <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-size:18px; font-weight:bold; cursor:pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                {label_btn}
            </button>
        </a>
        """, unsafe_allow_html=True)
