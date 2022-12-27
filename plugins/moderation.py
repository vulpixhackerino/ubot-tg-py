from pyrogram import Client, filters
from pyrogram.raw import functions, types
from datetime import datetime
import os
import sys
import math

mutati = []

@Client.on_message(filters.command("mute", '-') & filters.me & filters.private) # Mute, va solo in pvt
def mute(client, message):
    global mutati
    if message.chat.id in mutati:
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="L'utente è già mutato.", disable_web_page_preview=True)
    else:
        mutati.append(message.chat.id)
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Sei stato/a mutato. Ogni tuo messaggio sarà da ora eliminato fino all'unmute.", disable_web_page_preview=True)


@Client.on_message(filters.command("unmute", '-') & filters.me & filters.private) # Mute, va solo in pvt
def unmute(client, message):
    global mutati
    if message.chat.id in mutati:
        mutati.remove(message.chat.id)
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Sei stato/a smutato. Puoi tornare a scrivere.", disable_web_page_preview=True)
    else:
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="L'utente non è mutato.", disable_web_page_preview=True)


@Client.on_message(filters.private & filters.incoming)
def checkifmuted(client, message):
    global mutati
    if message.chat.id in mutati:
        client.delete_messages(message.chat.id, message.id, True)

@Client.on_message(filters.command("infoall", '-') & filters.me) # Comando infoall
def infoall(client, message):
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Sto ottenendo le info dal gruppo...", disable_web_page_preview=True)
    file = open(f"temp/{message.chat.id}.txt", "w", encoding='utf-8-sig')
    try:
        ulist = client.get_chat_members(message.chat.id)
    except:
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Non sono riuscito ad ottenere le info.", disable_web_page_preview=True)
    for users in ulist:
        id = users.user.id
        DC = users.user.dc_id
        fn = users.user.first_name
        ln = users.user.last_name
        if DC is None:
            DC = " Sconosciuto"
        try:
            uname = users.user.username
        except:
            uname = "Nessun username"
        text = ("╔ Nome utente: " + str(uname) + "\n╠ Nome: " + str(fn) + "\n╠ Cognome: " + str(ln) + "\n╠ ID Utente: " + str(id) + "\n╚ Datacenter Utente: DC" + str(DC) + "\n\n")
        file.write(text)
    file.close()
    client.delete_messages(message.chat.id, message.id, True)
    client.send_document(message.chat.id, f"temp/{message.chat.id}.txt")
    os.remove(f"temp/{message.chat.id}.txt")

@Client.on_message(filters.command("infouser", '-') & filters.me)
def infouser(client, message):
    """Questo comando restituisce tutte le informazioni di un utente tra cui foto profilo
                            ID, Nome e Cognome e datacenter"""
    client.delete_messages(message.chat.id, message.id, True)
    if message.reply_to_message is None:
        user = client.get_users(message.text[10::])
    else:
        user = client.get_users(message.reply_to_message.from_user.username)
    id = user.id
    bio = client.get_chat(id).bio
    DC = user.dc_id
    fn = user.first_name
    ln = user.last_name
    if DC is None:
        DC = " Sconosciuto"
    try:
        uname = user.username
    except:
        uname = "Nessun username"
    try:
        client.download_media(user.photo.big_file_id, "pfp.png")
        photo = "downloads/pfp.png"
    except:
        photo = "downloads/nophoto.png"
    text = ("╔ Nome utente: " + uname + "\n╠ Nome: " + str(fn) + "\n╠ Cognome: " + str(ln) + "\n╠ ID Utente: " + str(
        id) + "\n╠ Bio: " + str(bio) + "\n╚ Datacenter Utente: DC" + str(DC) + "")
    client.send_photo(chat_id=message.chat.id, photo=photo, caption=text)

@Client.on_message(filters.command("checkvoip", '-') & filters.me)
def checkvoip(client, message):
    try:
        if message.reply_to_message is None:
            user = client.get_users(message.text[11::])
        else:
            user = client.get_users(message.reply_to_message.from_user.username)
        DC = user.dc_id
        if DC == 4:
            client.edit_message_text(chat_id=message.chat.id, message_id=message.id,text=f"**Risultato Check VoIP**\n✅ L'utente {user.mention} non è un potenziale VoIP.\nIl suo DC è **4**.",disable_web_page_preview=True)
        elif DC == None:
            raise("Cavallo D:")
        else:
            client.edit_message_text(chat_id=message.chat.id, message_id=message.id,text=f"**Risultato Check VoIP**\n⚠ L'utente {user.mention} è un potenziale VoIP. Il suo DC è **{DC}**.", disable_web_page_preview=True)
    except:
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="**Risultato Check VoIP**\n❌ Non sono riuscito a reperire il DC dell'utente; potrebbe non esistere o non avere impostato una foto profilo.",disable_web_page_preview=True)

@Client.on_message(filters.command("readall", "-") & filters.me)
def readall(client, message):
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Leggo tutte le chat...",disable_web_page_preview=True)
    chatlist = client.invoke(functions.messages.GetAllChats(except_ids=[]))
    list = chatlist.chats
    for chats in list:
        try:
            chat = "-100" + str(chats.id)
            client.read_chat_history(chat)
        except:
            pass
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="✅ Tutte le chat sono state lette con successo.",disable_web_page_preview=True)

@Client.on_message(filters.command("ping", "-") & filters.me)
def ping(client, message):
    ps = datetime.now()
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="📶 Pong!", disable_web_page_preview=True)
    pe = datetime.now()
    ping = (pe-ps).microseconds / 1000
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f"📶 Pong! `{ping}ms`",disable_web_page_preview=True)

@Client.on_message(filters.command("eval", "-") & filters.me)
def evaluate(client, message):
    try:
        result = eval(message.text[6:])
    except Exception as e:
	    result = e
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=f"Risultato: `{result}`", disable_web_page_preview=True)
