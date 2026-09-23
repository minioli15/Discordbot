import os
import discord
from discord.ext import commands
from discord import ui

# Intents konfigurieren
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 1. Das Pop-up Formular (Modal)
class ApplicationModal(ui.Modal, title="Bewerbung / Namensänderung"):
    ingame_name = ui.TextInput(
        label="Dein Ingame-Name",
        placeholder="z.B. GamerPro123",
        min_length=2,
        max_length=32,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        neuer_name = self.ingame_name.value
        user = interaction.user

        try:
            await user.edit(nick=neuer_name)
            await interaction.response.send_message(
                f"✅ Dein Nickname wurde erfolgreich auf **{neuer_name}** geändert!", 
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Fehler: Ich habe keine Rechte, deinen Namen zu ändern. (Ist die Bot-Rolle im Server hoch genug?)", 
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Etwas ist schiefgelaufen: {e}", 
                ephemeral=True
            )

# 2. Der Button für die Nachricht
class ApplyButtonView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Bewerben / Name eintragen", style=discord.ButtonStyle.green, custom_id="apply_button")
    async def open_modal(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(ApplicationModal())

# 3. Bot Events & Setup-Befehl
@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="Willkommen auf dem Server!",
        description="Klicke auf den Button unten, um deinen Ingame-Namen einzutragen. Dein Server-Spitzname wird daraufhin automatisch angepasst.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=ApplyButtonView())
    await ctx.message.delete()

# Liest den Token sicher aus den Render-Umgebungsvariablen
bot.run(os.getenv("DISCORD_TOKEN"))
