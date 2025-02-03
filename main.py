import streamlit as st
import folium
from streamlit_folium import st_folium
import networkx as nx
import osmnx as ox
import time

# Configuração do layout
tabs = st.tabs(["Mapa", "Loja Online"])

# Simulação de login
st.sidebar.title("Login")
usuario = st.sidebar.text_input("Usuário", value="admin")
senha = st.sidebar.text_input("Senha", type="password", value="1234", key="password")

if usuario == "admin" and senha == "1234":
    with tabs[0]:
        st.title("🚴 Otimizador de Percurso - GPS Ativo")

        st.html("
<html>
  <head>
    <title>Maps and Places Autocomplete</title>
    <script>
      async function init() {
        await customElements.whenDefined('gmp-map');

        const map = document.querySelector('gmp-map');
        const marker = document.querySelector('gmp-advanced-marker');
        const placePicker = document.querySelector('gmpx-place-picker');
        const infowindow = new google.maps.InfoWindow();

        map.innerMap.setOptions({
          mapTypeControl: false
        });

        placePicker.addEventListener('gmpx-placechange', () => {
          const place = placePicker.value;

          if (!place.location) {
            window.alert(
              "No details available for input: '" + place.name + "'"
            );
            infowindow.close();
            marker.position = null;
            return;
          }

          if (place.viewport) {
            map.innerMap.fitBounds(place.viewport);
          } else {
            map.center = place.location;
            map.zoom = 17;
          }

          marker.position = place.location;
          infowindow.setContent(
            `<strong>${place.displayName}</strong><br>
             <span>${place.formattedAddress}</span>
          `);
          infowindow.open(map.innerMap, marker);
        });
      }

      document.addEventListener('DOMContentLoaded', init);
    </script>
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/@googlemaps/extended-component-library/0.6.11/index.min.js">
    </script>
    <style>
      html,
      body {
        height: 100%;
        margin: 0;
        padding: 0;
      }

      .place-picker-container {
        padding: 20px;
      }
    </style>
  </head>
  <body>
    <gmpx-api-loader key="AIzaSyCYgm77s7P8Hx3ucAPqSxej4jUpko46Rn0" solution-channel="GMP_GE_mapsandplacesautocomplete_v2">
    </gmpx-api-loader>
    <gmp-map center="40.749933,-73.98633" zoom="13" map-id="DEMO_MAP_ID">
      <div slot="control-block-start-inline-start" class="place-picker-container">
        <gmpx-place-picker placeholder="Enter an address"></gmpx-place-picker>
      </div>
      <gmp-advanced-marker></gmp-advanced-marker>
    </gmp-map>
  </body>
</html>")

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


#else:
    #st.sidebar.error("❌ Credenciais incorretas")
