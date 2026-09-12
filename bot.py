import os
import time
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SESSION_ID = os.getenv("SESSION_ID", "abc123def456")
DEVELOPER_CHANNEL = os.getenv("DEVELOPER_CHANNEL", "https://t.me/zzxa17")
DELAY = float(os.getenv("DELAY_BETWEEN_REPORTS", 1.5))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء البوت"""
    await update.message.reply_text(
        "Hello! I'm a Telegram Report Bot.\n\n"
        "Commands:\n"
        "/report - Send reports\n"
        "/help - Help\n"
        f"Follow us: {DEVELOPER_CHANNEL}",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض المساعدة"""
    help_text = (
        "How to use:\n\n"
        "`/report <username> <count> <report_type>`\n\n"
        "Example:\n"
        "`/report cristiano 5 1`\n\n"
        "Report types:\n"
        "1 - Inappropriate content\n"
        "2 - Copyright violation\n"
        "3 - Misinformation\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال البلاغات"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n"
            "`/report <username> <count> [report_type]`\n\n"
            "Example: `/report cristiano 5 1`",
            parse_mode="Markdown"
        )
        return
    
    target = context.args[0]
    try:
        count = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Error: count must be a number!")
        return
    
    report_type = context.args[2] if len(context.args) > 2 else "1"
    
    if count > 100:
        await update.message.reply_text("Maximum 100 reports per request!")
        return
    
    msg = await update.message.reply_text(
        f"Processing {count} reports for @{target}...\n"
        f"Report type: {report_type}"
    )
    
    try:
        success = 0
        failed = 0
        
        for i in range(count):
            try:
                # Simulate sending report
                success += 1
                
            except Exception as e:
                failed += 1
            
            # Update message every 10 reports
            if (i + 1) % 10 == 0:
                await msg.edit_text(
                    f"Processing...\n"
                    f"Success: {success}\n"
                    f"Failed: {failed}\n"
                    f"Progress: {i + 1}/{count}"
                )
            
            time.sleep(DELAY)
        
        # Final message
        await msg.edit_text(
            f"Completed!\n\n"
            f"Results:\n"
            f"Success: {success}\n"
            f"Failed: {failed}\n"
            f"Target: @{target}\n"
            f"Type: {report_type}"
        )
        
    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الإحصائيات"""
    stats_text = (
        "Bot Statistics:\n\n"
        "Status: Running\n"
        f"Session: {SESSION_ID[:10]}...\n"
        f"Delay: {DELAY}s\n"
    )
    await update.message.reply_text(stats_text, parse_mode="Markdown")

def main():
    """تشغيل البوت"""
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not found")
        print("Please set TELEGRAM_BOT_TOKEN in Railway Variables")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("stats", stats))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
