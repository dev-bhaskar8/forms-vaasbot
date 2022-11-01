#pip install discord-ext-forms
from discord.discord.ext.forms import Form
from discord.ext import commands
import discord
import os
from keep_alive import keep_alive
import requests
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import pandas as pd
import gspread

sheetURL = "1LG4M_HO2f60q6AVuC5j4ud1u7vOIe3zbK47Cr_Yw-4Y"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command()
async def optimize(ctx):
    form = Form(ctx,'Optimization Form')
    form.add_question('Scholar number (Eg. YGG 1785):','first')
    form.add_question('Please enter 3 Old Axies (Eg. 3333,4444,5555) :','axieIds')
    form.add_question('Please enter 3 Axies with replaced Axie (Eg. 1111,4444,5555)','newAxieIds')
    form.add_question('Reason: \n(Bot takes some time to load output) ' ,'reason')
    form.edit_and_delete(True)
    await form.set_color("#7289DA")
    result = await form.start()
    axieIds = result.axieIds.split(',')
    newAxieIds = result.newAxieIds.split(',')
    axie_images = []
    new_axie_images = []
    for i in range(3):
        url = f'https://assets.axieinfinity.com/axies/{str(axieIds[i])}/axie/axie-full-transparent.png'
        response = Image.open(BytesIO(requests.get(url).content))
        axie_images.append(cv2.cvtColor(np.array(response), cv2.COLOR_RGB2BGR))

    for i in range(3):
        url = f'https://assets.axieinfinity.com/axies/{str(newAxieIds[i])}/axie/axie-full-transparent.png'
        response = Image.open(BytesIO(requests.get(url).content))
        new_axie_images.append(cv2.cvtColor(np.array(response), cv2.COLOR_RGB2BGR))

    axie_stack1 = cv2.hconcat([axie for axie in axie_images])
    axie_stack2 = cv2.hconcat([axie for axie in new_axie_images])
    final = np.vstack([axie_stack1, axie_stack2])
    axieStr = ""
    changes = ""
    for i  in range(3):
        if axieIds[i] != newAxieIds[i]:
            final = cv2.arrowedLine(final, (550+1300*(i),800), (550+1300*(i),1000),(0, 0, 255), 10, tipLength = 0.5)
            cv2.imwrite('final.png', final)
            url = f'https://api.axie.technology/getaxies/{newAxieIds[i]}'
            axieStr+= str(axieIds[i])+" , "
            response = requests.get(url).json()
            parts="Old Axie : "+axieStr[:-2]
            changes+="\nRequest to change to "+str(response['class'])+' Axie of parts - '
            for i in range(2,6):
                changes = changes+str(response['parts'][i]['name'])+',' 
            changes=changes[:-1]  
            changes+='\nAnd of stats - '+ str(response['stats']).split("\'__typename")[0][1:-1][:-1].replace("\'","")+"\n"
            parts+=changes+'Reason : '+result.reason
            embed = discord.Embed(title=result.first, description=parts)
            file = discord.File("/home/runner/forms/final.png", filename="final.png")
    embed.set_image(url="attachment://final.png")
    await ctx.channel.send(file=file,embed=embed)  

@bot.command()
async def ticket(ctx):
    gc = gspread.service_account(filename='manager-319201-3dc4c609fd55.json')
    sh = gc.open_by_key(sheetURL)
    worksheet = sh.get_worksheet(0)
    list_of_lists = worksheet.get_all_values()
    num = len(list_of_lists)
    form = Form(ctx,'Support Ticket')
    form.edit_and_delete(True)
    form.add_question('Your Email','first')
    form.add_question('Wallet Address','second')
    form.add_question('Description','third')
    form.add_question("Type 'yes' and press enter",'forth')
    result = await form.start()
    worksheet.update_cell(num+1, 1, result.first)
    worksheet.update_cell(num+1, 2, result.second)
    worksheet.update_cell(num+1, 3, result.third)

@bot.command(pass_context = True)
async def areyouhere(ctx,ID_OF_MEMBER):
    guild = ctx.guild
    if guild.get_member(int(ID_OF_MEMBER)):
      await ctx.channel.send("Yes")
    else:
      await ctx.channel.send("No")
    
keep_alive()
bot.run(os.getenv("MYTOKEN"))