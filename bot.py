import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# लॉगिंग सेटअप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# बॉट टोकन
TOKEN = "8134315902:AAF6HECYvlvQPpxKgigrsbKY6BV3NLSijNI"

# स्टडी मटेरियल कैटेगरी
categories = {
    "papers": "पुराने पेपर",
    "notes": "अध्ययन नोट्स",
    "help": "अध्ययन सहायता",
    "doubts": "संदेह समाधान"
}

# स्टार्ट कमांड हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"नमस्ते {user.first_name}! मैं स्टडी हेल्पर बॉट हूँ। मैं आपको परीक्षा के पुराने पेपर, अध्ययन नोट्स और अन्य सहायता प्रदान कर सकता हूँ।\n\n"
        f"कृपया नीचे दिए गए विकल्पों में से चुनें:"
    )
    await show_categories(update, context)

# कैटेगरी दिखाने का फंक्शन
async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    row = []
    for i, (cat_id, cat_name) in enumerate(categories.items()):
        row.append(InlineKeyboardButton(cat_name, callback_data=f"category_{cat_id}"))
        if (i + 1) % 2 == 0 or i == len(categories) - 1:
            keyboard.append(row)
            row = []
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_text("कृपया एक श्रेणी चुनें:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("कृपया एक श्रेणी चुनें:", reply_markup=reply_markup)

# कैटेगरी हैंडलर
async def category_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    category = query.data.split("_")[1]
    
    if category == "papers":
        keyboard = [
            [InlineKeyboardButton("कक्षा 10", callback_data="papers_10")],
            [InlineKeyboardButton("कक्षा 12", callback_data="papers_12")],
            [InlineKeyboardButton("वापस जाएँ", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("किस कक्षा के पुराने पेपर चाहिए?", reply_markup=reply_markup)
    
    elif category == "notes":
        keyboard = [
            [InlineKeyboardButton("गणित", callback_data="notes_math")],
            [InlineKeyboardButton("विज्ञान", callback_data="notes_science")],
            [InlineKeyboardButton("अंग्रेजी", callback_data="notes_english")],
            [InlineKeyboardButton("वापस जाएँ", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("किस विषय के नोट्स चाहिए?", reply_markup=reply_markup)
    
    elif category == "help":
        keyboard = [
            [InlineKeyboardButton("होमवर्क सहायता", callback_data="help_homework")],
            [InlineKeyboardButton("परीक्षा तैयारी", callback_data="help_exam")],
            [InlineKeyboardButton("वापस जाएँ", callback_data="back_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("किस प्रकार की सहायता चाहिए?", reply_markup=reply_markup)
    
    elif category == "doubts":
        await query.edit_message_text(
            "अपना संदेह या प्रश्न टेक्स्ट के रूप में भेजें। हमारे शिक्षक जल्द ही आपके प्रश्न का उत्तर देंगे।\n\n"
            "वापस मुख्य मेनू पर जाने के लिए /start टाइप करें।"
        )

# सबकैटेगरी हैंडलर
async def subcategory_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split("_")
    category = data[0]
    subcategory = data[1]
    
    if category == "back":
        await show_categories(update, context)
        return
    
    # यहां आप फाइल भेजने का कोड जोड़ सकते हैं
    # उदाहरण के लिए:
    if category == "papers":
        await query.edit_message_text(
            f"कक्षा {subcategory} के पुराने पेपर यहां उपलब्ध होंगे।\n\n"
            "अभी यह सुविधा विकास के अधीन है। जल्द ही फाइल्स अपलोड की जाएंगी।\n\n"
            "वापस मुख्य मेनू पर जाने के लिए /start टाइप करें।"
        )
    elif category == "notes":
        subjects = {
            "math": "गणित",
            "science": "विज्ञान",
            "english": "अंग्रेजी"
        }
        await query.edit_message_text(
            f"{subjects[subcategory]} के नोट्स यहां उपलब्ध होंगे।\n\n"
            "अभी यह सुविधा विकास के अधीन है। जल्द ही नोट्स अपलोड किए जाएंगे।\n\n"
            "वापस मुख्य मेनू पर जाने के लिए /start टाइप करें।"
        )
    elif category == "help":
        help_types = {
            "homework": "होमवर्क सहायता",
            "exam": "परीक्षा तैयारी"
        }
        await query.edit_message_text(
            f"{help_types[subcategory]} के लिए यहां मार्गदर्शन उपलब्ध होगा।\n\n"
            "अभी यह सुविधा विकास के अधीन है। जल्द ही सामग्री अपलोड की जाएगी।\n\n"
            "वापस मुख्य मेनू पर जाने के लिए /start टाइप करें।"
        )

# फाइल अपलोड हैंडलर
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # यहां आप अपलोड की गई फाइलों को संभाल सकते हैं
    # उदाहरण के लिए, एडमिन्स द्वारा अपलोड की गई फाइलों को स्टोर करना
    document = update.message.document
    await update.message.reply_text(
        f"फाइल '{document.file_name}' प्राप्त हुई। धन्यवाद!\n\n"
        "यह फाइल हमारे डेटाबेस में संग्रहित की जाएगी और छात्रों के लिए उपलब्ध होगी।"
    )

# टेक्स्ट मैसेज हैंडलर
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(
        f"आपका संदेश प्राप्त हुआ: '{text}'\n\n"
        "हमारे शिक्षक जल्द ही आपके संदेश का जवाब देंगे।\n\n"
        "अन्य विकल्पों के लिए /start टाइप करें।"
    )

# मुख्य फंक्शन
def main():
    # बॉट एप्लिकेशन बनाएँ
    application = ApplicationBuilder().token(TOKEN).build()
    
    # कमांड हैंडलर्स जोड़ें
    application.add_handler(CommandHandler("start", start))
    
    # कॉलबैक क्वेरी हैंडलर्स
    application.add_handler(CallbackQueryHandler(category_handler, pattern=r"^category_"))
    application.add_handler(CallbackQueryHandler(subcategory_handler, pattern=r"^(papers|notes|help)_"))
    application.add_handler(CallbackQueryHandler(show_categories, pattern=r"^back_"))
    
    # डॉक्यूमेंट हैंडलर
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_document))
    
    # टेक्स्ट मैसेज हैंडलर
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # बॉट शुरू करें
    print("बॉट शुरू हो गया है...")
    application.run_polling()

if __name__ == "__main__":
    main()