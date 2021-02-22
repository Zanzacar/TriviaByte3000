import configparser
import os
from OpenTDB import OpenTDB

import discord
import asyncio

apiToke = ''

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read('config.ini')
    apiToken = config['api']['token']
else:
    print('Missing API Token/Config file')


class MyClient(discord.Client):

    async def on_ready(self):
        self.trivia = OpenTDB()
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!Q'):
            print(message.author)
            question = f'{self.trivia.get_category()} - {self.trivia.get_difficulty()}\n'
            question += self.trivia.get_question() + '\n'
            for a in self.trivia.get_all_answers():
                question += f'{a}: {self.trivia.answers[a]} \n'
            question += 'Enter Selection: \n'
            await message.channel.send(question)

            def is_correct(m):
                return m.author == message.author

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=60.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long it was {}.'.format(self.trivia.get_correct_answer()))

            if self.trivia.check_answer(guess.content) == True:
                await message.channel.send('You are right!')
                self.trivia.next_question()
            elif self.trivia.check_answer(guess.content) == False:
                await message.channel.send('Oops. It is actually {}.'.format(self.trivia.get_correct_answer()))
                self.trivia.next_question()
            else:
                await message.channel.send('Invalid Input')
                self.trivia.next_question()

client = MyClient()
client.run(apiToken)
