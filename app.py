import streamlit as st
from urllib.parse import quote

# 1. Configuração da Página
st.set_page_config(
    page_title="ZapCopy Pro",
    page_icon="🚀",
    layout="centered"
)

# Estilo CSS para dar uma cara mais profissional
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. Cabeçalho
st.title("🚀 ZapCopy Pro")
st.markdown("### Transforme conversas em dinheiro no WhatsApp")
st.markdown("---")

# 3. Barra Lateral (Dados Globais)
with st.sidebar:
    st.header("👤 Dados do Cliente")
    nome_cliente = st.text_input("Nome do Cliente", value="Fulano")
    
    st.header("🎨 Personalização")
    tom_voz = st.radio(
        "Tom da mensagem:",
        ["Amigável 😇", "Profissional 👔", "Persuasivo 🔥"]
    )
    
    st.info("👇 Selecione a categoria nas abas acima do gerador.")

# 4. Organização por Abas (Melhoria Visual)
aba1, aba2, aba3 = st.tabs(["💸 Cobrança", "💰 Vendas", "⭐ Pós-Venda"])

# Variável para guardar o script final
script_gerado = ""

# --- LÓGICA DA ABA COBRANÇA ---
with aba1:
    st.subheader("Recuperação de Valores")
    tipo_cobranca = st.selectbox(
        "Situação:",
        ["Lembrete de Vencimento", "Atraso (Primeiro Aviso)", "Atraso Crítico"]
    )
    valor = st.text_input("Valor em aberto (R$)", value="150,00")
    link_pix = st.text_input("Chave Pix (Opcional)", placeholder="Ex: CNPJ ou Email")

    if st.button("Gerar Cobrança"):
        if tipo_cobranca == "Lembrete de Vencimento":
            if tom_voz == "Profissional 👔":
                script_gerado = f"Olá, {nome_cliente}. Tudo bem?\nGostaria de lembrar que o vencimento da fatura de {valor} é hoje.\nCaso precise do boleto atualizado, estou à disposição."
            else: # Amigável ou Persuasivo
                script_gerado = f"Oi {nome_cliente}, tudo bom? 👋\nPassando só pra te lembrar que seu boleto de {valor} vence hoje.\nQualquer dúvida me chama!"
        
        elif tipo_cobranca == "Atraso (Primeiro Aviso)":
            pix_txt = f"Se facilitar, segue nosso Pix: {link_pix}" if link_pix else ""
            if tom_voz == "Profissional 👔":
                script_gerado = f"Prezado(a) {nome_cliente}.\nNão identificamos o pagamento de {valor} em nosso sistema.\nHouve algum imprevisto?\n{pix_txt}\nFicamos no aguardo."
            else:
                script_gerado = f"Opa {nome_cliente}, tudo certo? 🤔\nAcho que você esqueceu da gente rs. Não vi o pagamento de {valor} cair aqui.\n{pix_txt}\nConsegue ver isso pra mim hoje?"
        
        else: # Atraso Crítico
             script_gerado = f"Olá {nome_cliente}.\nPrecisamos regularizar a pendência de {valor} para evitar bloqueios ou juros.\nPodemos negociar? Aguardo seu retorno urgente."

# --- LÓGICA DA ABA VENDAS ---
with aba2:
    st.subheader("Aumentar Conversão")
    tipo_venda = st.selectbox(
        "Objetivo:",
        ["Oferta Irresistível", "Recuperar Carrinho", "Pedir Indicação"]
    )
    produto = st.text_input("Nome do Produto", value="Kit Premium")
    bonus = st.text_input("Bônus ou Desconto (Opcional)", placeholder="Ex: Frete Grátis")

    if st.button("Gerar Venda"):
        if tipo_venda == "Oferta Irresistível":
            oferta_extra = f"E ainda tem {bonus} se fechar agora!" if bonus else ""
            if tom_voz == "Persuasivo 🔥":
                script_gerado = f"⚠️ Atenção {nome_cliente}!\nÚltimas unidades do {produto} saindo agora.\nVocê não vai perder essa oportunidade né?\n{oferta_extra}\nDigita QUERO pra garantir o seu."
            else:
                script_gerado = f"Oi {nome_cliente}! 😍\nChegou reposição do {produto} que você queria.\n{oferta_extra}\nVamos separar um pra você?"
        
        elif tipo_venda == "Recuperar Carrinho":
             script_gerado = f"Ei {nome_cliente}, vi que você quase levou o {produto}!\nFicou com alguma dúvida? Posso te ajudar a finalizar?\nMe diz o que faltou pra gente fechar negócio."
        
        else: # Indicação
            script_gerado = f"{nome_cliente}, fico muito feliz que tenha gostado do {produto}!\nSe você indicar um amigo, os dois ganham um presente especial na próxima compra 🎁. O que acha?"

# --- LÓGICA DA ABA PÓS-VENDA ---
with aba3:
    st.subheader("Fidelização")
    tipo_suporte = st.selectbox("Ação:", ["Boas-vindas", "Pesquisa de Satisfação"])
    
    if st.button("Gerar Mensagem"):
        if tipo_suporte == "Boas-vindas":
            script_gerado = f"Parabéns pela compra, {nome_cliente}! 🎉\nSeu pedido já está sendo preparado com muito carinho.\nAssim que sair para entrega, eu te aviso aqui!"
        else:
            script_gerado = f"Oi {nome_cliente}! \nDe 0 a 10, qual nota você daria para nosso atendimento hoje? ⭐\nSua opinião é muito importante pra gente melhorar!"

# 5. Exibição do Resultado e Botão WhatsApp (A MÁGICA)
if script_gerado:
    st.success("Script Gerado com Sucesso! 👇")
    
    # Área de texto para copiar manualmente se quiser
    st.code(script_gerado, language=None)
    
    # Criação do Link do WhatsApp
    texto_encoded = quote(script_gerado)
    link_whatsapp = f"https://wa.me/?text={texto_encoded}"
    
    st.markdown(f"""
    <a href="{link_whatsapp}" target="_blank">
        <button style='background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-size:16px; cursor:pointer; width:100%;'>
            📲 <b>Enviar no WhatsApp Agora</b>
        </button>
    </a>
    """, unsafe_allow_html=True)
