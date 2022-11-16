from aiogram import types
import model
import messages
import random
from create_bot import bot

async def start(message: types.Message):
    model.setCount(150)
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}.\n\n{messages.menu}')

async def game(message: types.Message):
    model.setFirstTurn()
    firstTurn = model.getFirstTurn()
    if firstTurn:
        await bot.send_message(message.from_user.id, messages.first_move_player)
        await playerTake(message)
        await playerTurn(message)
    else:
        await bot.send_message(message.from_user.id, messages.first_move_bot)
        await enemyTurn(message)

async def playerTake(message: types.Message):
    await bot.send_message(message.from_user.id, f'{message.from_user.username}, {messages.enter}')

async def enemyTurn(message: types.Message):
    count = model.getCount()
    take = count%29 if count%29 != 0 else random.randint(1, 28)
    model.setTake(take)
    model.setCount(count - take)
    await bot.send_message(message.from_user.id, f'Бот взял {model.getTake()} конфет. На столе осталось {model.getCount()}')
    if model.checkWin():
        await bot.send_message(message.from_user.id, messages.bot_win)
        await bot.send_message(message.from_user.id, messages.menu)
        return
    await playerTake(message)

async def playerTurn(message: types.Message):
    take = None
    if message.text.isdigit():
        if int(message.text) == 0:
            await bot.send_message(message.from_user.id, messages.equal_zero)
            await playerTake(message)
        elif int(message.text) > 28:
            await bot.send_message(message.from_user.id, messages.more)
            await playerTake(message)
        else:
            take = int(message.text)
            model.setTake(int(message.text))
            model.setCount(model.getCount() - take)
            await bot.send_message(message.from_user.id, f'Вы взяли {take} конфет. На столе осталось {model.getCount()}')
            if model.checkWin():
                await bot.send_message(message.from_user.id, messages.player_win)
                await bot.send_message(message.from_user.id, messages.menu)
                return
            await enemyTurn(message)
    else:
        await bot.send_message(message.from_user.id, messages.uncorrect_enter)
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, messages.help)

async def finish(message: types.Message):
    await bot.send_message(message.from_user.id, f'Пока! \nСпасибо, что сыграл со мной')
    model.setCount(150)

