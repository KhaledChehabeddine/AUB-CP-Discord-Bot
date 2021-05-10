from cDatabase.DB_Users import DB_Users
from cDatabase.KV_Database import KV_Database
import discord, json

config = json.load(open('config.json', 'r'))

db_users = DB_Users("db_users")
cf_ranking = KV_Database('CodeForces_Ranking')

class User:
    id = None
    handle = None
    client = None

    def __init__(self, id = '', handle = '', client = None):
        if (id != '' and handle != ''):
            self.id, self.handle = id, handle
        elif (id != ''):
            self.id = id
            self.handle = db_users.find_handle(id)
        elif (handle != ''): 
            self.id = db_users.find_id(handle)
            self.handle = handle
        self.client = client

    def is_admin(self):
        if self.id in [
            '763289145288032268',
            '763319277540605972',
            '763345404674048020',
            '402887362046066698'
        ]: return True
        return False

    def tag(self):
        return '<@!' + str(self.id) + '>'

    def is_taken_id(self):
        if (self.id == None): return True
        return db_users.is_taken_id(self)

    def is_taken_handle(self):
        if (self.handle == None): return True
        return db_users.is_taken_handle(self)

    def is_registered(self):
        if (self.id == None or self.handle == None): return False
        return db_users.is_registered(self)

    def register(self):
        if (self.id == None or self.handle == None): return False
        return db_users.register(self)

    def change_handle(self, new_handle):
        if (self.handle == new_handle): return False
        if (not self.is_registered()): return False
        self.handle = new_handle
        return db_users.change_handle(self, new_handle)

    def delete(self):
        # Add remove from contests
        if (self.id == None or self.handle == None): return False
        return db_users.remove_user(self)

    def __str__(self):
        return "User: " + str(self.id) + ' ' + str(self.handle)

    async def add_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        await member.add_roles(role)

    async def get_roles(self):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        return member.roles

    async def has_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        return role in member.roles

    async def remove_role(self, _role):
        guild = self.client.get_guild(config['guild_id'])
        member = await guild.fetch_member(int(self.id))
        role = discord.utils.get(member.guild.roles, name = _role)
        await member.remove_roles(role)

    async def get_lower_roles(self, role):
        roles = await self.get_roles()
        x = cf_ranking.get(role)
        lst = []
       
        for r in roles:
          if r.name in cf_ranking.keys() and cf_ranking.get(r.name) < x:
            lst.append(r.name)

        return lst

