import discord #pycord
import os
from dotenv import load_dotenv

TOKEN = os.environ['TOKEN']
load_dotenv()
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

stack = dict()


@bot.event
async def on_ready():
	print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(message):
	if not message.channel.id in stack:
		stack.setdefault(message.channel.id, message)
	else:
		stack.update({message.channel.id: message})


class Button(discord.ui.View):
	def __init__(self, thread):
		super().__init__()
		self.thread = thread

	@discord.ui.button(label="보관", style=discord.ButtonStyle.success, emoji="📁")
	async def archive(self, button, interaction):
		await interaction.response.send_message("이 스레드는 보관되었습니다. 아무나 메시지를 보내 보관해제할 수 있습니다.")
		await self.thread.edit(archived=True)

	@discord.ui.button(label="잠금", style=discord.ButtonStyle.danger, emoji="🔒")
	async def lock(self, button, interaction):
		await interaction.response.send_message("이 스레드는 잠겼습니다. 오직 관리자만이 잠금해제할 수 있습니다.")
		await self.thread.edit(locked=True)


@bot.slash_command(name="thread", description="이전의 메시지에 스레드를 생성합니다.")
async def thread(ctx, auto_archive_duration=10080):
	message = stack[ctx.channel.id]
	thread = await message.create_thread(name=message.content[:50], auto_archive_duration=int(auto_archive_duration))
	await ctx.respond("성공!", ephemeral=True)
	await thread.send("<@&1077985851562278922>", view=Button(thread))


bot.run(TOKEN)
