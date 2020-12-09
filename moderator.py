from utils import *

def check_role(ctx):
    for role in ctx.message.author.roles:
        if role.name == 'Amministratore' or role.name == 'Comandante' or role.name == 'Ufficiale esecutivo' or role.name == 'Reclutatore':
            return True
    return False

def clan_message(flag):
    type = 'Battle.\n' if flag else 'Brawl.\n'
    message = '<@&680766615234543662>\nSegnalateci la vostra disponibilità per le Clan ' + type + 'Legenda:\n'
    for i in range(5):
        message = message + '- ' + votazioni_cb[i] + ' ' + significato_votazioni_cb[i] + '\n'
    return message

def clan_participation(flag, day, hour):
    type = 'Battle' if flag else 'Brawl'
    message = 'Presenze delle Clan ' + type + ' di ' + day + ', ore: ' + hour
    return message
