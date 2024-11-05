from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    welcome_message = (
        "👋 Добро пожаловать в Doctor Chat!\n\n"
        "Здесь вы сможете начать чат со специалистом и получить онлайн консультацию врача.\n\n"
        "Не стесняйтесь спрашивать - наши доктора отвечают на любые вопросы "
        "и никогда не нарушают врачебную тайну."
    )
    
    keyboard = [[InlineKeyboardButton("Выбрать врача", callback_data="choose_doctor")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)