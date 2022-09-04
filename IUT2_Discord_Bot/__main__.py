import json
import os
import hikari
import lightbulb
import miru
from dotenv import load_dotenv
from guilds.RoleViews import get_role_view
from utils.json_utils import remove_element_json_array

load_dotenv()

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    prefix="!",
    intents=hikari.Intents.ALL,
    default_enabled_guilds=list(map(int, os.getenv("GUILD_ID").split(","))),
)
miru.load(bot)

# récupération des messages dont il faut écouter les interactions
@bot.listen()
async def startup_views(event: hikari.StartedEvent) -> None:
    with open("guilds/selectors.json", "r") as file:
        data = json.load(file)

    if not data["selectors"]:
        return

    for index, selector in enumerate(data["selectors"]):
        try:
            # check if message still exists on discord
            await bot.rest.fetch_message(selector["channel_id"], selector["id"])

            # load the view and its listener
            view = get_role_view(selector["guild_id"])
            view.start_listener(message=selector["id"])
        except:
            # remove selectors that do not exists anymore from the json list of selectors
            remove_element_json_array(index, "selectors", "guilds/selectors.json")
    return


# load les fichiers python contenant des commandes
bot.load_extensions_from("./commands")

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()
