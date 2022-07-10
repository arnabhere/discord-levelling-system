import discord
from discord import File
import json
from discord.ext import commands
from easy_pil import Editor, Font, load_image_async

class ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, user:discord.Member = None):
        if user is None:
            user = ctx.author
        with open("data.json", "r") as f:
            user_data = json.load(f)
        id = user.id
        
        if str(id) in user_data:
            xp_have = user_data[str(id)]["xp"]
            xp_need = (user_data[str(id)]["level"] + 1) ** 3
            xp_percent = (xp_have/xp_need) * 100
        
                    
            poppins = Font("assets/poppins.ttf", size = 38)
            smallPoppins = Font("assets/poppins.ttf", size = 23)

            background = Editor("assets/bg.png")
            pfp = await load_image_async(str(user.avatar.url))
            pfp = Editor(pfp).resize((130,130)).circle_image()

            background.paste(pfp.image, ((50,45)))
            background.rectangle((50,210), width=650, height=40, fill="white", radius=20)
            background.bar((50,210), max_width=650, height=40,percentage=xp_percent ,fill="#621df2", radius=20)
            
            background.text((200,70), str(user), color="white", font = poppins)
            background.rectangle((200,120), width=350, height=2, fill="white", radius=20)
            background.text((200,140), f"Level - {user_data[str(user.id)]['level']}     {xp_have}/{xp_need}XP", color="white", font = smallPoppins)
            
            
            file = File(fp=background.image_bytes, filename="card.png")
            await ctx.send(file=file)
        else:
            with open("data.json", "r") as f:
                user = json.load(f)
            if str(id) not in user:
                user[str(id)] = {}
                user[str(id)]['xp'] = 0
                user[str(id)]['level'] = 1
                await ctx.reply("We just updated the database\nUse`?rank` again to check rank")
            with open("data.json", "w") as f:
                json.dump(user, f, indent=4)

                    