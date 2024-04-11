import discord
from discord.ext import commands, tasks
import requests
import discord
import asyncio
import json
import os
from datetime import datetime


intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix="bl!")



# Log
@bot.event
async def on_message(message):
    print(f'Message de {message.author}: {message.content}')
    await bot.process_commands(message)

# Função para deletar o comando usado e enviar mensagem
async def delete_command_and_send_message(ctx, message_content):
    await ctx.message.delete()  # Deleta o comando usado
    await ctx.send(message_content)  # Envia a mensagem

# Comandos
@bot.command(name="price")
async def price(ctx):
    await delete_command_and_send_message(ctx, "```BAIMLESS PREÇOS - BAIMLESS PRICES \n \n 24 hours:  R$ 35,99 - $ 7,28 \n \n Weekly: R$ 41,99 - $ 8,49 \n \n Half Month: R$ 55,97 - $ 11,32 \n \n Monthly: R$ 87,99 - $ 17,79 \n \n Quarterly: R$ 197,99 - $ 40,04 \n \n Lifetime: R$ 480,99 - $ 97,26```")

@bot.command(name="rules")
async def rules(ctx):
    await delete_command_and_send_message(ctx, "Você pode ver as regras em https://discord.com/channels/880951477441544242/923400884208169060 \n You can see the rules at https://discord.com/channels/880951477441544242/923400884208169060")

@bot.command(name="tutorial")
async def tutorial(ctx):
    await delete_command_and_send_message(ctx, "Parabéns seu produto foi ativado, siga o tutorial para prosseguir com a instalação https://youtu.be/CgNXrYc2CA8 \n \n **E também se possível deixe um feedback em**  https://discord.com/channels/880951477441544242/1004811524730265700 :smile:")

@bot.command(name="dollar")
async def dollar(ctx):
    price = await dollar_price()
    await delete_command_and_send_message(ctx, f"O preço do dólar é: R$ {price}")

#Comando vac
@bot.command(name="vac")
async def vac(ctx):
    await delete_command_and_send_message(ctx, "Compreendemos que você tenha sido banido do jogo devido a relatórios de comportamento em vez de um banimento VAC. É importante lembrar que banimento de jogo em registro é diferente de VAC, você provavelmente foi muito reportado.")

 #comando erros
@bot.command(name="erros")
async def erros(ctx):
    await delete_command_and_send_message(ctx, ">>> **Soluções para resolver durante a injeção** \n \n 1 - Desative o Windows Defender: Para evitar conflitos durante a injeção, é recomendável desativar temporariamente o Windows Defender. Isso pode ajudar a evitar bloqueios durante a injeção. \n \n 2 - Desligue a Proteção em Tempo Real: Além de desativar o Windows Defender, também é aconselhável desativar qualquer outra proteção em tempo real que possa estar em execução. \n \n 3 - Desative o Antivírus: Se você estiver usando um software antivírus, desative-o temporariamente durante a instalação. Isso pode prevenir possíveis conflitos que possam ocorrer. \n \n 4 - Atualize o DirectX: Verifique se a sua versão do DirectX está atualizada. Muitos programas e jogos dependem do DirectX para funcionar corretamente. Baixe e instale a versão mais recente do site oficial da Microsoft.")       

# Função para obter o preço do dólar
async def dollar_price():
    try:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/usd")
        data = response.json()
        price = data['USDBRL']['high']
        return price
    except Exception as e:
        print(f"Erro ao obter o preço do dólar: {e}")
        return "Erro ao obter o preço do dólar."

# Comando para banir um membro
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await delete_command_and_send_message(ctx, f"{member.mention} Quebrou as regras e foi de F.")

# Comando para desbanir um membro
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_id: int):
    banned_users = await ctx.guild.bans()
    member = discord.utils.get(banned_users, user_id=member_id)
    await ctx.guild.unban(member)
    await delete_command_and_send_message(ctx, f"Usuário com ID {member_id} Foi desbanido.")

# Comando para mutar um membro
@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await delete_command_and_send_message(ctx, f"{member.mention} Foi mutado.")

# Comando para desmutar um membro
@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await delete_command_and_send_message(ctx, f"{member.mention} Foi desmutado.")

# Comando para apagar todas as mensagens de um canal
@bot.command(name="apagar")
@commands.has_permissions(manage_messages=True)
async def apagar(ctx):
    await ctx.channel.purge()
    message = await ctx.send("```Mensagens excluídas \n \n Deleted messages```")
    await delete_command_and_send_message(ctx, "```Mensagens excluídas \n \n Deleted messages```")

# Comando de ajuda
@bot.command(name="ajuda")
async def ajuda(ctx):
    await delete_command_and_send_message(ctx, "**Maintenance**")


#comando close# Carregar a contagem de tickets do arquivo (se existir)
def load_ticket_count():
    try:
        with open('ticket_count.json', 'r') as file:
            data = json.load(file)
            return data['ticket_count']
    except FileNotFoundError:
        return 0  # Retorna 0 se o arquivo não existir

# Salvar a contagem de tickets no arquivo
def save_ticket_count(ticket_count):
    data = {'ticket_count': ticket_count}
    with open('ticket_count.json', 'w') as file:
        json.dump(data, file)

ticket_count = load_ticket_count()  # Inicializa a contagem de tickets


# Dicionário para armazenar os transcripts dos tickets
transcripts = {}
ticket_count = 0
ticket_claimed = {}  # Dicionário para controlar os tickets já assumidos

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def new_ticket(ctx, *, issue):
    global ticket_count  # Access the global ticket count variable
    
    # Cria um novo canal para o ticket
    channel = await ctx.guild.create_text_channel(name=f'ticket-{ticket_count + 1}', category=ctx.channel.category)

    # Adiciona o usuário ao canal
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

    # Armazena o canal e a descrição do ticket no dicionário de transcripts
    transcripts[channel.id] = {'user': ctx.author, 'issue': issue}
    ticket_count += 1  # Incrementa o contador de tickets

    await ctx.send(f'Your ticket has been created in {channel.mention}')

@bot.command(name="close")
@commands.has_permissions(manage_channels=True)
async def close(ctx):
    global ticket_count  # Access the global ticket count variable
    author_name = ctx.author.name
    
    # Get the name of the closed channel
    channel_name = ctx.channel.name

    # Delete the channel
    await ctx.channel.delete()

    # Send a message in the specified channel with user mention, closed channel name, and ticket count
    log_channel = bot.get_channel(1226957939269701722)  # Replace CHANNEL_ID with the desired channel ID
    if log_channel:
        ticket_count += 1  # Increment ticket count
        await log_channel.send(f">>> <@{ctx.author.id}> Fechou o {channel_name} e contém {ticket_count} tickets fechados.")
        await log_channel.send("-----------------------------------------------------")
    else:
        await ctx.send("Erro ao encontrar o canal de log.")

@bot.event
async def on_message(message):
    # Ignora mensagens do bot
    if message.author.bot:
        return

    # Verifica se a mensagem foi enviada em um canal de ticket e se é a primeira mensagem no ticket
    if isinstance(message.channel, discord.TextChannel) and message.channel.name.startswith('ticket-') and message.content.lower() != 'ticket tool':
        allowed_roles = ['Moderator', 'Staff', 'Technical Support']
        member_roles = [role.name for role in message.author.roles]

        # Verifica se o usuário tem um dos cargos permitidos
        if any(role in allowed_roles for role in member_roles):
            if message.channel.id not in ticket_claimed:
                ticket_claimed[message.channel.id] = True

                # Envia uma mensagem no canal especificado indicando que o usuário está assumindo o ticket
                log_channel = bot.get_channel(1226957939269701722)  # Replace CHANNEL_ID with the desired channel ID
                if log_channel:
                    ticket_number = message.channel.name.split('-')[1]
                    await log_channel.send(f">>> <@{message.author.id}> \n Está assumindo o ticket {ticket_number}")
                    await log_channel.send("-----------------------------------------------------")
                else:
                    await message.channel.send("Erro ao encontrar o canal de log.")

    await bot.process_commands(message)
# Comando para resetar a contagem de tickets
@bot.command(name="reset")
async def reset(ctx):
    global ticket_count  # Access the global ticket count variable
    ticket_count = 0  # Reset ticket count
    save_ticket_count(ticket_count)  # Salva a contagem de tickets no arquivo
    await ctx.send("Contagem de tickets resetada para zero.")
    await ctx.message.delete()

# Comando para visualizar a contagem de tickets
@bot.command(name="tickets")
async def tickets(ctx):
    await ctx.send(f"Contagem de tickets: {ticket_count}")
    await ctx.message.delete()

# Comando para atribuir pontos e resetar a contagem de tickets
@bot.command(name="pontos")
async def pontos(ctx, member: discord.Member):
    global ticket_count  # Access the global ticket count variable
    await ctx.send(f"O usuário {member.name} fechou ||{ticket_count}|| tickets.")
    ticket_count = 0  # Reset ticket count after displaying
    save_ticket_count(ticket_count)  # Salva a contagem de tickets no arquivo


#Comando para permitir ao bot enviar mensagens
@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    await ctx.message.delete()  # Deleta o comando usado
    await ctx.send(message)


# Tarefa para enviar a mensagem a cada 3 horas
async def send_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(1219448011030270054)  # Substitua pelo ID do canal desejado
    while not bot.is_closed():
        await channel.send("```PT-BR: Dúvidas sobre sua compra ou problemas com o software? Abra um ticket. \n \n EN-US: Questions about your purchase or problems with the software? Open a ticket.```")
        await asyncio.sleep(3 * 60 * 60)  # Espera 3 segundos antes de enviar a próxima mensagem


#setar tag pelo bot
@bot.command()
async def tag(ctx, member: discord.Member, days: int, *, role_name: str):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await member.add_roles(role)
        await ctx.send(f'>>> O cargo {role_name} foi atribuído a {member.mention} por {days} dias')
        await ctx.message.delete()


        await asyncio.sleep(days * 86400)  # Convert days to seconds
        await member.remove_roles(role)


        channel = bot.get_channel(923406276581527582)
        await channel.send(f'O cargo {role_name} foi removido de {member.mention} após {days} dias')


    else:
        await ctx.send(f'O cargo {role_name} não foi encontrado')




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(send_message())
bot.run('MTIxNDk2OTM4MTMwMjU3NTEwNA.GijwNK.CbHhyBSdcX3PADb9aPH_njmoY3KoyGZCAdn04s')


