from pyrogram import Client, filters
import time
import yt_dlp as ydl
from youtube_search import YoutubeSearch
import json
import os
import wikipedia
import random

wikipedia.set_lang("it")

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': "FFmpegExtractAudio",
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
"""

WIP

def txtcmd():  # Converte i file di testo in comandi utilizzabili da comanditxt
    global cmdlist
    cmdlist = "Tutti i comandi di testo disponibili:\n"
    root = os.getcwd()
    os.chdir(os.getcwd() + "/plugins/txtcmd/")
    files = os.listdir(os.getcwd())
    comandi = []
    i = 0
    for x in files:
        comandi.append(x.split(".")[0])
        cmdlist = cmdlist + "-" + comandi[i] + "\n"
        i += 1
    os.chdir(root)
    return comandi
"""

def sounds():  # Converte i file di testo in comandi utilizzabili da sounds
    global sblist
    sblist = "Tutti i suoni disponibili:\n"
    root = os.getcwd()
    os.chdir(os.getcwd() + "/plugins/sounds/")
    files = os.listdir(os.getcwd())
    soundboard = []
    i = 0
    for x in files:
        if x.endswith(".mp3"):
            soundboard.append(x.split(".")[0])
            sblist = sblist + "-" + soundboard[i] + "\n"
            i += 1
    os.chdir(root)
    return soundboard

def clips():  # Converte i file di testo in comandi utilizzabili da clips
    global cliplist
    cliplist = "Tutte le clip disponibili:\n"
    root = os.getcwd()
    os.chdir(os.getcwd() + "/plugins/clips/")
    files = os.listdir(os.getcwd())
    clips = []
    i = 0
    for x in files:
        if x.endswith(".mp4"):
            clips.append(x.split(".")[0])
            cliplist = cliplist + "-" + clips[i] + "\n"
            i += 1
    os.chdir(root)
    return clips

@Client.on_message(filters.command("corsivo", "-") & filters.me)
def corsivo(client, message):
    textnc = message.text[9::]
    a = ["æ", "ɑ", "ā", "ä"]
    e = ["ē", "é", "ě", "ȅ"]
    o = ["ô", "ö", "õ", "ø"]
    i = ["ī", "í", "ĩ", "ỉ"]
    u = ["û", "ù", "ŭ", "ü"]
    newtext = ""
    for word in textnc:
        if word == "a":
            newtext = newtext + random.choice(a)
        elif word == "e":
            newtext = newtext + random.choice(e)
        elif word == "i":
            newtext = newtext + random.choice(i)
        elif word == "o":
            newtext = newtext + random.choice(o)
        elif word == "u":
            newtext = newtext + random.choice(u)
        else:
            newtext = newtext + word
    newtext = newtext + " ✨"
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=newtext, disable_web_page_preview=True)

@Client.on_message(filters.command("alive", "-") & filters.me)
def alive(client, message):
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
    "`Uwa! Funziono!`\n"
    f"`L'uBot è collegato all'account di:` {message.from_user.mention}\n"
    "`Realizzato da `@pulpix  🦊", disable_web_page_preview=True)

@Client.on_message(filters.command("copy", '-') & filters.me)  # Comando copy - copia un messaggio e lo mette in load
def copycmd(client, message):
    if message.reply_to_message is None:
        client.delete_messages(message.chat.id, message.id, True)
    else:
        testo = message.reply_to_message.text
        file = open("plugins/txtcmd/load.txt", 'w', encoding='utf8')
        file.write(testo)
        file.close()
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="✅ Messaggio copiato!",
                                 disable_web_page_preview=True)

@Client.on_message(filters.command("sblist", "-") & filters.me)
def allsblist(client, message):
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=sblist, disable_web_page_preview=True)

@Client.on_message(filters.command("wiki", "-") & filters.me)
def wiki(client, message):
    result = wikipedia.summary(message.text)
    # for name in result:
    #    text = text + name + "\n"
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=result, disable_web_page_preview=True)

@Client.on_message(filters.command("type", '-') & filters.me)  # Comando type_
def typecmd(client, message):
    testo = message.text[6::]
    pivot = ""
    for i in testo:
        pivot = pivot + i + "_"
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=pivot,
                                 disable_web_page_preview=True)
        pivot = pivot.replace("_", "")
        time.sleep(0.300)
    pivot = pivot.replace("_", "")
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=pivot, disable_web_page_preview=True)

@Client.on_message(filters.command("testemoji", '-') & filters.me)  # Comando type_
def emojianimati(client, message):
    print(message.text)
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=message.text, disable_web_page_preview=True)

@Client.on_message(filters.command("song", '-') & filters.me)  # Comando per le canzoni
def song(client, message):
    search = message.text[6::]
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Sto scaricando il file...",
                             disable_web_page_preview=True)
    link = YoutubeSearch(search, max_results=1).to_json()
    data = json.loads(link)
    link = "https://youtube.com" + data['videos'][0]['url_suffix']
    title = data['videos'][0]['title']
    with ydl.YoutubeDL(ydl_opts) as ydown:
        ydown.download([link])
    client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="Sto caricando il file...",
                             disable_web_page_preview=True)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, f"{title}.mp3")
    if message.reply_to_message is not None:
        client.send_audio(message.chat.id, audio=f"{title}.mp3", reply_to_message_id=message.reply_to_message_id, title=title)
    else:
        client.send_audio(message.chat.id, audio=f"{title}.mp3", title=title)
    client.delete_messages(message.chat.id, message.id, True)
    os.remove(f"{title}.mp3")


@Client.on_message(filters.command("test", '-') & filters.me)  # Lunaaaaaa
def test(client, message):
    client.send_message(message.chat.id, "Questo messaggio ha una reply.")

@Client.on_message(filters.command("moon", '-') & filters.me)  # Lunaaaaaa
def moon(client, message):
    moon_list = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔"]
    for x in range(30):
        moon_list = moon_list[-1:] + moon_list[:-1]
        text = ''.join(moon_list[:5]) + " "
        client.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=text,
                                 disable_web_page_preview=True)
        time.sleep(0.1)
        
@Client.on_message(filters.command("spaziato", '-') & filters.me)
def spaziato(client, message):
    textns = message.text[10::]
    newtext = ""
    for word in textns:
        newtext = newtext + word + " "
    client.edit_message_text(message.chat.id, message.id, newtext, disable_web_page_preview=True)

@Client.on_message(filters.command(sounds(), '-') & filters.me)  # Gestisce tutta la soundboard
def sbcmd(client, message):  # Soundboard
    print(message.command)
    file = "plugins/sounds/" + message.command[0] + '.mp3'
    if message.reply_to_message is not None:
        client.send_audio(message.chat.id, audio=file, reply_to_message_id=message.reply_to_message_id)
    else:
        client.send_audio(message.chat.id, audio=file)
    client.delete_messages(message.chat.id, message.id, True)

@Client.on_message(filters.command(clips(), '-') & filters.me)  # Gestisce tutta la soundboard
def clip(client, message):  # Soundboard
    print(message.command)
    file = "plugins/clips/" + message.command[0] + '.mp4'
    if message.reply_to_message is not None:
        client.send_video(message.chat.id, video=file, reply_to_message_id=message.reply_to_message_id)
    else:
        client.send_video(message.chat.id, video=file)
    client.delete_messages(message.chat.id, message.id, True)
"""

@Client.on_message(filters.command("txtcmd", '-') & filters.me)  # Mostra tutti i txtcmd
def showtxtcmd(client, message):  # Soundboard
    client.edit_message_text(message.chat.id, message.id, cmdlist, disable_web_page_preview=True)
"""

@Client.on_message(filters.command("sb", '-') & filters.me)  # Gestisce tutta la soundboard
def showsb(client, message):  # Soundboard
    client.edit_message_text(message.chat.id, message.id, sblist, disable_web_page_preview=True)

@Client.on_message(filters.command("clips", '-') & filters.me)  # Gestisce tutta la soundboard
def showsb(client, message):  # Soundboard
    client.edit_message_text(message.chat.id, message.id, cliplist, disable_web_page_preview=True)

@Client.on_message(filters.command("dice", '-') & filters.me)
def dice(client, message):
    try:
        type = int(message.text[6::])
        number = random.randint(1, type)
        client.edit_message_text(message.chat.id, message.id, f"Dado da {type} facce.\nRisultato: **{number}**.", disable_web_page_preview=True)
    except:
        client.edit_message_text(message.chat.id, message.id, "Il dado che hai scelto non esiste. La sintassi è -dice [numerofacce].", disable_web_page_preview=True)