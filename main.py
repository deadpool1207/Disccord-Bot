############ alle import ############
import discord
from discord import app_commands
from discord.ext import commands
import config
from datetime import datetime, UTC


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


################## Bot Events ##################
@bot.event
async def on_ready():
    guild = discord.Object(id=config.guild_id)
    await bot.tree.sync(guild=guild)  
    print(f"Eingeloggt als {bot.user} (ID: {bot.user.id}) seit {bot.launch_time}")
    print("Slash Commands wurden für den Server synchronisiert.")



################### Discord API ##################
@bot.event
async def on_connect():
    bot.launch_time = datetime.now(UTC)
    print("Verbindung zur Discord API hergestellt.")


################## Welcome Message ##################
@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(config.welcome_channel_id)
    if channel is None:
        print("Willkommens-Channel nicht gefunden.")
        return
    

    if member.bot:
        print(f"Bot {member.name} ist dem Server beigetreten. Keine Nachricht gesendet.")
        return

    embed = discord.Embed(
        title=f"{member.mention}",
        description=config.WELCOME_TEXT,
        color=discord.Color.blue()
    )
    embed.set_footer(text="Community-Team")
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    await channel.send(embed=embed)



################### verlassen Message ##################
@bot.event
async def on_member_remove(member: discord.Member):
    channel = bot.get_channel(config.verlassen_channel_id)
    if channel is None:
        print("Verlassen Channel nicht gefunden.")
        return
    
    if member.bot:
        print(f"Bot {member.name} hat den Server verlassen. Keine Nachricht gesendet.")
        return

    embed = discord.Embed(
        title="Auf Wiedersehen!",
        description=f"{member.mention} hat den Server verlassen. Wir werden dich vermissen! 😢",
        color=discord.Color.red()
    )
    embed.set_footer(text="Community-Team")
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    await channel.send(embed=embed)

###################### Verify System ##################

   
verified_users = set()                

class VerifyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="✅ Verifizieren", style=discord.ButtonStyle.success)

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        role = interaction.guild.get_role(config.VERIFY_ROLE_ID)

        if not role:
            return await interaction.response.send_message("❌ Verify-Rolle nicht gefunden!", ephemeral=True)

        if role in member.roles:
            return await interaction.response.send_message("🔓 Du bist bereits verifiziert.", ephemeral=True)

        await member.add_roles(role)
        verified_users.add(member.id)
        await interaction.response.send_message("✅ Du bist jetzt verifiziert!", ephemeral=True)


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(VerifyButton())

@bot.tree.command(name="verify_setup", description="Sendet das Verifizierungs-Panel", guild=discord.Object(id=config.guild_id))
async def verify_setup(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "Du hast nicht die Berechtigung, administrator",
                ephemeral=True
            )
            return
        embed = discord.Embed(
            title="🔐 Verifizierung",
            description=config.VERIFY_TEXT,
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=VerifyView())


@bot.tree.command(name="verify_panel", description="Zeigt Admin-Panel für Verifizierungsstatus", guild=discord.Object(id=config.guild_id))
async def verify_panel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, administrator",
            ephemeral=True
        )
        return
    embed = discord.Embed(
        title="📊 Verify Panel",
        description="Status des Verifizierungssystems",
        color=discord.Color.blue()
    )
    embed.add_field(name="✅ Verifizierte Nutzer", value=str(len(verified_users)))
    embed.set_footer(text=f"Letzter Zugriff: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="verify_list", description="Liste aller verifizierten Nutzer", guild=discord.Object(id=config.guild_id))
async def verify_list(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, administrator",
            ephemeral=True
        )
        return
    if not verified_users:
        return await interaction.response.send_message("Noch keine verifizierten User.", ephemeral=True)

    lines = []
    for uid in verified_users:
        try:
            user = await bot.fetch_user(uid)
            lines.append(f"• {user.name}#{user.discriminator} (`{uid}`)")
        except:
            lines.append(f"• Unbekannt (`{uid}`)")

    message = "\n".join(lines)
    await interaction.response.send_message(f"👥 Verifizierte Nutzer:\n{message[:1900]}", ephemeral=True)


@bot.tree.command(name="verify_reset", description="Resetet alle verifizierten Nutzer (Admin)", guild=discord.Object(id=config.guild_id))
async def verify_reset(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, administrator",
            ephemeral=True
        )
        return
    verified_users.clear()
    await interaction.response.send_message("🔄 Alle verifizierten Nutzer wurden zurückgesetzt.", ephemeral=True)



###################### user info Command ##################
@bot.tree.command(name="userinfo", description="Zeigt Informationen über einen Benutzer an.", guild=discord.Object(id=config.guild_id))
@app_commands.describe(user="Der Benutzer, über den Informationen angezeigt werden sollen")
async def userinfo(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user

    member = interaction.guild.get_member(user.id) if interaction.guild else None

    embed = discord.Embed(
        title=f"Informationen über {user.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
    embed.add_field(name="Bot", value="Ja" if user.bot else "Nein", inline=True)
    embed.add_field(name="Erstellt am", value=user.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)

    if member:
        status = str(member.status).capitalize() if hasattr(member, 'status') else "Unbekannt"
        activity = str(member.activity) if member.activity else "Keine Aktivität"
    else:
        status = "Unbekannt"
        activity = "Keine Aktivität"
    embed.add_field(name="Status", value=status, inline=True)
    embed.add_field(name="Aktivität", value=activity, inline=True)

    mutual_guilds = user.mutual_guilds if hasattr(user, "mutual_guilds") else []
    embed.add_field(name="Gemeinsame Server", value=len(mutual_guilds), inline=True)

    embed.add_field(name="Avatar URL", value=user.avatar.url if user.avatar else "Kein Avatar", inline=True)

    banner_url = user.banner.url if user.banner else "Kein Banner"
    embed.add_field(name="Banner URL", value=banner_url, inline=True)

    nickname = member.nick if member and member.nick else "Kein Nickname"
    embed.add_field(name="Nickname", value=nickname, inline=True)

    if member:
        roles = [role.mention for role in member.roles[1:]]  
        roles_str = ", ".join(roles) if roles else "Keine Rollen"
    else:
        roles_str = "Keine Rollen"
    embed.add_field(name="Rollen", value=roles_str, inline=True)

    if member and member.joined_at:
        embed.add_field(name="Beigetreten am", value=member.joined_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    else:
        embed.add_field(name="Beigetreten am", value="Unbekannt", inline=False)

    embed.set_footer(text=f"Angefordert von {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

    await interaction.response.send_message(embed=embed)



###################### Server Info Command ##################


@bot.tree.command(name="serverinfo", description="Zeigt ausführliche Informationen über den Server an.", guild=discord.Object(id=config.guild_id))
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("Dieser Befehl kann nur in einem Server verwendet werden.", ephemeral=True)
        return

    static_emojis = len([e for e in guild.emojis if not e.animated])
    animated_emojis = len([e for e in guild.emojis if e.animated])

    rules_channel = None
    try:
        rules_channel = guild.rules_channel
    except:
        pass

    embed = discord.Embed(
        title=f"Ausführliche Informationen zum Server: {guild.name}",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)

    embed.add_field(name="Server-ID", value=guild.id, inline=True)
    embed.add_field(name="Erstellt am", value=guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Owner", value=f"{guild.owner} ({guild.owner_id})", inline=True)

    embed.add_field(name="Mitglieder gesamt", value=guild.member_count, inline=True)

    embed.add_field(name="Boost-Level", value=guild.premium_tier, inline=True)
    embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)

    embed.add_field(name="Textkanäle", value=len(guild.text_channels), inline=True)
    embed.add_field(name="Sprachkanäle", value=len(guild.voice_channels), inline=True)
    embed.add_field(name="Kategorien", value=len(guild.categories), inline=True)
    embed.add_field(name="Rollen", value=len(guild.roles), inline=True)

    embed.add_field(name="Statische Emojis", value=static_emojis, inline=True)
    embed.add_field(name="Animierte Emojis", value=animated_emojis, inline=True)

    embed.add_field(name="Vanity URL", value=guild.vanity_url_code if guild.vanity_url_code else "Keine Vanity URL", inline=True)

    embed.add_field(name="Regeln", value=f"Hier: {rules_channel.mention}" if rules_channel else "Keine Regeln definiert", inline=True)

    if guild.banner:
        embed.set_image(url=guild.banner.url)

    embed.set_footer(text=f"Angefordert von {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

    await interaction.response.send_message(embed=embed)



###################### update Commands ######################
@bot.tree.command(name="update", description="Sende ein Update mit Titel, Inhalt und optionalem Bild.", guild=discord.Object(id=config.guild_id))
@app_commands.describe(
    title="Titel des Updates",
    inhalt="Inhalt oder Beschreibung",
    bild="Link zu einem Bild (optional)"
)
async def update_command(interaction: discord.Interaction, title: str, inhalt: str, bild: str = None):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="⛔ Keine Berechtigung",
            description="Du brauchst die Administrator-Berechtigung, um diesen Befehl zu nutzen.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    embed = discord.Embed(title=title, description=inhalt, color=0x3498db)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

    if bild:
        embed.set_image(url=bild)

    await interaction.response.send_message(embed=embed)

####################### Ban Command ######################
@bot.tree.command(name="ban", description="Banne einen Benutzer.", guild=discord.Object(id=config.guild_id))
@app_commands.describe(
    user="Der Benutzer, der gebannt werden soll",
    reason="Grund für den Bann"
)
async def ban_command(interaction: discord.Interaction, user: discord.User, reason: str = "Kein Grund angegeben"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, Benutzer zu bannen.",
            ephemeral=True
        )
        return
    
    embed_dm = discord.Embed(
        title="🚫 Du wurdest gebannt",
        color=discord.Color.red()
    )
    embed_dm.add_field(name="Von", value=interaction.user.mention, inline=False)
    embed_dm.add_field(name="Grund", value=reason, inline=False)
    embed_dm.set_footer(text=f"Server: {interaction.guild.name}")
    embed_dm.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)


    print(f"Banning user: {user} for reason: {reason}")

    try:
        await user.send(embed=embed_dm)
    except discord.Forbidden:
        pass

    try:
        await interaction.guild.ban(user, reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Ich habe nicht die Berechtigung, diesen Benutzer zu bannen.",
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            "⚠️ Ein Fehler ist aufgetreten. Der Bann konnte nicht durchgeführt werden.",
            ephemeral=True
        )
        return

    embed_server = discord.Embed(
        title="🔨 Benutzer gebannt",
        description=f"{user.mention} wurde erfolgreich gebannt.",
        color=discord.Color.orange()
    )
    embed_server.add_field(name="Grund", value=reason, inline=False)
    embed_server.set_footer(text=f"Von {interaction.user}", icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed_server)


###################### Kick Command ######################
@bot.tree.command(name="kick", description="Kicke einen Benutzer.", guild=discord.Object(id=config.guild_id))
@app_commands.describe(
    user="Der Benutzer, der gekickt werden soll",
    reason="Grund für den Kick"
)
async def kick_command(interaction: discord.Interaction, user: discord.User, reason: str = "Kein Grund angegeben"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, Benutzer zu kicken.",
            ephemeral=True
        )
        return

    embed_dm = discord.Embed(
        title="👢 Du wurdest gekickt",
        color=discord.Color.red()
    )
    embed_dm.add_field(name="Von", value=interaction.user.mention, inline=False)
    embed_dm.add_field(name="Grund", value=reason, inline=False)
    embed_dm.set_footer(text=f"Server: {interaction.guild.name}")
    embed_dm.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else None)

    print(f"Kicking user: {user} for reason: {reason}")

    try:
        await user.send(embed=embed_dm)
    except discord.Forbidden:
        pass

    try:
        await interaction.guild.kick(user, reason=reason)
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Ich habe nicht die Berechtigung, diesen Benutzer zu kicken.",
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            "⚠️ Ein Fehler ist aufgetreten. Der Kick konnte nicht durchgeführt werden.",
            ephemeral=True
        )
        return

    embed_server = discord.Embed(
        title="👢 Benutzer gekickt",
        description=f"{user.mention} wurde erfolgreich gekickt.",
        color=discord.Color.orange()
    )
    embed_server.add_field(name="Grund", value=reason, inline=False)
    embed_server.set_footer(text=f"Von {interaction.user}", icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed_server)


####################### Help Command ######################
@bot.tree.command(name="help", description="Zeigt die verfügbaren Befehle an.", guild=discord.Object(id=config.guild_id))
async def help(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, Administrator.",
            ephemeral=True
        )
        return
    embed = discord.Embed(
        title="Hilfe",
        description="Hier sind die verfügbaren Befehle:",
        color=discord.Color.blue()
    )
    embed.add_field(name="/update", value="Sende ein Update mit Titel, Inhalt und optionalem Bild.", inline=False)
    embed.add_field(name="/ban", value="Banne einen Benutzer.", inline=False)
    embed.add_field(name="/kick", value="Kicke einen Benutzer.", inline=False)
    embed.add_field(name="/help", value="Zeigt diese Hilfe an.", inline=False)
    embed.add_field(name="/nuke", value="Löscht den aktuellen Channel und erstellt ihn neu.", inline=False)

    await interaction.response.send_message(embed=embed)





######################## Nuke Command ######################
@bot.tree.command(name="nuke", description="Löscht den aktuellen Channel und erstellt ihn neu.", guild=discord.Object(id=config.guild_id))
async def nuke(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message(
            "Du hast nicht die Berechtigung, Kanäle zu verwalten.",
            ephemeral=True
        )
        return

    channel = interaction.channel
    await channel.delete()
    new_channel = await interaction.guild.create_text_channel(channel.name)

    embed = discord.Embed(
        title="Channel wurde genuked",
        description=f"Der Channel {channel.mention} wurde gelöscht und neu erstellt.",
        color=discord.Color.red()
    )
    await new_channel.send(embed=embed)
    await interaction.response.send_message(f"Channel {new_channel.mention} wurde erfolgreich genuked.", ephemeral=True)


######################## activity System ########################


@bot.tree.command(name="set_activity", description="Setzt eine neue Aktivität für den Bot", guild=discord.Object(id=config.guild_id))
@app_commands.describe(
    activity_type="Art der Aktivität (playing, watching, listening, competing)",
    activity_text="Text der Aktivität"
)
async def set_activity(interaction: discord.Interaction, activity_type: str, activity_text: str):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="⛔ Keine Berechtigung",
            description="Du brauchst die Administrator-Berechtigung, um diesen Befehl zu nutzen.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    lower_text = activity_text.lower()
    for word in config.FORBIDDEN_WORDS:
        if word in lower_text:
            embed = discord.Embed(
                title="🚫 Verbotene Wörter erkannt",
                description="Die Aktivität enthält Wörter, die nicht erlaubt sind.",
                color=discord.Color.dark_red()
            )
            embed.add_field(name="Gefundenes Wort", value=f"`{word}`", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    type_map = {
        "playing": discord.ActivityType.playing,
        "watching": discord.ActivityType.watching,
        "listening": discord.ActivityType.listening,
        "competing": discord.ActivityType.competing
    }

    if activity_type.lower() not in type_map:
        embed = discord.Embed(
            title="❌ Ungültiger Typ",
            description="Bitte wähle zwischen: `playing`, `watching`, `listening`, `competing`",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    activity = discord.Activity(type=type_map[activity_type.lower()], name=activity_text)
    await bot.change_presence(activity=activity)

    embed = discord.Embed(
        title="✅ Aktivität gesetzt",
        color=discord.Color.green()
    )
    embed.add_field(name="Typ", value=activity_type.title(), inline=True)
    embed.add_field(name="Text", value=activity_text, inline=True)
    embed.set_footer(text=f"Gesetzt von {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

    await interaction.response.send_message(embed=embed, ephemeral=True)



@bot.tree.command(name="clear_activity", description="Löscht die aktuelle Aktivität des Bots", guild=discord.Object(id=config.guild_id))
async def clear_activity(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(
            title="⛔ Keine Berechtigung",
            description="Du brauchst die Administrator-Berechtigung, um diesen Befehl zu nutzen.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await bot.change_presence(activity=None)

    embed = discord.Embed(
        title="🧹 Aktivität gelöscht",
        description="Die Bot-Aktivität wurde erfolgreich entfernt.",
        color=discord.Color.orange()
    )
    embed.set_footer(text=f"Von {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    await interaction.response.send_message(embed=embed, ephemeral=True)





######################## discord logs ########################

async def message_delete(embed: discord.Embed):
    channel = bot.get_channel(config.message_delete)
    if channel:
        await channel.send(embed=embed)

async def message_edit(embed: discord.Embed):
    channel = bot.get_channel(config.message_edit)
    if channel:
        await channel.send(embed=embed)

async def member_ban(embed: discord.Embed):
    channel = bot.get_channel(config.member_ban)
    if channel:
        await channel.send(embed=embed)

async def member_unban(embed: discord.Embed):
    channel = bot.get_channel(config.member_unban)
    if channel:
        await channel.send(embed=embed)

async def member_update(embed: discord.Embed):
    channel = bot.get_channel(config.member_update)
    if channel:
        await channel.send(embed=embed)

async def voice_state(embed: discord.Embed):
    channel = bot.get_channel(config.voice_state)
    if channel:
        await channel.send(embed=embed)

@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    embed = discord.Embed(
        title="🗑️ Nachricht gelöscht",
        color=discord.Color.orange(),
        timestamp=datetime.now(UTC)
    )
    embed.add_field(name="Autor", value=f"{message.author} ({message.author.id})", inline=False)
    embed.add_field(name="Channel", value=message.channel.mention, inline=False)
    embed.add_field(name="Inhalt", value=message.content or "Kein Inhalt", inline=False)
    await message_delete(embed)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author.bot or before.content == after.content:
        return
    embed = discord.Embed(
        title="✏️ Nachricht bearbeitet",
        color=discord.Color.blue(),
        timestamp=datetime.now(UTC)
    )
    embed.add_field(name="Autor", value=f"{before.author} ({before.author.id})", inline=False)
    embed.add_field(name="Channel", value=before.channel.mention, inline=False)
    embed.add_field(name="Vorher", value=before.content or "Kein Inhalt", inline=False)
    embed.add_field(name="Nachher", value=after.content or "Kein Inhalt", inline=False)
    await message_edit(embed)



@bot.event
async def on_member_ban(guild, user):
    embed = discord.Embed(
        title="🔨 Benutzer gebannt",
        description=f"{user.mention} wurde gebannt.",
        color=discord.Color.dark_red(),
        timestamp=datetime.now(UTC)
    )
    embed.set_footer(text=f"User ID: {user.id}")
    await member_ban(embed)

@bot.event
async def on_member_unban(guild, user):
    embed = discord.Embed(
        title="♻️ Benutzer entbannt",
        description=f"{user.mention} wurde entbannt.",
        color=discord.Color.teal(),
        timestamp=datetime.now(UTC)
    )
    embed.set_footer(text=f"User ID: {user.id}")
    await member_unban(embed)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.timed_out_until != after.timed_out_until:
        if after.timed_out_until:
            title = "⏱️ Timeout"
            desc = f"{after.mention} wurde bis {after.timed_out_until.strftime('%d.%m.%Y %H:%M')} in Timeout gesetzt."
        else:
            title = "🔓 Timeout entfernt"
            desc = f"{after.mention} ist nicht mehr im Timeout."
        embed = discord.Embed(
            title=title,
            description=desc,
            color=discord.Color.light_grey(),
            timestamp=datetime.now(UTC)
        )
        embed.set_footer(text=f"User ID: {after.id}")
        await member_update(embed)

    if before.nick != after.nick:
        embed = discord.Embed(
            title="📝 Nickname geändert",
            description=f"{after.mention} hat seinen Nickname geändert.",
            color=discord.Color.dark_teal(),
            timestamp=datetime.now(UTC)
        )
        embed.add_field(name="Vorher", value=before.nick or "Kein Nickname", inline=True)
        embed.add_field(name="Nachher", value=after.nick or "Kein Nickname", inline=True)
        embed.set_footer(text=f"User ID: {after.id}")
        await member_update(embed)

    before_roles = set(before.roles)
    after_roles = set(after.roles)

    added = after_roles - before_roles
    removed = before_roles - after_roles

    for role in added:
        embed = discord.Embed(
            title="➕ Rolle hinzugefügt",
            description=f"{after.mention} hat die Rolle {role.mention} erhalten.",
            color=discord.Color.green(),
            timestamp=datetime.now(UTC)
        )
        await member_update(embed)

    for role in removed:
        embed = discord.Embed(
            title="➖ Rolle entfernt",
            description=f"{after.mention} hat die Rolle {role.mention} verloren.",
            color=discord.Color.red(),
            timestamp=datetime.now(UTC)
        )
        await member_update(embed)

@bot.event
async def on_voice_state_update(member, before, after):
    embed = discord.Embed(color=discord.Color.blurple(), timestamp=datetime.now(UTC))
    embed.set_footer(text=f"User ID: {member.id}")
    if before.channel is None and after.channel:
        embed.title = "🔊 Voice beigetreten"
        embed.description = f"{member.mention} ist {after.channel.mention} beigetreten."
    elif before.channel and after.channel is None:
        embed.title = "🔇 Voice verlassen"
        embed.description = f"{member.mention} hat {before.channel.mention} verlassen."
    elif before.channel != after.channel:
        embed.title = "🔁 Voice gewechselt"
        embed.description = f"{member.mention} wechselte von {before.channel.mention} zu {after.channel.mention}."
    else:
        return
    await voice_state(embed)



bot.run(config.TOKEN)