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
            {"nome": "Cesta Orgânica", "preco": 12.99, "img": "Horta.png"},
            {"nome": "Sabonete Natural", "preco": 7.50, "img": "soap.png"},
            {"nome": "Bolsa Ecológica", "preco": 15.00, "img": "BolsaCometico.png"},
            {"nome": "Kit Bambu", "preco": 9.99, "img": "KitBambu.png"},
            {"nome": "Mel Orgânico", "preco": 18.50, "img": "mel.png"},
            {"nome": "Horta Caseira", "preco": 25.00, "img": "Horta.jpg"},
            {"nome": "Cosméticos Naturais", "preco": 19.99, "img": "Cosmetico.png"},
            {"nome": "Chá Artesanal", "preco": 10.99, "img": "Cha.jpg"},
            {"nome": "Velas Ecológicas", "preco": 14.50, "img": "Velas.png"},
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
            🛬️ Novo pedido recebido!
            Produtos:
            {pedido}
            Total: €{total:.2f}
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
                            travelMode: google.maps.TravelMode.BICYCLING
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
                    width: 100%;
                    float: center;
                }}
                #directionsPanel {{
                    width: 100%;
                    height: 500px;
                    float: center;
                    overflow: auto;
                    
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
#float: right;  padding: 10px;
    def executar(self):
        """Método principal da aplicação."""
        st.sidebar.title("Login")
        usuario = st.sidebar.text_input("Usuário", value="admin")
        senha = st.sidebar.text_input("Senha", type="password", value="1234")

        if usuario == "admin" and senha == "1234":
            tabs = st.tabs(["Rota Verde", "Loja Online"])

            with tabs[0]:
                st.title("🌳 Percurso de ciclovia Verde")
                origem = st.selectbox("Selecione a origem:", self.cidades)
                destino = st.selectbox("Selecione o destino:", self.cidades)
                
                if st.button("Calcular Rota"):
                    mapa_html = self.gerar_mapa(origem, destino)
                    components.html(mapa_html, height=550)

            with tabs[1]:
                st.title("Loja Sustentável")
                if "carrinho" not in st.session_state:
                    st.session_state.carrinho = []
                
                cols = st.columns(3)
                for idx, produto in enumerate(self.produtos):
                    with cols[idx % 3]:
                        st.image(produto['img'], width=350)
                        st.write(f"**{produto['nome']}** - €{produto['preco']:.2f}")
                        if st.button(f"Adicionar {produto['nome']}", key=produto['nome']):
                            st.session_state.carrinho.append(produto)
                            st.success(f"{produto['nome']} adicionado ao carrinho!")

                if st.session_state.carrinho:
                    st.subheader("O Seu Carrinho")
                    total = sum(item['preco'] for item in st.session_state.carrinho)
                    for item in st.session_state.carrinho:
                        st.write(f"{item['nome']} - €{item['preco']:.2f}")
                    st.write(f"**Total: €{total:.2f}**")

                    endereco = st.text_input("Endereço para entrega")
                    pagamento = st.selectbox("Forma de pagamento", ["MBWAY","Cartão", "Dinheiro", "Transferência Bancária"])
                    if st.button("Finalizar Pedido"):
                        produtos_nomes = ', '.join([p['nome'] for p in st.session_state.carrinho])
                        if self.enviar_email(produtos_nomes, total, endereco, pagamento):
                            st.success("📧 Pedido enviado com sucesso!")
                            st.session_state.carrinho.clear()
                        else:
                            st.error("Erro ao enviar o pedido.")
        else:
            st.error("Credenciais incorretas")

if __name__ == "__main__":
    app = LojaSustentavelRotaVerde()
    app.executar()
