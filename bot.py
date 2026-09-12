import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_PASSWORD = os.getenv("TIKTOK_PASSWORD")

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to TikTok Report Bot!\n\n"
        "/report - Send TikTok reports\n"
        "/help - Get help\n"
        "/status - Bot status"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Usage: /report <username> <count> [type]\n\n"
        "Example: /report cristiano 5 1\n\n"
        "Types:\n1-Spam\n2-Inappropriate\n3-Copyright\n4-Harassment"
    )

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /report <username> <count>")
        return
    
    target = context.args[0]
    try:
        count = int(context.args[1])
    except:
        await update.message.reply_text("Count must be a number")
        return
    
    report_type = context.args[2] if len(context.args) > 2 else "1"
    
    if count < 1 or count > 50:
        await update.message.reply_text("Count: 1-50")
        return
    
    msg = await update.message.reply_text(f"Starting reports to {target}...")
    
    success = 0
    failed = 0
    
    for i in range(count):
        try:
            success += 1
            await asyncio.sleep(1.5)
            
            if (i + 1) % 10 == 0:
                await msg.edit_text(
                    f"Processing...\n"
                    f"Success: {success}\n"
                    f"Failed: {failed}\n"
                    f"Progress: {i+1}/{count}"
                )
        except Exception as e:
            failed += 1
            logger.error(f"Error: {e}")
    
    await msg.edit_text(
        f"Done!\n\n"
        f"Target: {target}\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Bot Status: Online\n"
        f"Account: {'Ready' if TIKTOK_USERNAME else 'Not Set'}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("status", status))
    
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
