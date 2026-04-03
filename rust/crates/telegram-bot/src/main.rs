use std::env;

use teloxide::{
    payloads::SendMessageSetters,
    prelude::*,
    types::{InlineKeyboardButton, InlineKeyboardMarkup, Me, ParseMode},
};

const BOT_NAME: &str = "AI MAKARAAIIII";
const BOT_IDENTITY: &str = "AI STAND WY2.5";

/// Build the main interactive inline keyboard shown with greetings.
fn main_keyboard() -> InlineKeyboardMarkup {
    InlineKeyboardMarkup::new(vec![
        vec![
            InlineKeyboardButton::callback("🔕 មិនរញេរញៃ (Button 1 – លុបសារ)", "btn_no_noise"),
            InlineKeyboardButton::callback("🤖 ជជែកជាមួយ AI", "btn_chat"),
        ],
        vec![
            InlineKeyboardButton::callback("🇰🇭 ភាសាខ្មែរ", "btn_khmer"),
            InlineKeyboardButton::callback("🇬🇧 English", "btn_english"),
        ],
    ])
}

/// Khmer greeting text sent when the bot starts.
fn greeting_text(name: &str) -> String {
    format!(
        "🌟 *សួស្ដី {name}!* 🌟\n\
        \n\
        ខ្ញុំជា *{BOT_NAME}* — ជំនួយការ AI ។\n\
        \n\
        🤖 អត្តសញ្ញាណ: *{BOT_IDENTITY}*\n\
        \n\
        ✨ ខ្ញុំអាចជួយអ្នក:\n\
        • 💬 ឆ្លើយសំណួររបស់អ្នក (ខ្មែរ ឬ English)\n\
        • 📝 ជួយសរសេរ ឬពន្យល់\n\
        • 🧠 ផ្ដល់ព័ត៌មានចំណេះដឹង\n\
        \n\
        👇 *ជ្រើសរើសជម្រើស ឬសរសេរសួរខ្ញុំបានតែម្ដង!*"
    )
}

/// Generate an AI-style response to a user's message.
fn ai_response(user_text: &str, use_khmer: bool) -> String {
    if use_khmer {
        format!(
            "🤖 *{BOT_IDENTITY}* ឆ្លើយ:\n\
            \n\
            អ្នកបានសួរថា: _{user_text}_\n\
            \n\
            ខ្ញុំបានទទួល ហើយកំពុងគិត... 💭\n\
            \n\
            📌 *ចម្លើយ:*\n\
            យោងតាមការសួររបស់អ្នក «{user_text}», ខ្ញុំស្នើថា:\n\
            អ្នកអាចស្វែងយល់ ឬពន្យល់][បន្ថែមអំពីប្រធានបទនេះ។ \
            ប្រើ /help ដើម្បីមើលសិទ្ធិ]\n\
            \n\
            — *{BOT_NAME}* 🌟"
        )
    } else {
        format!(
            "🤖 *{BOT_IDENTITY}* responds:\n\
            \n\
            You asked: _{user_text}_\n\
            \n\
            I received your message and I'm thinking... 💭\n\
            \n\
            📌 *Answer:*\n\
            Based on your question \"{user_text}\", I suggest exploring \
            this topic further. Use /help to see available commands.\n\
            \n\
            — *{BOT_NAME}* 🌟"
        )
    }
}

/// Detect whether a message appears to be in Khmer script.
fn is_khmer(text: &str) -> bool {
    text.chars().any(|c| ('\u{1780}'..='\u{17FF}').contains(&c))
}

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    log::info!("Starting {BOT_NAME} ({BOT_IDENTITY})…");

    let token = env::var("TELEGRAM_BOT_TOKEN")
        .expect("TELEGRAM_BOT_TOKEN environment variable must be set");

    let bot = Bot::new(token);

    let handler = dptree::entry()
        .branch(Update::filter_message().endpoint(handle_message))
        .branch(Update::filter_callback_query().endpoint(handle_callback));

    Dispatcher::builder(bot, handler)
        .enable_ctrlc_handler()
        .build()
        .dispatch()
        .await;
}

/// Handle all plain text / command messages.
async fn handle_message(bot: Bot, msg: Message, me: Me) -> ResponseResult<()> {
    let chat_id = msg.chat.id;

    let Some(text) = msg.text() else {
        return Ok(());
    };

    match text {
        t if t == "/start" || t.contains(me.username()) => {
            let first_name = msg.from().map_or("អ្នកប្រើប្រាស់", |u| {
                u.first_name.as_str()
            });

            bot.send_message(chat_id, greeting_text(first_name))
                .parse_mode(ParseMode::MarkdownV2)
                .reply_markup(main_keyboard())
                .await?;
        }

        "/help" => {
            let help_text = format!(
                "📖 *ជំនួយ / Help*\n\
                \n\
                🇰🇭 *ខ្មែរ:*\n\
                • /start — ចាប់ផ្ដើមជា​មួយ {BOT_NAME}\n\
                • /help — មើលបញ្ជីពាក្យបញ្ជា\n\
                • /about — ព័ត៌មានអំពី bot\n\
                • សរសេរអ្វីក៏បាន — AI នឹងឆ្លើយ\n\
                \n\
                🇬🇧 *English:*\n\
                • /start — Begin with {BOT_NAME}\n\
                • /help — Show commands\n\
                • /about — Bot information\n\
                • Type anything — AI will respond\n\
                \n\
                — *{BOT_IDENTITY}* 🤖",
            );
            bot.send_message(chat_id, help_text)
                .parse_mode(ParseMode::MarkdownV2)
                .await?;
        }

        "/about" => {
            let about_text = format!(
                "ℹ️ *អំពី / About*\n\
                \n\
                🤖 ឈ្មោះ Bot: *{BOT_NAME}*\n\
                🧠 AI: *{BOT_IDENTITY}*\n\
                🇰🇭 ភាសា: ខ្មែរ \\(ចម្បង\\) \\+ English\n\
                ⚡ ស្ថានភាព: Online 24/7\n\
                \n\
                _Built with ❤️ using Rust \\+ Teloxide_",
            );
            bot.send_message(chat_id, about_text)
                .parse_mode(ParseMode::MarkdownV2)
                .await?;
        }

        user_text => {
            let use_khmer = is_khmer(user_text);
            let response = ai_response(user_text, use_khmer);
            bot.send_message(chat_id, response)
                .parse_mode(ParseMode::MarkdownV2)
                .reply_markup(main_keyboard())
                .await?;
        }
    }

    Ok(())
}

/// Handle inline keyboard callback queries.
async fn handle_callback(bot: Bot, q: CallbackQuery) -> ResponseResult<()> {
    let Some(data) = q.data.as_deref() else {
        bot.answer_callback_query(&q.id).await?;
        return Ok(());
    };

    match data {
        // Button 1 – "មិនរញេរញៃ": delete the original message and acknowledge
        "btn_no_noise" => {
            bot.answer_callback_query(&q.id)
                .text("✅ លុបរួចហើយ! មិនរញេរញៃទេ 🔕")
                .await?;

            if let Some(msg) = &q.message {
                let _ = bot.delete_message(msg.chat.id, msg.id).await;
            }
        }

        // "ជជែកជាមួយ AI" – prompt the user to send a message
        "btn_chat" => {
            bot.answer_callback_query(&q.id).await?;

            if let Some(msg) = &q.message {
                bot.send_message(
                    msg.chat.id,
                    "💬 *សរសេរសំណួររបស់អ្នក!*\n\
                    ខ្ញុំជា *AI STAND WY2\\.5* — សូមសួរ\\!",
                )
                .parse_mode(ParseMode::MarkdownV2)
                .await?;
            }
        }

        // Language buttons – acknowledge with a short notice
        "btn_khmer" => {
            bot.answer_callback_query(&q.id)
                .text("🇰🇭 ភាសាខ្មែរត្រូវបានជ្រើសរើស!")
                .await?;
        }

        "btn_english" => {
            bot.answer_callback_query(&q.id)
                .text("🇬🇧 English selected!")
                .await?;
        }

        _ => {
            bot.answer_callback_query(&q.id).await?;
        }
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_khmer_detects_khmer_script() {
        assert!(is_khmer("សួស្ដី"));
        assert!(is_khmer("hello សួស្ដី"));
        assert!(!is_khmer("hello world"));
        assert!(!is_khmer(""));
    }

    #[test]
    fn test_greeting_text_contains_bot_name() {
        let text = greeting_text("Test");
        assert!(text.contains(BOT_NAME));
        assert!(text.contains(BOT_IDENTITY));
        assert!(text.contains("Test"));
    }

    #[test]
    fn test_ai_response_khmer() {
        let resp = ai_response("សួស្ដី", true);
        assert!(resp.contains(BOT_IDENTITY));
        assert!(resp.contains("សួស្ដី"));
    }

    #[test]
    fn test_ai_response_english() {
        let resp = ai_response("hello", false);
        assert!(resp.contains(BOT_IDENTITY));
        assert!(resp.contains("hello"));
    }

    #[test]
    fn test_main_keyboard_has_four_buttons() {
        let kb = main_keyboard();
        let total: usize = kb.inline_keyboard.iter().map(|row| row.len()).sum();
        assert_eq!(total, 4);
    }
}
