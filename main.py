import streamlit as st
import requests
import polyline
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Carregar variáveis de ambiente
load_dotenv()

class LojaSustentavelRotaVerde:
    def __init__(self):
        # Configurações de API (substitua com sua chave real)
        self.GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'AIzaSyCYgm77s7P8Hx3ucAPqSxej4jUpko46Rn0')
        self.CENTRO_AMADORA = "38.7613,-9.2351"
        
        # Configuração do Streamlit
        st.set_page_config(page_title="Loja Sustentável", page_icon="🌱", layout="wide")
        
        # Lista de produtos
        self.produtos = [
            {"nome": "Cesta Orgânica", "preco": 12.99},
            {"nome": "Sabonete Natural", "preco": 7.50},
            {"nome": "Bolsa Ecológica", "preco": 15.00}
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
            🛍️ Novo pedido recebido!
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
    
    def calcular_melhor_rota(self, origem, destino):
        """Obtém a melhor rota do Google Maps."""
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&mode=walking&key={self.GOOGLE_MAPS_API_KEY}"
        response = requests.get(url).json()
        if response['status'] == 'OK':
            rota = response['routes'][0]
            pontos = polyline.decode(rota['overview_polyline']['points'])
            return {'distancia': rota['legs'][0]['distance']['text'], 'duracao': rota['legs'][0]['duration']['text'], 'pontos': pontos}
        return None
    
    def executar(self):
        """Método principal da aplicação."""
        st.sidebar.title("Login")
        usuario = st.sidebar.text_input("Usuário", value="admin")
        senha = st.sidebar.text_input("Senha", type="password", value="1234")
        
        if usuario == "admin" and senha == "1234":
            tabs = st.tabs(["Rota Verde", "Loja Online"])
            
            with tabs[0]:
                st.title("🍃 Otimizador de Rota Verde")
                origem = st.text_input("Origem", value="Amadora, Portugal")
                destino = st.text_input("Destino", value="Queluz, Portugal")
                if st.button("Calcular Rota"):
                    rota = self.calcular_melhor_rota(origem, destino)
                    if rota:
                        st.success(f"Distância: {rota['distancia']}, Duração: {rota['duracao']}")
                    else:
                        st.error("Não foi possível calcular a rota.")
                
            with tabs[1]:
                st.title("🛍️ Loja Sustentável")
                for produto in self.produtos:
                    st.write(f"{produto['nome']} - 💲{produto['preco']:.2f}")
                    if st.button(f"Adicionar {produto['nome']}"):
                        st.success(f"{produto['nome']} adicionado ao carrinho!")

        else:
            st.error("Credenciais incorretas")

if __name__ == "__main__":
    app = LojaSustentavelRotaVerde()
    app.executar()


#if __name__ == "__main__":
    #main()
