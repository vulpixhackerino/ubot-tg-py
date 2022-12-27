from pyrogram import Client, filters
# import time
import os
# IMPORTS

id = # your api id
hash = #your api hash

plugins = dict(root="plugins")

app = Client("my_account", api_id=id, api_hash=hash, plugins=plugins)

app.run()


