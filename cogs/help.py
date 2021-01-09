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
`todo remove` - List of removable items
'''
        )
        
        e.set_footer(text='Stable v1.0 ∙ todo info to get started')

        e.set_author(name='AnyDo Help Module', icon_url=self.client.user.avatar_url)

        await ctx.send(embed=e)


    @commands.command()
    async def info(self, ctx):
        e = discord.Embed(
            color=0x2f3136,
            description='''
Hello, new user. I am a todo list bot. Get started by using todo help. This bot is by no means associated with the AnyDo App on Playstore and Appstore            
'''
        )

        e.set_footer(text='Created by the Aizor Studio Team')

        await ctx.send(embed=e)

    
    @commands.command()
    async def invite(self, ctx):
        e = discord.Embed(
            color=0x2f3136, description='You can invite me using this link: [Invite](https://discord.com/api/oauth2/authorize?client_id=792111431708704768&permissions=52224&scope=bot)'
        )

        await ctx.send(embed=e)

        
def setup(client):
    client.add_cog(Help(client))
