import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def help(self, ctx):
        e = discord.Embed(
            color=0x2f3136,
            description='''
`todo add [task]` - Adds a new task to your ToDo list
`todo list` - Returns a list of your tasks
'''
        )
        
        e.set_footer(text='The prefix is todo')

        e.set_author(name='AnyDo Help Module', icon_url=self.client.user.avatar_url)

        await ctx.send(embed=e)

        
def setup(client):
    client.add_cog(Help(client))
