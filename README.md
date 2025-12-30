# 🚀 Ultimate Server Cloner v2

**Ultimate Server Cloner** is a powerful Python-based tool that allows you to **clone entire Discord servers**, including all settings, roles, channels, messages, emojis, and stickers. It features an interactive terminal interface and advanced cloning capabilities.

⚠️ **Disclaimer**: This tool uses a user token and is intended for educational and administrative purposes **only**. Misuse of account tokens may result in a ban from Discord.

---

## 🧠 Features

- Clone **all roles**, **channels**, **categories**, and **server settings** from a source server to a target server.
- **Full Message Cloning** with two modes:
  - **Realistic Mode**: Uses webhooks to preserve original author usernames and avatars
  - **Classic Mode**: Direct message posting under your account
- Clone **emojis** and **stickers** with full preservation.
- Clone **server icon** and basic server settings.
- **Mass Clone**: Clone one server to multiple targets simultaneously.
- **Export Server Config**: Save server structure as JSON.
- Delete all existing roles/channels in the target server before cloning (Fresh Setup mode).
- Token validation and login feedback.
- Smart rate limiting (3 requests/second) to prevent API throttling.
- Interactive menu with 7 different options.

---

## 🛠 Requirements

- Python 3.11+
- A Discord user account **with admin permissions on the target server** where channels will be created.
- Required Python packages:
  - `discord.py`
  - `requests`

### 📦 Install Dependencies

```bash
pip install -U discord.py requests
```

---

## ⚙️ How to Use

1. **Run the script**:

```bash
python server_cloner.py
```

2. **Select an option** from the main menu (1-7).
3. **Enter your Discord account token** when prompted.
4. **Follow the on-screen prompts** for your chosen operation.
5. Sit back and watch the cloning process in action.

---

## 📋 Menu Options

```
[1] Clone Server (Full Replication)
[2] Clone Server with Messages
[3] Mass Clone (Multiple Targets)
[4] Steal Emojis & Stickers
[5] Export Server Settings
[6] Join Support Server
[7] Exit
```

### Option Details

**[1] Clone Server (Full Replication)**
- Validates your token
- Clones all roles, channels, and categories
- Option to clone messages with realistic or classic mode
- Automatically clones emojis and stickers

**[2] Clone Server with Messages**
- Focuses on message preservation
- Customizable message limit per channel
- Choice of realistic or classic message mode

**[3] Mass Clone**
- Clone one source server to multiple targets
- Comma-separated target server IDs

**[4] Steal Emojis & Stickers**
- Clone emojis and stickers independently
- Preserves animated emoji support

**[5] Export Server Settings**
- Exports server config as JSON file
- Includes roles, channels, and metadata

**[6] Join Support Server**
- Opens support Discord server in your browser

**[7] Exit**
- Safely closes the application

---

## 🧪 Example

```
> Select option: 1
> [TOKEN] Enter your Discord token: ****
> [VALIDATION] Checking token...
> [SUCCESS] Logged in as: username
> [SOURCE] Enter source server ID: 123456789
> [TARGET] Enter target server ID: 987654321
> [SETUP MODE] Fresh Setup or Keep Existing? 1
> [MESSAGE MODE] Realistic or Classic? 1
> [COMPLETE] Full server clone completed successfully!
```

---

## ❗ Important Notes

- The script uses your **Discord user token**, which can be risky. Use at your own discretion.
- The account **must** have admin permissions on the target server where channels will be created.
- This tool respects Discord rate limits and implements smart throttling.
- Large servers may take considerable time to clone.
- Some server settings may require specific permissions to modify.
- Avoid using this script on accounts that you cannot afford to lose.

---

## 🔒 Security

- Keep your Discord token **private** and never share it.
- Store tokens in environment variables for better security.
- Only use this tool on servers you **own** or have **explicit permission** to manage.

---

## 🐛 Troubleshooting

**"Invalid Token" Error**
- Verify your Discord token is correct
- Token may have been rotated; update it

**"Access Denied" Error**
- Confirm you have admin permissions on the target server
- Check bot permissions in server settings

**"Rate Limited" Message**
- Normal during bulk operations
- Tool automatically handles rate limiting
- Process will resume after delay

**Message Cloning Fails**
- Check channel history permissions
- Verify channels aren't access-restricted

**Emoji/Sticker Issues**
- Ensure target server has available slots
- Check Discord size/format requirements

---

## 📜 License

MIT License – Free to use and modify.

---

## 🔗 Community

Join the community Discord server here:  
👉 [https://discord.gg/zhM6BwFrEv](https://discord.gg/zhM6BwFrEv)

---

## 👨‍💻 Developer

Made with ❤️ by **zle0o**

---

Like this Cloner? Leave a ⭐ on GitHub!
