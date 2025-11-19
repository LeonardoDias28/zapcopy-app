import streamlit as st

# 1. Configuração da Página (Título e Ícone)
st.set_page_config(page_title="ZapCopy", page_icon="💬")

# 2. Cabeçalho e Título
st.title("💬 ZapCopy")
st.subheader("Gerador de Scripts para WhatsApp")
st.markdown("---")

# 3. Barra Lateral (Menu de Opções)
with st.sidebar:
    st.header("⚙️ Configurações")
    # O usuário escolhe o cenário aqui
    cenario = st.selectbox(
        "Qual é a situação?",
        [
            "Cobrança Amigável (Lembrete)",
            "Cobrança Firme (Atraso)",
            "Recuperar Cliente Sumido",
            "Pedir Feedback Pós-Venda"
        ]
    )
    st.info("💡 Dica: Preencha os dados ao lado para personalizar o script.")

# 4. Área de Inputs (Onde o usuário digita)
col1, col2 = st.columns(2)

with col1:
    nome_cliente = st.text_input("Nome do Cliente", value="Fulano")
with col2:
    valor_produto = st.text_input("Valor ou Produto", value="R$ 150,00")

# 5. Lógica de Geração dos Textos (O Cérebro do App)
def gerar_script(cenario, nome, valor):
    if cenario == "Cobrança Amigável (Lembrete)":
        return f"""
Olá, *{nome}*! Tudo bem? 👋

Passando só para lembrar que o boleto/pagamento referente a *{valor}* vence hoje.

Se já tiver feito o pagamento, pode desconsiderar essa mensagem, ok? 
Qualquer dúvida, estou à disposição!
        """
    
    elif cenario == "Cobrança Firme (Atraso)":
        return f"""
Bom dia, *{nome}*. 

Não identificamos o pagamento de *{valor}* no nosso sistema até o momento. 
Aconteceu algum imprevisto? 🤔

Podemos atualizar o boleto ou enviar um link do Pix para regularizar isso hoje?
Fico no aguardo.
        """
    
    elif cenario == "Recuperar Cliente Sumido":
        return f"""
Oi *{nome}*, sumiu! 😅

Estava olhando aqui e vi que faz tempo que a gente não se fala. 
Chegaram algumas novidades aqui que têm tudo a ver com o que você gosta.

Topa dar uma olhadinha sem compromisso?
        """
    
    elif cenario == "Pedir Feedback Pós-Venda":
        return f"""
Olá *{nome}*! 🌟

Espero que esteja gostando de *{valor}*!
Para nós é muito importante saber sua opinião. 

De 0 a 10, o que achou da experiência? Seu feedback nos ajuda muito a melhorar!
        """
    else:
        return "Selecione uma opção."

# 6. Botão e Exibição do Resultado
st.markdown("### 👇 Seu Script Gerado:")

if st.button("✨ Gerar Mensagem", type="primary"):
    # Chama a função e guarda o texto
    script_final = gerar_script(cenario, nome_cliente, valor_produto)
    
    # Mostra o texto numa caixa de código (fácil de copiar)
    st.code(script_final, language="markdown")
    st.success("Copiado! Agora é só colar no WhatsApp.")
