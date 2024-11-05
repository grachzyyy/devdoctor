from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.doctors import doctors
import os

async def choose_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    
    # Send doctor information with images
    for doctor_name, doctor_info in doctors.items():
        image_path = doctor_info['image']
        if os.path.exists(image_path):
            caption = f"🩺 {doctor_name}\n📋 Специализация: {doctor_info['specialization']}"
            try:
                with open(image_path, 'rb') as photo:
                    await query.message.reply_photo(
                        photo=photo,
                        caption=caption
                    )
            except Exception as e:
                print(f"Error sending photo for {doctor_name}: {e}")
    
    # Create keyboard with doctor selection buttons
    keyboard = []
    for doctor_name in doctors.keys():
        keyboard.append([InlineKeyboardButton(doctor_name, callback_data=f"doctor_{doctor_name}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выберите врача для консультации:", reply_markup=reply_markup)

async def doctor_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return
        
    await query.answer()
    
    doctor_name = query.data.replace("doctor_", "")
    if doctor_name not in doctors:
        await query.message.reply_text("Извините, произошла ошибка. Пожалуйста, попробуйте снова.")
        return
        
    # Store selected doctor in user data
    context.user_data['selected_doctor'] = doctor_name
    
    from config import CONSULTATION_PRICE, KASPI_PAYMENT_LINK
    payment_message = (
        f"Для начала чата с врачом необходимо внести 100% предоплату.\n"
        f"Стоимость онлайн консультации: {CONSULTATION_PRICE:,} тг\n\n"
        f"Если вы согласны с условиями, перейдите по ссылке для оплаты:"
    )
    
    keyboard = [
        [InlineKeyboardButton("Оплатить", url=KASPI_PAYMENT_LINK)],
        [InlineKeyboardButton("Подтвердить оплату", callback_data="confirm_payment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(payment_message, reply_markup=reply_markup)