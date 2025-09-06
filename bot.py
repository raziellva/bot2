lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl, lllllllllllIlII, lllllllllllIIll, lllllllllllIIlI, lllllllllllIIIl, lllllllllllIIII, llllllllllIllll, llllllllllIlllI, llllllllllIllIl = max, __name__, Exception, locals, enumerate, next, dict, len, round, bool, int, isinstance, list, abs, set, min, str, ValueError, float

from logging import getLogger as lIIlIIIIlIlIIl, INFO as IIIIlllIIIIlII, StreamHandler as lIIlIIlllllIIl, basicConfig as llIIllIIIlIllI, FileHandler as IIIIlllIIllIII
from asyncio import get_running_loop as lIIIIIIIllllll, PriorityQueue as lIlIlIlIIIIlll, set_event_loop as lIlllIIllIIlIl, sleep as lIllIllIlIIlII, new_event_loop as IIIIIIllIllIIl, create_task as lIIIlIlIlIIIlI
from datetime.datetime import now as lIlIlIIllllIll
from datetime import datetime as IlIllllIIIIllI, timedelta as IIlIIlIlIlllII
from random import choices as IIIllIlIlIIIlI
from string import digits as IIlIIIIlIllIll, ascii_letters as lIlllIIIlIlllI
from time import time as IIllIlIIlIllII
from os.path import getsize as IIIlIIIllIlIII, exists as lllllIIlIlIllI, splitext as IlIlIIIIlIIllI
from os import remove as IIlllllIlIllll
from ffmpeg import input as IIlIIIIIlllIll, probe as lllIllIlIIIIll
from subprocess import PIPE as lIlIIlIlllIIIl, Popen as lIlIIIlllIlIlI
from re import compile as lIlIIlllIIIIIl
from pyrogram import Client as lIllIlIIllllll, filters as IIlllIlIIllllI
from pyrogram.types import Message as llllllIlllIlIl, InlineKeyboardButton as llIlIIlIlllIII, InlineKeyboardMarkup as IlIIlIIllllIlI, ReplyKeyboardMarkup as llIIIIllIIllIl, KeyboardButton as IIlllIllIIIIll, CallbackQuery as IIllllllllIlIl
from pyrogram.errors import MessageNotModified as IIlllIIlIlllII
from pymongo import MongoClient as lIlIIlllllIlII
from config import *
from bson.objectid import ObjectId as IIllIIlIlIlIlI
llIIllIIIlIllI(level=IIIIlllIIIIlII, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=[IIIIlllIIllIII('bot.log'), lIIlIIlllllIIl()])
llIlllIIllIIlIIlll = lIIlIIIIlIlIIl(llllllllllllllI)
llIIIIIIIIlIIIllll = {'premium': 1, 'pro': 2, 'standard': 3}
IIllllIIllIllIllll = 5
lIllIlllIIIlIIIIIl = lIlIIlllllIlII(MONGO_URI)
IllllIlIllllllllll = lIllIlllIIIlIIIIIl[DATABASE_NAME]
IIlIlIIIlIIlIlIIlI = IllllIlIllllllllll['pending']
llIIllIIllIllIIlll = IllllIlIllllllllll['users']
lIlIIlllIIIIIlIIIl = IllllIlIllllllllll['temp_keys']
lllllIlIllIlIIlIll = IllllIlIllllllllll['banned_users']
IIIIlllIIIIIlIIIlI = IllllIlIllllllllll['pending_confirmations']
IlIIIIllIlIllIllIl = IllllIlIllllllllll['active_compressions']
IlIlIIllIIIlllIlll = API_ID
IIIllIIIIIIlIIllll = API_HASH
lllllIlIlIllIlIlll = BOT_TOKEN
IIIlIIIIlIIIIlllII = lIllIlIIllllll('compress_bot', api_id=IlIlIIllIIIlllIlll, api_hash=IIIllIIIIIIlIIllll, bot_token=lllllIlIlIllIlIlll)
lllIIIlIllIlllIIII = ADMINS_IDS
IIIIlllIlllllIIlll = []
IlllllIIIIlIIIIlll = lllllIlIllIlIIlIll.find({}, {'user_id': 1})
for lIIlIIIIIIlIlllIII in IlllllIIIIlIIIIlll:
    if lIIlIIIIIIlIlllIII['user_id'] not in IIIIlllIlllllIIlll:
        IIIIlllIlllllIIlll.append(lIIlIIIIIIlIlllIII['user_id'])
IlIIIIllIlIllIllIl.delete_many({})
llIlllIIllIIlIIlll.info('Compresiones activas previas eliminadas')
IIlllIlIlIlIllllIl = {'resolution': '854x480', 'crf': '28', 'audio_bitrate': '120k', 'fps': '22', 'preset': 'veryfast', 'codec': 'libx264'}
IlIIllIIllllIllIII = lIlIlIlIIIIlll()
IlIIlIIlIIlllIIIll = None
IlIllIIIIlllIIlIIl = concurrent.futures.ThreadPoolExecutor(max_workers=1)
lllIlIlIIlIIIIlllI = lllllllllllIIIl()
IllIlIIIIIlIlIlIIl = {}

def lIlllIllllIlIIllIl(lIllIIIIllIIIllIlI, IIIIlIIllIIIIIIIII, IIIIlIlIIlIlllIIll, llllIIIllIIIIlllII=None):
    """Registra una tarea que puede ser cancelada"""
    IllIlIIIIIlIlIlIIl[lIllIIIIllIIIllIlI] = {'type': IIIIlIIllIIIIIIIII, 'task': IIIIlIlIIlIlllIIll, 'original_message_id': llllIIIllIIIIlllII}

def IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI):
    """Elimina el registro de una tarea cancelable"""
    if lIllIIIIllIIIllIlI in IllIlIIIIIlIlIlIIl:
        del IllIlIIIIIlIlIlIIl[lIllIIIIllIIIllIlI]

def IIlIIllIIIIllIlIII(lIllIIIIllIIIllIlI):
    """Cancela la tarea activa de un usuario"""
    if lIllIIIIllIIIllIlI in IllIlIIIIIlIlIlIIl:
        IIlIlIllIlIIIIlIII = IllIlIIIIIlIlIlIIl[lIllIIIIllIIIllIlI]
        try:
            if IIlIlIllIlIIIIlIII['type'] == 'download':
                return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            elif IIlIlIllIlIIIIlIII['type'] == 'ffmpeg' and IIlIlIllIlIIIIlIII['task'].poll() is None:
                IIlIlIllIlIIIIlIII['task'].terminate()
                return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
            elif IIlIlIllIlIIIIlIII['type'] == 'upload':
                return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error cancelando tarea: {lIlllllIIIIllIIIIl}')
    return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('cancel') & IIlllIlIIllllI.private)
async def llIlIIIlIIIIlIlIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Maneja el comando de cancelación"""
    lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
    if lIllIIIIllIIIllIlI in IllIlIIIIIlIlIlIIl:
        if IIlIIllIIIIllIlIII(lIllIIIIllIIIllIlI):
            llllIIIllIIIIlllII = IllIlIIIIIlIlIlIIl[lIllIIIIllIIIllIlI].get('original_message_id')
            IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '⛔ **Operación cancelada por el usuario** ⛔', reply_to_message_id=llllIIIllIIIIlllII)
        else:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '⚠️ **No se pudo cancelar la operación**\nLa tarea podría haber finalizado ya.')
    else:
        lIlIlllllllIIIlIII = IIlIlIIIlIIlIlIIlI.delete_many({'user_id': lIllIIIIllIIIllIlI})
        if lIlIlllllllIIIlIII.deleted_count > 0:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, f'⛔ **Se cancelaron {lIlIlllllllIIIlIII.deleted_count} tareas pendientes en la cola.** ⛔')
        else:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, 'ℹ️ **No tienes operaciones activas ni en cola para cancelar.**')
    try:
        await IIIlIlIlIIlllIllII.delete()
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error borrando mensaje /cancel: {lIlllllIIIIllIIIIl}')

async def IIlIllIlllIIlIlllI(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIllI:
    """Verifica si el usuario ya tiene una compresión activa"""
    return lllllllllllIllI(IlIIIIllIlIllIllIl.find_one({'user_id': lIllIIIIllIIIllIlI}))

async def llIIlIIIllIIlIllIl(lIllIIIIllIIIllIlI: lllllllllllIlIl, IIIllIIIlIlIlIlIIl: llllllllllIllll):
    """Registra una nueva compresión activa"""
    IlIIIIllIlIllIllIl.insert_one({'user_id': lIllIIIIllIIIllIlI, 'file_id': IIIllIIIlIlIlIlIIl, 'start_time': lIlIIIlllIIIIIlIII()})

async def llllIIIllIIIllIIlI(lIllIIIIllIIIllIlI: lllllllllllIlIl):
    """Elimina una compresión activa"""
    IlIIIIllIlIllIllIl.delete_one({'user_id': lIllIIIIllIIIllIlI})

async def IlllIlIllIllllIIll(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIllI:
    """Verifica si el usuario tiene una confirmación pendiente (no expirada)"""
    lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
    IlllIllIllIIIIIIII = lIlIIIlllIIIIIlIII - IIlIIlIlIlllII(minutes=10)
    IIIIlllIIIIIlIIIlI.delete_many({'user_id': lIllIIIIllIIIllIlI, 'timestamp': {'$lt': IlllIllIllIIIIIIII}})
    return lllllllllllIllI(IIIIlllIIIIIlIIIlI.find_one({'user_id': lIllIIIIllIIIllIlI}))

async def IlIlIlIIlIIllIIIll(lIllIIIIllIIIllIlI: lllllllllllIlIl, lIlIIlIIllIlIIIIIl: lllllllllllIlIl, llIlIIIllIlIlllIIl: lllllllllllIlIl, IIIllIIIlIlIlIlIIl: llllllllllIllll, IlIIllIlllIIIllIII: llllllllllIllll):
    """Crea una nueva confirmación pendiente eliminando cualquier confirmación previa"""
    IIIIlllIIIIIlIIIlI.delete_many({'user_id': lIllIIIIllIIIllIlI})
    return IIIIlllIIIIIlIIIlI.insert_one({'user_id': lIllIIIIllIIIllIlI, 'chat_id': lIlIIlIIllIlIIIIIl, 'message_id': llIlIIIllIlIlllIIl, 'file_id': IIIllIIIlIlIlIlIIl, 'file_name': IlIIllIlllIIIllIII, 'timestamp': lIlIIIlllIIIIIlIII()}).inserted_id

async def llIllllllllIlllIll(IIlIIllIlIllIIIlII: IIllIIlIlIlIlI):
    """Elimina una confirmación pendiente"""
    IIIIlllIIIIIlIIIlI.delete_one({'_id': IIlIIllIlIllIIIlII})

async def lIlIlllllIIIIllIIl(IIlIIllIlIllIIIlII: IIllIIlIlIlIlI):
    """Obtiene una confirmación pendiente"""
    return IIIIlllIIIIIlIIIlI.find_one({'_id': IIlIIllIlIllIIIlII})

async def lIlIllllIlIlIllllI(lIllIIIIllIIIllIlI: lllllllllllIlIl):
    """Registra un nuevo usuario si no existe"""
    if not llIIllIIllIllIIlll.find_one({'user_id': lIllIIIIllIIIllIlI}):
        llIlllIIllIIlIIlll.info(f'Usuario no registrado: {lIllIIIIllIIIllIlI}')

async def lIIIIIlllIIIlIllll(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIllI:
    """Determina si el contenido debe protegerse según el plan del usuario"""
    if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
        return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    return lIllIlIIIllIIIlIll is None or lIllIlIIIllIIIlIll['plan'] == 'standard'

async def lIIlIlllIllllIllII(lIlIIlIIllIlIIIIIl: lllllllllllIlIl, IllllIIIlllllIIIll: llllllllllIllll, **llIIIlIIllIIIIIIII):
    """Envía un mensaje con protección según el plan del usuario"""
    IIIIlIIIlIlIIIllll = await lIIIIIlllIIIlIllll(lIlIIlIIllIlIIIIIl)
    return await IIIlIIIIlIIIIlllII.send_message(lIlIIlIIllIlIIIIIl, IllllIIIlllllIIIll, protect_content=IIIIlIIIlIlIIIllll, **llIIIlIIllIIIIIIII)

async def llIIlIIIllIlIIIlII(lIlIIlIIllIlIIIIIl: lllllllllllIlIl, llIIlIIIlllllIllII: llllllllllIllll, lIllIllIIIIlllIIll: llllllllllIllll=None, **llIIIlIIllIIIIIIII):
    """Envía un video con protección según el plan del usuario"""
    IIIIlIIIlIlIIIllll = await lIIIIIlllIIIlIllll(lIlIIlIIllIlIIIIIl)
    return await IIIlIIIIlIIIIlllII.send_video(lIlIIlIIllIlIIIIIl, llIIlIIIlllllIllII, caption=lIllIllIIIIlllIIll, protect_content=IIIIlIIIlIlIIIllll, **llIIIlIIllIIIIIIII)

async def lllllIIIIIlIIlllll(lIlIIlIIllIlIIIIIl: lllllllllllIlIl, lIIlIlIlIllIllllll: llllllllllIllll, lIllIllIIIIlllIIll: llllllllllIllll=None, **llIIIlIIllIIIIIIII):
    """Envía una foto con protección según el plan del usuario"""
    IIIIlIIIlIlIIIllll = await lIIIIIlllIIIlIllll(lIlIIlIIllIlIIIIIl)
    return await IIIlIIIIlIIIIlllII.send_photo(lIlIIlIIllIlIIIIIl, lIIlIlIlIllIllllll, caption=lIllIllIIIIlllIIll, protect_content=IIIIlIIIlIlIIIllll, **llIIIlIIllIIIIIIII)

async def IllIIllIIIlIIlIlII(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIlIl:
    """Obtiene la prioridad del usuario basada en su plan"""
    lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIlIIIllIIIlIll is None:
        return 4
    return llIIIIIIIIlIIIllll.get(lIllIlIIIllIIIlIll['plan'], 4)

def lllllIlIIllIlIIIIl(llIIllllIlIlIIllII: llllllllllIllll, IlIIIIIIlllIIIlllI: lllllllllllIlIl, lIIlIIlIIlIllIIIlI: llllllllllIllll):
    """Genera una clave temporal válida para un plan específico"""
    lIllIlIlIlIIlIllII = ''.join(IIIllIlIlIIIlI(lIlllIIIlIlllI + IIlIIIIlIllIll, k=10))
    IIlIllIlIlIlIlIlll = lIlIIIlllIIIIIlIII()
    if lIIlIIlIIlIllIIIlI == 'minutes':
        lllIlIIllllllIlIII = IIlIllIlIlIlIlIlll + IIlIIlIlIlllII(minutes=IlIIIIIIlllIIIlllI)
    elif lIIlIIlIIlIllIIIlI == 'hours':
        lllIlIIllllllIlIII = IIlIllIlIlIlIlIlll + IIlIIlIlIlllII(hours=IlIIIIIIlllIIIlllI)
    else:
        lllIlIIllllllIlIII = IIlIllIlIlIlIlIlll + IIlIIlIlIlllII(days=IlIIIIIIlllIIIlllI)
    lIlIIlllIIIIIlIIIl.insert_one({'key': lIllIlIlIlIIlIllII, 'plan': llIIllllIlIlIIllII, 'created_at': IIlIllIlIlIlIlIlll, 'expires_at': lllIlIIllllllIlIII, 'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'duration_value': IlIIIIIIlllIIIlllI, 'duration_unit': lIIlIIlIIlIllIIIlI})
    return lIllIlIlIlIIlIllII

def lIIIlIlIIllIlllIIl(lIllIlIlIlIIlIllII):
    """Verifica si una clave temporal es válida"""
    lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
    llllIIllIlllIIIlIl = lIlIIlllIIIIIlIIIl.find_one({'key': lIllIlIlIlIIlIllII, 'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'expires_at': {'$gt': lIlIIIlllIIIIIlIII}})
    return lllllllllllIllI(llllIIllIlllIIIlIl)

def llIlllllIIlIllIIlI(lIllIlIlIlIIlIllII):
    """Marca una clave como usada"""
    lIlIIlllIIIIIlIIIl.update_one({'key': lIllIlIlIlIIlIllII}, {'$set': {'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)}})

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('generatekey') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def lIllllIllllIllIIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Genera una nueva clave temporal para un plan específico (solo admins)"""
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 4:
            await IIIlIlIlIIlllIllII.reply('⚠️ Formato: /generatekey <plan> <cantidad> <unidad>\nEjemplo: /generatekey standard 2 hours\nUnidades válidas: minutes, hours, days')
            return
        llIIllllIlIlIIllII = lllIlIIllIllIlIllI[1].lower()
        lIlIIlIIIIIIlIllII = ['standard', 'pro', 'premium']
        if llIIllllIlIlIIllII not in lIlIIlIIIIIIlIllII:
            await IIIlIlIlIIlllIllII.reply(f"⚠️ Plan inválido. Opciones válidas: {', '.join(lIlIIlIIIIIIlIllII)}")
            return
        try:
            IlIIIIIIlllIIIlllI = lllllllllllIlIl(lllIlIIllIllIlIllI[2])
            if IlIIIIIIlllIIIlllI <= 0:
                await IIIlIlIlIIlllIllII.reply('⚠️ La cantidad debe ser un número positivo')
                return
        except llllllllllIlllI:
            await IIIlIlIlIIlllIllII.reply('⚠️ La cantidad debe ser un número entero')
            return
        lIIlIIlIIlIllIIIlI = lllIlIIllIllIlIllI[3].lower()
        IllIIllIllIllIlIlI = ['minutes', 'hours', 'days']
        if lIIlIIlIIlIllIIIlI not in IllIIllIllIllIlIlI:
            await IIIlIlIlIIlllIllII.reply(f"⚠️ Unidad inválida. Opciones válidas: {', '.join(IllIIllIllIllIlIlI)}")
            return
        lIllIlIlIlIIlIllII = lllllIlIIllIlIIIIl(llIIllllIlIlIIllII, IlIIIIIIlllIIIlllI, lIIlIIlIIlIllIIIlI)
        IIllllIllIIlllIlll = f'{IlIIIIIIlllIIIlllI} {lIIlIIlIIlIllIIIlI}'
        if IlIIIIIIlllIIIlllI == 1:
            IIllllIllIIlllIlll = IIllllIllIIlllIlll[:-1]
        await IIIlIlIlIIlllIllII.reply(f'>🔑 **Clave {llIIllllIlIlIIllII.capitalize()} generada**\n\n>Clave: `{lIllIlIlIlIIlIllII}`\n>Válida por: {IIllllIllIIlllIlll}\n\nComparte esta clave con el usuario usando:\n`/key {lIllIlIlIlIIlIllII}`')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error generando clave: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al generar la clave')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('listkeys') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIIlIIlIIlIlIlIIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Lista todas las claves temporales activas (solo admins)"""
    try:
        lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
        IIlIlIIIlllIIIllll = lllllllllllIIll(lIlIIlllIIIIIlIIIl.find({'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), 'expires_at': {'$gt': lIlIIIlllIIIIIlIII}}))
        if not IIlIlIIIlllIIIllll:
            await IIIlIlIlIIlllIllII.reply('>📭 **No hay claves activas.**')
            return
        llIlIIIlIIllllllII = '>🔑 **Claves temporales activas:**\n\n'
        for lIllIlIlIlIIlIllII in IIlIlIIIlllIIIllll:
            lllIlIIllllllIlIII = lIllIlIlIlIIlIllII['expires_at']
            IIlIIllIIIllllIlll = lllIlIIllllllIlIII - lIlIIIlllIIIIIlIII
            if IIlIIllIIIllllIlll.IIIIlllIIIIlllIllI > 0:
                lIlllllIIIlIIllIlI = f'{IIlIIllIIIllllIlll.IIIIlllIIIIlllIllI}d {IIlIIllIIIllllIlll.seconds // 3600}h'
            elif IIlIIllIIIllllIlll.seconds >= 3600:
                lIlllllIIIlIIllIlI = f'{IIlIIllIIIllllIlll.seconds // 3600}h {IIlIIllIIIllllIlll.seconds % 3600 // 60}m'
            else:
                lIlllllIIIlIIllIlI = f'{IIlIIllIIIllllIlll.seconds // 60}m'
            IlIIIIIIlllIIIlllI = lIllIlIlIlIIlIllII.get('duration_value', 0)
            lIIlIIlIIlIllIIIlI = lIllIlIlIlIIlIllII.get('duration_unit', 'days')
            lIIIIlIlIlIllllIII = f'{IlIIIIIIlllIIIlllI} {lIIlIIlIIlIllIIIlI}'
            if IlIIIIIIlllIIIlllI == 1:
                lIIIIlIlIlIllllIII = lIIIIlIlIlIllllIII[:-1]
            llIlIIIlIIllllllII += f"• `{lIllIlIlIlIIlIllII['key']}`\n  ↳ Plan: {lIllIlIlIlIIlIllII['plan'].capitalize()}\n  ↳ Duración: {lIIIIlIlIlIllllIII}\n  ⏱ Expira en: {lIlllllIIIlIIllIlI}\n\n"
        await IIIlIlIlIIlllIllII.reply(llIlIIIlIIllllllII)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error listando claves: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al listar claves')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('delkeys') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IllIIlIIlIlllIllIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Elimina claves temporales (solo admins)"""
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) < 2:
            await IIIlIlIlIIlllIllII.reply('⚠️ Formato: /delkeys <key> o /delkeys --all')
            return
        IIlIllIIIllIIllIII = lllIlIIllIllIlIllI[1]
        if IIlIllIIIllIIllIII == '--all':
            lIlIlllllllIIIlIII = lIlIIlllIIIIIlIIIl.delete_many({})
            await IIIlIlIlIIlllIllII.reply(f'🗑️ **Se eliminaron {lIlIlllllllIIIlIII.deleted_count} claves.**')
        else:
            lIllIlIlIlIIlIllII = IIlIllIIIllIIllIII
            lIlIlllllllIIIlIII = lIlIIlllIIIIIlIIIl.delete_one({'key': lIllIlIlIlIIlIllII})
            if lIlIlllllllIIIlIII.deleted_count > 0:
                await IIIlIlIlIIlllIllII.reply(f'✅ **Clave {lIllIlIlIlIIlIllII} eliminada.**')
            else:
                await IIIlIlIlIIlllIllII.reply('⚠️ **Clave no encontrada.**')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error eliminando claves: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ **Error al eliminar claves**')
IIIllIIIllIllllIIl = {'standard': 60, 'pro': 130, 'premium': 280}
lllIIIIIIllIlllIII = {'standard': '7 días', 'pro': '15 días', 'premium': '30 días'}

async def IllllIIllllIIllIIl(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> llllllllllllIIl:
    """Obtiene el plan del usuario desde la base de datos y elimina si ha expirado"""
    lIllIIIlllIllIIlII = llIIllIIllIllIIlll.find_one({'user_id': lIllIIIIllIIIllIlI})
    lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
    if lIllIIIlllIllIIlII:
        llIIllllIlIlIIllII = lIllIIIlllIllIIlII.get('plan')
        if llIIllllIlIlIIllII is None:
            llIIllIIllIllIIlll.delete_one({'user_id': lIllIIIIllIIIllIlI})
            return None
        lllIlIIllllllIlIII = lIllIIIlllIllIIlII.get('expires_at')
        if lllIlIIllllllIlIII and lIlIIIlllIIIIIlIII > lllIlIIllllllIlIII:
            llIIllIIllIllIIlll.delete_one({'user_id': lIllIIIIllIIIllIlI})
            return None
        IlIllllIlIlllllIIl = {}
        if 'used' not in lIllIIIlllIllIIlII:
            IlIllllIlIlllllIIl['used'] = 0
        if 'last_used_date' not in lIllIIIlllIllIIlII:
            IlIllllIlIlllllIIl['last_used_date'] = None
        if IlIllllIlIlllllIIl:
            llIIllIIllIllIIlll.update_one({'user_id': lIllIIIIllIIIllIlI}, {'$set': IlIllllIlIlllllIIl})
            lIllIIIlllIllIIlII.update(IlIllllIlIlllllIIl)
        return lIllIIIlllIllIIlII
    return None

async def lllIIIlIlIIIIllllI(lIllIIIIllIIIllIlI: lllllllllllIlIl):
    """Incrementa el contador de uso del usuario"""
    lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIIIlllIllIIlII:
        llIIllIIllIllIIlll.update_one({'user_id': lIllIIIIllIIIllIlI}, {'$inc': {'used': 1}})

async def IIIllIIIlIIlllIlIl(lIllIIIIllIIIllIlI: lllllllllllIlIl):
    """Resetea el contador de uso del usuario"""
    lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIIIlllIllIIlII:
        llIIllIIllIllIIlll.update_one({'user_id': lIllIIIIllIIIllIlI}, {'$set': {'used': 0}})

async def IIIIlIIllllIIIIlII(lIllIIIIllIIIllIlI: lllllllllllIlIl, llIIllllIlIlIIllII: llllllllllIllll, lIlllIIIlIIIIIlIll: lllllllllllIllI=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), lllIlIIllllllIlIII: IlIllllIIIIllI=None):
    """Establece el plan de un usuario y notifica si notify=True"""
    if llIIllllIlIlIIllII not in IIIllIIIllIllllIIl:
        return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
    lIIIllIIlllIlllIlI = {'plan': llIIllllIlIlIIllII, 'used': 0}
    if lllIlIIllllllIlIII is not None:
        lIIIllIIlllIlllIlI['expires_at'] = lllIlIIllllllIlIII
    IIIlllIlIlllllIlll = llIIllIIllIllIIlll.find_one({'user_id': lIllIIIIllIIIllIlI})
    if not IIIlllIlIlllllIlll:
        lIIIllIIlllIlllIlI['join_date'] = lIlIIIlllIIIIIlIII()
    llIIllIIllIllIIlll.update_one({'user_id': lIllIIIIllIIIllIlI}, {'$set': lIIIllIIlllIlllIlI}, upsert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    if lIlllIIIlIIIIIlIll:
        try:
            await lIIlIlllIllllIllII(lIllIIIIllIIIllIlI, f'>🎉 **¡Se te ha asignado un nuevo plan!**\n>Use el comando /start para iniciar en el bot\n\n>• **Plan**: {llIIllllIlIlIIllII.capitalize()}\n>• **Duración**: {lllIIIIIIllIlllIII[llIIllllIlIlIIllII]}\n>• **Videos disponibles**: {IIIllIIIllIllllIIl[llIIllllIlIlIIllII]}\n\n>¡Disfruta de tus beneficios! 🎬')
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error notificando al usuario {lIllIIIIllIIIllIlI}: {lIlllllIIIIllIIIIl}')
    return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

async def lllIllllllIIIlIlll(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIllI:
    """Verifica si el usuario ha alcanzado su límite de compresión"""
    lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIIIlllIllIIlII is None or lIllIIIlllIllIIlII.get('plan') is None:
        return lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)
    IllIIIIlIIIIIIIlIl = lIllIIIlllIllIIlII.get('used', 0)
    return IllIIIIlIIIIIIIlIl >= IIIllIIIllIllllIIl.get(lIllIIIlllIllIIlII['plan'], 0)

async def llIIlIIIIllIlllllI(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> llllllllllIllll:
    """Obtiene información del plan del usuario para mostrar"""
    lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIIIlllIllIIlII is None or lIllIIIlllIllIIlII.get('plan') is None:
        return '>➣ **No tienes un plan activo.**\n\n>Por favor, adquiere un plan para usar el bot.'
    IIlIIlIIIIlIlllIII = lIllIIIlllIllIIlII['plan'].capitalize()
    lIllIlIlIlIllllIlI = lIllIIIlllIllIIlII.get('used', 0)
    llllIllIllIlllIIIl = IIIllIIIllIllllIIl[lIllIIIlllIllIIlII['plan']]
    IIlIIllIIIllllIlll = lllllllllllllll(0, llllIllIllIlllIIIl - lIllIlIlIlIllllIlI)
    IIIllIIlIlIllIIIII = lllllllllllIIII(100, lIllIlIlIlIllllIlI / llllIllIllIlllIIIl * 100) if llllIllIllIlllIIIl > 0 else 0
    lIlIlIlIIlIIIlIllI = 15
    llIllIllIIIIlIllII = lllllllllllIlIl(lIlIlIlIIlIIIlIllI * IIIllIIlIlIllIIIII / 100)
    IIlIlIlIIllIIIIIll = '⬢' * llIllIllIIIIlIllII + '⬡' * (lIlIlIlIIlIIIlIllI - llIllIllIIIIlIllII)
    lllIlIIllllllIlIII = lIllIIIlllIllIIlII.get('expires_at')
    IIIllllIIIIIIlIlIl = 'No expira'
    if lllllllllllIlII(lllIlIIllllllIlIII, IlIllllIIIIllI):
        lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
        lIlllllIIIlIIllIlI = lllIlIIllllllIlIII - lIlIIIlllIIIIIlIII
        if lIlllllIIIlIIllIlI.total_seconds() <= 0:
            IIIllllIIIIIIlIlIl = 'Expirado'
        else:
            IIIIlllIIIIlllIllI = lIlllllIIIlIIllIlI.IIIIlllIIIIlllIllI
            IlllIIIlllIIIlIlll = lIlllllIIIlIIllIlI.seconds // 3600
            lIIlIIIllIlIlIIIlI = lIlllllIIIlIIllIlI.seconds % 3600 // 60
            if IIIIlllIIIIlllIllI > 0:
                IIIllllIIIIIIlIlIl = f'{IIIIlllIIIIlllIllI} días'
            elif IlllIIIlllIIIlIlll > 0:
                IIIllllIIIIIIlIlIl = f'{IlllIIIlllIIIlIlll} horas'
            else:
                IIIllllIIIIIIlIlIl = f'{lIIlIIIllIlIlIIIlI} minutos'
    return f'>╭✠━━━━━━━━━━━━━━━━━━✠╮\n>┠➣ **Plan actual**: {IIlIIlIIIIlIlllIII}\n>┠➣ **Videos usados**: {lIllIlIlIlIllllIlI}/{llllIllIllIlllIIIl}\n>┠➣ **Restantes**: {IIlIIllIIIllllIlll}\n>┠➣ **Progreso**:\n>[{IIlIlIlIIllIIIIIll}] {lllllllllllIlIl(IIIllIIlIlIllIIIII)}%\n>╰✠━━━━━━━━━━━━━━━━━━✠╯'

async def IIlIIlIlIllIIlIlIl(lIllIIIIllIIIllIlI: lllllllllllIlIl) -> lllllllllllIllI:
    """Verifica si el usuario tiene videos pendientes en la cola"""
    IlIlIlIlIIIlIIIlIl = IIlIlIIIlIIlIlIIlI.count_documents({'user_id': lIllIIIIllIIIllIlI})
    return IlIlIlIlIIIlIIIlIl > 0

def lllllIIlIIIIIllIlI(lIIlllIIIlIlIllllI, IIIllIlllIIllIIIII='B'):
    """Formatea el tamaño de bytes a formato legible"""
    for IlllIIlIllllIlIllI in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if lllllllllllIIlI(lIIlllIIIlIlIllllI) < 1024.0:
            return '%3.2f%s%s' % (lIIlllIIIlIlIllllI, IlllIIlIllllIlIllI, IIIllIlllIIllIIIII)
        lIIlllIIIlIlIllllI /= 1024.0
    return '%.2f%s%s' % (lIIlllIIIlIlIllllI, 'Yi', IIIllIlllIIllIIIII)

def IlllllIIIlIIIllIll(IlIlllIlIlIIllIIIl, lIIllllIIlIlIIlllI, IIIIIlIlIlllIlIlII, IlIlIIlIIlllllllIl=15):
    """Crea una barra de progreso visual"""
    if lIIllllIIlIlIIlllI == 0:
        lIIllllIIlIlIIlllI = 1
    IIIllIIlIlIllIIIII = IlIlllIlIlIIllIIIl / lIIllllIIlIlIIlllI
    llIllIllIIIIlIllII = lllllllllllIlIl(IlIlIIlIIlllllllIl * IIIllIIlIlIllIIIII)
    IIlIlIlIIllIIIIIll = '⬢' * llIllIllIIIIlIllII + '⬡' * (IlIlIIlIIlllllllIl - llIllIllIIIIlIllII)
    return f'    ╭━━━[🤖**Compress Bot**]━━━╮\n>┠➣ [{IIlIlIlIIllIIIIIll}] {lllllllllllIlll(IIIllIIlIlIllIIIII * 100)}%\n>┠➣ **Procesado**: {lllllIIlIIIIIllIlI(IlIlllIlIlIIllIIIl)}/{lllllIIlIIIIIllIlI(lIIllllIIlIlIIlllI)}\n>┠➣ **Estado**: __#{IIIIIlIlIlllIlIlII}__'
IlllIIlllIlIlIIIlI = {}

async def lIlIllIIlIllIlIlll(IlIlllIlIlIIllIIIl, lIIllllIIlIlIIlllI, IlIIlIIIIIlIIIIlIl, IIIIIlIlIlllIlIlII, IIlIIllIIIIlIIllII):
    """Callback para mostrar progreso de descarga/subida con verificación de cancelación"""
    try:
        if IlIIlIIIIIlIIIIlIl.id not in lllIlIlIIlIIIIlllI:
            return
        lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
        lIllIlIlIlIIlIllII = (IlIIlIIIIIlIIIIlIl.chat.id, IlIIlIIIIIlIIIIlIl.id)
        IIllIIllIlIlIlIllI = IlllIIlllIlIlIIIlI.get(lIllIlIlIlIIlIllII)
        if IIllIIllIlIlIlIllI and (lIlIIIlllIIIIIlIII - IIllIIllIlIlIlIllI).total_seconds() < 5:
            return
        IlllIIlllIlIlIIIlI[lIllIlIlIlIIlIllII] = lIlIIIlllIIIIIlIII
        IIIIIlIllIIllIlllI = IIllIlIIlIllII() - IIlIIllIIIIlIIllII
        lIlIIlIllllllIlIlI = IlIlllIlIlIIllIIIl / lIIllllIIlIlIIlllI
        lIllIIlIlIIlIIIIll = IlIlllIlIlIIllIIIl / IIIIIlIllIIllIlllI if IIIIIlIllIIllIlllI > 0 else 0
        llIllIIIIIIlllllII = (lIIllllIIlIlIIlllI - IlIlllIlIlIIllIIIl) / lIllIIlIlIIlIIIIll if lIllIIlIlIIlIIIIll > 0 else 0
        llIIIlIllIlIIIIIll = IlllllIIIlIIIllIll(IlIlllIlIlIIllIIIl, lIIllllIIlIlIIlllI, IIIIIlIlIlllIlIlII)
        IIllIIIlIIIIllllll = IlIIlIIllllIlI([[llIlIIlIlllIII('⛔ Cancelar ⛔', callback_data=f'cancel_task_{IlIIlIIIIIlIIIIlIl.chat.id}')]])
        try:
            await IlIIlIIIIIlIIIIlIl.edit(f'>   {llIIIlIllIlIIIIIll}\n>┠➣ **Velocidad** {lllllIIlIIIIIllIlI(lIllIIlIlIIlIIIIll)}/s\n>┠➣ **Tiempo restante:** {lllllllllllIlIl(llIllIIIIIIlllllII)}s\n>╰━━━━━━━━━━━━━━━━━━╯\n', reply_markup=IIllIIIlIIIIllllll)
        except IIlllIIlIlllII:
            pass
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error editando mensaje de progreso: {lIlllllIIIIllIIIIl}')
            if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en progress_callback: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

async def llIlIlIlIIIIIIllIl():
    while lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
        (IIlllllIIIIIIIIlll, IlIIllIlIlIllIIllI, (lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, IlIIlIlIIlllIIlIIl)) = await IlIIllIIllllIllIII.get()
        try:
            lIIlIllIlIIllIIIII = await IlIIlIlIIlllIIlIIl.edit('🗜️**Iniciando compresión**🎬')
            lIllIlIIlIIlIlIIIl = lIIIIIIIllllll()
            await lIllIlIIlIIlIlIIIl.run_in_executor(IlIllIIIIlllIIlIIl, lllllIIIlllIlIlIll, lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, lIIlIllIlIIllIIIII)
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error procesando video: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            await IIIlIIIIlIIIIlllII.send_message(IIIlIlIlIIlllIllII.chat.id, f'⚠️ Error al procesar el video: {llllllllllIllll(lIlllllIIIIllIIIIl)}')
        finally:
            IIlIlIIIlIIlIlIIlI.delete_one({'video_id': IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IIIllIIIlIlIlIlIIl})
            IlIIllIIllllIllIII.task_done()

def lllllIIIlllIlIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, lIIlIllIlIIllIIIII):
    lIllIlIIlIIlIlIIIl = IIIIIIllIllIIl()
    lIlllIIllIIlIl(lIllIlIIlIIlIlIIIl)
    lIllIlIIlIIlIlIIIl.run_until_complete(IIIIIIllIIIllIIlII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, lIIlIllIlIIllIIIII))
    lIllIlIIlIIlIlIIIl.close()

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI(['deleteall']) & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def lIIIllllIlllIlllIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    lIlIlllllllIIIlIII = IIlIlIIIlIIlIlIIlI.delete_many({})
    await IIIlIlIlIIlllIllII.reply(f'>🗑️ **Cola eliminada.**\n**Se eliminaron {lIlIlllllllIIIlIII.deleted_count} elementos.**')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.regex('^/del_(\\d+)$') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llllIlIIIIIlIIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    lIIlIIlIIlIIlIlIll = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.strip().split('_')
    if llllllllllllIII(lIIlIIlIIlIIlIlIll) != 2 or not lIIlIIlIIlIIlIlIll[1].isdigit():
        await IIIlIlIlIIlllIllII.reply('⚠️ Formato inválido. Usa `/del_1`, `/del_2`, etc.')
        return
    lllIlIIlIIIIIlIlll = lllllllllllIlIl(lIIlIIlIIlIIlIlIll[1]) - 1
    llllIIlIIlIIIIlIIl = lllllllllllIIll(IIlIlIIIlIIlIlIIlI.find().sort([('priority', 1), ('timestamp', 1)]))
    if lllIlIIlIIIIIlIlll < 0 or lllIlIIlIIIIIlIlll >= llllllllllllIII(llllIIlIIlIIIIlIIl):
        await IIIlIlIlIIlllIllII.reply('⚠️ Número fuera de rango.')
        return
    llllIIllIllllIIIIl = llllIIlIIlIIIIlIIl[lllIlIIlIIIIIlIlll]
    IIlIlIIIlIIlIlIIlI.delete_one({'_id': llllIIllIllllIIIIl['_id']})
    IlIIllIlllIIIllIII = llllIIllIllllIIIIl.get('file_name', '¿?')
    lIllIIIIllIIIllIlI = llllIIllIllllIIIIl['user_id']
    IlIIllIIllIIlIlIIl = llllIIllIllllIIIIl.get('timestamp')
    IIIllllIIIllllIlIl = IlIIllIIllIIlIlIIl.strftime('%Y-%m-d %H:%M:%S') if IlIIllIIllIIlIlIIl else '¿?'
    await IIIlIlIlIIlllIllII.reply(f'✅ Eliminado de la cola:\n📁 {IlIIllIlllIIIllIII}\n👤 ID: `{lIllIIIIllIIIllIlI}`\n⏰ {IIIllllIIIllllIlIl}')

async def llllIIIllIIIlIIIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Muestra la cola de compresión"""
    llllIIlIIlIIIIlIIl = lllllllllllIIll(IIlIlIIIlIIlIlIIlI.find().sort([('priority', 1), ('timestamp', 1)]))
    if not llllIIlIIlIIIIlIIl:
        await IIIlIlIlIIlllIllII.reply('>📭 **La cola está vacía.**')
        return
    lIlIllIIlIIIIlIIII = {v: k for (k, v) in llIIIIIIIIlIIIllll.items()}
    IIlIIlIllIllIlIlll = '>📋 **Cola de Compresión Activa (Priorizada)**\n\n'
    for (IIllIlIlIlllIllllI, llIIIIIIlIlIIIlIIl) in llllllllllllIll(llllIIlIIlIIIIlIIl, 1):
        lIllIIIIllIIIllIlI = llIIIIIIlIlIIIlIIl['user_id']
        IlIIllIlllIIIllIII = llIIIIIIlIlIIIlIIl.get('file_name', '¿?')
        IlIIllIIllIIlIlIIl = llIIIIIIlIlIIIlIIl.get('timestamp')
        IIIllllIIIllllIlIl = IlIIllIIllIIlIlIIl.strftime('%H:%M:%S') if IlIIllIIllIIlIlIIl else '¿?'
        IIlllllIIIIIIIIlll = llIIIIIIlIlIIIlIIl.get('priority', 4)
        IIlIIlIIIIlIlllIII = lIlIllIIlIIIIlIIII.get(IIlllllIIIIIIIIlll, 'Sin plan').capitalize()
        IIlIIlIllIllIlIlll += f'{IIllIlIlIlllIllllI}. 👤 ID: `{lIllIIIIllIIIllIlI}` | 📁 {IlIIllIlllIIIllIII} | ⏰ {IIIllllIIIllllIlIl} | 📋 {IIlIIlIIIIlIlllIII}\n'
    await IIIlIlIlIIlllIllII.reply(IIlIIlIllIllIlIlll)

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('cola') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIllIlIlIlIlIIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    await llllIIIllIIIlIIIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('auto') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIllllIIIlIllIlIIl(IllllIIlIIIlIlIlII, IIIlIlIlIIlllIllII):
    global IlIIlIIlIIlllIIIll
    IlIIlIIIIIlIIIIlIl = await IIIlIlIlIIlllIllII.reply('🔄 Iniciando procesamiento de la cola...')
    IIlIlIIIlIIlIlIIlI.update_many({'priority': {'$exists': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)}}, {'$set': {'priority': 4}})
    IlIIlIIlllIllIlllI = IIlIlIIIlIIlIlIIlI.find().sort([('priority', 1), ('timestamp', 1)])
    for llIIIIIIlIlIIIlIIl in IlIIlIIlllIllIlllI:
        try:
            lIllIIIIllIIIllIlI = llIIIIIIlIlIIIlIIl['user_id']
            lIlIIlIIllIlIIIIIl = llIIIIIIlIlIIIlIIl['chat_id']
            llIlIIIllIlIlllIIl = llIIIIIIlIlIIIlIIl['message_id']
            IIlllllIIIIIIIIlll = llIIIIIIlIlIIIlIIl.get('priority', 4)
            IlIIllIlIlIllIIllI = llIIIIIIlIlIIIlIIl['timestamp']
            IIIlIlIlIIlllIllII = await IIIlIIIIlIIIIlllII.get_messages(lIlIIlIIllIlIIIIIl, llIlIIIllIlIlllIIl)
            IlIIlIlIIlllIIlIIl = await IIIlIIIIlIIIIlllII.send_message(lIlIIlIIllIlIIIIIl, f'🔄 Recuperado desde cola persistente.')
            await IlIIllIIllllIllIII.put((IIlllllIIIIIIIIlll, IlIIllIlIlIllIIllI, (IIIlIIIIlIIIIlllII, IIIlIlIlIIlllIllII, IlIIlIlIIlllIIlIIl)))
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error cargando pendiente: {lIlllllIIIIllIIIIl}')
    if IlIIlIIlIIlllIIIll is None or IlIIlIIlIIlllIIIll.done():
        IlIIlIIlIIlllIIIll = lIIIlIlIlIIIlI(llIlIlIlIIIIIIllIl())
    await IlIIlIIIIIlIIIIlIl.edit('✅ Procesamiento de cola iniciado.')

def lllIlllIIIIllIIIIl(lIlIIIlIlIlIlllIlI: llllllllllIllll):
    try:
        IIIlIIllIIlllIllII = lIlIIIlIlIlIlllIlI.split()
        for lIIlIllllIIllIlIlI in IIIlIIllIIlllIllII:
            (lIllIlIlIlIIlIllII, IlIlllllIlIlIIlIIl) = lIIlIllllIIllIlIlI.split('=')
            IIlllIlIlIlIllllIl[lIllIlIlIlIIlIllII] = IlIlllllIlIlIIlIIl
        llIlllIIllIIlIIlll.info(f'⚙️Configuración actualizada⚙️: {IIlllIlIlIlIllllIl}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error actualizando configuración: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

def llIIIllllIllIIIlII(IIIllIIlIlIllIIIII, lIlIlIlIIlIIIlIllI=10):
    try:
        IIIllIIlIlIllIIIII = lllllllllllllll(0, lllllllllllIIII(100, IIIllIIlIlIllIIIII))
        lIllIIlIllIlllIlII = lllllllllllIlIl(lIlIlIlIIlIIIlIllI * IIIllIIlIlIllIIIII / 100)
        IIlIlIlIIllIIIIIll = '⬢' * lIllIIlIllIlllIlII + '⬡' * (lIlIlIlIIlIIIlIllI - lIllIIlIllIlllIlII)
        return f'[{IIlIlIlIIllIIIIIll}] {lllllllllllIlIl(IIIllIIlIlIllIIIII)}%'
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error creando barra de progreso: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return f'**Progreso**: {lllllllllllIlIl(IIIllIIlIlIllIIIII)}%'

async def IIIIIIllIIIllIIlII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII: llllllIlllIlIl, lIIlIllIlIIllIIIII):
    try:
        if not IIIlIlIlIIlllIllII.llIIlIIIlllllIllII:
            await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text='Por favor envía un vídeo válido')
            return
        llIlllIIllIIlIIlll.info(f'Iniciando compresión para chat_id: {IIIlIlIlIIlllIllII.chat.id}, video: {IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII}')
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        llllIIIllIIIIlllII = IIIlIlIlIIlllIllII.id
        await llIIlIIIllIIlIllIl(lIllIIIIllIIIllIlI, IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IIIllIIIlIlIlIlIIl)
        IlIIlIIIIIlIIIIlIl = await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text='📥 **Iniciando Descarga** 📥', reply_to_message_id=IIIlIlIlIIlllIllII.id)
        lllIlIlIIlIIIIlllI.add(IlIIlIIIIIlIIIIlIl.id)
        IIllIIIlIIIIllllll = IlIIlIIllllIlI([[llIlIIlIlllIII('⛔ Cancelar ⛔', callback_data=f'cancel_task_{lIllIIIIllIIIllIlI}')]])
        await IlIIlIIIIIlIIIIlIl.edit_reply_markup(IIllIIIlIIIIllllll)
        try:
            IIIIIIlllIIllIlIll = IIllIlIIlIllII()
            lIlllIllllIlIIllIl(lIllIIIIllIIIllIlI, 'download', None, original_message_id=llllIIIllIIIIlllII)
            lIIllIllllllllIIII = await IIIlIIIIlIIIIlllII.download_media(IIIlIlIlIIlllIllII.llIIlIIIlllllIllII, progress=lIlIllIIlIllIlIlll, progress_args=(IlIIlIIIIIlIIIIlIl, 'DESCARGA', IIIIIIlllIIllIlIll))
            llIlllIIllIIlIIlll.info(f'Video descargado: {lIIllIllllllllIIII}')
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error en descarga: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            await IlIIlIIIIIlIIIIlIl.edit(f'Error en descarga: {lIlllllIIIIllIIIIl}')
            await llllIIIllIIIllIIlI(lIllIIIIllIIIllIlI)
            IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)
            if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
            return
        if lIllIIIIllIIIllIlI not in IllIlIIIIIlIlIlIIl:
            if lIIllIllllllllIIII and lllllIIlIlIllI(lIIllIllllllllIIII):
                IIlllllIlIllll(lIIllIllllllllIIII)
            await llllIIIllIIIllIIlI(lIllIIIIllIIIllIlI)
            IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)
            try:
                await lIIlIllIlIIllIIIII.delete()
            except:
                pass
            if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
            return
        lIlllllIIIIIIlIlll = IIIlIIIllIlIII(lIIllIllllllllIIII)
        llIlllIIllIIlIIlll.info(f'Tamaño original: {lIlllllIIIIIIlIlll} bytes')
        await IlIlIllllllllIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, lIlllllIIIIIIlIlll, status='start')
        try:
            lIIllIlIllIllIllll = lIIllIlIllIllIllll(lIIllIllllllllIIII)
            llIIIIlIllIlIlIIIl = llllllllllIllIl(lIIllIlIllIllIllll['format']['duration'])
            llIlllIIllIIlIIlll.info(f'Duración del video: {llIIIIlIllIlIlIIIl} segundos')
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error obteniendo duración: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            llIIIIlIllIlIlIIIl = 0
        await IlIIlIIIIIlIIIIlIl.edit('>╭━━━━[🤖**Compress Bot**]━━━━━╮\n>┠➣ 🗜️𝗖𝗼𝗺𝗽𝗿𝗶𝗺𝗶𝗲𝗻𝗱𝗼 𝗩𝗶𝗱𝗲𝗼🎬\n>┠➣ **Progreso**: 📤 𝘊𝘢𝘳𝘨𝘢𝘯𝘥𝘰 𝘝𝘪𝘥𝘦𝘰 📤\n>╰━━━━━━━━━━━━━━━━━━━━━╯', reply_markup=IIllIIIlIIIIllllll)
        IlIIllIlllIIIlIlll = f'{IlIlIIIIlIIllI(lIIllIllllllllIIII)[0]}_compressed.mp4'
        llIlllIIllIIlIIlll.info(f'Ruta de compresión: {IlIIllIlllIIIlIlll}')
        IIlIIIlIIlllIIIIIl = f"drawtext=text='@InfiniteNetwork_KG':x=w-tw-10:y=10:fontsize=20:fontcolor=white"
        IIlIIlIllIIlIllIIl = ['ffmpeg', '-y', '-i', lIIllIllllllllIIII, '-vf', f"scale={IIlllIlIlIlIllllIl['resolution']},{IIlIIIlIIlllIIIIIl}", '-crf', IIlllIlIlIlIllllIl['crf'], '-b:a', IIlllIlIlIlIllllIl['audio_bitrate'], '-r', IIlllIlIlIlIllllIl['fps'], '-preset', IIlllIlIlIlIllllIl['preset'], '-c:v', IIlllIlIlIlIllllIl['codec'], IlIIllIlllIIIlIlll]
        llIlllIIllIIlIIlll.info(f"Comando FFmpeg: {' '.join(IIlIIlIllIIlIllIIl)}")
        try:
            IIlIIllIIIIlIIllII = lIlIIIlllIIIIIlIII()
            IllIIllllIlIllIlIl = lIlIIIlllIlIlI(IIlIIlIllIIlIllIIl, stderr=lIlIIlIlllIIIl, text=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), bufsize=1)
            lIlllIllllIlIIllIl(lIllIIIIllIIIllIlI, 'ffmpeg', IllIIllllIlIllIlIl, original_message_id=llllIIIllIIIIlllII)
            IIlIlIIIlllllIlIlI = 0
            lllIIlllIlIIlIlIII = 0
            IlIIllIIlIIlIllllI = lIlIIlllIIIIIl('time=(\\d+:\\d+:\\d+\\.\\d+)')
            while lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
                if lIllIIIIllIIIllIlI not in IllIlIIIIIlIlIlIIl:
                    IllIIllllIlIllIlIl.kill()
                    if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                        lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
                    try:
                        await IlIIlIIIIIlIIIIlIl.delete()
                        await lIIlIllIlIIllIIIII.delete()
                    except:
                        pass
                    if lIIllIllllllllIIII and lllllIIlIlIllI(lIIllIllllllllIIII):
                        IIlllllIlIllll(lIIllIllllllllIIII)
                    if IlIIllIlllIIIlIlll and lllllIIlIlIllI(IlIIllIlllIIIlIlll):
                        IIlllllIlIllll(IlIIllIlllIIIlIlll)
                    await llllIIIllIIIllIIlI(lIllIIIIllIIIllIlI)
                    IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)
                    return
                lIIlIllIIIIlllIlIl = IllIIllllIlIllIlIl.stderr.readline()
                if not lIIlIllIIIIlllIlIl and IllIIllllIlIllIlIl.poll() is not None:
                    break
                if lIIlIllIIIIlllIlIl:
                    lIIlIIlIIlIIlIlIll = IlIIllIIlIIlIllllI.search(lIIlIllIIIIlllIlIl)
                    if lIIlIIlIIlIIlIlIll and llIIIIlIllIlIlIIIl > 0:
                        IIIlIIIlIIlIlIlIIl = lIIlIIlIIlIIlIlIll.group(1)
                        (IIllIIIlllIIllIllI, IlIIlIIlIIllIIlllI, IIIIIIIllIlIIIIIII) = IIIlIIIlIIlIlIlIIl.split(':')
                        IlIIllIlIIlIIllllI = lllllllllllIlIl(IIllIIIlllIIllIllI) * 3600 + lllllllllllIlIl(IlIIlIIlIIllIIlllI) * 60 + llllllllllIllIl(IIIIIIIllIlIIIIIII)
                        IIIllIIlIlIllIIIII = lllllllllllIIII(100, IlIIllIlIIlIIllllI / llIIIIlIllIlIlIIIl * 100)
                        if IIIllIIlIlIllIIIII - IIlIlIIIlllllIlIlI >= 5:
                            IIlIlIlIIllIIIIIll = llIIIllllIllIIIlII(IIIllIIlIlIllIIIII)
                            IIllIIIlIIIIllllll = IlIIlIIllllIlI([[llIlIIlIlllIII('⛔ Cancelar ⛔', callback_data=f'cancel_task_{lIllIIIIllIIIllIlI}')]])
                            try:
                                await IlIIlIIIIIlIIIIlIl.edit(f'>╭━━━━[**🤖Compress Bot**]━━━━━╮\n>┠➣ 🗜️𝗖𝗼𝗺𝗽𝗿𝗶𝗺𝗶𝗲𝗻𝗱𝗼 𝗩𝗶𝗱𝗲𝗼🎬\n>┠➣ **Progreso**: {IIlIlIlIIllIIIIIll}\n>╰━━━━━━━━━━━━━━━━━━━━━╯', reply_markup=IIllIIIlIIIIllllll)
                            except IIlllIIlIlllII:
                                pass
                            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                                llIlllIIllIIlIIlll.error(f'Error editando mensaje de progreso: {lIlllllIIIIllIIIIl}')
                                if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                                    lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
                            IIlIlIIIlllllIlIlI = IIIllIIlIlIllIIIII
                            lllIIlllIlIIlIlIII = IIllIlIIlIllII()
            lIlIIIIIIIllIlIIlI = IIIlIIIllIlIII(IlIIllIlllIIIlIlll)
            llIlllIIllIIlIIlll.info(f'Compresión completada. Tamaño comprimido: {lIlIIIIIIIllIlIIlI} bytes')
            try:
                lIIllIlIllIllIllll = lIIllIlIllIllIllll(IlIIllIlllIIIlIlll)
                lIlIlIlIlIIIllllll = lllllllllllIlIl(llllllllllIllIl(lIIllIlIllIllIllll.get('format', {}).get('duration', 0)))
                if lIlIlIlIlIIIllllll == 0:
                    for IIlIIlIllIlllllllI in lIIllIlIllIllIllll.get('streams', []):
                        if 'duration' in IIlIIlIllIlllllllI:
                            lIlIlIlIlIIIllllll = lllllllllllIlIl(llllllllllIllIl(IIlIIlIllIlllllllI['duration']))
                            break
                if lIlIlIlIlIIIllllll == 0:
                    lIlIlIlIlIIIllllll = 0
                llIlllIIllIIlIIlll.info(f'Duración del video comprimido: {lIlIlIlIlIIIllllll} segundos')
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error obteniendo duración comprimido: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                lIlIlIlIlIIIllllll = 0
            lllIlIIlIIlIllIIII = f'{IlIIllIlllIIIlIlll}_thumb.jpg'
            try:
                IIlIIIIIlllIll(IlIIllIlllIIIlIlll, ss=lIlIlIlIlIIIllllll // 2 if lIlIlIlIlIIIllllll > 0 else 0).filter('scale', 320, -1).output(lllIlIIlIIlIllIIII, vframes=1).overwrite_output().run(capture_stdout=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), capture_stderr=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                llIlllIIllIIlIIlll.info(f'Miniatura generada: {lllIlIIlIIlIllIIII}')
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error generando miniatura: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                lllIlIIlIIlIllIIII = None
            IllIlIIllIlIIlIIlI = lIlIIIlllIIIIIlIII() - IIlIIllIIIIlIIllII
            IlIIIlIIIlIIIlllII = llllllllllIllll(IllIlIIllIlIIlIIlI).split('.')[0]
            lllIIIlIIIlIIIllII = f'>╭✠━━━━━━━━━━━━━━━━━━━━✠╮\n>┠➣**Tiempo transcurrido**: {IlIIIlIIIlIIIlllII}\n>╰✠━━━━━━━━━━━━━━━━━━━━✠╯\n'
            try:
                IlllllllIlIIlllIII = IIllIlIIlIllII()
                lIlllIlIlllIlIIllI = await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text='📤 **Subiendo video comprimido** 📤', reply_to_message_id=IIIlIlIlIIlllIllII.id)
                lllIlIlIIlIIIIlllI.add(lIlllIlIlllIlIIllI.id)
                lIlllIllllIlIIllIl(lIllIIIIllIIIllIlI, 'upload', None, original_message_id=llllIIIllIIIIlllII)
                if lllIlIIlIIlIllIIII and lllllIIlIlIllI(lllIlIIlIIlIllIIII):
                    await llIIlIIIllIlIIIlII(chat_id=IIIlIlIlIIlllIllII.chat.id, video=IlIIllIlllIIIlIlll, caption=lllIIIlIIIlIIIllII, thumb=lllIlIIlIIlIllIIII, duration=lIlIlIlIlIIIllllll, reply_to_message_id=IIIlIlIlIIlllIllII.id, progress=lIlIllIIlIllIlIlll, progress_args=(lIlllIlIlllIlIIllI, 'SUBIDA', IlllllllIlIIlllIII))
                else:
                    await llIIlIIIllIlIIIlII(chat_id=IIIlIlIlIIlllIllII.chat.id, video=IlIIllIlllIIIlIlll, caption=lllIIIlIIIlIIIllII, duration=lIlIlIlIlIIIllllll, reply_to_message_id=IIIlIlIlIIlllIllII.id, progress=lIlIllIIlIllIlIlll, progress_args=(lIlllIlIlllIlIIllI, 'SUBIDA', IlllllllIlIIlllIII))
                try:
                    await lIlllIlIlllIlIIllI.delete()
                    llIlllIIllIIlIIlll.info('Mensaje de subida eliminado')
                except:
                    pass
                llIlllIIllIIlIIlll.info('✅ Video comprimido enviado como respuesta al original')
                await IlIlIllllllllIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII, lIlllllIIIIIIlIlll, compressed_size=lIlIIIIIIIllIlIIlI, status='done')
                await lllIIIlIlIIIIllllI(IIIlIlIlIIlllIllII.from_user.id)
                try:
                    await lIIlIllIlIIllIIIII.delete()
                    llIlllIIllIIlIIlll.info("Mensaje 'Iniciando compresión' eliminado")
                except lllllllllllllIl as lIlllllIIIIllIIIIl:
                    llIlllIIllIIlIIlll.error(f'Error eliminando mensaje de inicio: {lIlllllIIIIllIIIIl}')
                try:
                    await IlIIlIIIIIlIIIIlIl.delete()
                    llIlllIIllIIlIIlll.info('Mensaje de progreso eliminado')
                except lllllllllllllIl as lIlllllIIIIllIIIIl:
                    llIlllIIllIIlIIlll.error(f'Error eliminando mensaje de progreso: {lIlllllIIIIllIIIIl}')
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error enviando video: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text='⚠️ **Error al enviar el video comprimido**')
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error en compresión: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            await IlIIlIIIIIlIIIIlIl.delete()
            await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text=f'Ocurrió un error al comprimir el video: {lIlllllIIIIllIIIIl}')
        finally:
            try:
                if IlIIlIIIIIlIIIIlIl.id in lllIlIlIIlIIIIlllI:
                    lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIlIIIIlIl.id)
                if 'upload_msg' in lllllllllllllII() and lIlllIlIlllIlIIllI.id in lllIlIlIIlIIIIlllI:
                    lllIlIlIIlIIIIlllI.remove(lIlllIlIlllIlIIllI.id)
                for IIIlllllIIIIIlIIll in [lIIllIllllllllIIII, IlIIllIlllIIIlIlll]:
                    if IIIlllllIIIIIlIIll and lllllIIlIlIllI(IIIlllllIIIIIlIIll):
                        IIlllllIlIllll(IIIlllllIIIIIlIIll)
                        llIlllIIllIIlIIlll.info(f'Archivo temporal eliminado: {IIIlllllIIIIIlIIll}')
                if 'thumbnail_path' in lllllllllllllII() and lllIlIIlIIlIllIIII and lllllIIlIlIllI(lllIlIIlIIlIllIIII):
                    IIlllllIlIllll(lllIlIIlIIlIllIIII)
                    llIlllIIllIIlIIlll.info(f'Miniatura eliminada: {lllIlIIlIIlIllIIII}')
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error eliminando archivos temporales: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.critical(f'Error crítico en compress_video: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIIIIlIIIIlllII.send_message(chat_id=IIIlIlIlIIlllIllII.chat.id, text='⚠️ Ocurrió un error crítico al procesar el video')
    finally:
        await llllIIIllIIIllIIlI(lIllIIIIllIIIllIlI)
        IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)

def lllIIlIlIlIIIllIII():
    return llIIIIllIIllIl([[IIlllIllIIIIll('⚙️ Settings'), IIlllIllIIIIll('📋 Planes')], [IIlllIllIIIIll('📊 Mi Plan'), IIlllIllIIIIll('ℹ️ Ayuda')], [IIlllIllIIIIll('👀 Ver Cola')]], resize_keyboard=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), one_time_keyboard=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0))

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('settings') & IIlllIlIIllllI.private)
async def IlIlllllIIllIIlIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    IllIIllIIlIlIlllIl = IlIIlIIllllIlI([[llIlIIlIlllIII('🗜️Compresión General🔧', callback_data='general')], [llIlIIlIlllIII('📱 Reels y Videos cortos', callback_data='reels')], [llIlIIlIlllIII('📺 Shows/Reality', callback_data='show')], [llIlIIlIlllIII('🎬 Anime y series animadas', callback_data='anime')]])
    await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '⚙️𝗦𝗲𝗹𝗲𝗰𝗰𝗶𝗼𝗻𝗮𝗿 𝗖𝗮𝗹𝗶𝗱𝗮𝗱⚙️', reply_markup=IllIIllIIlIlIlllIl)

def lIllllllIlllllllIl():
    return IlIIlIIllllIlI([[llIlIIlIlllIII('🧩 Estándar', callback_data='plan_standard')], [llIlIIlIlllIII('💎 Pro', callback_data='plan_pro')], [llIlIIlIlllIII('👑 Premium', callback_data='plan_premium')]])

async def IlllIIlIIllIIlIIlI(lIllIIIIllIIIllIlI: lllllllllllIlIl):
    lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIIIlllIllIIlII is None or lIllIIIlllIllIIlII.get('plan') is None:
        return ('>➣ **No tienes un plan activo.**\n\n>Por favor, adquiere un plan para usar el bot.\n\n>📋 **Selecciona un plan para más información:**', lIllllllIlllllllIl())
    IIlIIlIIIIlIlllIII = lIllIIIlllIllIIlII['plan'].capitalize()
    lIllIlIlIlIllllIlI = lIllIIIlllIllIIlII.get('used', 0)
    llllIllIllIlllIIIl = IIIllIIIllIllllIIl[lIllIIIlllIllIIlII['plan']]
    IIlIIllIIIllllIlll = lllllllllllllll(0, llllIllIllIlllIIIl - lIllIlIlIlIllllIlI)
    return (f'> ╭✠━━━━━━━━━━━━━━━━━━━━━━✠╮\n> ┠➣ **Tu plan actual**: {IIlIIlIIIIlIlllIII}\n> ┠➣ **Videos usados**: {lIllIlIlIlIllllIlI}/{llllIllIllIlllIIIl}\n> ┠➣ **Restantes**: {IIlIIllIIIllllIlll}\n> ╰✠━━━━━━━━━━━━━━━━━━━━━━✠╯\n\n> 📋 **Selecciona un plan para más información:**', lIllllllIlllllllIl())

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('planes') & IIlllIlIIllllI.private)
async def IIIllIlIlllllllIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        (IlllIlIIllIllIIIII, IllIIllIIlIlIlllIl) = await IlllIIlIIllIIlIIlI(IIIlIlIlIIlllIllII.from_user.id)
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, IlllIlIIllIllIIIII, reply_markup=IllIIllIIlIlIlllIl)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en planes_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '⚠️ Error al mostrar los planes')

@IIIlIIIIlIIIIlllII.on_callback_query()
async def lllIIIIIIIIllIIlll(lIlIllIIllIIIllIIl, lllIlIlIIlIIlIIlll: IIllllllllIlIl):
    lIlIIlIllIlIlIIIII = {'general': 'resolution=854x480 crf=28 audio_bitrate=70k fps=22 preset=veryfast codec=libx264', 'reels': 'resolution=420x720 crf=25 audio_bitrate=70k fps=30 preset=veryfast codec=libx264', 'show': 'resolution=854x480 crf=32 audio_bitrate=70k fps=20 preset=veryfast codec=libx264', 'anime': 'resolution=854x480 crf=32 audio_bitrate=150k fps=18 preset=veryfast codec=libx264'}
    IllIIIIlIIllIIlIII = {'general': '🗜️Compresión General🔧', 'reels': '📱 Reels y Videos cortos', 'show': '📺 Shows/Reality', 'anime': '🎬 Anime y series animadas'}
    if lllIlIlIIlIIlIIlll.data.startswith('cancel_task_'):
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIlIIlIIlIIlll.data.split('_')[2])
        if lllIlIlIIlIIlIIlll.from_user.id != lIllIIIIllIIIllIlI:
            await lllIlIlIIlIIlIIlll.answer('⚠️ Solo el propietario puede cancelar esta tarea', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return
        if IIlIIllIIIIllIlIII(lIllIIIIllIIIllIlI):
            llllIIIllIIIIlllII = IllIlIIIIIlIlIlIIl[lIllIIIIllIIIllIlI].get('original_message_id')
            IIIlIIllllIlIIIlIl(lIllIIIIllIIIllIlI)
            IlIIlIIIIIllIlIlIl = lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII
            if IlIIlIIIIIllIlIlIl.id in lllIlIlIIlIIIIlllI:
                lllIlIlIIlIIIIlllI.remove(IlIIlIIIIIllIlIlIl.id)
            try:
                await IlIIlIIIIIllIlIlIl.delete()
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error eliminando mensaje de progreso: {lIlllllIIIIllIIIIl}')
            await lllIlIlIIlIIlIIlll.answer('⛔ Tarea cancelada! ⛔', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            try:
                await IIIlIIIIlIIIIlllII.send_message(lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.chat.id, '⛔ **Operación cancelada por el usuario** ⛔', reply_to_message_id=llllIIIllIIIIlllII)
            except:
                await IIIlIIIIlIIIIlllII.send_message(lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.chat.id, '⛔ **Operación cancelada por el usuario** ⛔')
        else:
            await lllIlIlIIlIIlIIlll.answer('⚠️ No se pudo cancelar la tarea', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    if lllIlIlIIlIIlIIlll.data.startswith(('confirm_', 'cancel_')):
        (IlIlIIIIIlIllIllIl, lllllllIllIlIlIlll) = lllIlIlIIlIIlIIlll.data.split('_', 1)
        IIlIIllIlIllIIIlII = IIllIIlIlIlIlI(lllllllIllIlIlIlll)
        llIllllIIllllIIlII = await lIlIlllllIIIIllIIl(IIlIIllIlIllIIIlII)
        if not llIllllIIllllIIlII:
            await lllIlIlIIlIIlIIlll.answer('⚠️ Esta solicitud ha expirado o ya fue procesada.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return
        lIllIIIIllIIIllIlI = lllIlIlIIlIIlIIlll.from_user.id
        if lIllIIIIllIIIllIlI != llIllllIIllllIIlII['user_id']:
            await lllIlIlIIlIIlIIlll.answer('⚠️ No tienes permiso para esta acción.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            return
        if IlIlIIIIIlIllIllIl == 'confirm':
            if await lllIllllllIIIlIlll(lIllIIIIllIIIllIlI):
                await lllIlIlIIlIIlIIlll.answer('⚠️ Has alcanzado tu límite mensual de compresiones.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
                return
            lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
            lIlIIllIIIIlllIIII = IIlIlIIIlIIlIlIIlI.count_documents({'user_id': lIllIIIIllIIIllIlI})
            if lIllIlIIIllIIIlIll and lIllIlIIIllIIIlIll['plan'] == 'premium':
                if lIlIIllIIIIlllIIII >= IIllllIIllIllIllll:
                    await lllIlIlIIlIIlIIlll.answer(f'⚠️ Ya tienes {lIlIIllIIIIlllIIII} videos en cola (límite: {IIllllIIllIllIllll}).\nEspera a que se procesen antes de enviar más.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                    await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
                    return
            elif await IIlIllIlllIIlIlllI(lIllIIIIllIIIllIlI) or lIlIIllIIIIlllIIII > 0:
                await lllIlIlIIlIIlIIlll.answer('⚠️ Ya hay un video en proceso de compresión o en cola.\nEspera a que termine antes de enviar otro video.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
                return
            try:
                IIIlIlIlIIlllIllII = await IIIlIIIIlIIIIlllII.get_messages(llIllllIIllllIIlII['chat_id'], llIllllIIllllIIlII['message_id'])
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error obteniendo mensaje: {lIlllllIIIIllIIIIl}')
                await lllIlIlIIlIIlIIlll.answer('⚠️ Error al obtener el video. Intenta enviarlo de nuevo.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
                return
            await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
            IlIlIIIlIllIIIIllI = IlIIllIIllllIllIII.qsize()
            IlIIlIlIIlllIIlIIl = await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text(f'⏳ Tu video ha sido añadido a la cola.\n\n📋 Tamaño actual de la cola: {IlIlIIIlIllIIIIllI}\n\n• **Espere que otros procesos terminen** ⏳')
            IIlllllIIIIIIIIlll = await IllIIllIIIlIIlIlII(lIllIIIIllIIIllIlI)
            IlIIllIlIlIllIIllI = lIlIIIlllIIIIIlIII()
            global IlIIlIIlIIlllIIIll
            if IlIIlIIlIIlllIIIll is None or IlIIlIIlIIlllIIIll.done():
                IlIIlIIlIIlllIIIll = lIIIlIlIlIIIlI(llIlIlIlIIIIIIllIl())
            IIlIlIIIlIIlIlIIlI.insert_one({'user_id': lIllIIIIllIIIllIlI, 'video_id': IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IIIllIIIlIlIlIlIIl, 'file_name': IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII, 'chat_id': IIIlIlIlIIlllIllII.chat.id, 'message_id': IIIlIlIlIIlllIllII.id, 'timestamp': IlIIllIlIlIllIIllI, 'priority': IIlllllIIIIIIIIlll})
            await IlIIllIIllllIllIII.put((IIlllllIIIIIIIIlll, IlIIllIlIlIllIIllI, (IIIlIIIIlIIIIlllII, IIIlIlIlIIlllIllII, IlIIlIlIIlllIIlIIl)))
            llIlllIIllIIlIIlll.info(f'Video confirmado y encolado de {lIllIIIIllIIIllIlI}: {IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII}')
        elif IlIlIIIIIlIllIllIl == 'cancel':
            await llIllllllllIlllIll(IIlIIllIlIllIIIlII)
            await lllIlIlIIlIIlIIlll.answer('⛔ Compresión cancelada.⛔', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            try:
                await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text('⛔ **Compresión cancelada.** ⛔')
                await lIllIllIlIIlII(5)
                await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.delete()
            except:
                pass
        return
    if lllIlIlIIlIIlIIlll.data == 'plan_back':
        try:
            (IlllIlIIllIllIIIII, IllIIllIIlIlIlllIl) = await IlllIIlIIllIIlIIlI(lllIlIlIIlIIlIIlll.from_user.id)
            await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text(IlllIlIIllIllIIIII, reply_markup=IllIIllIIlIlIlllIl)
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'Error en plan_back: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            await lllIlIlIIlIIlIIlll.answer('⚠️ Error al volver al menú de planes', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        return
    elif lllIlIlIIlIIlIIlll.data.startswith('plan_'):
        lIIIIlIlllIllllIII = lllIlIlIIlIIlIIlll.data.split('_')[1]
        lIllIIIIllIIIllIlI = lllIlIlIIlIIlIIlll.from_user.id
        IlIlIlIllllIIlIlll = IlIIlIIllllIlI([[llIlIIlIlllIII('🔙 Volver', callback_data='plan_back'), llIlIIlIlllIII('📝 Contratar Plan', url='https://t.me/InfiniteNetworkAdmin?text=Hola,+estoy+interesad@+en+un+plan+del+bot+de+comprimír+vídeos')]])
        if lIIIIlIlllIllllIII == 'standard':
            await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text('> 🧩**Plan Estándar**🧩\n\n> ✅ **Beneficios:**\n> • **Hasta 60 videos comprimidos**\n\n> ❌ **Desventajas:**\n> • **Prioridad baja en la cola de procesamiento**\n>• **No podá reenviar del bot**\n>• **Solo podá comprimír 1 video a la ves**\n\n> • **Precio:** **180Cup**💵\n> **• Duración 7 dias**\n\n', reply_markup=IlIlIlIllllIIlIlll)
        elif lIIIIlIlllIllllIII == 'pro':
            await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text('>💎**Plan Pro**💎\n\n>✅ **Beneficios:**\n>• **Hasta 130 videos comprimidos**\n>• **Prioridad alta en la cola de procesamiento**\n>• **Podá reenviar del bot**\n\n>❌ **Desventajas**\n>• **Solo podá comprimír 1 video a la ves**\n\n>• **Precio:** **300Cup**💵\n>**• Duración 15 dias**\n\n', reply_markup=IlIlIlIllllIIlIlll)
        elif lIIIIlIlllIllllIII == 'premium':
            await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text(f'>👑**Plan Premium**👑\n\n>✅ **Beneficios:**\n>• **Hasta 280 videos comprimidos**\n>• **Máxima prioridad en procesamiento**\n>• **Soporte prioritario 24/7**\n>• **Podá reenviar del bot**\n>• **Múltiples videos en cola** (hasta {IIllllIIllIllIllll})\n\n>• **Precio:** **500Cup**💵\n>**• Duración 30 dias**\n\n', reply_markup=IlIlIlIllllIIlIlll)
        return
    lIIIlIllIIlllllllI = lIlIIlIllIlIlIIIII.get(lllIlIlIIlIIlIIlll.data)
    if lIIIlIllIIlllllllI:
        lllIlllIIIIllIIIIl(lIIIlIllIIlllllllI)
        IlIlIlIllllIIlIlll = IlIIlIIllllIlI([[llIlIIlIlllIII('🔙 Volver', callback_data='back_to_settings')]])
        IIlIlIIlIlIlIIllIl = IllIIIIlIIllIIlIII.get(lllIlIlIIlIIlIIlll.data, 'Calidad Desconocida')
        await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text(f'>**{IIlIlIIlIlIlIIllIl}\n>aplicada correctamente**✅', reply_markup=IlIlIlIllllIIlIlll)
    elif lllIlIlIIlIIlIIlll.data == 'back_to_settings':
        IllIIllIIlIlIlllIl = IlIIlIIllllIlI([[llIlIIlIlllIII('🗜️Compresión General🔧', callback_data='general')], [llIlIIlIlllIII('📱 Reels y Videos cortos', callback_data='reels')], [llIlIIlIlllIII('📺 Shows/Reality', callback_data='show')], [llIlIIlIlllIII('🎬 Anime y series animadas', callback_data='anime')]])
        await lllIlIlIIlIIlIIlll.IIIlIlIlIIlllIllII.edit_text(' ⚙️𝗦𝗲𝗹𝗲𝗰𝗰𝗶𝗼𝗻𝗮𝗿 𝗖𝗮𝗹𝗶𝗱𝗮𝗱⚙️', reply_markup=IllIIllIIlIlIlllIl)
    else:
        await lllIlIlIIlIIlIIlll.answer('Opción inválida.', show_alert=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('start'))
async def IIIlIIIIllIIlllIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            llIlllIIllIIlIIlll.warning(f'Usuario baneado intentó usar /start: {lIllIIIIllIIIllIlI}')
            return
        lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
        if lIllIlIIIllIIIlIll is None or lIllIlIIIllIIIlIll.get('plan') is None:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '>➣ **Usted no tiene acceso al bot.**\n\n>💲 Para ver los planes disponibles usa el comando /planes\n\n>👨🏻\u200d💻 Para más información, contacte a @InfiniteNetworkAdmin.')
            return
        IllllIIllIlIlIllll = 'logo.jpg'
        lIllIllIIIIlllIIll = '> **🤖 Bot para comprimir videos**\n> ➣**Creado por** @InfiniteNetworkAdmin\n\n> **¡Bienvenido!** Puedo reducir el tamaño de los vídeos hasta un 80% o más y se verán bien sin perder tanta calidad\n>Usa los botones del menú para interactuar conmigo.Si tiene duda use el botón ℹ️ Ayuda\n\n> **⚙️ Versión 16.5.0 ⚙️**'
        await lllllIIIIIlIIlllll(chat_id=IIIlIlIlIIlllIllII.chat.id, photo=IllllIIllIlIlIllll, caption=lIllIllIIIIlllIIll, reply_markup=lllIIlIlIlIIIllIII())
        llIlllIIllIIlIIlll.info(f'Comando /start ejecutado por {IIIlIlIlIIlllIllII.from_user.id}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en handle_start: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.IllllIIIlllllIIIll & IIlllIlIIllllI.private)
async def IllIlIllllIIIllIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        IllllIIIlllllIIIll = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.lower()
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            return
        if IllllIIIlllllIIIll == '⚙️ settings':
            await IlIlllllIIllIIlIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll == '📋 planes':
            await IIIllIlIlllllllIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll == '📊 mi plan':
            await llllIlllIIIlIlIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll == 'ℹ️ ayuda':
            lIlIIllIIIIIlllllI = IlIIlIIllllIlI([[llIlIIlIlllIII('👨🏻\u200d💻 Soporte', url='https://t.me/InfiniteNetworkAdmin')]])
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '> 👨🏻\u200d💻 **Información**\n\n> • Configurar calidad: Usa el botón ⚙️ Settings\n> • Para comprimir un video: Envíalo directamente al bot\n> • Ver planes: Usa el botón 📋 Planes\n> • Ver tu estado: Usa el botón 📊 Mi Plan\n> • Usa /start para iniciar en el bot nuevamente\n> • Ver cola de compresión: Usa el botón 👀 Ver Cola\n\n', reply_markup=lIlIIllIIIIIlllllI)
        elif IllllIIIlllllIIIll == '👀 ver cola':
            await IIIlIIIlIIllIllIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll == '/cancel':
            await llIlIIIlIIIIlIlIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        else:
            await IlIIIIIlllIlIllIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en main_menu_handler: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('desuser') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llIlllIIlIIIIlIIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 2:
            await IIIlIlIlIIlllIllII.reply('Formato: /desuser <user_id>')
            return
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            IIIIlllIlllllIIlll.remove(lIllIIIIllIIIllIlI)
        lIlIlllllllIIIlIII = lllllIlIllIlIIlIll.delete_one({'user_id': lIllIIIIllIIIllIlI})
        if lIlIlllllllIIIlIII.deleted_count > 0:
            await IIIlIlIlIIlllIllII.reply(f'>➣ Usuario {lIllIIIIllIIIllIlI} desbaneado exitosamente.')
            try:
                await IIIlIIIIlIIIIlllII.send_message(lIllIIIIllIIIllIlI, '>✅ **Tu acceso al bot ha sido restaurado.**\n\n>Ahora puedes volver a usar el bot.')
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'No se pudo notificar al usuario {lIllIIIIllIIIllIlI}: {lIlllllIIIIllIIIIl}')
        else:
            await IIIlIlIlIIlllIllII.reply(f'>➣ El usuario {lIllIIIIllIIIllIlI} no estaba baneado.')
        llIlllIIllIIlIIlll.info(f'Usuario desbaneado: {lIllIIIIllIIIllIlI} por admin {IIIlIlIlIIlllIllII.from_user.id}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en unban_user_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al desbanear usuario. Formato: /desuser [user_id]')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('deleteuser') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def lIlIllIIIIlIIIlllI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 2:
            await IIIlIlIlIIlllIllII.reply('Formato: /deleteuser <user_id>')
            return
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        lIlIlllllllIIIlIII = llIIllIIllIllIIlll.delete_one({'user_id': lIllIIIIllIIIllIlI})
        if lIllIIIIllIIIllIlI not in IIIIlllIlllllIIlll:
            IIIIlllIlllllIIlll.append(lIllIIIIllIIIllIlI)
        lllllIlIllIlIIlIll.insert_one({'user_id': lIllIIIIllIIIllIlI, 'banned_at': lIlIIIlllIIIIIlIII()})
        lIIIIlIIIIIlIIIIlI = IIlIlIIIlIIlIlIIlI.delete_many({'user_id': lIllIIIIllIIIllIlI})
        await IIIlIlIlIIlllIllII.reply(f'>➣ Usuario {lIllIIIIllIIIllIlI} eliminado y baneado exitosamente.\n>🗑️ Tareas pendientes eliminadas: {lIIIIlIIIIIlIIIIlI.deleted_count}')
        llIlllIIllIIlIIlll.info(f'Usuario eliminado y baneado: {lIllIIIIllIIIllIlI} por admin {IIIlIlIlIIlllIllII.from_user.id}')
        try:
            await IIIlIIIIlIIIIlllII.send_message(lIllIIIIllIIIllIlI, '>🔒 **Tu acceso al bot ha sido revocado.**\n\n>No podrás usar el bot hasta nuevo aviso.')
        except lllllllllllllIl as lIlllllIIIIllIIIIl:
            llIlllIIllIIlIIlll.error(f'No se pudo notificar al usuario {lIllIIIIllIIIllIlI}: {lIlllllIIIIllIIIIl}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en delete_user_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al eliminar usuario. Formato: /deleteuser [user_id]')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('viewban') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIlllIlIlllIIIllll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lIllIIIllIlIllIIII = lllllllllllIIll(lllllIlIllIlIIlIll.find({}))
        if not lIllIIIllIlIllIIII:
            await IIIlIlIlIIlllIllII.reply('>📭 **No hay usuarios baneados.**')
            return
        llIlIIIlIIllllllII = '>🔒 **Usuarios Baneados**\n\n'
        for (IIllIlIlIlllIllllI, lIIlIIIIIIlIlllIII) in llllllllllllIll(lIllIIIllIlIllIIII, 1):
            lIllIIIIllIIIllIlI = lIIlIIIIIIlIlllIII['user_id']
            llIIlIllIIIIlllIll = lIIlIIIIIIlIlllIII.get('banned_at', 'Fecha desconocida')
            try:
                lIllIIIlllIllIIlII = await IIIlIIIIlIIIIlllII.get_users(lIllIIIIllIIIllIlI)
                lIIIIIIIllIllIlIIl = f'@{lIllIIIlllIllIIlII.lIIIIIIIllIllIlIIl}' if lIllIIIlllIllIIlII.lIIIIIIIllIllIlIIl else 'Sin username'
            except:
                lIIIIIIIllIllIlIIl = 'Sin username'
            if lllllllllllIlII(llIIlIllIIIIlllIll, IlIllllIIIIllI):
                lIlIIIlIlIIIIllIIl = llIIlIllIIIIlllIll.strftime('%Y-%m-%d %H:%M:%S')
            else:
                lIlIIIlIlIIIIllIIl = llllllllllIllll(llIIlIllIIIIlllIll)
            llIlIIIlIIllllllII += f'{IIllIlIlIlllIllllI}. 👤 {lIIIIIIIllIllIlIIl}\n   🆔 ID: `{lIllIIIIllIIIllIlI}`\n   ⏰ Fecha: {lIlIIIlIlIIIIllIIl}\n\n'
        await IIIlIlIlIIlllIllII.reply(llIlIIIlIIllllllII)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en view_banned_users_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al obtener la lista de usuarios baneados')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI(['banuser', 'deluser']) & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llIIlllIllIlIIIlll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 2:
            await IIIlIlIlIIlllIllII.reply('Formato: /comando <user_id>')
            return
        IIIIlIlIIlllIllllI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        if IIIIlIlIIlllIllllI in lllIIIlIllIlllIIII:
            await IIIlIlIlIIlllIllII.reply('>➣ No puedes banear a un administrador.')
            return
        lIlIlllllllIIIlIII = llIIllIIllIllIIlll.delete_one({'user_id': IIIIlIlIIlllIllllI})
        if IIIIlIlIIlllIllllI not in IIIIlllIlllllIIlll:
            IIIIlllIlllllIIlll.append(IIIIlIlIIlllIllllI)
        lllllIlIllIlIIlIll.insert_one({'user_id': IIIIlIlIIlllIllllI, 'banned_at': lIlIIIlllIIIIIlIII()})
        await IIIlIlIlIIlllIllII.reply(f'>➣ Usuario {IIIIlIlIIlllIllllI} baneado y eliminado de la base de datos.' if lIlIlllllllIIIlIII.deleted_count > 0 else f'>➣ Usuario {IIIIlIlIIlllIllllI} baneado (no estaba en la base de datos).')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en ban_or_delete_user_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error en el comando')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('key') & IIlllIlIIllllI.private)
async def llIllIlIllllIllIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '🚫 Tu acceso ha sido revocado.')
            return
        llIlllIIllIIlIIlll.info(f'Comando key recibido de {lIllIIIIllIIIllIlI}')
        if not IIIlIlIlIIlllIllII.IllllIIIlllllIIIll or llllllllllllIII(IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()) < 2:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '❌ Formato: /key <clave>')
            return
        lIllIlIlIlIIlIllII = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()[1].strip()
        lIlIIIlllIIIIIlIII = lIlIIIlllIIIIIlIII()
        llllIIllIlllIIIlIl = lIlIIlllIIIIIlIIIl.find_one({'key': lIllIlIlIlIIlIllII, 'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)})
        if not llllIIllIlllIIIlIl:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '❌ **Clave inválida o ya ha sido utilizada.**')
            return
        if llllIIllIlllIIIlIl['expires_at'] < lIlIIIlllIIIIIlIII:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '❌ **La clave ha expirado.**')
            return
        lIlIIlllIIIIIlIIIl.update_one({'_id': llllIIllIlllIIIlIl['_id']}, {'$set': {'used': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)}})
        lIIIlIIIllIlllllII = llllIIllIlllIIIlIl['plan']
        IlIIIIIIlllIIIlllI = llllIIllIlllIIIlIl['duration_value']
        lIIlIIlIIlIllIIIlI = llllIIllIlllIIIlIl['duration_unit']
        if lIIlIIlIIlIllIIIlI == 'minutes':
            lllIlIIllllllIlIII = lIlIIIlllIIIIIlIII() + IIlIIlIlIlllII(minutes=IlIIIIIIlllIIIlllI)
        elif lIIlIIlIIlIllIIIlI == 'hours':
            lllIlIIllllllIlIII = lIlIIIlllIIIIIlIII() + IIlIIlIlIlllII(hours=IlIIIIIIlllIIIlllI)
        else:
            lllIlIIllllllIlIII = lIlIIIlllIIIIIlIII() + IIlIIlIlIlllII(days=IlIIIIIIlllIIIlllI)
        lIlIIIIlIIIllIIlll = await IIIIlIIllllIIIIlII(lIllIIIIllIIIllIlI, lIIIlIIIllIlllllII, notify=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), expires_at=lllIlIIllllllIlIII)
        if lIlIIIIlIIIllIIlll:
            IIllllIllIIlllIlll = f'{IlIIIIIIlllIIIlllI} {lIIlIIlIIlIllIIIlI}'
            if IlIIIIIIlllIIIlllI == 1:
                IIllllIllIIlllIlll = IIllllIllIIlllIlll[:-1]
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, f'>✅ **Plan {lIIIlIIIllIlllllII.capitalize()} activado!**\n>**Válido por {IIllllIllIIlllIlll}**\n\n>**Ahora tienes {IIIllIIIllIllllIIl[lIIIlIIIllIlllllII]} videos disponibles**\n>Use el comando /start para iniciar en el bot')
            llIlllIIllIIlIIlll.info(f'Plan actualizado a {lIIIlIIIllIlllllII} para {lIllIIIIllIIIllIlI} con clave {lIllIlIlIlIIlIllII}')
        else:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '❌ **Error al activar el plan. Contacta con el administrador.**')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en key_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '❌ **Error al procesar la solicitud de acceso**')
IIllllIIIllllIIlIl = {}

def lIIIIlIIllIlIIllIl():
    return BOT_IS_PUBLIC and BOT_IS_PUBLIC.lower() == 'true'

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('myplan') & IIlllIlIIllllI.private)
async def llllIlllIIIlIlIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lIIIIllIllIIlIIIlI = await llIIlIIIIllIlllllI(IIIlIlIlIIlllIllII.from_user.id)
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, lIIIIllIllIIlIIIlI, reply_markup=lllIIlIlIlIIIllIII())
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en my_plan_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '⚠️ **Error al obtener información de tu plan**', reply_markup=lllIIlIlIlIIIllIII())

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('setplan') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIllIIlIlIlIlIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 3:
            await IIIlIlIlIIlllIllII.reply('Formato: /setplan <user_id> <plan>')
            return
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        llIIllllIlIlIIllII = lllIlIIllIllIlIllI[2].lower()
        if llIIllllIlIlIIllII not in IIIllIIIllIllllIIl:
            await IIIlIlIlIIlllIllII.reply(f"⚠️ Plan inválido. Opciones válidas: {', '.join(IIIllIIIllIllllIIl.IIlIlIIIlllIIIllll())}")
            return
        if await IIIIlIIllllIIIIlII(lIllIIIIllIIIllIlI, llIIllllIlIlIIllII, expires_at=None):
            await IIIlIlIlIIlllIllII.reply(f'>➣ **Plan del usuario {lIllIIIIllIIIllIlI} actualizado a {llIIllllIlIlIIllII}.**')
        else:
            await IIIlIlIlIIlllIllII.reply('⚠️ **Error al actualizar el plan.**')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en set_plan_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ **Error en el comando**')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('resetuser') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llIlIIIIIIlIIlIIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 2:
            await IIIlIlIlIIlllIllII.reply('Formato: /resetuser <user_id>')
            return
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        await IIIllIIIlIIlllIlIl(lIllIIIIllIIIllIlI)
        await IIIlIlIlIIlllIllII.reply(f'>➣ **Contador de videos del usuario {lIllIIIIllIIIllIlI} reiniciado a 0.**')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en reset_user_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error en el comando')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('userinfo') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llIlIIIIIllllIIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()
        if llllllllllllIII(lllIlIIllIllIlIllI) != 2:
            await IIIlIlIlIIlllIllII.reply('Formato: /userinfo <user_id>')
            return
        lIllIIIIllIIIllIlI = lllllllllllIlIl(lllIlIIllIllIlIllI[1])
        lIllIIIlllIllIIlII = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
        if lIllIIIlllIllIIlII:
            llIIllllIlIlIIllII = lIllIIIlllIllIIlII['plan'].capitalize() if lIllIIIlllIllIIlII.get('plan') else 'Ninguno'
            lIllIlIlIlIllllIlI = lIllIIIlllIllIIlII.get('used', 0)
            llllIllIllIlllIIIl = IIIllIIIllIllllIIl[lIllIIIlllIllIIlII['plan']] if lIllIIIlllIllIIlII.get('plan') else 0
            lIlIIIIllIlIlllIII = lIllIIIlllIllIIlII.get('join_date', 'Desconocido')
            lllIlIIllllllIlIII = lIllIIIlllIllIIlII.get('expires_at', 'No expira')
            if lllllllllllIlII(lIlIIIIllIlIlllIII, IlIllllIIIIllI):
                lIlIIIIllIlIlllIII = lIlIIIIllIlIlllIII.strftime('%Y-%m-%d %H:%M:%S')
            if lllllllllllIlII(lllIlIIllllllIlIII, IlIllllIIIIllI):
                lllIlIIllllllIlIII = lllIlIIllllllIlIII.strftime('%Y-%m-%d %H:%M:%S')
            await IIIlIlIlIIlllIllII.reply(f'>👤 **ID**: `{lIllIIIIllIIIllIlI}`\n>📝 **Plan**: {llIIllllIlIlIIllII}\n>🔢 **Videos comprimidos**: {lIllIlIlIlIllllIlI}/{llllIllIllIlllIIIl}\n>📅 **Fecha de registro**: {lIlIIIIllIlIlllIII}\n')
        else:
            await IIIlIlIlIIlllIllII.reply('⚠️ Usuario no registrado o sin plan')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en user_info_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error en el comando')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('restuser') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def llIIlIIllIlIIllIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        lIlIlllllllIIIlIII = llIIllIIllIllIIlll.delete_many({})
        await IIIlIlIlIIlllIllII.reply(f'>➣ **Todos los usuarios han sido eliminados**\n>➣ Usuarios eliminados: {lIlIlllllllIIIlIII.deleted_count}\n>➣ Contadores de vídeos restablecidos a 0')
        llIlllIIllIIlIIlll.info(f'Todos los usuarios eliminados por admin {IIIlIlIlIIlllIllII.from_user.id}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en reset_all_users_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al eliminar usuarios')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('user') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def lIllIIllllllIIllII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        IIlIIIIIIIIIlIlIlI = lllllllllllIIll(llIIllIIllIllIIlll.find({}))
        if not IIlIIIIIIIIIlIlIlI:
            await IIIlIlIlIIlllIllII.reply('>📭 **No hay usuarios registrados.**')
            return
        llIlIIIlIIllllllII = '>👥 **Lista de Usuarios Registrados**\n\n'
        for (IIllIlIlIlllIllllI, lIllIIIlllIllIIlII) in llllllllllllIll(IIlIIIIIIIIIlIlIlI, 1):
            lIllIIIIllIIIllIlI = lIllIIIlllIllIIlII['user_id']
            llIIllllIlIlIIllII = lIllIIIlllIllIIlII['plan'].capitalize() if lIllIIIlllIllIIlII.get('plan') else 'Ninguno'
            try:
                IIllllllIllIllIllI = await IIIlIIIIlIIIIlllII.get_users(lIllIIIIllIIIllIlI)
                lIIIIIIIllIllIlIIl = f'@{IIllllllIllIllIllI.lIIIIIIIllIllIlIIl}' if IIllllllIllIllIllI.lIIIIIIIllIllIlIIl else 'Sin username'
            except:
                lIIIIIIIllIllIlIIl = 'Sin username'
            llIlIIIlIIllllllII += f'{IIllIlIlIlllIllllI}. {lIIIIIIIllIllIlIIl}\n   👤 ID: `{lIllIIIIllIIIllIlI}`\n   📝 Plan: {llIIllllIlIlIIllII}\n\n'
        await IIIlIlIlIIlllIllII.reply(llIlIIIlIIllllllII)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en list_users_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ **Error al listar usuarios**')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('admin') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def lIllIIlllIlllIIIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        IIIllIllIllIIIIlIl = [{'$match': {'plan': {'$exists': lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), '$ne': None}}}, {'$group': {'_id': '$plan', 'count': {'$sum': 1}, 'total_used': {'$sum': '$used'}}}]
        IlIlIIIIIIllllIlII = lllllllllllIIll(llIIllIIllIllIIlll.aggregate(IIIllIllIllIIIIlIl))
        IIIIIlIlIllIlIllll = llIIllIIllIllIIlll.count_documents({})
        lllllllIllllllIIll = llIIllIIllIllIIlll.aggregate([{'$group': {'_id': None, 'total': {'$sum': '$used'}}}])
        lllllllIllllllIIll = llllllllllllIlI(lllllllIllllllIIll, {}).get('total', 0)
        llIlIIIlIIllllllII = '>📊 **Estadísticas de Administrador**\n\n'
        llIlIIIlIIllllllII += f'>👥 **Total de usuarios:** {IIIIIlIlIllIlIllll}\n'
        llIlIIIlIIllllllII += f'>🔢 **Total de compresiones:** {lllllllIllllllIIll}\n\n'
        llIlIIIlIIllllllII += '>📝 **Distribución por Planes:**\n'
        llllllIIlIlllIIllI = {'standard': '>🧩 Estándar', 'pro': '>💎 Pro', 'premium': '>👑 Premium'}
        for llIIIllIlIIlllllII in IlIlIIIIIIllllIlII:
            lIIIIlIlllIllllIII = llIIIllIlIIlllllII['_id']
            IlIlIlIlIIIlIIIlIl = llIIIllIlIIlllllII['count']
            lIllIlIlIlIllllIlI = llIIIllIlIIlllllII['total_used']
            IIlIIlIIIIlIlllIII = llllllIIlIlllIIllI.get(lIIIIlIlllIllllIII, lIIIIlIlllIllllIII.capitalize() if lIIIIlIlllIllllIII else '❓ Desconocido')
            llIlIIIlIIllllllII += f'\n{IIlIIlIIIIlIlllIII}:\n>  👥 Usuarios: {IlIlIlIlIIIlIIIlIl}\n>  🔢 Comprs: {lIllIlIlIlIllllIlI}\n'
        await IIIlIlIlIIlllIllII.reply(llIlIIIlIIllllllII)
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en admin_stats_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ **Error al generar estadísticas**')

async def IIIIIlllIIIIIlIllI(lIlIlIIlIlllllIIIl: lllllllllllIlIl, lIllllIlllIllIlIll: llllllllllIllll):
    try:
        IIIlllIllllllllIII = lllllllllllIIIl()
        for lIllIIIlllIllIIlII in llIIllIIllIllIIlll.find({}, {'user_id': 1}):
            IIIlllIllllllllIII.add(lIllIIIlllIllIIlII['user_id'])
        IIIlllIllllllllIII = [IlIlIlIllIIIllIIlI for IlIlIlIllIIIllIIlI in IIIlllIllllllllIII if IlIlIlIllIIIllIIlI not in IIIIlllIlllllIIlll]
        IIIIIlIlIllIlIllll = llllllllllllIII(IIIlllIllllllllIII)
        if IIIIIlIlIllIlIllll == 0:
            await IIIlIIIIlIIIIlllII.send_message(lIlIlIIlIlllllIIIl, '📭 No hay usuarios para enviar el mensaje.')
            return
        await IIIlIIIIlIIIIlllII.send_message(lIlIlIIlIlllllIIIl, f'📤 **Iniciando difusión a {IIIIIlIlIllIlIllll} usuarios...**\n⏱ Esto puede tomar varios minutos.')
        lIlIIIIlIIIllIIlll = 0
        lIIIIIIlllIlIlIlII = 0
        IlIlIlIlIIIlIIIlIl = 0
        for lIllIIIIllIIIllIlI in IIIlllIllllllllIII:
            IlIlIlIlIIIlIIIlIl += 1
            try:
                await lIIlIlllIllllIllII(lIllIIIIllIIIllIlI, f'>🔔**Notificación:**\n\n{lIllllIlllIllIlIll}')
                lIlIIIIlIIIllIIlll += 1
                await lIllIllIlIIlII(0.5)
            except lllllllllllllIl as lIlllllIIIIllIIIIl:
                llIlllIIllIIlIIlll.error(f'Error enviando mensaje a {lIllIIIIllIIIllIlI}: {lIlllllIIIIllIIIIl}')
                lIIIIIIlllIlIlIlII += 1
        await IIIlIIIIlIIIIlllII.send_message(lIlIlIIlIlllllIIIl, f'✅ **Difusión completada!**\n\n👥 Total de usuarios: {IIIIIlIlIllIlIllll}\n✅ Enviados correctamente: {lIlIIIIlIIIllIIlll}\n❌ Fallidos: {lIIIIIIlllIlIlIlII}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en broadcast_message: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIIIIlIIIIlllII.send_message(lIlIlIIlIlllllIIIl, f'⚠️ Error en difusión: {llllllllllIllll(lIlllllIIIIllIIIIl)}')

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.lIlIIIlIlIlIlllIlI('msg') & IIlllIlIIllllI.lIllIIIlllIllIIlII(lllIIIlIllIlllIIII))
async def IIIIlIIIIlIIlIIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        if not IIIlIlIlIIlllIllII.IllllIIIlllllIIIll or llllllllllllIII(IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split()) < 2:
            await IIIlIlIlIIlllIllII.reply('⚠️ Formato: /msg <mensaje>')
            return
        lllIlIIllIllIlIllI = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll.split(maxsplit=1)
        llIIIlllIllIlIIIII = lllIlIIllIllIlIllI[1] if llllllllllllIII(lllIlIIllIllIlIllI) > 1 else ''
        if not llIIIlllIllIlIIIII.strip():
            await IIIlIlIlIIlllIllII.reply('⚠️ El mensaje no puede estar vacío')
            return
        lIlIlIIlIlllllIIIl = IIIlIlIlIIlllIllII.from_user.id
        lIIIlIlIlIIIlI(IIIIIlllIIIIIlIllI(lIlIlIIlIlllllIIIl, llIIIlllIllIlIIIII))
        await IIIlIlIlIIlllIllII.reply('📤 **Difusión iniciada!**\n⏱ Los mensajes se enviarán progresivamente a todos los usuarios.\nRecibirás un reporte final cuando se complete.')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en broadcast_command: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        await IIIlIlIlIIlllIllII.reply('⚠️ Error al iniciar la difusión')

async def IIIlIIIlIIllIllIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    """Muestra información sobre la cola de compresión"""
    lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
    lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
    if lIllIlIIIllIIIlIll is None or lIllIlIIIllIIIlIll.get('plan') is None:
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '>➣ **Usted no tiene acceso para usar este bot.**\n\n>Por favor, adquiera un plan para poder ver la cola de compresión.')
        return
    if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
        await llllIIIllIIIlIIIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        return
    lIIllllIIlIlIIlllI = IIlIlIIIlIIlIlIIlI.count_documents({})
    IlIllIllIlllllIlII = lllllllllllIIll(IIlIlIIIlIIlIlIIlI.find({'user_id': lIllIIIIllIIIllIlI}))
    lIlIllIIlIlIlllIlI = llllllllllllIII(IlIllIllIlllllIlII)
    if lIIllllIIlIlIIlllI == 0:
        llIlIIIlIIllllllII = '>➣**La cola de compresión está vacía.**'
    else:
        llllIIlIIlIIIIlIIl = lllllllllllIIll(IIlIlIIIlIIlIlIIlI.find().sort([('priority', 1), ('timestamp', 1)]))
        lIlllIlllllllIIIII = None
        for (IIIllIIIllIllllIll, llIIIIIIlIlIIIlIIl) in llllllllllllIll(llllIIlIIlIIIIlIIl, 1):
            if llIIIIIIlIlIIIlIIl['user_id'] == lIllIIIIllIIIllIlI:
                lIlllIlllllllIIIII = IIIllIIIllIllllIll
                break
        if lIlIllIIlIlIlllIlI == 0:
            llIlIIIlIIllllllII = f'>📋 **Estado de la cola**\n\n>• Total de videos en cola: {lIIllllIIlIlIIlllI}\n>• Tus videos en cola: 0\n\n>No tienes videos pendientes de compresión.'
        else:
            llIlIIIlIIllllllII = f'>📋 **Estado de la cola**\n\n>• Total de videos en cola: {lIIllllIIlIlIIlllI}\n>• Tus videos en cola: {lIlIllIIlIlIlllIlI}\n>• Posición de tu primer video: {lIlllIlllllllIIIII}\n\n>⏱ Por favor ten paciencia mientras se procesa tu video.'
    await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, llIlIIIlIIllllllII)

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.llIIlIIIlllllIllII)
async def IlIlIIIllllIIlIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII: llllllIlllIlIl):
    try:
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            llIlllIIllIIlIIlll.warning(f'Intento de uso por usuario baneado: {lIllIIIIllIIIllIlI}')
            return
        lIllIlIIIllIIIlIll = await IllllIIllllIIllIIl(lIllIIIIllIIIllIlI)
        if lIllIlIIIllIIIlIll is None or lIllIlIIIllIIIlIll.get('plan') is None:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '>➣ **Usted no tiene acceso para usar este bot.**\n\n>👨🏻\u200d💻**Contacta con @InfiniteNetworkAdmin para actualizar tu Plan**')
            return
        if await IlllIlIllIllllIIll(lIllIIIIllIIIllIlI):
            llIlllIIllIIlIIlll.info(f'Usuario {lIllIIIIllIIIllIlI} tiene confirmación pendiente, ignorando video adicional')
            return
        if await lllIllllllIIIlIlll(lIllIIIIllIIIllIlI):
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, f">⚠️ **Límite alcanzado**\n>Has usado {lIllIlIIIllIIIlIll['used']}/{IIIllIIIllIllllIIl[lIllIlIIIllIIIlIll['plan']]} videos.\n\n>👨🏻\u200d💻**Contacta con @InfiniteNetworkAdmin para actualizar tu Plan**")
            return
        lIlIIllIIIlIIllllI = await IIlIllIlllIIlIlllI(lIllIIIIllIIIllIlI)
        lIlIIllIIIIlllIIII = IIlIlIIIlIIlIlIIlI.count_documents({'user_id': lIllIIIIllIIIllIlI})
        if lIllIlIIIllIIIlIll['plan'] == 'premium':
            if lIlIIllIIIIlllIIII >= IIllllIIllIllIllll:
                await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, f'>➣ Ya tienes {lIlIIllIIIIlllIIII} videos en cola (límite: {IIllllIIllIllIllll}).\n>Por favor espera a que se procesen antes de enviar más.')
                return
        elif lIlIIllIIIlIIllllI or lIlIIllIIIIlllIIII > 0:
            await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, '>➣ Ya tienes un video en proceso de compresión o en cola.\n>Por favor espera a que termine antes de enviar otro video.')
            return
        IIlIIllIlIllIIIlII = await IlIlIlIIlIIllIIIll(lIllIIIIllIIIllIlI, IIIlIlIlIIlllIllII.chat.id, IIIlIlIlIIlllIllII.id, IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IIIllIIIlIlIlIlIIl, IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII)
        IllIIllIIlIlIlllIl = IlIIlIIllllIlI([[llIlIIlIlllIII('🟢 Confirmar compresión 🟢', callback_data=f'confirm_{IIlIIllIlIllIIIlII}')], [llIlIIlIlllIII('⛔ Cancelar ⛔', callback_data=f'cancel_{IIlIIllIlIllIIIlII}')]])
        await lIIlIlllIllllIllII(IIIlIlIlIIlllIllII.chat.id, f'>🎬 **Video recibido para comprimír:** `{IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII}`\n\n>¿Deseas comprimir este video?', reply_to_message_id=IIIlIlIlIIlllIllII.id, reply_markup=IllIIllIIlIlIlllIl)
        llIlllIIllIIlIIlll.info(f'Solicitud de confirmación creada para {lIllIIIIllIIIllIlI}: {IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en handle_video: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

@IIIlIIIIlIIIIlllII.on_message(IIlllIlIIllllI.IllllIIIlllllIIIll)
async def IlIIIIIlllIlIllIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII):
    try:
        IllllIIIlllllIIIll = IIIlIlIlIIlllIllII.IllllIIIlllllIIIll
        lIIIIIIIllIllIlIIl = IIIlIlIlIIlllIllII.from_user.lIIIIIIIllIllIlIIl
        lIlIIlIIllIlIIIIIl = IIIlIlIlIIlllIllII.chat.id
        lIllIIIIllIIIllIlI = IIIlIlIlIIlllIllII.from_user.id
        if lIllIIIIllIIIllIlI in IIIIlllIlllllIIlll:
            return
        llIlllIIllIIlIIlll.info(f'Mensaje recibido de {lIllIIIIllIIIllIlI}: {IllllIIIlllllIIIll}')
        if IllllIIIlllllIIIll.startswith(('/calidad', '.calidad')):
            lllIlllIIIIllIIIIl(IllllIIIlllllIIIll[llllllllllllIII('/calidad '):])
            await IIIlIlIlIIlllIllII.reply(f'>⚙️ Configuración Actualizada✅: {IIlllIlIlIlIllllIl}')
        elif IllllIIIlllllIIIll.startswith(('/settings', '.settings')):
            await IlIlllllIIllIIlIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/banuser', '.banuser', '/deluser', '.deluser')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await llIIlllIllIlIIIlll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
            else:
                llIlllIIllIIlIIlll.warning(f'Intento no autorizado de banuser/deluser por {lIllIIIIllIIIllIlI}')
        elif IllllIIIlllllIIIll.startswith(('/cola', '.cola')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIllIlIlIlIlIIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/auto', '.auto')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIllllIIIlIllIlIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/myplan', '.myplan')):
            await llllIlllIIIlIlIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/setplan', '.setplan')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIllIIlIlIlIlIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/resetuser', '.resetuser')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await llIlIIIIIIlIIlIIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/userinfo', '.userinfo')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await llIlIIIIIllllIIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/planes', '.planes')):
            await IIIllIlIlllllllIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/generatekey', '.generatekey')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await lIllllIllllIllIIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/listkeys', '.listkeys')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIIlIIlIIlIlIlIIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/delkeys', '.delkeys')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IllIIlIIlIlllIllIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/user', '.user')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await lIllIIllllllIIllII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/admin', '.admin')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await lIllIIlllIlllIIIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/restuser', '.restuser')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await llIIlIIllIlIIllIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/desuser', '.desuser')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await llIlllIIlIIIIlIIlI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/deleteuser', '.deleteuser')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await lIlIllIIIIlIIIlllI(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/viewban', '.viewban')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIlllIlIlllIIIllll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/msg', '.msg')):
            if lIllIIIIllIIIllIlI in lllIIIlIllIlllIIII:
                await IIIIlIIIIlIIlIIIIl(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/cancel', '.cancel')):
            await llIlIIIlIIIIlIlIII(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        elif IllllIIIlllllIIIll.startswith(('/key', '.key')):
            await llIllIlIllllIllIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII)
        if IIIlIlIlIIlllIllII.reply_to_message:
            IIIllIlllllIIIlIlI = IIllllIIIllllIIlIl.get(IIIlIlIlIIlllIllII.reply_to_message.id)
            if IIIllIlllllIIIlIlI:
                lIllIIIIllIIIllIlI = IIIllIlllllIIIlIlI['user_id']
                IlllllIlIIIIllIllI = f'Respuesta de @{IIIlIlIlIIlllIllII.from_user.lIIIIIIIllIllIlIIl}' if IIIlIlIlIIlllIllII.from_user.lIIIIIIIllIllIlIIl else f'Respuesta de user ID: {IIIlIlIlIIlllIllII.from_user.id}'
                await lIIlIlllIllllIllII(lIllIIIIllIIIllIlI, f'{IlllllIlIIIIllIllI}: {IIIlIlIlIIlllIllII.IllllIIIlllllIIIll}')
                llIlllIIllIIlIIlll.info(f'Respuesta enviada a {lIllIIIIllIIIllIlI}')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error en handle_message: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))

async def IlIlIllllllllIlIll(lIlIllIIllIIIllIIl, IIIlIlIlIIlllIllII: llllllIlllIlIl, lIlllllIIIIIIlIlll: lllllllllllIlIl, lIlIIIIIIIllIlIIlI: lllllllllllIlIl=None, llIIIlIIllIIllllII: llllllllllIllll='start'):
    try:
        lllllIIIllIIllIlIl = -4826894501
        lIllIIIlllIllIIlII = IIIlIlIlIIlllIllII.from_user
        lIIIIIIIllIllIlIIl = f'@{lIllIIIlllIllIIlII.lIIIIIIIllIllIlIIl}' if lIllIIIlllIllIIlII.lIIIIIIIllIllIlIIl else 'Sin username'
        IlIIllIlllIIIllIII = IIIlIlIlIIlllIllII.llIIlIIIlllllIllII.IlIIllIlllIIIllIII or 'Sin nombre'
        IIIllIIIIIlIIIllll = lIlllllIIIIIIlIlll // (1024 * 1024)
        if llIIIlIIllIIllllII == 'start':
            IllllIIIlllllIIIll = f'>📤 **Nuevo video recibido para comprimir**\n\n>👤 **Usuario:** {lIIIIIIIllIllIlIIl}\n>🆔 **ID:** `{lIllIIIlllIllIIlII.id}`\n>📦 **Tamaño original:** {IIIllIIIIIlIIIllll} MB\n>📁 **Nombre:** `{IlIIllIlllIIIllIII}`'
        elif llIIIlIIllIIllllII == 'done':
            IIIlIlIIIlIlIIIllI = lIlIIIIIIIllIlIIlI // (1024 * 1024)
            IllllIIIlllllIIIll = f'>📥 **Video comprimido y enviado**\n\n>👤 **Usuario:** {lIIIIIIIllIllIlIIl}\n>🆔 **ID:** `{lIllIIIlllIllIIlII.id}`\n>📦 **Tamaño original:** {IIIllIIIIIlIIIllll} MB\n>📉 **Tamaño comprimido:** {IIIlIlIIIlIlIIIllI} MB\n>📁 **Nombre:** `{IlIIllIlllIIIllIII}`'
        await IIIlIIIIlIIIIlllII.send_message(chat_id=lllllIIIllIIllIlIl, text=IllllIIIlllllIIIll)
        llIlllIIllIIlIIlll.info(f'Notificación enviada al grupo: {lIllIIIlllIllIIlII.id} - {IlIIllIlllIIIllIII} ({llIIIlIIllIIllllII})')
    except lllllllllllllIl as lIlllllIIIIllIIIIl:
        llIlllIIllIIlIIlll.error(f'Error enviando notificación al grupo: {lIlllllIIIIllIIIIl}')
try:
    llIlllIIllIIlIIlll.info('Iniciando el bot...')
    IIIlIIIIlIIIIlllII.run()
except lllllllllllllIl as lIlllllIIIIllIIIIl:
    llIlllIIllIIlIIlll.critical(f'Error fatal al iniciar el bot: {lIlllllIIIIllIIIIl}', exc_info=lllllllllllIllI(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))