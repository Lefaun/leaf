import streamlit as st
import folium
from streamlit_folium import st_folium
import networkx as nx
import osmnx as ox
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Carregar variáveis de ambiente
load_dotenv()

class LojaSustentavel:
    def __init__(self):
        # Configuração inicial
        st.set_page_config(page_title="Loja Sustentável", page_icon="🌱", layout="wide")
        
        # Lista de produtos
        self.produtos = [
            {"nome": "Cesta Orgânica", "preco": 12.99, "img": "https://via.placeholder.com/150"},
            {"nome": "Sabonete Natural", "preco": 7.50, "img": "https://via.placeholder.com/150"},
            {"nome": "Bolsa Ecológica", "preco": 15.00, "img": "https://via.placeholder.com/150"},
            {"nome": "Kit Bambu", "preco": 9.99, "img": "https://via.placeholder.com/150"},
            {"nome": "Mel Orgânico", "preco": 18.50, "img": "https://via.placeholder.com/150"},
            {"nome": "Horta Caseira", "preco": 25.00, "img": "https://via.placeholder.com/150"},
            {"nome": "Cosméticos Naturais", "preco": 19.99, "img": "https://via.placeholder.com/150"},
            {"nome": "Chá Artesanal", "preco": 10.99, "img": "https://via.placeholder.com/150"},
            {"nome": "Velas Ecológicas", "preco": 14.50, "img": "https://via.placeholder.com/150"},
        ]

    def enviar_email(self, pedido, total, endereco, pagamento):
        """Enviar e-mail com detalhes do pedido"""
        try:
            # Configurações de e-mail
            EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'seuemail@gmail.com')
            SENHA_EMAIL = os.getenv('SENHA_EMAIL', 'suasenha')
            EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', 'seuemail@gmail.com')

            # Criação da mensagem
            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = EMAIL_DESTINATARIO
            msg["Subject"] = "Novo Pedido - Loja Sustentável"

            # Corpo do e-mail
            corpo_email = f"""
            🛍️ Novo pedido recebido!
            
            Produtos:
            {pedido}
            
            Total: 💲{total:.2f}
            
            Forma de pagamento: {pagamento}
            Endereço de entrega: {endereco}
            
            Obrigado por sua compra! 🌱
            """
            msg.attach(MIMEText(corpo_email, "plain"))

            # Envio do e-mail
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls()
                servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
                servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
            
            return True
        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
            return False

    def criar_mapa_folium(self):
        """Criar mapa interativo usando Folium"""
        m = folium.Map(location=[-23.5505, -46.6333], zoom_start=12)  # Coordenadas de São Paulo
        
        # Adicionar marcadores de exemplo
        folium.Marker(
            location=[-23.5505, -46.6333],
            popup="Localização da Loja",
            icon=folium.Icon(color='green', icon='store')
        ).add_to(m)
        
        return m

    def executar(self):
        """Método principal de execução da aplicação"""
        # Simulação de login
        st.sidebar.title("Login")
        usuario = st.sidebar.text_input("Usuário", value="admin")
        senha = st.sidebar.text_input("Senha", type="password", value="1234")

        # Inicializar carrinho se não existir
        if "carrinho" not in st.session_state:
            st.session_state["carrinho"] = {}

        # Verificação de credenciais
        if usuario == "admin" and senha == "1234":
            # Criação das abas
            tabs = st.tabs(["Mapa", "Loja Online"])

            with tabs[0]:
                st.title("🚴 Otimizador de Percurso - GPS Ativo")
                
                # Criar mapa usando Folium
                mapa = self.criar_mapa_folium()
                st_folium(mapa, width=725)

                # Adicionar campo de busca
                endereco = st.text_input("Digite um endereço para pesquisar")
                if endereco:
                    st.write(f"Endereço digitado: {endereco}")

            with tabs[1]:
                st.title("🛍️ Loja Sustentável")

                # Exibição dos produtos
                cols = st.columns(3)
                for i, produto in enumerate(self.produtos):
                    with cols[i % 3]:
                        st.image(produto["img"], caption=produto["nome"])
                        st.write(f"💲 {produto['preco']:.2f}")
                        if st.button(f"🛒 Adicionar {produto['nome']}", key=produto["nome"]):
                            self.adicionar_ao_carrinho(produto["nome"])
                            st.success(f"{produto['nome']} adicionado ao carrinho!")

                # Exibição do carrinho
                st.sidebar.title("🛒 Carrinho de Compras")
                if st.session_state["carrinho"]:
                    total = 0
                    pedido = ""
                    for item, qtd in st.session_state["carrinho"].items():
                        preco = next(p["preco"] for p in self.produtos if p["nome"] == item)
                        subtotal = preco * qtd
                        total += subtotal
                        pedido += f"{item} ({qtd}x) - 💲{subtotal:.2f}\n"
                        st.sidebar.write(f"{item} ({qtd}x) - 💲{subtotal:.2f}")

                    st.sidebar.write(f"**Total: 💲{total:.2f}**")
                    
                    # Finalização do pedido
                    endereco = st.sidebar.text_input("📍 Endereço de Entrega")
                    pagamento = st.sidebar.selectbox("💳 Forma de Pagamento", 
                        ["Transferência Bancária", "MB Way", "PayPal"])

                    if st.sidebar.button("✅ Finalizar Pedido"):
                        if endereco:
                            if self.enviar_email(pedido, total, endereco, pagamento):
                                st.sidebar.success("Pedido realizado com sucesso! 📩")
                                st.session_state["carrinho"] = {}
                            else:
                                st.sidebar.error("❌ Erro ao enviar e-mail. Tente novamente.")
                        else:
                            st.sidebar.error("❌ Informe um endereço de entrega.")
                else:
                    st.sidebar.write("Seu carrinho está vazio.")

        else:
            st.error("Credenciais incorretas")

    def adicionar_ao_carrinho(self, produto):
        """Adicionar produto ao carrinho"""
        if produto in st.session_state["carrinho"]:
            st.session_state["carrinho"][produto] += 1
        else:
            st.session_state["carrinho"][produto] = 1

def main():
    app = LojaSustentavel()
    app.executar()

if __name__ == "__main__":
    main()
