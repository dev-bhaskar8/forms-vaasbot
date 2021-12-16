#pip install discord-ext-forms
from discord.discord.ext.forms import Form
from discord.ext import commands
import os
from keep_alive import keep_alive
bot = commands.Bot(command_prefix="$app")

@bot.command()
async def ly(ctx):
    form = Form(ctx,'Scholarship Form')
    form.add_question('What is your age?','first')
    form.add_question('Big fan of Vaas?','second')
    form.add_question('Apply for scholarship or grab a beer?','third')
    form.add_question('You have applied for scholarship, please wait for us to get back. Respond with "ok" to end prompt.','fourth')
    form.edit_and_delete(True)
    form.set_timeout(60)
    await form.set_color("#7289DA")
    result = await form.start()
    return result

keep_alive()
bot.run(os.getenv("TOKEN"))