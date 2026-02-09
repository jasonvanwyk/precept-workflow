# Deploying Precept Telegram Bot

Target: dev server (10.0.10.21, user: jason)

## Prerequisites

1. **Create bot** via @BotFather on Telegram -- copy the bot token
2. **Get your Telegram user ID** -- message `@userinfobot` on Telegram
3. **Get an OpenAI API key** -- https://platform.openai.com/api-keys

## 1. Clone repo and set up venv

```bash
cd ~/Projects
git clone git@github.com:jasonvanwyk/precept-workflow.git  # if not already cloned
cd precept-workflow/src/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Create env file

```bash
mkdir -p ~/.config/precept
cat > ~/.config/precept/telegram-bot.env << 'EOF'
TELEGRAM_BOT_TOKEN=your-bot-token-here
OPENAI_API_KEY=sk-your-openai-key-here
ALLOWED_USER_ID=your-telegram-user-id
EOF
chmod 600 ~/.config/precept/telegram-bot.env
```

## 3. Test manually

```bash
source venv/bin/activate
export $(cat ~/.config/precept/telegram-bot.env | xargs)
python bot.py
```

Send `/start` from Telegram to verify it works, then Ctrl+C.

## 4. Install systemd user service

```bash
mkdir -p ~/.config/systemd/user
cp deploy/precept-bot.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable precept-bot.service
systemctl --user start precept-bot.service
```

## 5. Enable lingering (boot startup without login)

```bash
sudo loginctl enable-linger jason
```

## 6. Check status

```bash
systemctl --user status precept-bot.service
journalctl --user -u precept-bot.service -f
```
