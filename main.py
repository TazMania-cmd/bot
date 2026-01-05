import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CONFIGURAÇÃO ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("ERRO: Configure o arquivo .env")
    exit()

logging.basicConfig(level=logging.INFO)

# --- MENU FIXO (Carrega apenas uma vez na memória) ---
# Otimização: Criamos o objeto do teclado FORA das funções para não processar repetidamente
MENU_BOTOES = [
    ["💍 Catálogo Rápido", "💰 Tabela de Preços"],
    ["💎 Lançamentos", "📦 Rastrear Pedido"],
    ["🗣 Falar com Humano", "📸 Instagram"]
]
TECLADO_FIXO = ReplyKeyboardMarkup(MENU_BOTOES, resize_keyboard=True, is_persistent=True)

# --- 1. START (A única vez que mandamos foto) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.effective_user.first_name
    
    # Usamos uma foto PEQUENA ou texto puro para carregar rápido
    # Se quiser mais rápido ainda, troque send_photo por send_message
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://cdn-icons-png.flaticon.com/512/3594/3594435.png", # Ícone leve de Joia (carrega rápido)
        caption=f"Olá, *{nome}*! 👋\n\nSou o assistente da **Cruz Joias**.\nToque nas opções abaixo para resposta imediata:",
        reply_markup=TECLADO_FIXO,
        parse_mode='Markdown'
    )

# --- 2. RESPOSTAS (Focadas em Texto = Velocidade) ---
async def responder_botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    chat_id = update.effective_chat.id

    # Otimização: Usamos send_message em vez de send_photo
    # O teclado não precisa ser enviado de novo se já é persistent=True no start,
    # mas enviamos por segurança caso o usuário tenha limpado o chat.
    
    if texto == "💍 Catálogo Rápido":
        msg = (
            "💎 **CATÁLOGO EXPRESS**\n\n"
            "1️⃣ **Corrente Grumet** - R$ 120,00\n"
            "2️⃣ **Pulseira Cartier** - R$ 90,00\n"
            "3️⃣ **Anel Solitário** - R$ 150,00\n\n"
            "Quer ver fotos reais? Acesse nosso Instagram no botão abaixo!"
        )
    
    elif texto == "💰 Tabela de Preços":
        msg = "💵 **Condições de Pagamento:**\n\n• PIX: 5% de Desconto\n• Cartão: Até 3x Sem Juros\n• Boleto: À vista"
        
    elif texto == "💎 Lançamentos":
        msg = "✨ **Acabou de chegar:**\n\nNova coleção Prata Bali. Estoque limitado!"
        
    elif texto == "📦 Rastrear Pedido":
        msg = "📦 Para rastrear, acesse: www.correios.com.br e digite seu código."
        
    elif texto == "🗣 Falar com Humano":
        msg = "👨‍💻 Clique aqui para chamar no WhatsApp: https://wa.me/5562999999999"
        
    elif texto == "📸 Instagram":
        msg = "📸 Veja as fotos no nosso perfil: https://instagram.com/cruzjoias"
        
    else:
        msg = "👇 Use o menu abaixo:"

    # Envio único e rápido
    await context.bot.send_message(chat_id=chat_id, text=msg, reply_markup=TECLADO_FIXO, parse_mode='Markdown')

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder_botoes))
    
    print("🚀 Bot OTIMIZADO Iniciado!")
    app.run_polling()