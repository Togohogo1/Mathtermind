import discord
from discord import Colour
from discord.ext import commands

from classes.classic import Classic
from classes.repeat import Repeat


class Gamemodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Frequently used embeds
        self.ready_play = discord.Embed(
            description="Ready to play",
            color=Colour.green()
        )
        self.in_game = discord.Embed(
            description="User is already in a game",
            color=Colour.red()
        )

        # Storing dict of users in bot, also reload doesn't erase gamestates
        if not hasattr(bot, "games"):
            bot.games = {}

    @commands.command(aliases=["cl"])
    async def classic(self, ctx):
        """Starts a Mathtermind game in classic mode

        7 Guesses to find winning combo, 8th Guess to determine it
        Each guess consists of 1-4 unique numbers
        Winning combo consists of 3 unique numbers from 1-15
        """

        await self.create_game(ctx, Classic(ctx.author))

    @commands.command(aliases=["rp"])
    async def repeat(self, ctx):
        """Starts a Mathtermind game in repeat mode

        The winning combo and user's Guesses do not have to contain unique numbers
        Otherwise, the same rules follow for classic mode [;help classic]
        """

        await self.create_game(ctx, Repeat(ctx.author))

    async def create_game(self, ctx, gametype):
        if self.key(ctx) not in self.bot.games:
            self.bot.games[self.key(ctx)] = gametype
            await ctx.send(embed=self.ready_play)
        else:
            await ctx.send(embed=self.in_game)

    def key(self, ctx):
        """Each game is unique based on the player and the guild"""

        return ctx.author.id, ctx.guild.id


def setup(bot):
    bot.add_cog(Gamemodes(bot))
