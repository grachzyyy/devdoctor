from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.doctors import doctors

async def confirm_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    
    if 'selected_doctor' not in context.user_data:
        await query.message.reply_text("Извините, произошла ошибка. Пожалуйста, начните сначала.")
        return
    
    doctor_name = context.user_data['selected_doctor']
    if doctor_name not in doctors:
        await query.message.reply_text("Извините, произошла ошибка. Пожалуйста, начните сначала.")
        return
    
    success_message = (
        "✅ Ваш платеж успешно совершен!\n\n"
        "❗️Формат консультации:\n"
        "Получение ответа в реальном времени (скорость ответа в течении от минуты до 2-х часов) "
        "в порядке «онлайн живая очередь» с учетом часового времени вашего врача.\n\n"
        "Пожалуйста, сформируйте свой консультационный вопрос и отправьте ваши данные "
        "(анализы, описание состояния, снимки исследований и т.д.)"
    )
    
    doctor_link = doctors[doctor_name]['chat_link']
    keyboard = [
        [InlineKeyboardButton("Перейти к консультации", url=doctor_link)],
        [InlineKeyboardButton("Завершить консультацию", callback_data="end_consultation")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(success_message, reply_markup=reply_markup)