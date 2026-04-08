use reqwest::blocking::Client;
use serde_json::json;
use std::thread;
use std::time::Duration;

pub fn execute_discord_webhook(webhook_url: Option<String>, content: String) {
    let Some(webhook_url) = webhook_url.filter(|url| !url.is_empty()) else {
        return;
    };

    thread::spawn(move || {
        let client = Client::builder()
            .timeout(Duration::from_millis(5000))
            .build()
            .unwrap();

        let payload = json!({
            "content": content,
            "username": "yulesxoxo",
            "avatar_url": "https://raw.githubusercontent.com/yulesxoxo/AdbBot/refs/heads/main/app-icon.png",
        });

        let _ = client.post(&webhook_url).json(&payload).send();
    });
}
