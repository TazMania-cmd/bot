import logging
import os
from dotenv import load_dotenv # Biblioteca para ler o arquivo .env
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# --- CONFIGURAÇÃO ---
load_dotenv()  # Carrega as variáveis do arquivo .env
TOKEN = os.getenv('TELEGRAM_TOKEN')  

if not TOKEN:
    print("Erro: Token do Telegram não encontrado. Verifique o arquivo .env.")
    exit()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- 1. FUNÇÃO QUE MOSTRA O MENU (/start) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.effective_user.first_name
    
    # Definindo os botões (Lista de Listas)
    # Cada lista interna [] é uma LINHA de botões
    teclado = [
        [
            InlineKeyboardButton("💍 Ver Catálogo", callback_data='btn_catalogo'),
            InlineKeyboardButton("💰 Preços", callback_data='btn_precos')
        ],
        [
            InlineKeyboardButton("🗣 Falar com Humano", callback_data='btn_suporte')
        ],
        [
            # Botão de URL (abre o navegador direto, não precisa de callback_data)
            InlineKeyboardButton("📸 Seguir no Instagram", url='https://instagram.com/seuperfil')
        ]
    ]
    
    # Transforma a lista num Objeto de Markup
    reply_markup = InlineKeyboardMarkup(teclado)
    
    texto_inicial = f"Olá, {nome}! Bem-vindo à **Cruz Joias**.\nSelecione uma opção abaixo:"
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=texto_inicial, 
        reply_markup=reply_markup
    )

# --- 2. FUNÇÃO QUE TRATA O CLIQUE NO BOTÃO ---
async def tratar_clique(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pega o evento do clique
    query = update.callback_query
    
    # Avisa o Telegram que o clique foi recebido (para parar a bolinha de "a carregar")
    await query.answer()
    
    # Verifica qual botão foi apertado pelo ID (callback_data)
    dado = query.data
    
    if dado == 'btn_catalogo':
        # Edita a mensagem anterior para mostrar o resultado
        await query.edit_message_text(
            text="💎 **Catálogo Prata 925**\n\n1. Corrente Grumet - R$ 120\n2. Pingente Cruz - R$ 89\n3. Anel Solitário - R$ 150\n\nEscolha outra opção se desejar:",
            # Podemos colocar um botão de "Voltar" aqui se quiser
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar ao Início", callback_data='btn_voltar')]])
        )
        
    elif dado == 'btn_precos':
        await query.edit_message_text(
            text="💵 Aceitamos PIX com 5% de desconto ou Cartão em até 3x sem juros.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='btn_voltar')]])
        )

    elif dado == 'btn_suporte':
        await query.edit_message_text(text="Um dos nossos atendentes vai entrar em contacto consigo em breve. Aguarde...")

    elif dado == 'btn_voltar':
        # Chama a função start de novo para mostrar o menu principal
        await start(update, context)

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Adiciona o comando /start
    application.add_handler(CommandHandler('start', start))
    
    # Adiciona o Gerente de Cliques (CallbackQueryHandler)
    # Ele vai pegar QUALQUER clique em botão inline
    application.add_handler(CallbackQueryHandler(tratar_clique))
    
    print("🤖 Bot com Menu Inline Iniciado!")
    application.run_polling()