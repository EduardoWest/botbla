import discord
from discord.ext import commands

id_do_servidor =
id_cargo_atendente = 
token_bot = ""

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="Support", label="Criar um ticket | Creat a Ticket", emoji="📨"),
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Support":
            await interaction.response.send_message("Click below to open a ticket", ephemeral=True, view=CreateTicket())

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None

    @discord.ui.button(label="Open a ticket", style=discord.ButtonStyle.blurple, emoji="📨")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(ephemeral=True, content=">>> You already have a ticket in progress!")
                    return

        async for thread in interaction.channel.archived_threads(private=True):
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.edit_original_response(content="You already have a ticket in progress!", view=None)
                    return
        
        if ticket is not None:
            await ticket.edit(archived=False, locked=False)
            await ticket.edit(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080, invitable=False)
        else:
            ticket = await interaction.channel.create_thread(name=f"{interaction.user.name} ({interaction.user.id})", auto_archive_duration=10080, type=discord.ChannelType.private_thread)
            await ticket.edit(invitable=False)

        await interaction.response.send_message(ephemeral=True, content=f">>> I created a ticket for you {ticket.mention}")
        await ticket.send(f">>> Ticket created! Send as much information as possible about your case and wait for an agent to respond.")

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(guild=discord.Object(id=id_do_servidor), name='tickets', description='Setup')
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):
    await interaction.channel.send("Dashboard message", view=DropdownView()) 

    mod = interaction.guild.get_role(880953319500165121, 880952299386724434, 880969747280318505, 1216536639317475479, 880951808871243797, 994008545907445780, 986797422032343040, 880951605380382760)
    if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.roles:
        await interaction.response.send_message(f"The ticket was archived by {interaction.user.mention}, **Thanks for contacting us**")
        await interaction.channel.edit(archived=True, locked=True)
    else:
        await interaction.response.send_message(">>> This can't be done here...")

bot.run(token_bot)
