import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import polyline
import numpy as np
import pandas as pd
import geopandas as gpd
import osmnx as ox
import networkx as nx
from shapely.geometry import Point, LineString
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Carregar variáveis de ambiente
load_dotenv()

class LojaSustentavelRotaVerde:
    def __init__(self):
        # Configurações de API (substitua com suas credenciais)
        self.GOOGLE_MAPS_API_KEY = 'AIzaSyCYgm77s7P8Hx3ucAPqSxej4jUpko46Rn0'
        
        # Coordenadas centrais de Amadora/Queluz
        self.CENTRO_AMADORA = (38.7613, -9.2351)
        
        # Configurações iniciais do Streamlit
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

    def obter_dados_ambientais(self):
        """
        Simula obtenção de dados de qualidade ambiental
        """
        zonas_verdes = [
            {"nome": "Parque Aventura", "lat": 38.7550, "lon": -9.2300, "qualidade": 0.9},
            {"nome": "Jardim Municipal", "lat": 38.7600, "lon": -9.2400, "qualidade": 0.8},
            {"nome": "Área Verde Queluz", "lat": 38.7580, "lon": -9.2450, "qualidade": 0.85}
        ]
        return pd.DataFrame(zonas_verdes)

    def calcular_melhor_rota(self, origem, destino):
        """
        Calcula rota otimizada considerando zonas verdes
        """
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&mode=walking&alternatives=true&key={self.GOOGLE_MAPS_API_KEY}"
        
        response = requests.get(url).json()
        
        if response['status'] == 'OK':
            rotas = []
            for rota in response.get('routes', []):
                pontos = polyline.decode(rota['overview_polyline']['points'])
                qualidade_rota = self.avaliar_qualidade_rota(pontos)
                
                rotas.append({
                    'distancia': rota['legs'][0]['distance']['text'],
                    'duracao': rota['legs'][0]['duration']['text'],
                    'pontos': pontos,
                    'qualidade_ambiental': qualidade_rota
                })
            
            return max(rotas, key=lambda x: x['qualidade_ambiental'])
        
        return None

    def avaliar_qualidade_rota(self, pontos):
        """
        Avalia qualidade ambiental da rota
        """
        zonas_verdes = self.obter_dados_ambientais()
        
        pontuacao_total = 0
        for lat, lon in pontos:
            for _, zona in zonas_verdes.iterrows():
                distancia = np.sqrt((lat - zona['lat'])**2 + (lon - zona['lon'])**2)
                if distancia < 0.01:
                    pontuacao_total += zona['qualidade']
        
        return pontuacao_total / len(pontos)

    def criar_mapa_interativo(self, rota):
        """Cria mapa interativo com rota otimizada"""
        m = folium.Map(location=self.CENTRO_AMADORA, zoom_start=13)
        
        # Adiciona pontos de zonas verdes
        zonas_verdes = self.obter_dados_ambientais()
        for _, zona in zonas_verdes.iterrows():
            folium.CircleMarker(
                location=[zona['lat'], zona['lon']],
                radius=5,
                popup=zona['nome'],
                color='green',
                fill=True,
                fillColor='green'
            ).add_to(m)
        
        # Adiciona rota
        if rota:
            folium.PolyLine(
                locations=rota['pontos'], 
                color='blue', 
                weight=5, 
                opacity=0.8
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
            tabs = st.tabs(["Rota Verde", "Loja Online"])

            with tabs[0]:
                st.title("🍃 Otimizador de Rota Verde")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    origem = st.text_input("Origem", value="Amadora, Portugal")
                
                with col2:
                    destino = st.text_input("Destino", value="Queluz, Portugal")
                
                if st.button("Calcular Melhor Rota Verde"):
                    with st.spinner('Calculando rota otimizada...'):
                        rota = self.calcular_melhor_rota(origem, destino)
                        
                        if rota:
                            st.success(f"Rota encontrada!")
                            st.write(f"Distância: {rota['distancia']}")
                            st.write(f"Duração: {rota['duracao']}")
                            st.write(f"Qualidade Ambiental: {rota['qualidade_ambiental']:.2%}")
                            
                            # Mapa interativo
                            mapa = self.criar_mapa_interativo(rota)
                            st_folium(mapa, width=700)
                        else:
                            st.error("Não foi possível calcular a rota.")

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
    app = LojaSustentavelRotaVerde()
    app.executar()

if __name__ == "__main__":
    main()
