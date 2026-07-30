import re
from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH, TARGET_CHANNEL

app = Client(
    "MovieSorterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

movies = {}

def clean_name(name):
    name = re.sub(r"\[.*?\]", "", name)
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"720p|1080p|2160p|480p|WEBRip|BluRay|HDRip|HEVC|x264|x265", "", name, flags=re.I)
    return name.strip()

@app.on_message(filters.document | filters.video)
async def receive(client, message):
    media = message.video or message.document

    filename = media.file_name
    size = media.file_size

    movie = clean_name(filename)

    if movie not in movies:
        movies[movie] = []

    movies[movie].append((size, message))

    await message.reply_text(
        f"✅ Added\n\n📁 {filename}\n💾 {round(size/1024/1024,2)} MB"
    )

@app.on_message(filters.command("send"))
async def send_all(client, message):

    for movie in sorted(movies):
        await client.send_message(
            TARGET_CHANNEL,
            f"🎬 {movie}\nFiles: {len(movies[movie])}"
        )

        for _, msg in sorted(movies[movie], key=lambda x: x[0]):
            await msg.copy(TARGET_CHANNEL)

    movies.clear()
    await message.reply_text("✅ All files sent successfully.")

app.run()
