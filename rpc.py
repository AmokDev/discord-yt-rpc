from pypresence import Presence
from ytmusicapi import YTMusic

from json import load, dump
from json.decoder import JSONDecodeError

from time import time, sleep

RPC = Presence("1102779428888641547")
RPC.connect() # mq

try:
    app = YTMusic("oauth.json")
except (JSONDecodeError):
    print("""
Вы не сгенерировали сессию oauth.json! Без нее скрипт чисто физически не сможет получить данные о ваших прослушиваниях!
Для подключения сессии испольхуйте комманду `ytmusicapi oauth` в терминале и следуйте указанным инструкциям!

За дополнительной помощью можете обратиться ко мне в тг: @AmokDev
""")
    sleep(100)

def getTrack():
    song = app.get_history()[0]
    name = song["title"]
    id = song["videoId"]
    img = song["thumbnails"][-1]["url"]
    artist = song["artists"][0]["name"]
    return name, id, img, artist

def getTimer() -> int:
    title, id, img, artist = getTrack()
    with open("config.json", "r") as f:
            data = load(f)
    track = data["track"]
    if title == track:
        return int(data["time"])
    else:
        with open("config.json", "w") as f:
            data["track"] = title
            data["time"] = time()
            data = dump(data, f)

print("YouTube Music 'Discord rich presence' Client Started!")
while True:    
    try:
        name, id, img, artist = getTrack()
        RPC.update(
            buttons = [{"label": "Слушать", "url": f"https://music.youtube.com/watch?v={id}"}],
            state = "▶ " + name,
            details = artist,
            large_image = img,
            large_text = "YouTube Music",
            small_image = "yt_avatar",
            small_text = "#NoWar",
            start = getTimer()
        )
        sleep(8)
    except Exception as e:
        print(e)
        print("Отправьте скриншот ошибки DS: neynq или TG: @neynq")
        RPC.update(
            state="Сейчас ничего не играет!",
            large_image="yt_avatar",
            large_text="YouTube Music"
        )
        sleep(60)
