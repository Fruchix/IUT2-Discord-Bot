import hikari
import miru
import lightbulb


@lightbulb.command("ping", "Responds \"Pong\"")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def ping(ctx: lightbulb.context.SlashContext) -> None:
    await ctx.respond("Pong")
    return


class ButtonView(miru.View):

    @miru.button(label="C1", style=hikari.ButtonStyle.SECONDARY)
    async def btn1(self, ctx: miru.Context) -> None:
        if 957568326211616840 not in [role.id for role in ctx.member.get_roles()]:
            await ctx.member.add_role(role=957568326211616840)
            self.btn1.style = hikari.ButtonStyle.PRIMARY
        else:
            await ctx.member.remove_role(role=957568326211616840)
            self.btn1.style = hikari.ButtonStyle.SECONDARY

        await self.message.edit(components=self.build())
        return


@lightbulb.command("buttons", "Send a message with buttons underneath")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def buttons(ctx: lightbulb.context.SlashContext) -> None:

    view = ButtonView(timeout=60)
    resp = await ctx.respond("Choisissez un bouton !", components=view.build())
    message = await resp.message()
    view.start(message=message)
    return


# =======================================================


class RoleButton(miru.Button):

    role_id = None

    def __init__(self, role_id=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.role_id = role_id

    async def callback(self, ctx: miru.Context) -> None:
        if self.role_id not in [role.id for role in ctx.member.get_roles()]:
            await ctx.member.add_role(role=self.role_id)
            self.style = hikari.ButtonStyle.PRIMARY
        else:
            await ctx.member.remove_role(role=self.role_id)
            self.style = hikari.ButtonStyle.SECONDARY

        await ctx.message.edit(components=self.view.build())
        return


@lightbulb.command("buttonsbis", "Send a message with buttons underneath")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def buttonsbis(ctx: lightbulb.context.SlashContext) -> None:

    view = miru.View(timeout=60)
    view.add_item(RoleButton(style=hikari.ButtonStyle.SECONDARY if 957568326211616840 not in [role.id for role in ctx.member.get_roles()] else hikari.ButtonStyle.PRIMARY,
                             label="Role C2",
                             role_id=957568326211616840))
    resp = await ctx.respond("Choisissez un bouton !", components=view.build())
    message = await resp.message()
    view.start(message=message)
    return


@lightbulb.command("infos", "Testing infos")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def infos(ctx: lightbulb.context.SlashContext) -> None:

    channels = [channel for channel in await ctx.bot.rest.fetch_guild_channels(ctx.guild_id) if channel.type == hikari.ChannelType.GUILD_TEXT]
    print(channels)

    await ctx.respond("Coinc")
    return


def load(bot: lightbulb.BotApp) -> None:
    bot.command(ping)
    bot.command(buttons)
    bot.command(buttonsbis)
    bot.command(infos)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_command(bot.get_slash_command("ping"))
    bot.remove_command(bot.get_slash_command("buttons"))
    bot.remove_command(bot.get_slash_command("buttonsbis"))
    bot.remove_command(bot.get_slash_command("infos"))
