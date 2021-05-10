from asyncio import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message

from .. import queues
from ..callsmusic import callsmusic
from ..helpers.decorators import authorized_users_only
from ..helpers.decorators import errors
from ..helpers.filters import command
from ..helpers.filters import other_filters


@Client.on_message(command('pause') & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    (
        await message.reply_text('Paused!', False)
    ) if (
        callsmusic.pause(message.chat.id)
    ) else (
        await message.reply_text('Nothing is playing!', False)
    )


@Client.on_message(command('resume') & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    (
        await message.reply_text('Resumed!', False)
    ) if (
        callsmusic.resume(message.chat.id)
    ) else (
        await message.reply_text('Nothing is paused!', False)
    )


@Client.on_message(command('stop') & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text('Nothing is playing!', False)
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass
        await callsmusic.stop(message.chat.id)
        await message.reply_text('Cleared the queue and left the call!', False)


@Client.on_message(command('skip') & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text('Nothing is playing!', False)
    else:
        queues.task_done(message.chat.id)
        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
        else:
            await callsmusic.set_stream(
                message.chat.id,
                queues.get(message.chat.id)['file'],
            )
        await message.reply_text('Skipped!', False)


@Client.on_message(command('mute') & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(message.chat.id)
    (
        await message.reply_text('Muted!', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('Already muted!', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('Not in voice chat!', False)
    )


@Client.on_message(command('unmute') & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(message.chat.id)
    (
        await message.reply_text('Unmuted!', False)
    ) if (
        result == 0
    ) else (
        await message.reply_text('Not muted!', False)
    ) if (
        result == 1
    ) else (
        await message.reply_text('Not in voice chat!', False)
    )
