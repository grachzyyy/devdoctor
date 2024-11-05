import asyncio
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TOKEN
from handlers.start import start_command
from handlers.doctor_selection import choose_doctor, doctor_selected
from handlers.payment import confirm_payment
from handlers.consultation import end_consultation

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    try:
        # Initialize bot
        application = Application.builder().token(TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(choose_doctor, pattern="^choose_doctor$"))
        application.add_handler(CallbackQueryHandler(doctor_selected, pattern="^doctor_"))
        application.add_handler(CallbackQueryHandler(confirm_payment, pattern="^confirm_payment$"))
        application.add_handler(CallbackQueryHandler(end_consultation, pattern="^end_consultation$"))
        
        # Start bot
        await application.initialize()
        await application.start()
        await application.run_polling()
        
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())