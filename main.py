import streamlit as st
import requests
import polyline
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components
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


                 components.html("
<html>
  <head>
    <title>Displaying Text Directions With setPanel()</title>
    <script>
      /**
       * @license
       * Copyright 2019 Google LLC. All Rights Reserved.
       * SPDX-License-Identifier: Apache-2.0
       */
      function initMap() {
        const directionsRenderer = new google.maps.DirectionsRenderer();
        const directionsService = new google.maps.DirectionsService();
        const map = new google.maps.Map(document.getElementById("map"), {
          zoom: 7,
          center: { lat: 41.85, lng: -87.65 },
          disableDefaultUI: true,
        });

        directionsRenderer.setMap(map);
        directionsRenderer.setPanel(document.getElementById("sidebar"));

        const control = document.getElementById("floating-panel");

        map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);

        const onChangeHandler = function () {
          calculateAndDisplayRoute(directionsService, directionsRenderer);
        };

        document
          .getElementById("start")
          .addEventListener("change", onChangeHandler);
        document
          .getElementById("end")
          .addEventListener("change", onChangeHandler);
        document
          .getElementById("mode")
          .addEventListener("change", onChangeHandler);
      }

      function calculateAndDisplayRoute(directionsService, directionsRenderer) {
        const start = document.getElementById("start").value;
        const end = document.getElementById("end").value;
        const selectedMode = document.getElementById("mode").value;

        directionsService
          .route({
            origin: start,
            destination: end,
            travelMode: google.maps.TravelMode[selectedMode],
          })
          .then((response) => {
            directionsRenderer.setDirections(response);
          })
          .catch((e) =>
            window.alert("Directions request failed due to " + status)
          );
      }

      window.initMap = initMap;
    </script>
    <style>
      /**
       * @license
       * Copyright 2019 Google LLC. All Rights Reserved.
       * SPDX-License-Identifier: Apache-2.0
       */
      /* Optional: Makes the sample page fill the window. */
      html,
      body {
        height: 100%;
        margin: 0;
        padding: 0;
      }

      #container {
        height: 100%;
        display: flex;
      }

      #sidebar {
        flex-basis: 15rem;
        flex-grow: 1;
        padding: 1rem;
        max-width: 30rem;
        height: 100%;
        box-sizing: border-box;
        overflow: auto;
      }

      #map {
        flex-basis: 0;
        flex-grow: 4;
        height: 100%;
      }

      #floating-panel {
        position: absolute;
        top: 10px;
        left: 25%;
        z-index: 5;
        background-color: #fff;
        padding: 5px;
        border: 1px solid #999;
        text-align: center;
        font-family: "Roboto", "sans-serif";
        line-height: 30px;
        padding-left: 10px;
      }

      #floating-panel {
        background-color: #fff;
        border: 0;
        border-radius: 2px;
        box-shadow: 0 1px 4px -1px rgba(0, 0, 0, 0.3);
        margin: 10px;
        padding: 0 0.5em;
        font: 400 18px Roboto, Arial, sans-serif;
        overflow: hidden;
        padding: 5px;
        font-size: 14px;
        text-align: center;
        line-height: 30px;
        height: auto;
      }

      #map {
        flex: auto;
      }

      #sidebar {
        flex: 0 1 auto;
        padding: 0;
      }
      #sidebar > div {
        padding: 0.5rem;
      }
    </style>
  </head>
  <body>
    <div id="floating-panel">
      <strong>Start:</strong>
      <select id="start">
        <option value="chicago, il">Chicago</option>
        <option value="st louis, mo">St Louis</option>
        <option value="joplin, mo">Joplin, MO</option>
        <option value="oklahoma city, ok">Oklahoma City</option>
        <option value="amarillo, tx">Amarillo</option>
        <option value="gallup, nm">Gallup, NM</option>
        <option value="flagstaff, az">Flagstaff, AZ</option>
        <option value="winona, az">Winona</option>
        <option value="kingman, az">Kingman</option>
        <option value="barstow, ca">Barstow</option>
        <option value="san bernardino, ca">San Bernardino</option>
        <option value="los angeles, ca">Los Angeles</option>
      </select>
      <br />
      <strong>End:</strong>
      <select id="end">
        <option value="chicago, il">Chicago</option>
        <option value="st louis, mo">St Louis</option>
        <option value="joplin, mo">Joplin, MO</option>
        <option value="oklahoma city, ok">Oklahoma City</option>
        <option value="amarillo, tx">Amarillo</option>
        <option value="gallup, nm">Gallup, NM</option>
        <option value="flagstaff, az">Flagstaff, AZ</option>
        <option value="winona, az">Winona</option>
        <option value="kingman, az">Kingman</option>
        <option value="barstow, ca">Barstow</option>
        <option value="san bernardino, ca">San Bernardino</option>
        <option value="los angeles, ca">Los Angeles</option>
      </select>
      <br />
      <b>Mode of Travel: </b>
      <select id="mode">
        <option value="DRIVING">Driving</option>
        <option value="WALKING">Walking</option>
        <option value="BICYCLING">Bicycling</option>
        <option value="TRANSIT">Transit</option>
      </select>
    </div>
    <div id="container">
      <div id="map"></div>
      <div id="sidebar"></div>
    </div>
    <div style="display: none">
      <div id="floating-panel">
        <strong>Start:</strong>
        <select id="start">
          <option value="chicago, il">Chicago</option>
          <option value="st louis, mo">St Louis</option>
          <option value="joplin, mo">Joplin, MO</option>
          <option value="oklahoma city, ok">Oklahoma City</option>
          <option value="amarillo, tx">Amarillo</option>
          <option value="gallup, nm">Gallup, NM</option>
          <option value="flagstaff, az">Flagstaff, AZ</option>
          <option value="winona, az">Winona</option>
          <option value="kingman, az">Kingman</option>
          <option value="barstow, ca">Barstow</option>
          <option value="san bernardino, ca">San Bernardino</option>
          <option value="los angeles, ca">Los Angeles</option>
        </select>
        <br />
        <strong>End:</strong>
        <select id="end">
          <option value="chicago, il">Chicago</option>
          <option value="st louis, mo">St Louis</option>
          <option value="joplin, mo">Joplin, MO</option>
          <option value="oklahoma city, ok">Oklahoma City</option>
          <option value="amarillo, tx">Amarillo</option>
          <option value="gallup, nm">Gallup, NM</option>
          <option value="flagstaff, az">Flagstaff, AZ</option>
          <option value="winona, az">Winona</option>
          <option value="kingman, az">Kingman</option>
          <option value="barstow, ca">Barstow</option>
          <option value="san bernardino, ca">San Bernardino</option>
          <option value="los angeles, ca">Los Angeles</option>
        </select>
      </div>
    </div>
    <script
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCYgm77s7P8Hx3ucAPqSxej4jUpko46Rn0&callback=initMap&v=weekly&solution_channel=GMP_CCS_textdirections_v2"
      defer
    ></script>
  </body>
</html>
    ")

        else:
            st.error("Credenciais incorretas")

if __name__ == "__main__":
    app = LojaSustentavelRotaVerde()
    app.executar()


#if __name__ == "__main__":
    #main()
