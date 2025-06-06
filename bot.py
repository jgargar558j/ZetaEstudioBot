# bot.py
# Este es un bot de Discord que permite a los usuarios registrarse enviando su nombre y apellido.
import random
import string
import discord
import os

TOKEN = os.getenv("TOKEN")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", "0").strip().replace("=", "")
ADMIN_USER_ID = int(ADMIN_USER_ID)
DOMAIN = os.getenv("DOMAIN")

intents = discord.Intents.default()
intents.message_content = True 
intents.dm_messages = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().strip() == "!registrar":
        await message.channel.send("¡Vamos a registrarte! Escribe tu nombre:")

        def check(m): return m.author == message.author and m.channel == message.channel
        nombre_msg = await client.wait_for("message", check=check)
        nombre_msg.content = nombre_msg.content.lower().replace(" ", "")
        nombre = nombre_msg.content.strip()

        await message.channel.send("Ahora escribe tu apellido:")
        apellido_msg = await client.wait_for("message", check=check)
        apellido_msg.content = apellido_msg.content.lower().replace(" ", "")
        apellido = apellido_msg.content.strip()

        admin_user = await client.fetch_user(ADMIN_USER_ID)

        await admin_user.send(f"🔔 Nueva solicitud de correo:\nNombre: {nombre}\nApellido: {apellido}\nCuenta: {generate_email(nombre, apellido)}\nContraseña: {generate_password()}\nUsuario: {message.author}")

        await message.channel.send("✅ ¡Solicitud enviada correctamente! Un administrador te contactará pronto.")

def generate_password(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation 
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def generate_email(nombre, apellido):
    nombre_filtrado = nombre[:5] 
    apellido_filtrado = apellido[:3] 

    email = f"{nombre_filtrado}.{apellido_filtrado}.{DOMAIN}"
    return email.lower().replace(" ", "")

client.run(TOKEN)
