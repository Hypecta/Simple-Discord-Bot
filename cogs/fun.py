from discord.ext import commands
import numpy as np

class Fun(commands.Cog, name="Fun"):
    '''Fun commands'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def box(self, ctx, *, sentence: str):
        '''Creates a box'''
        if len(sentence) % 2 == 1:
            diags = len(sentence) // 2 // 2
        else:
            diags = len(sentence[:len(sentence) // 2]) - 2
        ret = np.full(
            (len(sentence) + diags + 1, len(sentence) + diags + 1),
            " ",
            dtype=str
        )
        # do the first 4 edges
        ret[0, :len(sentence)] = list(sentence)
        ret[:len(sentence), 0] = list(sentence)
        ret[len(sentence)-1, :len(sentence)] = list(sentence)[::-1]
        ret[:len(sentence), len(sentence)-1] = list(sentence)[::-1]

        ret = np.roll(ret, diags+1, axis=0)
        ret = np.roll(ret, diags+1, axis=1)

        # do the next 4 edges
        ret[0, :len(sentence)] = list(sentence)
        ret[:len(sentence), 0] = list(sentence)
        ret[len(sentence)-1, :len(sentence)] = list(sentence)[::-1]
        ret[:len(sentence), len(sentence)-1] = list(sentence)[::-1]

        # complete the diagonal connections
        for i in range(diags):
            char = "\\"
            ret[i + 1, i + 1] = char
            ret[i + 1, len(sentence) + i] = char
            ret[len(sentence) + i, i + 1] = char
            ret[len(sentence) + i, len(sentence) + i] = char

        # turn it into a list of strings
        ret = [" ".join(row).rstrip() for row in ret]
        ret = "\n".join(ret)

        # replace 4 spaces with tabs for the character limit
        ret.replace("    ", "\t")
        await ctx.send(f'```\n{ret}\n```')
