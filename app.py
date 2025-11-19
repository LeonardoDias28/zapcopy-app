import streamlit as st
from urllib.parse import quote
import unicodedata

# --- FUNÇÃO PARA REMOVER ACENTOS (CORREÇÃO DO ERRO 2056) ---
def remover_acentos(texto):
    if not texto: return ""
    # Normaliza para remover acentos (Ex: São Paulo -> Sao Paulo)
    nfkd = unicodedata.normalize('NFKD', texto)
    texto_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    # Remove caracteres especiais que não sejam letras/numeros/espaços
    return texto_sem_acento.upper()

# --- FUNÇÃO GERAÇÃO PIX (AGORA BLINDADA) ---
def gerar_payload_pix(chave, nome, cidade, valor):
    # 1. Limpeza dos dados (Crucial para não dar erro no banco)
    nome_tratado = remover_acentos(nome)[0:25].ljust(25) # Max 25 chars
    cidade_tratada = remover_acentos(cidade)[0:15].ljust(15) # Max 15 chars
    chave_tratada = remover_acentos(chave) # Remove acentos da chave tbm
    
    valor_str = "{:.2f}".format(float(valor.replace(",", ".")))
    
    # 2. Montagem do Payload
    payload = f"00020126330014BR.GOV.BCB.PIX0114{chave_tratada}520400005303986540{len(valor_str)}{valor_str}5802BR59{len(nome_tratado)}{nome_tratado}60{len(cidade_tratada)}{cidade_tratada}62070503***6304"
    
    # 3. Cálculo CRC16
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

st.title("🚀 ZapCopy Pro")
st.markdown("##### O jeito certo de cobrar e vender no WhatsApp.")
st.divider()

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuração Pix")
    st.info("Seus dados para gerar o QR Code sem erros.")
    meu_pix = st.text_input("Sua Chave Pix", placeholder="CPF, Email ou Celular")
    meu_nome = st.text_input("Seu Nome Completo", placeholder="Ex: Leonardo Dias")
    minha_cidade = st.text_input("Sua Cidade", placeholder="Ex: Osasco")

# --- ÁREA PRINCIPAL ---
with st.container(border=True):
    st.subheader("👤 Cliente")
    col1, col2 = st.columns(2)
    with col1:
        nome_cliente = st.text_input("Nome", value="Fulano")
    with col2:
        celular_cliente = st.text_input("WhatsApp (Opcional)", placeholder="11999998888")
    
    st.write("") 
    
    # ABAS
    tab1, tab2 = st.tabs(["💸 Gerar Cobrança + Pix", "🛒 Gerar Venda"])
    
    script_final = ""
    pix_copia_cola = ""

    # --- ABA COBRANÇA ---
    with tab1:
        valor_cobranca = st.text_input("Valor a cobrar (R$)", value="100,00")
        motivo = st.selectbox("Motivo:", ["Enviar Boleto/Pix", "Lembrete de Vencimento", "Cobrança Atrasada"])
        
        if st.button("✨ Gerar Cobrança", type="primary", use_container_width=True):
            # Verifica se tem dados do Pix preenchidos
            if meu_pix and meu_nome and minha_cidade:
                # Gera o Pix
                pix_copia_cola = gerar_payload_pix(meu_pix, meu_nome, minha_cidade, valor_cobranca)
                
                # Monta o texto com separação visual clara
                if motivo == "Enviar Boleto/Pix":
                    msg_intro = f"Olá {nome_cliente}, tudo bem? Segue os dados para pagamento de R$ {valor_cobranca} conforme combinamos."
                elif motivo == "Lembrete de Vencimento":
                    msg_intro = f"Oi {nome_cliente}! Passando pra lembrar do vencimento de R$ {valor_cobranca} hoje."
                else:
                    msg_intro = f"Olá {nome_cliente}. Não identificamos o pagamento de R$ {valor_cobranca}. Podemos regularizar hoje?"

                # AQUI ESTÁ O TRUQUE DA SEPARAÇÃO
                script_final = f"""{msg_intro}

Para facilitar, use a opção "Pix Copia e Cola" do seu banco com o código abaixo:

👇 COPIE APENAS O CÓDIGO ABAIXO:
{pix_copia_cola}"""
            
            else:
                st.error("⚠️ Para gerar cobrança, preencha SEUS DADOS na barra lateral esquerda!")

    # --- ABA VENDAS ---
    with tab2:
        produto = st.text_input("Produto em oferta", value="Serviço Especial")
        if st.button("✨ Gerar Oferta", type="primary", use_container_width=True):
            script_final = f"Opa {nome_cliente}! \nSeparei uma condição exclusiva para o {produto}. \nQuer dar uma olhada sem compromisso?"

# --- RESULTADO ---
if script_final:
    st.divider()
    
    # Visualização do QR Code (Apenas para o dono da loja ver)
    if pix_copia_cola:
        st.markdown("### 📱 QR Code (Teste com App do Banco)")
        col_qr, col_aviso = st.columns([1, 2])
        with col_qr:
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={quote(pix_copia_cola)}"
            st.image(qr_url, width=150)
        with col_aviso:
            st.warning("DICA: No WhatsApp, o cliente receberá o código em texto 'Copia e Cola', pois a imagem não pode ser enviada automaticamente.")
    
    st.markdown("### ✅ Mensagem Pronta:")
    # Mostra o texto na tela
    st.text_area("Prévia da mensagem:", value=script_final, height=250)

    # BOTÃO WHATSAPP
    texto_encoded = quote(script_final)
    
    if celular_cliente:
        nums = "".join(filter(str.isdigit, celular_cliente))
        if not nums.startswith("55"): nums = "55" + nums
        link_zap = f"https://api.whatsapp.com/send?phone={nums}&text={texto_encoded}"
        btn_label = f"Enviar para {nome_cliente} 📲"
    else:
        link_zap = f"https://api.whatsapp.com/send?text={texto_encoded}"
        btn_label = "Abrir WhatsApp e Escolher Contato 📲"

    st.link_button(btn_label, link_zap, type="primary", use_container_width=True)
