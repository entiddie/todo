import discord
from discord.ext import commands
import json
from pymongo import MongoClient

uri = ""

cluster = MongoClient(uri)
db = cluster["todo"]
col = db["todo"]


def new_user(u_id):
    post = {"user": u_id}
    col.insert_one(post)


def add_array(u_id):
    q = {'user': u_id}
    values = {'$set': {'do': []}}
    values2 = {'$set': {'done': []}}

    col.update_one(q, values)
    col.update_one(q, values2)


def add_task(u_id, task):
    query = {'user': u_id}
    col.update(query, {'$push': {'do': task}})


def add_task_done(u_id, task):
    query = {'user': u_id}
    col.update(query, {'$push': {'done': task}})


def remove_task(u_id, index):
    query = {'user': u_id}
    for x in col.find(query):
        doc = x

    item = doc['do'][index]
    col.update(query, {'$pull': {'do': {item}}})


def task_list(u_id):
    query = {'user': u_id}
    for x in col.find(query):
        return x


emotes = {
    'pointer1': '<:pointer1:797104573310697534>',
    'pointer2': '<:pointer2:797104573881909278>',
}


class ToDo(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def add(self, ctx, *, task: str=None):

        if not task:
            e = discord.Embed(
                description="Usage: `todo add [task]`", color=0x2f3136
            )

            await ctx.send(embed=e)
            return

        user = ctx.author.id

        add_task(user, task)

        await ctx.send("Added task")

    
    @commands.command()
    async def done(self, ctx, *, task: str=None):

        if not task:
            e = discord.Embed(
                description="Usage: `todo done [task]`", color=0x2f3136
            )

            await ctx.send(embed=e)
            return

        user = ctx.author.id

        add_task_done(user, task)

        await ctx.send("Added task")

    
    @commands.command()
    async def list(self, ctx):

        user = ctx.author.id

        x = dict(task_list(user))

        if col.count({'user': user}) == 0:
            await ctx.send("You have no tasks in your list")

        else:

            tasks_do = f'\n<:pointer1:797104573310697534> '.join(x['do'])
            tasks_do = '<:pointer1:797104573310697534> ' + tasks_do 

            tasks_done = f'\n<:pointer2:797104573881909278> '.join(x['done'])
            tasks_done = '<:pointer2:797104573881909278> ' + tasks_done
            
            if len(x['do']) == 0:
                e = discord.Embed(
                    color=0x2f3136,
                    description=f"{tasks_done}"
                )

                e.set_author(name=f"{ctx.author.display_name}'s Todo List", icon_url=ctx.author.avatar_url)

                await ctx.send(embed=e)

            elif len(x['done']) == 0:
                e = discord.Embed(
                    color=0x2f3136,
                    description=f"{tasks_do}"
                )

                e.set_author(name=f"{ctx.author.display_name}'s Todo List", icon_url=ctx.author.avatar_url)

                await ctx.send(embed=e)

            else:
                e = discord.Embed(
                    color=0x2f3136,
                    description=f"{tasks_do}\n{tasks_done}"
                )

                e.set_author(name=f"{ctx.author.display_name}'s Todo List", icon_url=ctx.author.avatar_url)

                await ctx.send(embed=e)

        
def setup(client):
    client.add_cog(ToDo(client))
