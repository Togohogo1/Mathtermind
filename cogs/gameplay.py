import discord
from discord import Colour
from discord.ext import commands

from classes.classic_solver import ClassicSolver
from classes.repeat_solver import RepeatSolver
from classes.detective_solver import DetectiveSolver


class Gameplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Frequently used embed
        self.not_in_game = discord.Embed(
            description="User is not in a game",
            color=Colour.red()
        )

    @commands.command(aliases=["g"])
    async def guess(self, ctx, *nums: int):
        """Makes a guess

        Examples:
            ;g 1        -> guesses 1
            ;g 5 6      -> guesses 5 and 6
            ;g 10 7 8 4 -> guesses 10, 7, 8 and 4
        """

        if self.key(ctx) not in self.bot.games:
            await ctx.send(embed=self.not_in_game)
            return

        game = self.bot.games[self.key(ctx)]
        name = game.__class__.__name__
        print("args", nums, type(game))

        if not game.valid_guess(nums):
            await ctx.send(embed=game.log_msg)
            return

        game.add_round(nums)
        game.board_items.append((
            f"Guess {game.round_number}: `{', '.join(map(str, game.rounds[-1]))}`",
            f"{'❓ '*(name == 'Detective')}{game.matches[-1]} match{'es'*(game.matches[-1] != 1)}"
        ))

        if game.game_over:
            await ctx.send(embed=game.log_msg)
            self.reset_game(ctx)
            return

        await ctx.send(embed=discord.Embed(
            title=f"Guess {game.round_number}",
            description=f"{game.matches[-1]} number{'s'*(game.matches[-1] != 1)} from the winning combo "
                        f"match{'es'*(game.matches[-1] == 1)} the user's guess{'❓'*(name == 'Detective')}"
        ))

    @commands.command(aliases=["sh"])
    async def show(self, ctx):
        """Shows the full guess history of the user's current game"""

        if self.key(ctx) in self.bot.games:
            await ctx.send(embed=self.bot.games[self.key(ctx)].create_board())
        else:
            await ctx.send(embed=self.not_in_game)

    @commands.command(aliases=["lv"])
    async def leave(self, ctx):
        """Leaves the user's current game"""

        if self.key(ctx) in self.bot.games:
            await ctx.send(embed=discord.Embed(
                description="User successfully left the game",
                color=Colour.green()
            ))
            self.reset_game(ctx)
        else:
            await ctx.send(embed=self.not_in_game)

    @commands.command(aliases=["sv"])
    async def solve(self, ctx):
        """Lists out all the possible combos for the user's current game

        The possible combos of any gamestate for any Mathtermind game type will be listed out in sorted order if
        there are 64 or less
        """

        if self.key(ctx) not in self.bot.games:
            await ctx.send(embed=self.not_in_game)
            return

        game = self.bot.games[self.key(ctx)]
        name = game.__class__.__name__

        if name == "Classic":
            solution = ClassicSolver(game.rounds, game.matches, game.verified)
        elif name == "Repeat":
            solution = RepeatSolver(game.rounds, game.matches, game.verified)
        else:
            solution = DetectiveSolver(game.rounds, game.matches, game.verified)

        solution.solve()
        await ctx.send(embed=solution.sol_panel)

    @commands.command(aliases=["id"])
    async def identify(self, ctx):
        """Help

        Description
        """

        await ctx.send("identifies the lie")

    def reset_game(self, ctx):
        self.bot.games.pop(self.key(ctx))

    def key(self, ctx):
        """Each game is unique based on the player and the guild"""

        return ctx.author.id, ctx.guild.id


def setup(bot):
    bot.add_cog(Gameplay(bot))