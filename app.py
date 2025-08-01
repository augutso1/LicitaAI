import streamlit as st
import time
import random

# Configuração da página
st.set_page_config(
    page_title="Licita-IA | Agente de Cotações",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para o tema escuro e estilos dos botões
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }
    
    .stop-button > button {
        background-color: #f44336 !important;
        color: white !important;
    }
    
    .stop-button > button:hover {
        background-color: #d32f2f !important;
    }
    
    .edit-button > button {
        background-color: #3A3B47 !important;
        color: #FAFAFA !important;
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 16px !important;
    }
    
    .edit-button > button:hover {
        background-color: #4A4B57 !important;
    }
    
    .status-container {
        background-color: #3A3B47;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    
    .progress-step {
        padding: 0.3rem 0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    
    .step-completed {
        color: #4CAF50;
    }
    
    .step-current {
        color: #FF6B6B;
        font-weight: bold;
    }
    
    .step-pending {
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas
    welcome_message = "Olá! Estou pronto para ajudar a encontrar os melhores produtos para sua licitação. Por favor, descreva o que você precisa."
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

if "processing" not in st.session_state:
    st.session_state.processing = False

if "current_step" not in st.session_state:
    st.session_state.current_step = 0

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1

# Título da aplicação
st.title("🏢 Licita-IA | Agente de Cotações")

# Função para simular o processo do agente de IA
def simulate_ai_process():
    """Simula o processo do agente de IA com steps em tempo real"""
    steps = [
        "[PASSO 1/5] 🕵️‍♂️ Ativando Agente de Pesquisa...",
        "[PASSO 2/5] 🌐 Rastreando a web em busca de produtos e fornecedores...",
        "[PASSO 3/5] 🔬 Analisando 3 produtos compatíveis. Verificando especificações e CNPJ dos vendedores...",
        "[PASSO 4/5] 📸 Capturando screenshots das páginas de produto para evidência...",
        "[PASSO 5/5] 📊 Gerando o relatório final em Excel...",
        "[CONCLUÍDO] ✅ Processo finalizado! Seu relatório está pronto."
    ]
    
    return steps

def stop_processing():
    """Para o processamento atual"""
    st.session_state.processing = False
    st.session_state.current_step = 0
    # Adiciona mensagem de cancelamento
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "❌ Processo cancelado pelo usuário. Você pode iniciar uma nova consulta a qualquer momento."
    })

def start_edit_mode(index):
    """Inicia o modo de edição para uma mensagem específica"""
    st.session_state.edit_mode = True
    st.session_state.edit_index = index

def cancel_edit():
    """Cancela o modo de edição"""
    st.session_state.edit_mode = False
    st.session_state.edit_index = -1

def save_edit(new_content):
    """Salva a edição e reinicia o processo"""
    if st.session_state.edit_index != -1:
        # Atualiza a mensagem editada
        st.session_state.messages[st.session_state.edit_index]["content"] = new_content
        
        # Remove todas as mensagens após a editada
        st.session_state.messages = st.session_state.messages[:st.session_state.edit_index + 1]
        
        # Reinicia o processo
        st.session_state.processing = True
        st.session_state.current_step = 0
        
        # Adiciona mensagem inicial do assistente
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Entendido. Iniciando o processo de cotação para o seu produto. Acompanhe meu progresso abaixo:"
        })
        
        # Cancela o modo de edição
        cancel_edit()

# Área de chat - exibe todas as mensagens
chat_container = st.container()

with chat_container:
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            col1, col2 = st.columns([0.95, 0.05])
            
            with col1:
                # Modo de edição para mensagens do usuário
                if (st.session_state.edit_mode and 
                    st.session_state.edit_index == i and 
                    message["role"] == "user"):
                    
                    edit_content = st.text_area(
                        "Edite sua mensagem:",
                        value=message["content"],
                        key=f"edit_area_{i}",
                        height=100
                    )
                    
                    col_save, col_cancel = st.columns([1, 1])
                    with col_save:
                        if st.button("💾 Salvar", key=f"save_{i}"):
                            save_edit(edit_content)
                            st.rerun()
                    
                    with col_cancel:
                        if st.button("❌ Cancelar", key=f"cancel_{i}"):
                            cancel_edit()
                            st.rerun()
                else:
                    st.write(message["content"])
            
            # Botão de edição para mensagens do usuário
            with col2:
                if (message["role"] == "user" and 
                    not st.session_state.processing and 
                    not st.session_state.edit_mode):
                    
                    if st.button("✏️", key=f"edit_{i}", help="Editar mensagem"):
                        start_edit_mode(i)
                        st.rerun()

# Container para o processo em andamento
if st.session_state.processing:
    with st.container():
        st.markdown('<div class="status-container">', unsafe_allow_html=True)
        
        steps = simulate_ai_process()
        
        # Exibe todos os steps com status
        for idx, step in enumerate(steps):
            if idx < st.session_state.current_step:
                # Step concluído
                st.markdown(f'<div class="progress-step step-completed">{step}</div>', 
                           unsafe_allow_html=True)
            elif idx == st.session_state.current_step:
                # Step atual
                st.markdown(f'<div class="progress-step step-current">{step}</div>', 
                           unsafe_allow_html=True)
            else:
                # Step pendente
                st.markdown(f'<div class="progress-step step-pending">{step}</div>', 
                           unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botão de parar
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.markdown('<div class="stop-button">', unsafe_allow_html=True)
            if st.button("🛑 Parar Processo", key="stop_button"):
                stop_processing()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Processamento automático em background
if st.session_state.processing and st.session_state.current_step < 6:
    # Simula delay realista para cada step
    time.sleep(random.uniform(1.5, 3.0))
    st.session_state.current_step += 1
    
    if st.session_state.current_step >= 6:
        # Processo concluído
        st.session_state.processing = False
        st.session_state.current_step = 0
        
        # Adiciona mensagem de conclusão detalhada
        completion_message = """
**📋 Relatório de Cotação Concluído!**

✅ **3 produtos encontrados** com especificações compatíveis
✅ **Fornecedores verificados** com CNPJ válido
✅ **Screenshots capturadas** para evidência
✅ **Planilha Excel gerada** com comparativo de preços

**Próximos passos:**
- Baixe o relatório completo
- Revise as especificações técnicas
- Entre em contato com os fornecedores selecionados

*Precisa de outra cotação? Digite uma nova especificação abaixo.*
        """
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": completion_message
        })
    
    st.rerun()

# Input do usuário na parte inferior
if not st.session_state.edit_mode:
    user_input = st.chat_input(
        placeholder="Descreva o produto que você precisa cotar...",
        disabled=st.session_state.processing
    )

    if user_input and not st.session_state.processing:
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Inicia o processo de IA
        st.session_state.processing = True
        st.session_state.current_step = 0
        
        # Adiciona mensagem inicial do assistente
        initial_response = "Entendido. Iniciando o processo de cotação para o seu produto. Acompanhe meu progresso abaixo:"
        st.session_state.messages.append({"role": "assistant", "content": initial_response})
        
        st.rerun()

# Informações adicionais na sidebar (se necessário)
with st.sidebar:
    st.markdown("### ℹ️ Sobre o Licita-IA")
    st.markdown("""
    **Funcionalidades:**
    - 🔍 Pesquisa automática de produtos
    - 🏢 Verificação de fornecedores
    - 📊 Geração de relatórios
    - 📸 Captura de evidências
    - ✏️ Edição de consultas
    - 🛑 Controle de processo
    
    **Como usar:**
    1. Digite a especificação do produto
    2. Acompanhe o progresso em tempo real
    3. Use ✏️ para editar consultas anteriores
    4. Use 🛑 para cancelar se necessário
    """)
    
    st.markdown("---")
    st.markdown("*Desenvolvido para automatizar processos de licitação*")
