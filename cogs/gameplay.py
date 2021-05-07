import discord
from discord.ext import commands


from classes.classic_solver import ClassicSolver

class Gameplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["g"])
    async def guess(self, ctx, *nums: int):
        """Makes a guess

        Examples:
            ;g 1        -> guesses 1
            ;g 5 6      -> guesses 5 and 6
            ;g 10 7 8 4 -> guesses 10, 7, 8 and 4
        """

        if ctx.author in self.bot.games and nums:
            game = self.bot.games[ctx.author]
            # board = self.bot.boards[ctx.author]

            print("args", nums, type(game))

            if not game.valid_guess(nums):
                await ctx.send(game.log_msg)
                return

            game.add_round(nums)
            guess_str = f"Guess {game.round_number}: `{', '.join(map(str, game.rounds[-1]))}`"
            match_str = f"{game.matches[-1]} match(es)"
            game.board.add_field(name=guess_str, value=match_str, inline=False)
            # game.board += f"{guess_str}\n{match_str}\n"

            # TODO better code for this error thing
            if game.game_over:
                await ctx.send(f"{ctx.author.mention}, {game.log_msg}")
                self.reset_game(ctx)
                return

            await ctx.send(embed=discord.Embed(title=f"Guess {game.round_number}", description=f"{game.matches[-1]} of guessed numbers match the winning combo"))

    @commands.command(aliases=["sh"])
    async def show(self, ctx):
        """Shows the full guess history of the user's current game"""

        if ctx.author in self.bot.games:
            await ctx.send(embed=self.bot.games[ctx.author].board)
        else:
            await ctx.send("User is not in a game")

    @commands.command(aliases=["lv"])
    async def leave(self, ctx):
        """Leaves the user's current game"""

        if ctx.author in self.bot.games:
            await ctx.send("Left game")
            self.reset_game(ctx)
        else:
            await ctx.send("User is not in a game")

    @commands.command(aliases=["sv"])
    async def solve(self, ctx):
        ## TODO fix keyerror bug
        print(ctx)
        solution = ClassicSolver(self.bot.games[ctx.author].rounds, self.bot.games[ctx.author].matches)
        solution.solve()
        await ctx.send(embed=solution.sol_panel)

    def reset_game(self, ctx):
        self.bot.games.pop(ctx.author)


def setup(bot):
    bot.add_cog(Gameplay(bot))
