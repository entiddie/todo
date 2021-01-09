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

    col.update_one(q, values)


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

    
    @commands.command(aliases=['task', 'new'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def add(self, ctx, *, task: str=None):

        if not task:
            e = discord.Embed(
                description="Usage: `todo add [task]`", color=0x2f3136
            )

            await ctx.send(embed=e)
            return

        if len(task) > 250:
            await ctx.send("Task cannot contain more than 250 characters")
            return

        user = ctx.author.id

        if col.count({'user': user}) == 0:
            new_user(user)

        add_task(user, task)

        await ctx.send("Added task")


    @commands.command(aliases=['done', 'delete'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, index=None):

        if not index:
            u_id = ctx.author.id

            query = {'user': u_id}
            for x in col.find(query):
                doc = x

            dos = doc['do']

            li = []

            for i in range(len(dos)):
                li.append(f"{i+1}: {dos[i]}")

            mes = '\n'.join(li)

            e = discord.Embed(
                color=0x2f3136, description=f"{mes}"
            )

            e.set_author(name="Removable Tasks", icon_url=ctx.author.avatar_url)
            e.set_footer(text="todo remove [index] to remove a task")

            await ctx.send(embed=e)
        
        else:
            try:
                u_id = ctx.author.id

                query = {'user': u_id}
                for x in col.find(query):
                    doc = x

                dos = doc['do']

                dos.pop(int(index)-1)

                q = {'user': u_id}
                values = {'$set': {'do': dos}}

                col.update_one(q, values)

                await ctx.send("Removed task")

            except:
                await ctx.send("Range out of index")


    @commands.command(aliases=['all'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list(self, ctx):

        user = ctx.author.id

        if col.count({'user': user}) == 0:
            await ctx.send("You have no tasks in your list")

        else:

            x = dict(task_list(user))

            if len(x['do']) == 0:
                await ctx.send("You have no tasks in your list")
                return

            tasks_do = f'\n<:pointer1:797104573310697534> '.join(x['do'])
            tasks_do = '<:pointer1:797104573310697534> ' + tasks_do

            if len(tasks_do) > 2000:
                tasks_do[:2000] + ...

            # tasks_done = f'\n<:pointer2:797104573881909278> '.join(x['done'])
            # tasks_done = '<:pointer2:797104573881909278> ' + tasks_done
            
            e = discord.Embed(
                color=0x2f3136,
                description=f"{tasks_do}"
            )

            e.set_author(name=f"{ctx.author.display_name}'s Todo List", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=e)

        
def setup(client):
    client.add_cog(ToDo(client))
