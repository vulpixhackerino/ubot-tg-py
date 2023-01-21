from pyrogram import Client, filters
from pyrogram.types import EmojiStatus
from pyrogram.raw import functions, types
from datetime import datetime
import os, pytz, time, math, atexit

ita = pytz.timezone("Europe/Rome")
clock = False
fname = ""
lname = ""


@Client.on_message(filters.command("backup", '-') & filters.me) # Backup dell'account in un qualsiasi momento (Include foto, nome, bio)
def backup(client, message):
    n = 0
    client.edit_message_text(message.chat.id, message.id, "Sto salvando le info dell'account...", disable_web_page_preview=True)
    for f in os.listdir("plugins/backup/pics"):
        os.remove(os.path.join("plugins/backup/pics", f))
    for photo in client.get_chat_photos("me"):
        client.download_media(photo.file_id, f"plugins/backup/pics/pfp{n}.png")
        n = n + 1
    bio = open("plugins/backup/bio.txt", "w")
    name = open("plugins/backup/name.txt", "w")
    bio.write(str(client.get_chat("me").bio))
    name.write(str(client.get_chat("me").first_name + "\n" + str(client.get_chat("me").last_name)))
    client.edit_message_text(message.chat.id, message.id, "Account salvato!",disable_web_page_preview=True)

@Client.on_message(filters.command("restore", '-') & filters.me)
def restore(client, message):
    pics = []
    client.edit_message_text(message.chat.id, message.id, "Torno all'ultimo backup, ci potrei mettere un po'.",disable_web_page_preview=True)
    for photo in client.get_chat_photos("me"):
        client.delete_profile_photos(photo.file_id)
    for f in os.listdir("plugins/backup/pics"):
        pics.append(f)
    for n in range(len(pics)):
        client.set_profile_photo(photo=f"plugins/backup/pics/pfp{len(pics)-1-n}.png")
        n += 2
    bio = open("plugins/backup/bio.txt", "r")
    name = open("plugins/backup/name.txt", "r")
    biotext = bio.readline()
    fname = name.readline()
    lname = name.readline()
    if lname == "None":
        client.update_profile(first_name=fname, bio=biotext, last_name="")
    else:
        client.update_profile(first_name=fname, last_name=lname, bio=biotext)
    client.edit_message_text(message.chat.id, message.id, "Backup ripristinato con successo!", disable_web_page_preview=True)

@Client.on_message(filters.command("fakedeleted", '-') & filters.me)
def fakedeleted(client, message):
    client.edit_message_text(message.chat.id, message.id, "Elimino l'account...",disable_web_page_preview=True)
    for photo in client.get_chat_photos("me"):
        client.delete_profile_photos(photo.file_id)
    client.set_profile_photo(photo=f"plugins/deleted.jpg")
    client.update_profile(first_name="Account Eliminato", bio="", last_name="")
    client.edit_message_text(message.chat.id, message.id, "Account eliminato!",disable_web_page_preview=True)

@Client.on_message(filters.command("clock", '-') & filters.me)
def clock(client, message):
    global clock, fname, lname
    clock = True
    client.edit_message_text(message.chat.id, message.id, "Orologio attivato.", disable_web_page_preview=True)
    fname = str(message.from_user.first_name)
    lname = str(message.from_user.last_name)
    if lname == "None" or None:
        lname = ""
    currmin = 0
    while clock:  
        lastmin = currmin
        now = datetime.now(ita)
        current_time = now.strftime("『%H:%M』")
        currmin = now.minute
        if currmin != lastmin:
            client.update_profile(
                first_name=fname,
                last_name= lname + current_time
            )
            print("Cambio user!")
        time.sleep(1)


@Client.on_message(filters.command("unclock", '-') & filters.me)
def unclock(client, message):
    global clock, fname, lname
    clock = False
    client.edit_message_text(message.chat.id, message.id, "Orologio disattivato.", disable_web_page_preview=True)
    client.update_profile(
        first_name=fname,
        last_name= lname
    )

    time.sleep(1)

def on_exit():
    global clock
    clock = False

atexit.register(on_exit)

