import streamlit as st
import requests
import polyline
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit.components.v1 as components

# Carregar variáveis de ambiente
load_dotenv()

class LojaSustentavelRotaVerde:
    def __init__(self):
        # Configurações de API
        self.GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyCYgm77s7P8Hx3ucAPqSxej4jUpko46Rn0')

        
        # Configuração do Streamlit
        st.set_page_config(page_title="Loja Sustentável", page_icon="🌱", layout="wide")
        
        # Lista de produtos
        self.produtos = [
            {"nome": "Cesta Orgânica", "preco": 12.99},
            {"nome": "Sabonete Natural", "preco": 7.50},
            {"nome": "Bolsa Ecológica", "preco": 15.00}
        ]

        # Lista de cidades
        self.cidades = [
            "Sintra", "Oeiras", "Queluz", "Amadora", "Benfica", 
            "Cascais", "Lisboa", "Almada", "Setúbal"
        ]

    def enviar_email(self, pedido, total, endereco, pagamento):
        """Envia um e-mail com os detalhes do pedido."""
        try:
            EMAIL_REMETENTE = os.getenv('EMAIL_REMETENTE', 'seuemail@gmail.com')
            SENHA_EMAIL = os.getenv('SENHA_EMAIL', 'suasenha')
            EMAIL_DESTINATARIO = os.getenv('EMAIL_DESTINATARIO', 'seuemail@gmail.com')
            
            msg = MIMEMultipart()
            msg["From"] = EMAIL_REMETENTE
            msg["To"] = EMAIL_DESTINATARIO
            msg["Subject"] = "Novo Pedido - Loja Sustentável"
            
            corpo_email = f"""
            🛙️ Novo pedido recebido!
            Produtos:
            {pedido}
            Total: 💲{total:.2f}
            Forma de pagamento: {pagamento}
            Endereço de entrega: {endereco}
            Obrigado por sua compra! 🌱
            """
            msg.attach(MIMEText(corpo_email, "plain"))
            
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls()
                servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
                servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
            
            return True
        except Exception as e:
            st.error(f"Erro ao enviar e-mail: {e}")
            return False

    def gerar_mapa(self, origem, destino):
        """Gera o código HTML para exibir o mapa com a rota."""
        mapa_html = f'''
        <html>
        <head>
            <script src="https://maps.googleapis.com/maps/api/js?key={self.GOOGLE_MAPS_API_KEY}&callback=initMap" async defer></script>
            <script>
                function initMap() {{
                    const directionsService = new google.maps.DirectionsService();
                    const directionsRenderer = new google.maps.DirectionsRenderer();
                    const map = new google.maps.Map(document.getElementById("map"), {{
                        zoom: 12,
                        center: {{ lat: 38.7169, lng: -9.1399 }},
                        mapTypeId: google.maps.MapTypeId.ROADMAP,
                        tilt: 45
                    }});

                    directionsRenderer.setMap(map);
                    directionsRenderer.setPanel(document.getElementById("directionsPanel"));

                    directionsService.route(
                        {{
                            origin: "{origem}, Portugal",
                            destination: "{destino}, Portugal",
                            travelMode: google.maps.TravelMode.WALKING
                        }},
                        (response, status) => {{
                            if (status === "OK") {{
                                directionsRenderer.setDirections(response);
                            }} else {{
                                alert("Falha ao encontrar a rota: " + status);
                            }}
                        }}
                    );
                }}
            </script>
            <style>
                #map {{
                    height: 500px;
                    width: 70%;
                    float: left;
                }}
                #directionsPanel {{
                    width: 28%;
                    height: 500px;
                    float: right;
                    overflow: auto;
                    padding: 10px;
                    background: #f0f0f0;
                }}
            </style>
        </head>
        <body onload="initMap()">
            <div id="map"></div>
            <div id="directionsPanel"></div>
        </body>
        </html>
        '''
        return mapa_html

    def executar(self):
        """Método principal da aplicação."""
        st.sidebar.title("Login")
        usuario = st.sidebar.text_input("Usuário", value="admin")
        senha = st.sidebar.text_input("Senha", type="password", value="1234")

        if usuario == "admin" and senha == "1234":
            tabs = st.tabs(["Rota Verde", "Loja Online"])

            with tabs[0]:
                st.title("🌳 Otimizador de Rota Verde")
                origem = st.selectbox("Selecione a origem:", self.cidades)
                destino = st.selectbox("Selecione o destino:", self.cidades)
                
                if st.button("Calcular Rota"):
                    mapa_html = self.gerar_mapa(origem, destino)
                    components.html(mapa_html, height=550)

            with tabs[1]:
                st.title("🛙️ Loja Sustentável")
                carrinho = []
                total = 0
                
                for produto in self.produtos:
                    if st.button(f"Adicionar {produto['nome']}"):
                        carrinho.append(produto)
                        total += produto['preco']
                        st.success(f"{produto['nome']} adicionado ao carrinho!")

                if carrinho:
                    st.subheader("🍭 Seu Carrinho")
                    for item in carrinho:
                        st.write(f"{item['nome']} - 💲{item['preco']:.2f}")
                    st.write(f"**Total: 💲{total:.2f}**")

                    endereco = st.text_input("Endereço para entrega")
                    pagamento = st.selectbox("Forma de pagamento", ["Cartão", "Dinheiro", "Transferência Bancária"])
                    if st.button("Finalizar Pedido"):
                        produtos_nomes = ', '.join([p['nome'] for p in carrinho])
                        if self.enviar_email(produtos_nomes, total, endereco, pagamento):
                            st.success("📧 Pedido enviado com sucesso!")
                        else:
                            st.error("Erro ao enviar o pedido.")
        else:
            st.error("Credenciais incorretas")
with tabs[1]:  # Correção da posição da aba Loja Online
        st.title("🛍️ Loja Sustentável")

        # Lista de produtos
        produtos = [
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

        # Inicializar carrinho
        st.session_state.setdefault("carrinho", {})

        def adicionar_ao_carrinho(produto):
            if produto in st.session_state["carrinho"]:
                st.session_state["carrinho"][produto] += 1
            else:
                st.session_state["carrinho"][produto] = 1

        cols = st.columns(3)  # Ajusta a disposição dos produtos

        for i, produto in enumerate(produtos):
            with cols[i % 3]:
                st.image(produto["img"], caption=produto["nome"])
                st.write(f"💲 {produto['preco']:.2f}")
                if st.button(f"🛒 Adicionar {produto['nome']}", key=produto["nome"]):
                    adicionar_ao_carrinho(produto["nome"])
                    st.success(f"{produto['nome']} adicionado ao carrinho!")

        # Exibir Carrinho
        st.sidebar.title("🛒 Carrinho de Compras")
        if st.session_state["carrinho"]:
            total = 0
            for item, qtd in st.session_state["carrinho"].items():
                preco = next(p["preco"] for p in produtos if p["nome"] == item)
                subtotal = preco * qtd
                total += subtotal
                st.sidebar.write(f"{item} ({qtd}x) - 💲{subtotal:.2f}")

            st.sidebar.write(f"**Total: 💲{total:.2f}**")
            if st.sidebar.button("✅ Finalizar Pedido"):
                st.sidebar.success("Pedido realizado com sucesso! 🌱")
                st.session_state["carrinho"] = {}
        else:
            st.sidebar.write("Seu carrinho está vazio.")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Função para enviar o e-mail
def enviar_email(pedido, total):
    remetente = "seuemail@gmail.com"  # Substitua pelo seu e-mail
    senha = "suasenha"  # Use senha do app se necessário (não use senhas reais diretamente no código)
    destinatario = "seuemail@gmail.com"  # E-mail para onde o pedido será enviado

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Novo Pedido - Loja Sustentável"

    corpo_email = f"""
    Novo pedido recebido! 🛍️
    
    Produtos:
    {pedido}
    
    Total: 💲{total:.2f}
    
    Forma de pagamento: Transferência bancária / MB Way / PayPal
    Endereço de entrega: [Preencher com o endereço do cliente]

    Obrigado por sua compra! 🌱
    """

    msg.attach(MIMEText(corpo_email, "plain"))

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        return False


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Configuração do e-mail
EMAIL_REMETENTE = "seuemail@gmail.com"  # Substitua pelo seu e-mail
SENHA_EMAIL = "suasenha"  # Use uma senha de aplicativo para maior segurança
EMAIL_DESTINATARIO = "seuemail@gmail.com"  # Para onde o pedido será enviado
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587

def enviar_email(pedido, total, endereco, pagamento):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO
    msg["Subject"] = "Novo Pedido - Loja Sustentável"

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

    try:
        servidor = smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        servidor.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Inicializa o carrinho na sessão
if "carrinho" not in st.session_state:
    st.session_state["carrinho"] = {}


st.sidebar.title("🛒 Carrinho de Compras")

if st.session_state["carrinho"]:
    total = 0
    pedido = ""
    for item, qtd in st.session_state["carrinho"].items():
        preco = next(p["preco"] for p in produtos if p["nome"] == item)
        subtotal = preco * qtd
        total += subtotal
        pedido += f"{item} ({qtd}x) - 💲{subtotal:.2f}\n"

    st.sidebar.write(f"**Total: 💲{total:.2f}**")
    endereco = st.sidebar.text_input("📍 Endereço de Entrega")
    pagamento = st.sidebar.selectbox("💳 Forma de Pagamento", ["Transferência Bancária", "MB Way", "PayPal"])

    if st.sidebar.button("✅ Finalizar Pedido"):
        if endereco:
            if enviar_email(pedido, total, endereco, pagamento):
                st.sidebar.success("Pedido realizado com sucesso! Um e-mail foi enviado. 📩")
                st.session_state["carrinho"] = {}
            else:
                st.sidebar.error("❌ Erro ao enviar e-mail. Tente novamente.")
        else:
            st.sidebar.error("❌ Informe um endereço de entrega.")
else:
    st.sidebar.write("Seu carrinho está vazio.")

if __name__ == "__main__":
    app = LojaSustentavelRotaVerde()
    app.executar()
