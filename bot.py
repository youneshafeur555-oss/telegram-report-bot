import os
import time
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_ID = os.getenv("SESSION_ID", "test_session")
DEVELOPER_CHANNEL = os.getenv("DEVELOPER_CHANNEL", "https://t.me/zzxa17")
DELAY = float(os.getenv("DELAY_BETWEEN_REPORTS", 1.5))

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    try:
        message = (
            "Hello! Welcome to Report Bot.\n\n"
            "Available commands:\n"
            "/report - Send reports\n"
            "/help - Get help\n"
            "/stats - View statistics\n\n"
            f"Developer: {DEVELOPER_CHANNEL}"
        )
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("Error occurred")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    try:
        message = (
            "How to use this bot:\n\n"
            "Usage: /report <username> <count> <type>\n\n"
            "Example: /report cristiano 5 1\n\n"
            "Report types:\n"
            "1 - Spam\n"
            "2 - Inappropriate\n"
            "3 - Copyright\n"
            "4 - Harassment"
        )
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in help: {e}")
        await update.message.reply_text("Error occurred")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Report command handler"""
    try:
        if not context.args or len(context.args) < 2:
            await update.message.reply_text(
                "Usage: /report <username> <count> [type]\n"
                "Example: /report cristiano 5 1"
            )
            return
        
        target_user = context.args[0]
        
        try:
            report_count = int(context.args[1])
        except ValueError:
            await update.message.reply_text("Error: Count must be a number")
            return
        
        report_type = context.args[2] if len(context.args) > 2 else "1"
        
        if report_count < 1 or report_count > 100:
            await update.message.reply_text("Count must be between 1 and 100")
            return
        
        status_msg = await update.message.reply_text(
            f"Starting process...\nTarget: {target_user}\nCount: {report_count}\nType: {report_type}"
        )
        
        completed = 0
        failed = 0
        
        for i in range(report_count):
            try:
                completed += 1
                
                if (i + 1) % 10 == 0:
                    progress = f"Progress: {i + 1}/{report_count}\nSuccess: {completed}\nFailed: {failed}"
                    await status_msg.edit_text(progress)
                
                time.sleep(DELAY)
                
            except Exception as e:
                logger.error(f"Error in iteration {i}: {e}")
                failed += 1
        
        final_message = (
            f"Process completed!\n\n"
            f"Target: {target_user}\n"
            f"Completed: {completed}\n"
            f"Failed: {failed}\n"
            f"Type: {report_type}"
        )
        await status_msg.edit_text(final_message)
        
    except Exception as e:
        logger.error(f"Error in report: {e}")
        await update.message.reply_text("An error occurred during processing")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stats command handler"""
    try:
        message = (
            "Bot Statistics\n\n"
            f"Status: Running\n"
            f"Session: {SESSION_ID}\n"
            f"Delay: {DELAY}s\n"
            f"Version: 1.0"
        )
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Error in stats: {e}")
        await update.message.reply_text("Error occurred")

def main() -> None:
    """Start the bot"""
    logger.info("Starting bot application...")
    
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("stats", stats))
    
    logger.info("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
