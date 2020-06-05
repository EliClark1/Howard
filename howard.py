import asyncio
import jedit
from os import remove
from random import choice, randint

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from gtts import gTTS

import markov
from downloadimg import download

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_message(msg):
	await bot.process_commands(msg)

	def check(m):
		return m.channel == msg.channel and m.author == msg.author

	def check2(m):
		return m.channel == msg.channel and m.author.id != 452343038887329803 and "what" in m.content

	def check3(m):
		return m.channel == msg.channel and m.author.id != 452343038887329803 and "howard" in m.content

	try:
		if " " in msg.content:
			markov.write("markov.db", msg.content)

		if "egg" in msg.content.lower().replace(" ", ""):
			await msg.add_reaction("🥚")

		if msg.content.lower() == "are these men gonna hurt us walter?":
			await msg.channel.send("no donny these men are cowards")

		if "<@52343038887329803>" in msg.content:
			await msg.channel.trigger_typing()

			split = msg.content.split()
			split.remove("<@52343038887329803>")
			c = 20

			if "count=" in split:
				i = split.index("count=")
				del split[i]

				try:
					c = int(split[i])

					del split[i]
				except(ValueError):
					c = 20
			try:
				if len(split) > 0:
					message = markov.create("markov.db", word=choice(split), count=c)
				else:
					message = markov.create("markov.db", count=c)

				if randint(1, 5) == 1:
					word = choice(message.split())
					img = download(word)

				await msg.channel.send(message, file=discord.File(img[word][0]))

				remove(img[word][0])

				await bot.wait_for("message", check=check2, timeout=60)
				await msg.channel.send("it " + word)
				
			except(discord.errors.HTTPException):
				await msg.channel.send("what are you doing you give me httpexception")
			except(UnboundLocalError):
				await msg.channel.send(message)
			except(IndexError):
				await msg.channel.send(message)
			else:
				await msg.channel.send(message)
		elif randint(1, 5) == 1:
			await msg.channel.trigger_typing()

			if randint(1, 2) == 1:
				split = msg.content.split()

				try:
					message = markov.create("markov.db", word=choice(split), count=randint(20, 50))
				except(IndexError):
					message = markov.create("markov.db", count=randint(20, 50))
			else:
				message = markov.create("markov.db", count=randint(20, 50))

			if randint(1, 5) == 1:
				word = choice(message.split())
				img = download(word)

				await msg.channel.send(message, file=discord.File(img[word][0]))

				remove(img[word][0])

				await bot.wait_for("message", check=check2, timeout=60)
				await msg.channel.send("it " + word)
			else:
				await msg.channel.send(message)

		if "thans" in msg.content.lower() or "thank" in msg.content.lower():
			channel = msg.channel
			smsg = await channel.send("no problem")

			next = await bot.wait_for("message", check=check)

			if "no" in next.content:
				await smsg.delete()

	except(asyncio.TimeoutError):
		pass

token = YOURTOKENGOESHERE
bot.run(token)