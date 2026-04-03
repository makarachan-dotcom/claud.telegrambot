//! AI MAKARAAIIII Telegram Bot
//!
//! Bot identity: AI STAND WY2.5
//! Primary language: Khmer (ភាសាខ្មែរ)
//! Secondary language: English

use std::collections::HashMap;
use std::env;
use std::sync::Arc;
use teloxide::{
    payloads::SendMessageSetters,
    prelude::*,
    types::{ChatId, InlineKeyboardButton, InlineKeyboardMarkup, MessageId, ParseMode},
};

const BOT_IDENTITY: &str = "AI STAND WY2.5";
const BOT_NAME: &str = "AI MAKARAAIIII";

// Callback data constants
const CB_NO_SPAM: &str = "no_spam";
const CB_ABOUT: &str = "about";
const CB_HELP: &str = "help";
const CB_LANGUAGE: &str = "language";

/// Shared state for tracking per-user last bot message IDs (for deletion).
#[derive(Clone, Default)]
struct BotState {
    /// Map of `chat_id` -> last bot message id that can be deleted
    last_bot_messages: Arc<tokio::sync::Mutex<HashMap<i64, MessageId>>>,
}

/// Build the main interactive inline keyboard with Khmer labels.
fn main_keyboard() -> InlineKeyboardMarkup {
    InlineKeyboardMarkup::new(vec![
        vec![
            InlineKeyboardButton::callback("🚫 មិនរញេរញៃ (Button 1 - លុប)", CB_NO_SPAM),
            InlineKeyboardButton::callback("🤖 អំពី AI", CB_ABOUT),
        ],
        vec![
            InlineKeyboardButton::callback("❓ ជំនួយ / Help", CB_HELP),
            InlineKeyboardButton::callback("🌐 ភាសា / Language", CB_LANGUAGE),
        ],
    ])
}

/// Format the greeting message in Khmer with cool HTML styling.
fn greeting_message() -> String {
    format!(
        "🌟 <b>សួស្ដី! ខ្ញុំជា {BOT_NAME}</b> 🌟\n\
         ════════════════════\n\
         🤖 <b>អត្តសញ្ញាណ:</b> <code>{BOT_IDENTITY}</code>\n\
         🇰🇭 <b>ភាសា:</b> ខ្មែរ (ចម្បង) · English (បន្ថែម)\n\
         ════════════════════\n\
         ✨ ខ្ញុំត្រៀមខ្លួនជួយអ្នករួចហើយ!\n\
         💬 សូមវាយអ្វីមួយ ហើយខ្ញុំនឹងឆ្លើយតប...\n\
         ════════════════════\n\
         <i>Powered by {BOT_IDENTITY}</i>"
    )
}

/// Generate an AI-style response to the user's message.
fn generate_ai_response(user_text: &str) -> String {
    let lower = user_text.to_lowercase();

    if lower.contains("hello") || lower.contains("hi") || lower.contains("សួស្ដី") {
        format!(
            "🤖 <b>{BOT_IDENTITY}</b> នៅទីនេះ!\n\
             ════════════════════\n\
             👋 សួស្ដី! ខ្ញុំរីករាយណាស់ដែលបានឮពីអ្នក.\n\
             Hello! I'm happy to hear from you.\n\
             ════════════════════\n\
             💬 អ្នកចង់និយាយអំពីអ្វី? / What would you like to talk about?"
        )
    } else if lower.contains("ឈ្មោះ")
        || lower.contains("name")
        || lower.contains("អ្នកជានរណា")
        || lower.contains("who are you")
    {
        format!(
            "🤖 <b>{BOT_IDENTITY}</b>\n\
             ════════════════════\n\
             🌟 ខ្ញុំឈ្មោះ <b>{BOT_NAME}</b>\n\
             🧠 ខ្ញុំជា AI ដ៏ឆ្លាតវៃ\n\
             🇰🇭 ខ្ញុំនិយាយភាសាខ្មែរ និង English\n\
             ════════════════════\n\
             I am <b>{BOT_NAME}</b>, an intelligent AI assistant\n\
             powered by {BOT_IDENTITY}."
        )
    } else if lower.contains("អរគុណ") || lower.contains("thank") || lower.contains("thanks")
    {
        format!(
            "🤖 <b>{BOT_IDENTITY}</b>\n\
             ════════════════════\n\
             🙏 អរគុណដែរ! សូមឱ្យជោគជ័យ!\n\
             You're welcome! Have a great day! 😊\n\
             ════════════════════\n\
             💬 តើមានអ្វីទៀតដែលខ្ញុំអាចជួយ?"
        )
    } else if lower.contains("bye") || lower.contains("លា") || lower.contains("លាហើយ")
    {
        format!(
            "🤖 <b>{BOT_IDENTITY}</b>\n\
             ════════════════════\n\
             👋 លាហើយ! សូមមានសុខភាពល្អ!\n\
             Goodbye! Take care and stay safe! 🌟\n\
             ════════════════════\n\
             <i>វានឹងរង់ចាំអ្នក... / I'll be waiting for you...</i>"
        )
    } else if lower.contains("help") || lower.contains("ជំនួយ") || lower.contains("ជួយ")
    {
        format!(
            "🤖 <b>{BOT_IDENTITY}</b> - ជំនួយ / Help\n\
             ════════════════════\n\
             📋 <b>ពាក្យបញ្ជា / Commands:</b>\n\
             • /start - ចាប់ផ្ដើម / Start\n\
             • /help - ជំនួយ / Help\n\
             • /about - អំពីខ្ញុំ / About me\n\
             ════════════════════\n\
             💬 អ្នកអាចនិយាយជាភាសាខ្មែរ ឬ English\n\
             You can chat in Khmer or English!"
        )
    } else {
        // Generic intelligent response — HTML-escape user text to prevent injection
        let safe_text = user_text
            .replace('&', "&amp;")
            .replace('<', "&lt;")
            .replace('>', "&gt;");
        format!(
            "🤖 <b>{BOT_IDENTITY}</b>\n\
             ════════════════════\n\
             💭 ខ្ញុំបានទទួលសារ: <i>\"{safe_text}\"</i>\n\
             \n\
             🧠 ការវិភាគ: ខ្ញុំយល់ពីសំណើរបស់អ្នក។\n\
             ════════════════════\n\
             ✨ ខ្ញុំ <b>{BOT_NAME}</b> - AI ឆ្លាតវៃ\n\
             I understand your message and I'm here to help!\n\
             \n\
             💬 <i>សូមបន្តសន្ទនា... / Please continue the conversation...</i>"
        )
    }
}

#[tokio::main]
async fn main() {
    pretty_env_logger::init();

    let token = env::var("TELEGRAM_BOT_TOKEN")
        .expect("TELEGRAM_BOT_TOKEN environment variable must be set");
    let bot = Bot::new(token);
    let state = BotState::default();

    log::info!("Starting {BOT_NAME} ({BOT_IDENTITY})...");

    let handler = dptree::entry()
        .branch(Update::filter_message().endpoint(handle_message))
        .branch(Update::filter_callback_query().endpoint(handle_callback));

    Dispatcher::builder(bot, handler)
        .dependencies(dptree::deps![state])
        .enable_ctrlc_handler()
        .build()
        .dispatch()
        .await;
}

/// Handle incoming text messages.
async fn handle_message(bot: Bot, msg: Message, state: BotState) -> ResponseResult<()> {
    let chat_id = msg.chat.id;

    if let Some(text) = msg.text() {
        if text == "/start" {
            handle_start(&bot, chat_id, &state).await?;
        } else if text == "/help" {
            let response = generate_ai_response("help");
            send_tracked_message(&bot, chat_id, &response, Some(main_keyboard()), &state).await?;
        } else if text == "/about" {
            let about = format!(
                "🤖 <b>{BOT_NAME}</b>\n\
                 ════════════════════\n\
                 🌟 <b>{BOT_IDENTITY}</b>\n\
                 🇰🇭 ភាសាខ្មែរ (ចម្បង) + English (បន្ថែម)\n\
                 ════════════════════\n\
                 <i>Built with love in Rust</i>"
            );
            send_tracked_message(&bot, chat_id, &about, Some(main_keyboard()), &state).await?;
        } else {
            let response = generate_ai_response(text);
            send_tracked_message(&bot, chat_id, &response, Some(main_keyboard()), &state).await?;
        }
    }

    Ok(())
}

/// Handle /start command: send greeting with keyboard.
async fn handle_start(bot: &Bot, chat_id: ChatId, state: &BotState) -> ResponseResult<()> {
    let greeting = greeting_message();
    send_tracked_message(bot, chat_id, &greeting, Some(main_keyboard()), state).await
}

/// Send a message and track its ID for potential future deletion.
async fn send_tracked_message(
    bot: &Bot,
    chat_id: ChatId,
    text: &str,
    keyboard: Option<InlineKeyboardMarkup>,
    state: &BotState,
) -> ResponseResult<()> {
    let mut req = bot.send_message(chat_id, text).parse_mode(ParseMode::Html);

    if let Some(kb) = keyboard {
        req = req.reply_markup(kb);
    }

    let sent = req.await?;

    // Store this message ID so it can be deleted when the user presses Button 1
    let mut map = state.last_bot_messages.lock().await;
    map.insert(chat_id.0, sent.id);

    Ok(())
}

/// Handle inline keyboard button presses.
async fn handle_callback(bot: Bot, query: CallbackQuery, state: BotState) -> ResponseResult<()> {
    let Some(data) = query.data.as_deref() else {
        return Ok(());
    };

    let chat_id = if let Some(msg) = &query.message {
        msg.chat.id
    } else {
        bot.answer_callback_query(&query.id).await?;
        return Ok(());
    };

    match data {
        CB_NO_SPAM => {
            // Button 1: "មិនរញេរញៃ" — delete the last tracked bot message (no spam/redundancy)
            bot.answer_callback_query(&query.id)
                .text("🚫 លុបសារហើយ! / Message deleted!")
                .await?;

            let msg_id = {
                let map = state.last_bot_messages.lock().await;
                map.get(&chat_id.0).copied()
            };

            if let Some(id) = msg_id {
                let _ = bot.delete_message(chat_id, id).await;
                let mut map = state.last_bot_messages.lock().await;
                map.remove(&chat_id.0);
            }

            // Brief clean acknowledgement
            let ack = format!(
                "✅ <b>{BOT_NAME}</b>\n\
                 🚫 <i>មិនរញេរញៃ — សារត្រូវបានលុបរួចហើយ!</i>\n\
                 <i>(No spam — message has been removed!)</i>"
            );
            bot.send_message(chat_id, ack)
                .parse_mode(ParseMode::Html)
                .await?;
        }

        CB_ABOUT => {
            bot.answer_callback_query(&query.id).await?;
            let about = format!(
                "🤖 <b>{BOT_NAME}</b>\n\
                 ════════════════════\n\
                 🌟 Identity: <b>{BOT_IDENTITY}</b>\n\
                 🇰🇭 ភាសា: ខ្មែរ + English\n\
                 🦀 Built with Rust\n\
                 ════════════════════\n\
                 <i>AI ឆ្លាតវៃ ជួយអ្នករាល់ថ្ងៃ!</i>"
            );
            send_tracked_message(&bot, chat_id, &about, Some(main_keyboard()), &state).await?;
        }

        CB_HELP => {
            bot.answer_callback_query(&query.id).await?;
            let help = generate_ai_response("help");
            send_tracked_message(&bot, chat_id, &help, Some(main_keyboard()), &state).await?;
        }

        CB_LANGUAGE => {
            bot.answer_callback_query(&query.id).await?;
            let lang_msg = format!(
                "🌐 <b>{BOT_NAME}</b> — ភាសា / Language\n\
                 ════════════════════\n\
                 🇰🇭 <b>ខ្មែរ</b> (ចម្បង / Primary)\n\
                 🇬🇧 <b>English</b> (បន្ថែម / Secondary)\n\
                 ════════════════════\n\
                 💬 អ្នកអាចសរសេរភាសាណាក៏បាន!\n\
                 You can write in any language!"
            );
            send_tracked_message(&bot, chat_id, &lang_msg, Some(main_keyboard()), &state).await?;
        }

        _ => {
            bot.answer_callback_query(&query.id).await?;
        }
    }

    Ok(())
}
