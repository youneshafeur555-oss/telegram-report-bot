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
        "👋 مرحباً! أنا بوت TikTok Report 🤖\n\n"
        "الأوامر المتاحة:\n"
        "/report - إرسال بلاغات\n"
        "/help - المساعدة\n"
        f"💬 [تابعنا]({DEVELOPER_CHANNEL})",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض المساعدة"""
    help_text = (
        "📋 **كيفية الاستخدام:**\n\n"
        "`/report <username> <count> <report_type>`\n\n"
        "**مثال:**\n"
        "`/report cristiano 5 1`\n\n"
        "**أنواع البلاغات:**\n"
        "1️⃣ محتوى مسيء\n"
        "2️⃣ انتهاك الملكية الفكرية\n"
        "3️⃣ معلومات مضللة\n"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال البلاغات"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ الاستخدام الصحيح:\n"
            "`/report <username> <count> [report_type]`\n\n"
            "مثال: `/report cristiano 5 1`",
            parse_mode="Markdown"
        )
        return
    
    target = context.args[0]
    try:
        count = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ عدد البلاغات يجب أن يكون رقم!")
        return
    
    report_type = context.args[2] if len(context.args) > 2 else "1"
    
    if count > 100:
        await update.message.reply_text("⚠️ الحد الأقصى 100 بلاغ في المرة!")
        return
    
    msg = await update.message.reply_text(
        f"⏳ جاري إرسال {count} بلاغات لـ @{target}...\n"
        f"نوع البلاغ: {report_type}"
    )
    
    try:
        success = 0
        failed = 0
        
        for i in range(count):
            try:
                # محاكاة إرسال البلاغ
                # في الواقع، ستحتاج إلى API صحيح لـ TikTok
                response = requests.post(
                    "https://api.tiktok.com/report",
                    headers={"Authorization": f"Bearer {SESSION_ID}"},
                    json={
                        "username": target,
                        "report_type": report_type
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    success += 1
                else:
                    failed += 1
                
            except:
                failed += 1
            
            # تحديث الرسالة كل 10 بلاغات
            if (i + 1) % 10 == 0:
                await msg.edit_text(
                    f"⏳ جاري الإرسال...\n"
                    f"✅ نجح: {success}\n"
                    f"❌ فشل: {failed}\n"
                    f"📊 {i + 1}/{count}"
                )
            
            time.sleep(DELAY)
        
        # الرسالة النهائية
        await msg.edit_text(
            f"✅ انتهت العملية!\n\n"
            f"📊 النتائج:\n"
            f"✅ نجح: {success}\n"
            f"❌ فشل: {failed}\n"
            f"🎯 المستهدف: @{target}\n"
            f"📝 النوع: {report_type}"
        )
        
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ: {str(e)}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الإحصائيات"""
    stats_text = (
        "📊 **الإحصائيات:**\n\n"
        "البوت جاهز للعمل ✅\n"
        f"Session ID: `{SESSION_ID[:10]}...`\n"
        f"Delay: {DELAY}s\n"
    )
    await update.message.reply_text(stats_text, parse_mode="Markdown")

def main():
    """تشغيل البوت"""
    if not TOKEN:
        print("❌ خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN")
        print("تأكد من إضافة المتغير في Railway أو ملف .env")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("stats", stats))
    
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
