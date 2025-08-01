# 🤖 Discord Bot – Mehrsprachig (Deutsch / English)

Ein vielseitiger Discord-Bot mit nützlichen Moderationstools, Nutzer- und Serverinfos, Verifizierungssystem, Aktivitätssteuerung und mehr!

A powerful, multi-purpose Discord bot including moderation tools, user/server info commands, a verification system, activity management, and more.

---

## 📌 Funktionen / Features

### 🇩🇪 Deutsch
- 👋 **Willkommensnachricht**: Sendet automatisch eine Nachricht, wenn ein neuer User den Server betritt.
- 👋 **Verlassen-Nachricht**: Informiert den Server, wenn ein User geht.
- ✅ **Verifizierungssystem**: Mitglieder können sich mit einem Button verifizieren.
- 📊 **Verify Panel & Liste**: Admins können den Verifizierungsstatus und verifizierte Nutzer einsehen oder zurücksetzen.
- 👤 **/userinfo**: Zeigt Profilinformationen eines Benutzers.
- 🏠 **/serverinfo**: Zeigt ausführliche Infos zum Server.
- 📢 **/update**: Admins können Updates posten (mit Titel, Text & optionalem Bild).
- 🔨 **/ban** & 👢 **/kick**: Bannt oder kickt Benutzer (mit Grund).
- 💣 **/nuke**: Löscht und erstellt den aktuellen Channel neu.
- 🆘 **/help**: Zeigt eine Liste aller Admin-Befehle.
- 🎮 **/set_activity**: Setzt die Aktivität des Bots (Spielt, Hört zu, Schaut, Kämpft).
- 🔐 **Admin-Only Zugriff**: Viele Befehle sind nur für Administratoren zugänglich.
- 🚫 **Wortfilter**: Verhindert unerwünschte Wörter in Aktivitäten.

---

### 🇬🇧 English
- 👋 **Welcome Message**: Sends an embedded welcome message when a new member joins.
- 👋 **Leave Message**: Notifies when a member leaves the server.
- ✅ **Verification System**: Users can verify themselves via a button.
- 📊 **Verify Panel & List**: Admins can view or reset the verification list.
- 👤 **/userinfo**: Displays detailed info about any user.
- 🏠 **/serverinfo**: Detailed info about the server.
- 📢 **/update**: Post updates with a title, message, and optional image.
- 🔨 **/ban** & 👢 **/kick**: Ban or kick users (with a reason).
- 💣 **/nuke**: Deletes and recreates the current channel.
- 🆘 **/help**: Lists all available admin commands.
- 🎮 **/set_activity**: Sets the bot's activity (Playing, Watching, Listening, Competing).
- 🔐 **Admin-Only Access**: Many commands are admin-restricted.
- 🚫 **Word Filter**: Prevents forbidden words in activities.

---

## ⚙️ Setup

1. Lege deine Konfigurationsdatei `config.py` an mit z. B.:

```python
guild_id = 1234567890
welcome_channel_id = 1234567890
verlassen_channel_id = 1234567890
VERIFY_ROLE_ID = 1234567890
VERIFY_TEXT = "Bitte klicke unten auf den Button, um dich zu verifizieren."
WELCOME_TEXT = "Willkommen auf unserem Server!"
FORBIDDEN_WORDS = ["badword1", "badword2"]






MFG DeadPool 

