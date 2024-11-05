from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import REVIEW_CHANNEL, DISCOUNT_PERCENTAGE, DISCOUNT_VALIDITY_MONTHS

async def end_consultation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    
    end_message = (
        "Спасибо за использование Doctor Chat!\n\n"
        f"🌟 Поделитесь своим опытом в нашем канале отзывов.\n"
        f"💎 Получите скидку {DISCOUNT_PERCENTAGE}% на следующую консультацию "
        f"(действительна {DISCOUNT_VALIDITY_MONTHS} месяца)!"
    )
    
    keyboard = [[InlineKeyboardButton("Оставить отзыв", url=REVIEW_CHANNEL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(end_message, reply_markup=reply_markup)
    
    # Clear user data
    context.user_data.clear()