TITLE, DESCRIPTION, DATE, TIME, NOTES = range(5)
CHOOSE_EVENT, CHOOSE_FIELD, UPDATE_FIELD = range(5, 8)
CHOOSE_EVENT_TO_DELETE = 8
CHOOSE_EVENT_FOR_MINUTES, ENTER_MINUTES = range(9, 11)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import ConversationHandler, MessageHandler, filters
from db import add_event
from db import init_db
from db import get_events
from db import get_events_with_ids, update_event_field
from db import delete_event
from db import add_or_update_user
from db import get_user_profile, get_upcoming_events


TOKEN = "7660174882:AAE1OvnclaOEhkvCEF7baPDokG0hoCYh-eU"  # Replace with your Bot token from BotFather

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_or_update_user(user.id, user.username or "unknown")
    
    await update.message.reply_text(
        "👋 Hello! I'm your Event Calendar Bot.\n\nUse /addevent to add a new event!"
    )



async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    profile_data, event_count = get_user_profile(user.id)
    events = get_upcoming_events(user.id)

    if profile_data:
        username, last_login = profile_data
        text = (
            f"👤 Profile Info:\n"
            f"Username: {username or 'N/A'}\n"
            f"Last Login: {last_login or 'N/A'}\n"
            f"Total Events: {event_count}\n\n"
        )

        if events:
            text += "📅 Upcoming Events:\n"
            for i, (title, date, time) in enumerate(events, 1):
                text += f"{i}. {title} - {date} at {time}\n"
        else:
            text += "📭 No upcoming events."
    else:
        text = "⚠️ You are not registered yet. Send /start to initialize your profile."

    await update.message.reply_text(text)



async def addevent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 What's the title of the event?")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['title'] = update.message.text
    await update.message.reply_text("✏️ Description?")
    return DESCRIPTION

async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['description'] = update.message.text
    await update.message.reply_text("📅 Date? (YYYY-MM-DD)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text
    await update.message.reply_text("⏰ Time? (HH:MM in 24hr)")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text
    await update.message.reply_text("📝 Any notes?")
    return NOTES

async def get_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['notes'] = update.message.text
    user = update.effective_user

    # Save to DB
    add_event(
        user.id,
        context.user_data['title'],
        context.user_data['description'],
        context.user_data['date'],
        context.user_data['time'],
        context.user_data['notes'],
    )

    await update.message.reply_text("✅ Event saved!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Event creation cancelled.")
    return ConversationHandler.END



   
async def viewevents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    events = get_events(user.id)
    
    if not events:
        await update.message.reply_text("📭 You have no upcoming events.")
        return
    
    msg = "📅 Your upcoming events:\n\n"
    for i, (title, description, date, time, notes) in enumerate(events, 1):
        msg += (f"{i}. *{title}*\n"
                f"   Description: {description}\n"
                f"   Date: {date} Time: {time}\n"
                f"   Notes: {notes}\n\n")
    
    await update.message.reply_text(msg, parse_mode="Markdown")
   
   
   

async def editevent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    events = get_events_with_ids(user.id)
    
    if not events:
        await update.message.reply_text("📭 You have no events to edit.")
        return ConversationHandler.END

    context.user_data['events'] = events
    msg = "📝 Choose an event to edit:\n\n"
    for i, event in enumerate(events, 1):
        msg += f"{i}. {event[1]} ({event[3]} {event[4]})\n"
    
    await update.message.reply_text(msg)
    return CHOOSE_EVENT

async def choose_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        index = int(update.message.text.strip()) - 1
        selected = context.user_data['events'][index]
        context.user_data['event_id'] = selected[0]
        await update.message.reply_text(
            "Which field do you want to edit? (title / description / date / time / notes)"
        )
        return CHOOSE_FIELD
    except:
        await update.message.reply_text("⚠️ Invalid selection. Please enter a number.")
        return CHOOSE_EVENT

async def choose_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    field = update.message.text.strip().lower()
    valid_fields = ["title", "description", "date", "time", "notes"]
    if field not in valid_fields:
        await update.message.reply_text("⚠️ Invalid field. Please choose from: title, description, date, time, notes.")
        return CHOOSE_FIELD
    
    context.user_data['field'] = field
    await update.message.reply_text(f"Enter new value for {field}:")
    return UPDATE_FIELD

async def update_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_value = update.message.text
    event_id = context.user_data['event_id']
    field = context.user_data['field']
    
    update_event_field(event_id, field, new_value)
    await update.message.reply_text("✅ Event updated successfully!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END



async def deleteevent_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    events = get_events_with_ids(user.id)

    if not events:
        await update.message.reply_text("📭 You have no events to delete.")
        return ConversationHandler.END

    context.user_data['events'] = events
    msg = "🗑️ Choose an event to delete:\n\n"
    for i, event in enumerate(events, 1):
        msg += f"{i}. {event[1]} ({event[3]} {event[4]})\n"
    
    await update.message.reply_text(msg)
    return CHOOSE_EVENT_TO_DELETE

async def delete_selected_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        index = int(update.message.text.strip()) - 1
        selected = context.user_data['events'][index]
        event_id = selected[0]
        delete_event(event_id)
        await update.message.reply_text("✅ Event deleted successfully.")
        return ConversationHandler.END
    except:
        await update.message.reply_text("⚠️ Invalid selection. Please enter a number.")
        return CHOOSE_EVENT_TO_DELETE



async def logminutes_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    events = get_events_with_ids(user.id)

    if not events:
        await update.message.reply_text("📭 You have no events to log minutes for.")
        return ConversationHandler.END

    context.user_data['events'] = events
    msg = "📝 Choose an event to log minutes for:\n\n"
    for i, event in enumerate(events, 1):
        msg += f"{i}. {event[1]} ({event[3]} {event[4]})\n"
    
    await update.message.reply_text(msg)
    return CHOOSE_EVENT_FOR_MINUTES

async def choose_event_for_minutes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        index = int(update.message.text.strip()) - 1
        selected = context.user_data['events'][index]
        context.user_data['event_id'] = selected[0]
        await update.message.reply_text("🗒️ Please type the meeting minutes you want to log:")
        return ENTER_MINUTES
    except:
        await update.message.reply_text("⚠️ Invalid selection. Please enter a number.")
        return CHOOSE_EVENT_FOR_MINUTES

async def enter_minutes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notes = update.message.text
    event_id = context.user_data['event_id']
    
    update_event_field(event_id, "notes", notes)
    await update.message.reply_text("✅ Minutes of meeting saved successfully.")
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Available Commands:\n"
        "/start - Start the bot\n"
        "/addevent - Add a new event\n"
        "/editevent - Edit an event\n"
        "/deleteevent - Delete an event\n"
        "/viewevents - View your events\n"
        "/logminutes - Log minutes for a meeting\n"
        "/profile - View your profile and upcoming events\n"
        "/help - Show this help message"
    )






def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile))




    addevent_handler = ConversationHandler(
    entry_points=[CommandHandler("addevent", addevent_start)],
    states={
        TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_title)],
        DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_description)],
        DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
        TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        NOTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_notes)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(addevent_handler)


    app.add_handler(CommandHandler("viewevents", viewevents))
    edit_event_handler = ConversationHandler(
    entry_points=[CommandHandler("editevent", editevent_start)],
    states={
        CHOOSE_EVENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_event)],
        CHOOSE_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_field)],
        UPDATE_FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_field)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(edit_event_handler)
    
    delete_event_handler = ConversationHandler(
    entry_points=[CommandHandler("deleteevent", deleteevent_start)],
    states={
        CHOOSE_EVENT_TO_DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_selected_event)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(delete_event_handler)


    log_minutes_handler = ConversationHandler(
    entry_points=[CommandHandler("logminutes", logminutes_start)],
    states={
        CHOOSE_EVENT_FOR_MINUTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_event_for_minutes)],
        ENTER_MINUTES: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_minutes)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(log_minutes_handler)




    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
