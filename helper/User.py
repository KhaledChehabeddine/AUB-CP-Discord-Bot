import json
import discord
from cDatabase.DB_Users import DB_Users
import discord, json

config = json.load(open('config.json', 'r'))

config = json.load(open('config.json', 'r'))
database_users = DB_Users("db_users")

# ------------------------------------ { User } ------------------------------------ # 
    # ------------------ [ __init__() ] ------------------ # 
        # Initializes id and handle based on given parameters
    
    # ------------------ [ is_admin() ] ------------------ # 
        # Returns true if user is Ahmad, Khaled, Miguel, or MB, otherwise false
    
    # ------------------ [ tag() ] ------------------ # 
        # Tags the user that called the command

    # ------------------ [ is_taken_id() ] ------------------ # 
        # Checks if the ID is already registered
    
    # ------------------ [ is_taken_handle() ] ------------------ # 
        # Checks if an ID is already registered to another handle

    # ------------------ [ is_registered() ] ------------------ # 
        # Checks if user is in the database

    # ------------------ [ register() ] ------------------ # 
        # Registers the user to the bot's database

    # ------------------ [ change_handle() ] ------------------ # 
        # Changes the user's handle in the database

    # ------------------ [ delete() ] ------------------ # 
        # Deletes the user from the database

    # ------------------ [ __str__() ] ------------------ # 
        # Returns a string representation of the user with their id and handle
    
    # ------------------ [ add_role() ] ------------------ # 
        # Adds a role to the database
    
    # ------------------ [ get_roles() ] ------------------ # 
        # Retrieves the role from the database

    # ------------------ [ has_role() ] ------------------ # 
        # Creates a list of the roles of the user
        # Checks if the target role is in the list

class User:
    id = None
    handle = None
    client = None

    def __init__(self, id = '', handle = '', client = None):
        if (id != '' and handle != ''):
            self.id, self.handle = id, handle
        elif (id != ''):
            self.id = id
            self.handle = database_users.find_handle(id)
        elif (handle != ''): 
            self.id = database_users.find_id(handle)
            self.handle = handle
        self.client = client

    def is_admin(self):
        if self.id in [
            '763289145288032268',
            '763319277540605972',
            '763345404674048020',
            '402887362046066698']: return True
        return False

    def tag(self):
        return '<@!' + str(self.id) + '>'

    def is_taken_id(self):
        if (self.id == None): return True
        return database_users.is_taken_id(self)

    def is_taken_handle(self):
        if (self.handle == None): return True
        return database_users.is_taken_handle(self)

    def is_registered(self):
        if (self.id == None or self.handle == None): return False
        return database_users.is_registered(self)

    def register(self):
        if (self.id == None or self.handle == None): return False
        return database_users.register(self)

    def change_handle(self, new_handle):
        if (self.handle == new_handle): return False
        if (not self.is_registered()): return False
        self.handle = new_handle
        return database_users.change_handle(self, new_handle)

    def delete(self):
        if (self.id == None or self.handle == None): return False
        return database_users.remove_user(self)

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