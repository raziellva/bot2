_z='video_id'
_y='No expira'
_x='join_date'
_w='file_id'
_v='cancel'
_u='upload'
_t='download'
_s='preset'
_r='audio_bitrate'
_q='resolution'
_p='⚠️ Error en el comando'
_o='%Y-%m-%d %H:%M:%S'
_n='banned_at'
_m='🎬 Anime y series animadas'
_l='📺 Shows/Reality'
_k='📱 Reels y Videos cortos'
_j='🗜️Compresión General🔧'
_i='duration_unit'
_h='duration_value'
_g='hours'
_f='minutes'
_e='⛔ **Operación cancelada por el usuario** ⛔'
_d='ffmpeg'
_c='original_message_id'
_b='task'
_a='anime'
_Z='show'
_Y='reels'
_X='general'
_W='start'
_V='¿?'
_U='⛔ Cancelar ⛔'
_T='file_name'
_S='message_id'
_R='chat_id'
_Q='type'
_P='Sin username'
_O='$set'
_N='pro'
_M='key'
_L='standard'
_K='premium'
_J='priority'
_I='expires_at'
_H='_id'
_G='timestamp'
_F=False
_E='used'
_D='plan'
_C=None
_B='user_id'
_A=True
import os,logging,asyncio,threading,concurrent.futures
from pyrogram import Client,filters
import random,string,datetime,subprocess
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,CallbackQuery
from pyrogram.errors import MessageNotModified
import ffmpeg,re,time
from pymongo import MongoClient
from config import*
from bson.objectid import ObjectId
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',handlers=[logging.FileHandler('bot.log'),logging.StreamHandler()])
logger=logging.getLogger(__name__)
PLAN_PRIORITY={_K:1,_N:2,_L:3}
PREMIUM_QUEUE_LIMIT=5
mongo_client=MongoClient(MONGO_URI)
db=mongo_client[DATABASE_NAME]
pending_col=db['pending']
users_col=db['users']
temp_keys_col=db['temp_keys']
banned_col=db['banned_users']
pending_confirmations_col=db['pending_confirmations']
active_compressions_col=db['active_compressions']
api_id=API_ID
api_hash=API_HASH
bot_token=BOT_TOKEN
app=Client('compress_bot',api_id=api_id,api_hash=api_hash,bot_token=bot_token)
admin_users=ADMINS_IDS
ban_users=[]
banned_users_in_db=banned_col.find({},{_B:1})
for banned_user in banned_users_in_db:
	if banned_user[_B]not in ban_users:ban_users.append(banned_user[_B])
active_compressions_col.delete_many({})
logger.info('Compresiones activas previas eliminadas')
video_settings={_q:'854x480','crf':'28',_r:'120k','fps':'22',_s:'veryfast','codec':'libx264'}
compression_queue=asyncio.PriorityQueue()
processing_task=_C
executor=concurrent.futures.ThreadPoolExecutor(max_workers=1)
active_messages=set()
cancel_tasks={}
def register_cancelable_task(user_id,task_type,task,original_message_id=_C):'Registra una tarea que puede ser cancelada';cancel_tasks[user_id]={_Q:task_type,_b:task,_c:original_message_id}
def unregister_cancelable_task(user_id):
	'Elimina el registro de una tarea cancelable'
	if user_id in cancel_tasks:del cancel_tasks[user_id]
def cancel_user_task(user_id):
	'Cancela la tarea activa de un usuario'
	if user_id in cancel_tasks:
		task_info=cancel_tasks[user_id]
		try:
			if task_info[_Q]==_t:return _A
			elif task_info[_Q]==_d and task_info[_b].poll()is _C:task_info[_b].terminate();return _A
			elif task_info[_Q]==_u:return _A
		except Exception as e:logger.error(f"Error cancelando tarea: {e}")
	return _F
@app.on_message(filters.command(_v)&filters.private)
async def cancel_command(client,message):
	'Maneja el comando de cancelación';user_id=message.from_user.id
	if user_id in cancel_tasks:
		if cancel_user_task(user_id):original_message_id=cancel_tasks[user_id].get(_c);unregister_cancelable_task(user_id);await send_protected_message(message.chat.id,_e,reply_to_message_id=original_message_id)
		else:await send_protected_message(message.chat.id,'⚠️ **No se pudo cancelar la operación**\nLa tarea podría haber finalizado ya.')
	else:
		result=pending_col.delete_many({_B:user_id})
		if result.deleted_count>0:await send_protected_message(message.chat.id,f"⛔ **Se cancelaron {result.deleted_count} tareas pendientes en la cola.** ⛔")
		else:await send_protected_message(message.chat.id,'ℹ️ **No tienes operaciones activas ni en cola para cancelar.**')
	try:await message.delete()
	except Exception as e:logger.error(f"Error borrando mensaje /cancel: {e}")
async def has_active_compression(user_id):'Verifica si el usuario ya tiene una compresión activa';return bool(active_compressions_col.find_one({_B:user_id}))
async def add_active_compression(user_id,file_id):'Registra una nueva compresión activa';active_compressions_col.insert_one({_B:user_id,_w:file_id,'start_time':datetime.datetime.now()})
async def remove_active_compression(user_id):'Elimina una compresión activa';active_compressions_col.delete_one({_B:user_id})
async def has_pending_confirmation(user_id):'Verifica si el usuario tiene una confirmación pendiente (no expirada)';now=datetime.datetime.now();expiration_time=now-datetime.timedelta(minutes=10);pending_confirmations_col.delete_many({_B:user_id,_G:{'$lt':expiration_time}});return bool(pending_confirmations_col.find_one({_B:user_id}))
async def create_confirmation(user_id,chat_id,message_id,file_id,file_name):'Crea una nueva confirmación pendiente eliminando cualquier confirmación previa';pending_confirmations_col.delete_many({_B:user_id});return pending_confirmations_col.insert_one({_B:user_id,_R:chat_id,_S:message_id,_w:file_id,_T:file_name,_G:datetime.datetime.now()}).inserted_id
async def delete_confirmation(confirmation_id):'Elimina una confirmación pendiente';pending_confirmations_col.delete_one({_H:confirmation_id})
async def get_confirmation(confirmation_id):'Obtiene una confirmación pendiente';return pending_confirmations_col.find_one({_H:confirmation_id})
async def register_new_user(user_id):
	'Registra un nuevo usuario si no existe'
	if not users_col.find_one({_B:user_id}):logger.info(f"Usuario no registrado: {user_id}")
async def should_protect_content(user_id):
	'Determina si el contenido debe protegerse según el plan del usuario'
	if user_id in admin_users:return _F
	user_plan=await get_user_plan(user_id);return user_plan is _C or user_plan[_D]==_L
async def send_protected_message(chat_id,text,**kwargs):'Envía un mensaje con protección según el plan del usuario';protect=await should_protect_content(chat_id);return await app.send_message(chat_id,text,protect_content=protect,**kwargs)
async def send_protected_video(chat_id,video,caption=_C,**kwargs):'Envía un video con protección según el plan del usuario';protect=await should_protect_content(chat_id);return await app.send_video(chat_id,video,caption=caption,protect_content=protect,**kwargs)
async def send_protected_photo(chat_id,photo,caption=_C,**kwargs):'Envía una foto con protección según el plan del usuario';protect=await should_protect_content(chat_id);return await app.send_photo(chat_id,photo,caption=caption,protect_content=protect,**kwargs)
async def get_user_priority(user_id):
	'Obtiene la prioridad del usuario basada en su plan';user_plan=await get_user_plan(user_id)
	if user_plan is _C:return 4
	return PLAN_PRIORITY.get(user_plan[_D],4)
def generate_temp_key(plan,duration_value,duration_unit):
	'Genera una clave temporal válida para un plan específico';key=''.join(random.choices(string.ascii_letters+string.digits,k=10));created_at=datetime.datetime.now()
	if duration_unit==_f:expires_at=created_at+datetime.timedelta(minutes=duration_value)
	elif duration_unit==_g:expires_at=created_at+datetime.timedelta(hours=duration_value)
	else:expires_at=created_at+datetime.timedelta(days=duration_value)
	temp_keys_col.insert_one({_M:key,_D:plan,'created_at':created_at,_I:expires_at,_E:_F,_h:duration_value,_i:duration_unit});return key
def is_valid_temp_key(key):'Verifica si una clave temporal es válida';now=datetime.datetime.now();key_data=temp_keys_col.find_one({_M:key,_E:_F,_I:{'$gt':now}});return bool(key_data)
def mark_key_used(key):'Marca una clave como usada';temp_keys_col.update_one({_M:key},{_O:{_E:_A}})
@app.on_message(filters.command('generatekey')&filters.user(admin_users))
async def generate_key_command(client,message):
	'Genera una nueva clave temporal para un plan específico (solo admins)'
	try:
		parts=message.text.split()
		if len(parts)!=4:await message.reply('⚠️ Formato: /generatekey <plan> <cantidad> <unidad>\nEjemplo: /generatekey standard 2 hours\nUnidades válidas: minutes, hours, days');return
		plan=parts[1].lower();valid_plans=[_L,_N,_K]
		if plan not in valid_plans:await message.reply(f"⚠️ Plan inválido. Opciones válidas: {', '.join(valid_plans)}");return
		try:
			duration_value=int(parts[2])
			if duration_value<=0:await message.reply('⚠️ La cantidad debe ser un número positivo');return
		except ValueError:await message.reply('⚠️ La cantidad debe ser un número entero');return
		duration_unit=parts[3].lower();valid_units=[_f,_g,'days']
		if duration_unit not in valid_units:await message.reply(f"⚠️ Unidad inválida. Opciones válidas: {', '.join(valid_units)}");return
		key=generate_temp_key(plan,duration_value,duration_unit);duration_text=f"{duration_value} {duration_unit}"
		if duration_value==1:duration_text=duration_text[:-1]
		await message.reply(f""">🔑 **Clave {plan.capitalize()} generada**

>Clave: `{key}`
>Válida por: {duration_text}

Comparte esta clave con el usuario usando:
`/key {key}`""")
	except Exception as e:logger.error(f"Error generando clave: {e}",exc_info=_A);await message.reply('⚠️ Error al generar la clave')
@app.on_message(filters.command('listkeys')&filters.user(admin_users))
async def list_keys_command(client,message):
	'Lista todas las claves temporales activas (solo admins)'
	try:
		now=datetime.datetime.now();keys=list(temp_keys_col.find({_E:_F,_I:{'$gt':now}}))
		if not keys:await message.reply('>📭 **No hay claves activas.**');return
		response='>🔑 **Claves temporales activas:**\n\n'
		for key in keys:
			expires_at=key[_I];remaining=expires_at-now
			if remaining.days>0:time_remaining=f"{remaining.days}d {remaining.seconds//3600}h"
			elif remaining.seconds>=3600:time_remaining=f"{remaining.seconds//3600}h {remaining.seconds%3600//60}m"
			else:time_remaining=f"{remaining.seconds//60}m"
			duration_value=key.get(_h,0);duration_unit=key.get(_i,'days');duration_display=f"{duration_value} {duration_unit}"
			if duration_value==1:duration_display=duration_display[:-1]
			response+=f"""• `{key[_M]}`
  ↳ Plan: {key[_D].capitalize()}
  ↳ Duración: {duration_display}
  ⏱ Expira en: {time_remaining}

"""
		await message.reply(response)
	except Exception as e:logger.error(f"Error listando claves: {e}",exc_info=_A);await message.reply('⚠️ Error al listar claves')
@app.on_message(filters.command('delkeys')&filters.user(admin_users))
async def del_keys_command(client,message):
	'Elimina claves temporales (solo admins)'
	try:
		parts=message.text.split()
		if len(parts)<2:await message.reply('⚠️ Formato: /delkeys <key> o /delkeys --all');return
		option=parts[1]
		if option=='--all':result=temp_keys_col.delete_many({});await message.reply(f"🗑️ **Se eliminaron {result.deleted_count} claves.**")
		else:
			key=option;result=temp_keys_col.delete_one({_M:key})
			if result.deleted_count>0:await message.reply(f"✅ **Clave {key} eliminada.**")
			else:await message.reply('⚠️ **Clave no encontrada.**')
	except Exception as e:logger.error(f"Error eliminando claves: {e}",exc_info=_A);await message.reply('⚠️ **Error al eliminar claves**')
PLAN_LIMITS={_L:60,_N:130,_K:280}
PLAN_DURATIONS={_L:'7 días',_N:'15 días',_K:'30 días'}
async def get_user_plan(user_id):
	'Obtiene el plan del usuario desde la base de datos y elimina si ha expirado';A='last_used_date';user=users_col.find_one({_B:user_id});now=datetime.datetime.now()
	if user:
		plan=user.get(_D)
		if plan is _C:users_col.delete_one({_B:user_id});return
		expires_at=user.get(_I)
		if expires_at and now>expires_at:users_col.delete_one({_B:user_id});return
		update_data={}
		if _E not in user:update_data[_E]=0
		if A not in user:update_data[A]=_C
		if update_data:users_col.update_one({_B:user_id},{_O:update_data});user.update(update_data)
		return user
async def increment_user_usage(user_id):
	'Incrementa el contador de uso del usuario';user=await get_user_plan(user_id)
	if user:users_col.update_one({_B:user_id},{'$inc':{_E:1}})
async def reset_user_usage(user_id):
	'Resetea el contador de uso del usuario';user=await get_user_plan(user_id)
	if user:users_col.update_one({_B:user_id},{_O:{_E:0}})
async def set_user_plan(user_id,plan,notify=_A,expires_at=_C):
	'Establece el plan de un usuario y notifica si notify=True'
	if plan not in PLAN_LIMITS:return _F
	user_data={_D:plan,_E:0}
	if expires_at is not _C:user_data[_I]=expires_at
	existing_user=users_col.find_one({_B:user_id})
	if not existing_user:user_data[_x]=datetime.datetime.now()
	users_col.update_one({_B:user_id},{_O:user_data},upsert=_A)
	if notify:
		try:await send_protected_message(user_id,f""">🎉 **¡Se te ha asignado un nuevo plan!**
>Use el comando /start para iniciar en el bot

>• **Plan**: {plan.capitalize()}
>• **Duración**: {PLAN_DURATIONS[plan]}
>• **Videos disponibles**: {PLAN_LIMITS[plan]}

>¡Disfruta de tus beneficios! 🎬""")
		except Exception as e:logger.error(f"Error notificando al usuario {user_id}: {e}")
	return _A
async def check_user_limit(user_id):
	'Verifica si el usuario ha alcanzado su límite de compresión';user=await get_user_plan(user_id)
	if user is _C or user.get(_D)is _C:return _A
	used_count=user.get(_E,0);return used_count>=PLAN_LIMITS.get(user[_D],0)
async def get_plan_info(user_id):
	'Obtiene información del plan del usuario para mostrar';user=await get_user_plan(user_id)
	if user is _C or user.get(_D)is _C:return'>➣ **No tienes un plan activo.**\n\n>Por favor, adquiere un plan para usar el bot.'
	plan_name=user[_D].capitalize();used=user.get(_E,0);limit=PLAN_LIMITS[user[_D]];remaining=max(0,limit-used);percent=min(100,used/limit*100)if limit>0 else 0;bar_length=15;filled=int(bar_length*percent/100);bar='⬢'*filled+'⬡'*(bar_length-filled);expires_at=user.get(_I);expires_text=_y
	if isinstance(expires_at,datetime.datetime):
		now=datetime.datetime.now();time_remaining=expires_at-now
		if time_remaining.total_seconds()<=0:expires_text='Expirado'
		else:
			days=time_remaining.days;hours=time_remaining.seconds//3600;minutes=time_remaining.seconds%3600//60
			if days>0:expires_text=f"{days} días"
			elif hours>0:expires_text=f"{hours} horas"
			else:expires_text=f"{minutes} minutos"
	return f""">╭✠━━━━━━━━━━━━━━━━━━✠╮
>┠➣ **Plan actual**: {plan_name}
>┠➣ **Videos usados**: {used}/{limit}
>┠➣ **Restantes**: {remaining}
>┠➣ **Progreso**:
>[{bar}] {int(percent)}%
>╰✠━━━━━━━━━━━━━━━━━━✠╯"""
async def has_pending_in_queue(user_id):'Verifica si el usuario tiene videos pendientes en la cola';count=pending_col.count_documents({_B:user_id});return count>0
def sizeof_fmt(num,suffix='B'):
	'Formatea el tamaño de bytes a formato legible'
	for unit in['','K','M','G','T','P','E','Z']:
		if abs(num)<1024.:return'%3.2f%s%s'%(num,unit,suffix)
		num/=1024.
	return'%.2f%s%s'%(num,'Yi',suffix)
def create_progress_bar(current,total,proceso,length=15):
	'Crea una barra de progreso visual'
	if total==0:total=1
	percent=current/total;filled=int(length*percent);bar='⬢'*filled+'⬡'*(length-filled);return f"    ╭━━━[🤖**Compress Bot**]━━━╮\n>┠➣ [{bar}] {round(percent*100)}%\n>┠➣ **Procesado**: {sizeof_fmt(current)}/{sizeof_fmt(total)}\n>┠➣ **Estado**: __#{proceso}__"
last_progress_update={}
async def progress_callback(current,total,msg,proceso,start_time):
	'Callback para mostrar progreso de descarga/subida con verificación de cancelación'
	try:
		if msg.id not in active_messages:return
		now=datetime.datetime.now();key=msg.chat.id,msg.id;last_time=last_progress_update.get(key)
		if last_time and(now-last_time).total_seconds()<5:return
		last_progress_update[key]=now;elapsed=time.time()-start_time;percentage=current/total;speed=current/elapsed if elapsed>0 else 0;eta=(total-current)/speed if speed>0 else 0;progress_bar=create_progress_bar(current,total,proceso);cancel_button=InlineKeyboardMarkup([[InlineKeyboardButton(_U,callback_data=f"cancel_task_{msg.chat.id}")]])
		try:await msg.edit(f">   {progress_bar}\n>┠➣ **Velocidad** {sizeof_fmt(speed)}/s\n>┠➣ **Tiempo restante:** {int(eta)}s\n>╰━━━━━━━━━━━━━━━━━━╯\n",reply_markup=cancel_button)
		except MessageNotModified:pass
		except Exception as e:
			logger.error(f"Error editando mensaje de progreso: {e}")
			if msg.id in active_messages:active_messages.remove(msg.id)
	except Exception as e:logger.error(f"Error en progress_callback: {e}",exc_info=_A)
async def process_compression_queue():
	while _A:
		priority,timestamp,(client,message,wait_msg)=await compression_queue.get()
		try:start_msg=await wait_msg.edit('🗜️**Iniciando compresión**🎬');loop=asyncio.get_running_loop();await loop.run_in_executor(executor,threading_compress_video,client,message,start_msg)
		except Exception as e:logger.error(f"Error procesando video: {e}",exc_info=_A);await app.send_message(message.chat.id,f"⚠️ Error al procesar el video: {str(e)}")
		finally:pending_col.delete_one({_z:message.video.file_id});compression_queue.task_done()
def threading_compress_video(client,message,start_msg):loop=asyncio.new_event_loop();asyncio.set_event_loop(loop);loop.run_until_complete(compress_video(client,message,start_msg));loop.close()
@app.on_message(filters.command(['deleteall'])&filters.user(admin_users))
async def delete_all_pending(client,message):result=pending_col.delete_many({});await message.reply(f">🗑️ **Cola eliminada.**\n**Se eliminaron {result.deleted_count} elementos.**")
@app.on_message(filters.regex('^/del_(\\d+)$')&filters.user(admin_users))
async def delete_one_from_pending(client,message):
	match=message.text.strip().split('_')
	if len(match)!=2 or not match[1].isdigit():await message.reply('⚠️ Formato inválido. Usa `/del_1`, `/del_2`, etc.');return
	index=int(match[1])-1;cola=list(pending_col.find().sort([(_J,1),(_G,1)]))
	if index<0 or index>=len(cola):await message.reply('⚠️ Número fuera de rango.');return
	eliminado=cola[index];pending_col.delete_one({_H:eliminado[_H]});file_name=eliminado.get(_T,_V);user_id=eliminado[_B];tiempo=eliminado.get(_G);tiempo_str=tiempo.strftime('%Y-%m-d %H:%M:%S')if tiempo else _V;await message.reply(f"✅ Eliminado de la cola:\n📁 {file_name}\n👤 ID: `{user_id}`\n⏰ {tiempo_str}")
async def show_queue(client,message):
	'Muestra la cola de compresión';cola=list(pending_col.find().sort([(_J,1),(_G,1)]))
	if not cola:await message.reply('>📭 **La cola está vacía.**');return
	priority_to_plan={v:k for(k,v)in PLAN_PRIORITY.items()};respuesta='>📋 **Cola de Compresión Activa (Priorizada)**\n\n'
	for(i,item)in enumerate(cola,1):user_id=item[_B];file_name=item.get(_T,_V);tiempo=item.get(_G);tiempo_str=tiempo.strftime('%H:%M:%S')if tiempo else _V;priority=item.get(_J,4);plan_name=priority_to_plan.get(priority,'Sin plan').capitalize();respuesta+=f"{i}. 👤 ID: `{user_id}` | 📁 {file_name} | ⏰ {tiempo_str} | 📋 {plan_name}\n"
	await message.reply(respuesta)
@app.on_message(filters.command('cola')&filters.user(admin_users))
async def ver_cola_command(client,message):await show_queue(client,message)
@app.on_message(filters.command('auto')&filters.user(admin_users))
async def startup_command(_,message):
	global processing_task;msg=await message.reply('🔄 Iniciando procesamiento de la cola...');pending_col.update_many({_J:{'$exists':_F}},{_O:{_J:4}});pendientes=pending_col.find().sort([(_J,1),(_G,1)])
	for item in pendientes:
		try:user_id=item[_B];chat_id=item[_R];message_id=item[_S];priority=item.get(_J,4);timestamp=item[_G];message=await app.get_messages(chat_id,message_id);wait_msg=await app.send_message(chat_id,f"🔄 Recuperado desde cola persistente.");await compression_queue.put((priority,timestamp,(app,message,wait_msg)))
		except Exception as e:logger.error(f"Error cargando pendiente: {e}")
	if processing_task is _C or processing_task.done():processing_task=asyncio.create_task(process_compression_queue())
	await msg.edit('✅ Procesamiento de cola iniciado.')
def update_video_settings(command):
	try:
		settings=command.split()
		for setting in settings:key,value=setting.split('=');video_settings[key]=value
		logger.info(f"⚙️Configuración actualizada⚙️: {video_settings}")
	except Exception as e:logger.error(f"Error actualizando configuración: {e}",exc_info=_A)
def create_compression_bar(percent,bar_length=10):
	try:percent=max(0,min(100,percent));filled_length=int(bar_length*percent/100);bar='⬢'*filled_length+'⬡'*(bar_length-filled_length);return f"[{bar}] {int(percent)}%"
	except Exception as e:logger.error(f"Error creando barra de progreso: {e}",exc_info=_A);return f"**Progreso**: {int(percent)}%"
async def compress_video(client,message,start_msg):
	C='SUBIDA';B='format';A='duration'
	try:
		if not message.video:await app.send_message(chat_id=message.chat.id,text='Por favor envía un vídeo válido');return
		logger.info(f"Iniciando compresión para chat_id: {message.chat.id}, video: {message.video.file_name}");user_id=message.from_user.id;original_message_id=message.id;await add_active_compression(user_id,message.video.file_id);msg=await app.send_message(chat_id=message.chat.id,text='📥 **Iniciando Descarga** 📥',reply_to_message_id=message.id);active_messages.add(msg.id);cancel_button=InlineKeyboardMarkup([[InlineKeyboardButton(_U,callback_data=f"cancel_task_{user_id}")]]);await msg.edit_reply_markup(cancel_button)
		try:start_download_time=time.time();register_cancelable_task(user_id,_t,_C,original_message_id=original_message_id);original_video_path=await app.download_media(message.video,progress=progress_callback,progress_args=(msg,'DESCARGA',start_download_time));logger.info(f"Video descargado: {original_video_path}")
		except Exception as e:
			logger.error(f"Error en descarga: {e}",exc_info=_A);await msg.edit(f"Error en descarga: {e}");await remove_active_compression(user_id);unregister_cancelable_task(user_id)
			if msg.id in active_messages:active_messages.remove(msg.id)
			return
		if user_id not in cancel_tasks:
			if original_video_path and os.path.exists(original_video_path):os.remove(original_video_path)
			await remove_active_compression(user_id);unregister_cancelable_task(user_id)
			try:await start_msg.delete()
			except:pass
			if msg.id in active_messages:active_messages.remove(msg.id)
			return
		original_size=os.path.getsize(original_video_path);logger.info(f"Tamaño original: {original_size} bytes");await notify_group(client,message,original_size,status=_W)
		try:probe=ffmpeg.probe(original_video_path);dur_total=float(probe[B][A]);logger.info(f"Duración del video: {dur_total} segundos")
		except Exception as e:logger.error(f"Error obteniendo duración: {e}",exc_info=_A);dur_total=0
		await msg.edit('>╭━━━━[🤖**Compress Bot**]━━━━━╮\n>┠➣ 🗜️𝗖𝗼𝗺𝗽𝗿𝗶𝗺𝗶𝗲𝗻𝗱𝗼 𝗩𝗶𝗱𝗲𝗼🎬\n>┠➣ **Progreso**: 📤 𝘊𝘢𝘳𝘨𝘢𝘯𝘥𝘰 𝘝𝘪𝘥𝘦𝘰 📤\n>╰━━━━━━━━━━━━━━━━━━━━━╯',reply_markup=cancel_button);compressed_video_path=f"{os.path.splitext(original_video_path)[0]}_compressed.mp4";logger.info(f"Ruta de compresión: {compressed_video_path}");drawtext_filter=f"drawtext=text='@InfiniteNetwork_KG':x=w-tw-10:y=10:fontsize=20:fontcolor=white";ffmpeg_command=[_d,'-y','-i',original_video_path,'-vf',f"scale={video_settings[_q]},{drawtext_filter}",'-crf',video_settings['crf'],'-b:a',video_settings[_r],'-r',video_settings['fps'],'-preset',video_settings[_s],'-c:v',video_settings['codec'],compressed_video_path];logger.info(f"Comando FFmpeg: {' '.join(ffmpeg_command)}")
		try:
			start_time=datetime.datetime.now();process=subprocess.Popen(ffmpeg_command,stderr=subprocess.PIPE,text=_A,bufsize=1);register_cancelable_task(user_id,_d,process,original_message_id=original_message_id);last_percent=0;last_update_time=0;time_pattern=re.compile('time=(\\d+:\\d+:\\d+\\.\\d+)')
			while _A:
				if user_id not in cancel_tasks:
					process.kill()
					if msg.id in active_messages:active_messages.remove(msg.id)
					try:await msg.delete();await start_msg.delete()
					except:pass
					if original_video_path and os.path.exists(original_video_path):os.remove(original_video_path)
					if compressed_video_path and os.path.exists(compressed_video_path):os.remove(compressed_video_path)
					await remove_active_compression(user_id);unregister_cancelable_task(user_id);return
				line=process.stderr.readline()
				if not line and process.poll()is not _C:break
				if line:
					match=time_pattern.search(line)
					if match and dur_total>0:
						time_str=match.group(1);h,m,s=time_str.split(':');current_time=int(h)*3600+int(m)*60+float(s);percent=min(100,current_time/dur_total*100)
						if percent-last_percent>=5:
							bar=create_compression_bar(percent);cancel_button=InlineKeyboardMarkup([[InlineKeyboardButton(_U,callback_data=f"cancel_task_{user_id}")]])
							try:await msg.edit(f">╭━━━━[**🤖Compress Bot**]━━━━━╮\n>┠➣ 🗜️𝗖𝗼𝗺𝗽𝗿𝗶𝗺𝗶𝗲𝗻𝗱𝗼 𝗩𝗶𝗱𝗲𝗼🎬\n>┠➣ **Progreso**: {bar}\n>╰━━━━━━━━━━━━━━━━━━━━━╯",reply_markup=cancel_button)
							except MessageNotModified:pass
							except Exception as e:
								logger.error(f"Error editando mensaje de progreso: {e}")
								if msg.id in active_messages:active_messages.remove(msg.id)
							last_percent=percent;last_update_time=time.time()
			compressed_size=os.path.getsize(compressed_video_path);logger.info(f"Compresión completada. Tamaño comprimido: {compressed_size} bytes")
			try:
				probe=ffmpeg.probe(compressed_video_path);duration=int(float(probe.get(B,{}).get(A,0)))
				if duration==0:
					for stream in probe.get('streams',[]):
						if A in stream:duration=int(float(stream[A]));break
				if duration==0:duration=0
				logger.info(f"Duración del video comprimido: {duration} segundos")
			except Exception as e:logger.error(f"Error obteniendo duración comprimido: {e}",exc_info=_A);duration=0
			thumbnail_path=f"{compressed_video_path}_thumb.jpg"
			try:ffmpeg.input(compressed_video_path,ss=duration//2 if duration>0 else 0).filter('scale',320,-1).output(thumbnail_path,vframes=1).overwrite_output().run(capture_stdout=_A,capture_stderr=_A);logger.info(f"Miniatura generada: {thumbnail_path}")
			except Exception as e:logger.error(f"Error generando miniatura: {e}",exc_info=_A);thumbnail_path=_C
			processing_time=datetime.datetime.now()-start_time;processing_time_str=str(processing_time).split('.')[0];description=f">╭✠━━━━━━━━━━━━━━━━━━━━✠╮\n>┠➣**Tiempo transcurrido**: {processing_time_str}\n>╰✠━━━━━━━━━━━━━━━━━━━━✠╯\n"
			try:
				start_upload_time=time.time();upload_msg=await app.send_message(chat_id=message.chat.id,text='📤 **Subiendo video comprimido** 📤',reply_to_message_id=message.id);active_messages.add(upload_msg.id);register_cancelable_task(user_id,_u,_C,original_message_id=original_message_id)
				if thumbnail_path and os.path.exists(thumbnail_path):await send_protected_video(chat_id=message.chat.id,video=compressed_video_path,caption=description,thumb=thumbnail_path,duration=duration,reply_to_message_id=message.id,progress=progress_callback,progress_args=(upload_msg,C,start_upload_time))
				else:await send_protected_video(chat_id=message.chat.id,video=compressed_video_path,caption=description,duration=duration,reply_to_message_id=message.id,progress=progress_callback,progress_args=(upload_msg,C,start_upload_time))
				try:await upload_msg.delete();logger.info('Mensaje de subida eliminado')
				except:pass
				logger.info('✅ Video comprimido enviado como respuesta al original');await notify_group(client,message,original_size,compressed_size=compressed_size,status='done');await increment_user_usage(message.from_user.id)
				try:await start_msg.delete();logger.info("Mensaje 'Iniciando compresión' eliminado")
				except Exception as e:logger.error(f"Error eliminando mensaje de inicio: {e}")
				try:await msg.delete();logger.info('Mensaje de progreso eliminado')
				except Exception as e:logger.error(f"Error eliminando mensaje de progreso: {e}")
			except Exception as e:logger.error(f"Error enviando video: {e}",exc_info=_A);await app.send_message(chat_id=message.chat.id,text='⚠️ **Error al enviar el video comprimido**')
		except Exception as e:logger.error(f"Error en compresión: {e}",exc_info=_A);await msg.delete();await app.send_message(chat_id=message.chat.id,text=f"Ocurrió un error al comprimir el video: {e}")
		finally:
			try:
				if msg.id in active_messages:active_messages.remove(msg.id)
				if'upload_msg'in locals()and upload_msg.id in active_messages:active_messages.remove(upload_msg.id)
				for file_path in[original_video_path,compressed_video_path]:
					if file_path and os.path.exists(file_path):os.remove(file_path);logger.info(f"Archivo temporal eliminado: {file_path}")
				if'thumbnail_path'in locals()and thumbnail_path and os.path.exists(thumbnail_path):os.remove(thumbnail_path);logger.info(f"Miniatura eliminada: {thumbnail_path}")
			except Exception as e:logger.error(f"Error eliminando archivos temporales: {e}",exc_info=_A)
	except Exception as e:logger.critical(f"Error crítico en compress_video: {e}",exc_info=_A);await app.send_message(chat_id=message.chat.id,text='⚠️ Ocurrió un error crítico al procesar el video')
	finally:await remove_active_compression(user_id);unregister_cancelable_task(user_id)
def get_main_menu_keyboard():return ReplyKeyboardMarkup([[KeyboardButton('⚙️ Settings'),KeyboardButton('📋 Planes')],[KeyboardButton('📊 Mi Plan'),KeyboardButton('ℹ️ Ayuda')],[KeyboardButton('👀 Ver Cola')]],resize_keyboard=_A,one_time_keyboard=_F)
@app.on_message(filters.command('settings')&filters.private)
async def settings_menu(client,message):keyboard=InlineKeyboardMarkup([[InlineKeyboardButton(_j,callback_data=_X)],[InlineKeyboardButton(_k,callback_data=_Y)],[InlineKeyboardButton(_l,callback_data=_Z)],[InlineKeyboardButton(_m,callback_data=_a)]]);await send_protected_message(message.chat.id,'⚙️𝗦𝗲𝗹𝗲𝗰𝗰𝗶𝗼𝗻𝗮𝗿 𝗖𝗮𝗹𝗶𝗱𝗮𝗱⚙️',reply_markup=keyboard)
def get_plan_menu_keyboard():return InlineKeyboardMarkup([[InlineKeyboardButton('🧩 Estándar',callback_data='plan_standard')],[InlineKeyboardButton('💎 Pro',callback_data='plan_pro')],[InlineKeyboardButton('👑 Premium',callback_data='plan_premium')]])
async def get_plan_menu(user_id):
	user=await get_user_plan(user_id)
	if user is _C or user.get(_D)is _C:return'>➣ **No tienes un plan activo.**\n\n>Por favor, adquiere un plan para usar el bot.\n\n>📋 **Selecciona un plan para más información:**',get_plan_menu_keyboard()
	plan_name=user[_D].capitalize();used=user.get(_E,0);limit=PLAN_LIMITS[user[_D]];remaining=max(0,limit-used);return f"""> ╭✠━━━━━━━━━━━━━━━━━━━━━━✠╮
> ┠➣ **Tu plan actual**: {plan_name}
> ┠➣ **Videos usados**: {used}/{limit}
> ┠➣ **Restantes**: {remaining}
> ╰✠━━━━━━━━━━━━━━━━━━━━━━✠╯

> 📋 **Selecciona un plan para más información:**""",get_plan_menu_keyboard()
@app.on_message(filters.command('planes')&filters.private)
async def planes_command(client,message):
	try:texto,keyboard=await get_plan_menu(message.from_user.id);await send_protected_message(message.chat.id,texto,reply_markup=keyboard)
	except Exception as e:logger.error(f"Error en planes_command: {e}",exc_info=_A);await send_protected_message(message.chat.id,'⚠️ Error al mostrar los planes')
@app.on_callback_query()
async def callback_handler(client,callback_query):
	C='back_to_settings';B='🔙 Volver';A='plan_back';config_map={_X:'resolution=854x480 crf=28 audio_bitrate=70k fps=22 preset=veryfast codec=libx264',_Y:'resolution=420x720 crf=25 audio_bitrate=70k fps=30 preset=veryfast codec=libx264',_Z:'resolution=854x480 crf=32 audio_bitrate=70k fps=20 preset=veryfast codec=libx264',_a:'resolution=854x480 crf=32 audio_bitrate=150k fps=18 preset=veryfast codec=libx264'};quality_names={_X:_j,_Y:_k,_Z:_l,_a:_m}
	if callback_query.data.startswith('cancel_task_'):
		user_id=int(callback_query.data.split('_')[2])
		if callback_query.from_user.id!=user_id:await callback_query.answer('⚠️ Solo el propietario puede cancelar esta tarea',show_alert=_A);return
		if cancel_user_task(user_id):
			original_message_id=cancel_tasks[user_id].get(_c);unregister_cancelable_task(user_id);msg_to_delete=callback_query.message
			if msg_to_delete.id in active_messages:active_messages.remove(msg_to_delete.id)
			try:await msg_to_delete.delete()
			except Exception as e:logger.error(f"Error eliminando mensaje de progreso: {e}")
			await callback_query.answer('⛔ Tarea cancelada! ⛔',show_alert=_A)
			try:await app.send_message(callback_query.message.chat.id,_e,reply_to_message_id=original_message_id)
			except:await app.send_message(callback_query.message.chat.id,_e)
		else:await callback_query.answer('⚠️ No se pudo cancelar la tarea',show_alert=_A)
		return
	if callback_query.data.startswith(('confirm_','cancel_')):
		action,confirmation_id_str=callback_query.data.split('_',1);confirmation_id=ObjectId(confirmation_id_str);confirmation=await get_confirmation(confirmation_id)
		if not confirmation:await callback_query.answer('⚠️ Esta solicitud ha expirado o ya fue procesada.',show_alert=_A);return
		user_id=callback_query.from_user.id
		if user_id!=confirmation[_B]:await callback_query.answer('⚠️ No tienes permiso para esta acción.',show_alert=_A);return
		if action=='confirm':
			if await check_user_limit(user_id):await callback_query.answer('⚠️ Has alcanzado tu límite mensual de compresiones.',show_alert=_A);await delete_confirmation(confirmation_id);return
			user_plan=await get_user_plan(user_id);pending_count=pending_col.count_documents({_B:user_id})
			if user_plan and user_plan[_D]==_K:
				if pending_count>=PREMIUM_QUEUE_LIMIT:await callback_query.answer(f"⚠️ Ya tienes {pending_count} videos en cola (límite: {PREMIUM_QUEUE_LIMIT}).\nEspera a que se procesen antes de enviar más.",show_alert=_A);await delete_confirmation(confirmation_id);return
			elif await has_active_compression(user_id)or pending_count>0:await callback_query.answer('⚠️ Ya hay un video en proceso de compresión o en cola.\nEspera a que termine antes de enviar otro video.',show_alert=_A);await delete_confirmation(confirmation_id);return
			try:message=await app.get_messages(confirmation[_R],confirmation[_S])
			except Exception as e:logger.error(f"Error obteniendo mensaje: {e}");await callback_query.answer('⚠️ Error al obtener el video. Intenta enviarlo de nuevo.',show_alert=_A);await delete_confirmation(confirmation_id);return
			await delete_confirmation(confirmation_id);queue_size=compression_queue.qsize();wait_msg=await callback_query.message.edit_text(f"⏳ Tu video ha sido añadido a la cola.\n\n📋 Tamaño actual de la cola: {queue_size}\n\n• **Espere que otros procesos terminen** ⏳");priority=await get_user_priority(user_id);timestamp=datetime.datetime.now();global processing_task
			if processing_task is _C or processing_task.done():processing_task=asyncio.create_task(process_compression_queue())
			pending_col.insert_one({_B:user_id,_z:message.video.file_id,_T:message.video.file_name,_R:message.chat.id,_S:message.id,_G:timestamp,_J:priority});await compression_queue.put((priority,timestamp,(app,message,wait_msg)));logger.info(f"Video confirmado y encolado de {user_id}: {message.video.file_name}")
		elif action==_v:
			await delete_confirmation(confirmation_id);await callback_query.answer('⛔ Compresión cancelada.⛔',show_alert=_A)
			try:await callback_query.message.edit_text('⛔ **Compresión cancelada.** ⛔');await asyncio.sleep(5);await callback_query.message.delete()
			except:pass
		return
	if callback_query.data==A:
		try:texto,keyboard=await get_plan_menu(callback_query.from_user.id);await callback_query.message.edit_text(texto,reply_markup=keyboard)
		except Exception as e:logger.error(f"Error en plan_back: {e}",exc_info=_A);await callback_query.answer('⚠️ Error al volver al menú de planes',show_alert=_A)
		return
	elif callback_query.data.startswith('plan_'):
		plan_type=callback_query.data.split('_')[1];user_id=callback_query.from_user.id;back_keyboard=InlineKeyboardMarkup([[InlineKeyboardButton(B,callback_data=A),InlineKeyboardButton('📝 Contratar Plan',url='https://t.me/InfiniteNetworkAdmin?text=Hola,+estoy+interesad@+en+un+plan+del+bot+de+comprimír+vídeos')]])
		if plan_type==_L:await callback_query.message.edit_text('> 🧩**Plan Estándar**🧩\n\n> ✅ **Beneficios:**\n> • **Hasta 60 videos comprimidos**\n\n> ❌ **Desventajas:**\n> • **Prioridad baja en la cola de procesamiento**\n>• **No podá reenviar del bot**\n>• **Solo podá comprimír 1 video a la ves**\n\n> • **Precio:** **180Cup**💵\n> **• Duración 7 dias**\n\n',reply_markup=back_keyboard)
		elif plan_type==_N:await callback_query.message.edit_text('>💎**Plan Pro**💎\n\n>✅ **Beneficios:**\n>• **Hasta 130 videos comprimidos**\n>• **Prioridad alta en la cola de procesamiento**\n>• **Podá reenviar del bot**\n\n>❌ **Desventajas**\n>• **Solo podá comprimír 1 video a la ves**\n\n>• **Precio:** **300Cup**💵\n>**• Duración 15 dias**\n\n',reply_markup=back_keyboard)
		elif plan_type==_K:await callback_query.message.edit_text(f""">👑**Plan Premium**👑

>✅ **Beneficios:**
>• **Hasta 280 videos comprimidos**
>• **Máxima prioridad en procesamiento**
>• **Soporte prioritario 24/7**
>• **Podá reenviar del bot**
>• **Múltiples videos en cola** (hasta {PREMIUM_QUEUE_LIMIT})

>• **Precio:** **500Cup**💵
>**• Duración 30 dias**

""",reply_markup=back_keyboard)
		return
	config=config_map.get(callback_query.data)
	if config:update_video_settings(config);back_keyboard=InlineKeyboardMarkup([[InlineKeyboardButton(B,callback_data=C)]]);quality_name=quality_names.get(callback_query.data,'Calidad Desconocida');await callback_query.message.edit_text(f">**{quality_name}\n>aplicada correctamente**✅",reply_markup=back_keyboard)
	elif callback_query.data==C:keyboard=InlineKeyboardMarkup([[InlineKeyboardButton(_j,callback_data=_X)],[InlineKeyboardButton(_k,callback_data=_Y)],[InlineKeyboardButton(_l,callback_data=_Z)],[InlineKeyboardButton(_m,callback_data=_a)]]);await callback_query.message.edit_text(' ⚙️𝗦𝗲𝗹𝗲𝗰𝗰𝗶𝗼𝗻𝗮𝗿 𝗖𝗮𝗹𝗶𝗱𝗮𝗱⚙️',reply_markup=keyboard)
	else:await callback_query.answer('Opción inválida.',show_alert=_A)
@app.on_message(filters.command(_W))
async def start_command(client,message):
	try:
		user_id=message.from_user.id
		if user_id in ban_users:logger.warning(f"Usuario baneado intentó usar /start: {user_id}");return
		user_plan=await get_user_plan(user_id)
		if user_plan is _C or user_plan.get(_D)is _C:await send_protected_message(message.chat.id,'>➣ **Usted no tiene acceso al bot.**\n\n>💲 Para ver los planes disponibles usa el comando /planes\n\n>👨🏻\u200d💻 Para más información, contacte a @InfiniteNetworkAdmin.');return
		image_path='logo.jpg';caption='> **🤖 Bot para comprimir videos**\n> ➣**Creado por** @InfiniteNetworkAdmin\n\n> **¡Bienvenido!** Puedo reducir el tamaño de los vídeos hasta un 80% o más y se verán bien sin perder tanta calidad\n>Usa los botones del menú para interactuar conmigo.Si tiene duda use el botón ℹ️ Ayuda\n\n> **⚙️ Versión 16.5.0 ⚙️**';await send_protected_photo(chat_id=message.chat.id,photo=image_path,caption=caption,reply_markup=get_main_menu_keyboard());logger.info(f"Comando /start ejecutado por {message.from_user.id}")
	except Exception as e:logger.error(f"Error en handle_start: {e}",exc_info=_A)
@app.on_message(filters.text&filters.private)
async def main_menu_handler(client,message):
	try:
		text=message.text.lower();user_id=message.from_user.id
		if user_id in ban_users:return
		if text=='⚙️ settings':await settings_menu(client,message)
		elif text=='📋 planes':await planes_command(client,message)
		elif text=='📊 mi plan':await my_plan_command(client,message)
		elif text=='ℹ️ ayuda':support_keyboard=InlineKeyboardMarkup([[InlineKeyboardButton('👨🏻\u200d💻 Soporte',url='https://t.me/InfiniteNetworkAdmin')]]);await send_protected_message(message.chat.id,'> 👨🏻\u200d💻 **Información**\n\n> • Configurar calidad: Usa el botón ⚙️ Settings\n> • Para comprimir un video: Envíalo directamente al bot\n> • Ver planes: Usa el botón 📋 Planes\n> • Ver tu estado: Usa el botón 📊 Mi Plan\n> • Usa /start para iniciar en el bot nuevamente\n> • Ver cola de compresión: Usa el botón 👀 Ver Cola\n\n',reply_markup=support_keyboard)
		elif text=='👀 ver cola':await queue_command(client,message)
		elif text=='/cancel':await cancel_command(client,message)
		else:await handle_message(client,message)
	except Exception as e:logger.error(f"Error en main_menu_handler: {e}",exc_info=_A)
@app.on_message(filters.command('desuser')&filters.user(admin_users))
async def unban_user_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=2:await message.reply('Formato: /desuser <user_id>');return
		user_id=int(parts[1])
		if user_id in ban_users:ban_users.remove(user_id)
		result=banned_col.delete_one({_B:user_id})
		if result.deleted_count>0:
			await message.reply(f">➣ Usuario {user_id} desbaneado exitosamente.")
			try:await app.send_message(user_id,'>✅ **Tu acceso al bot ha sido restaurado.**\n\n>Ahora puedes volver a usar el bot.')
			except Exception as e:logger.error(f"No se pudo notificar al usuario {user_id}: {e}")
		else:await message.reply(f">➣ El usuario {user_id} no estaba baneado.")
		logger.info(f"Usuario desbaneado: {user_id} por admin {message.from_user.id}")
	except Exception as e:logger.error(f"Error en unban_user_command: {e}",exc_info=_A);await message.reply('⚠️ Error al desbanear usuario. Formato: /desuser [user_id]')
@app.on_message(filters.command('deleteuser')&filters.user(admin_users))
async def delete_user_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=2:await message.reply('Formato: /deleteuser <user_id>');return
		user_id=int(parts[1]);result=users_col.delete_one({_B:user_id})
		if user_id not in ban_users:ban_users.append(user_id)
		banned_col.insert_one({_B:user_id,_n:datetime.datetime.now()});pending_result=pending_col.delete_many({_B:user_id});await message.reply(f">➣ Usuario {user_id} eliminado y baneado exitosamente.\n>🗑️ Tareas pendientes eliminadas: {pending_result.deleted_count}");logger.info(f"Usuario eliminado y baneado: {user_id} por admin {message.from_user.id}")
		try:await app.send_message(user_id,'>🔒 **Tu acceso al bot ha sido revocado.**\n\n>No podrás usar el bot hasta nuevo aviso.')
		except Exception as e:logger.error(f"No se pudo notificar al usuario {user_id}: {e}")
	except Exception as e:logger.error(f"Error en delete_user_command: {e}",exc_info=_A);await message.reply('⚠️ Error al eliminar usuario. Formato: /deleteuser [user_id]')
@app.on_message(filters.command('viewban')&filters.user(admin_users))
async def view_banned_users_command(client,message):
	try:
		banned_users=list(banned_col.find({}))
		if not banned_users:await message.reply('>📭 **No hay usuarios baneados.**');return
		response='>🔒 **Usuarios Baneados**\n\n'
		for(i,banned_user)in enumerate(banned_users,1):
			user_id=banned_user[_B];banned_at=banned_user.get(_n,'Fecha desconocida')
			try:user=await app.get_users(user_id);username=f"@{user.username}"if user.username else _P
			except:username=_P
			if isinstance(banned_at,datetime.datetime):banned_at_str=banned_at.strftime(_o)
			else:banned_at_str=str(banned_at)
			response+=f"{i}. 👤 {username}\n   🆔 ID: `{user_id}`\n   ⏰ Fecha: {banned_at_str}\n\n"
		await message.reply(response)
	except Exception as e:logger.error(f"Error en view_banned_users_command: {e}",exc_info=_A);await message.reply('⚠️ Error al obtener la lista de usuarios baneados')
@app.on_message(filters.command(['banuser','deluser'])&filters.user(admin_users))
async def ban_or_delete_user_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=2:await message.reply('Formato: /comando <user_id>');return
		ban_user_id=int(parts[1])
		if ban_user_id in admin_users:await message.reply('>➣ No puedes banear a un administrador.');return
		result=users_col.delete_one({_B:ban_user_id})
		if ban_user_id not in ban_users:ban_users.append(ban_user_id)
		banned_col.insert_one({_B:ban_user_id,_n:datetime.datetime.now()});await message.reply(f">➣ Usuario {ban_user_id} baneado y eliminado de la base de datos."if result.deleted_count>0 else f">➣ Usuario {ban_user_id} baneado (no estaba en la base de datos).")
	except Exception as e:logger.error(f"Error en ban_or_delete_user_command: {e}",exc_info=_A);await message.reply(_p)
@app.on_message(filters.command(_M)&filters.private)
async def key_command(client,message):
	try:
		user_id=message.from_user.id
		if user_id in ban_users:await send_protected_message(message.chat.id,'🚫 Tu acceso ha sido revocado.');return
		logger.info(f"Comando key recibido de {user_id}")
		if not message.text or len(message.text.split())<2:await send_protected_message(message.chat.id,'❌ Formato: /key <clave>');return
		key=message.text.split()[1].strip();now=datetime.datetime.now();key_data=temp_keys_col.find_one({_M:key,_E:_F})
		if not key_data:await send_protected_message(message.chat.id,'❌ **Clave inválida o ya ha sido utilizada.**');return
		if key_data[_I]<now:await send_protected_message(message.chat.id,'❌ **La clave ha expirado.**');return
		temp_keys_col.update_one({_H:key_data[_H]},{_O:{_E:_A}});new_plan=key_data[_D];duration_value=key_data[_h];duration_unit=key_data[_i]
		if duration_unit==_f:expires_at=datetime.datetime.now()+datetime.timedelta(minutes=duration_value)
		elif duration_unit==_g:expires_at=datetime.datetime.now()+datetime.timedelta(hours=duration_value)
		else:expires_at=datetime.datetime.now()+datetime.timedelta(days=duration_value)
		success=await set_user_plan(user_id,new_plan,notify=_F,expires_at=expires_at)
		if success:
			duration_text=f"{duration_value} {duration_unit}"
			if duration_value==1:duration_text=duration_text[:-1]
			await send_protected_message(message.chat.id,f">✅ **Plan {new_plan.capitalize()} activado!**\n>**Válido por {duration_text}**\n\n>**Ahora tienes {PLAN_LIMITS[new_plan]} videos disponibles**\n>Use el comando /start para iniciar en el bot");logger.info(f"Plan actualizado a {new_plan} para {user_id} con clave {key}")
		else:await send_protected_message(message.chat.id,'❌ **Error al activar el plan. Contacta con el administrador.**')
	except Exception as e:logger.error(f"Error en key_command: {e}",exc_info=_A);await send_protected_message(message.chat.id,'❌ **Error al procesar la solicitud de acceso**')
sent_messages={}
def is_bot_public():return BOT_IS_PUBLIC and BOT_IS_PUBLIC.lower()=='true'
@app.on_message(filters.command('myplan')&filters.private)
async def my_plan_command(client,message):
	try:plan_info=await get_plan_info(message.from_user.id);await send_protected_message(message.chat.id,plan_info,reply_markup=get_main_menu_keyboard())
	except Exception as e:logger.error(f"Error en my_plan_command: {e}",exc_info=_A);await send_protected_message(message.chat.id,'⚠️ **Error al obtener información de tu plan**',reply_markup=get_main_menu_keyboard())
@app.on_message(filters.command('setplan')&filters.user(admin_users))
async def set_plan_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=3:await message.reply('Formato: /setplan <user_id> <plan>');return
		user_id=int(parts[1]);plan=parts[2].lower()
		if plan not in PLAN_LIMITS:await message.reply(f"⚠️ Plan inválido. Opciones válidas: {', '.join(PLAN_LIMITS.keys())}");return
		if await set_user_plan(user_id,plan,expires_at=_C):await message.reply(f">➣ **Plan del usuario {user_id} actualizado a {plan}.**")
		else:await message.reply('⚠️ **Error al actualizar el plan.**')
	except Exception as e:logger.error(f"Error en set_plan_command: {e}",exc_info=_A);await message.reply('⚠️ **Error en el comando**')
@app.on_message(filters.command('resetuser')&filters.user(admin_users))
async def reset_user_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=2:await message.reply('Formato: /resetuser <user_id>');return
		user_id=int(parts[1]);await reset_user_usage(user_id);await message.reply(f">➣ **Contador de videos del usuario {user_id} reiniciado a 0.**")
	except Exception as e:logger.error(f"Error en reset_user_command: {e}",exc_info=_A);await message.reply(_p)
@app.on_message(filters.command('userinfo')&filters.user(admin_users))
async def user_info_command(client,message):
	try:
		parts=message.text.split()
		if len(parts)!=2:await message.reply('Formato: /userinfo <user_id>');return
		user_id=int(parts[1]);user=await get_user_plan(user_id)
		if user:
			plan=user[_D].capitalize()if user.get(_D)else'Ninguno';used=user.get(_E,0);limit=PLAN_LIMITS[user[_D]]if user.get(_D)else 0;join_date=user.get(_x,'Desconocido');expires_at=user.get(_I,_y)
			if isinstance(join_date,datetime.datetime):join_date=join_date.strftime(_o)
			if isinstance(expires_at,datetime.datetime):expires_at=expires_at.strftime(_o)
			await message.reply(f">👤 **ID**: `{user_id}`\n>📝 **Plan**: {plan}\n>🔢 **Videos comprimidos**: {used}/{limit}\n>📅 **Fecha de registro**: {join_date}\n")
		else:await message.reply('⚠️ Usuario no registrado o sin plan')
	except Exception as e:logger.error(f"Error en user_info_command: {e}",exc_info=_A);await message.reply(_p)
@app.on_message(filters.command('restuser')&filters.user(admin_users))
async def reset_all_users_command(client,message):
	try:result=users_col.delete_many({});await message.reply(f">➣ **Todos los usuarios han sido eliminados**\n>➣ Usuarios eliminados: {result.deleted_count}\n>➣ Contadores de vídeos restablecidos a 0");logger.info(f"Todos los usuarios eliminados por admin {message.from_user.id}")
	except Exception as e:logger.error(f"Error en reset_all_users_command: {e}",exc_info=_A);await message.reply('⚠️ Error al eliminar usuarios')
@app.on_message(filters.command('user')&filters.user(admin_users))
async def list_users_command(client,message):
	try:
		all_users=list(users_col.find({}))
		if not all_users:await message.reply('>📭 **No hay usuarios registrados.**');return
		response='>👥 **Lista de Usuarios Registrados**\n\n'
		for(i,user)in enumerate(all_users,1):
			user_id=user[_B];plan=user[_D].capitalize()if user.get(_D)else'Ninguno'
			try:user_info=await app.get_users(user_id);username=f"@{user_info.username}"if user_info.username else _P
			except:username=_P
			response+=f"{i}. {username}\n   👤 ID: `{user_id}`\n   📝 Plan: {plan}\n\n"
		await message.reply(response)
	except Exception as e:logger.error(f"Error en list_users_command: {e}",exc_info=_A);await message.reply('⚠️ **Error al listar usuarios**')
@app.on_message(filters.command('admin')&filters.user(admin_users))
async def admin_stats_command(client,message):
	F='total';E='$used';D='total_used';C='count';B='$group';A='$sum'
	try:
		pipeline=[{'$match':{_D:{'$exists':_A,'$ne':_C}}},{B:{_H:'$plan',C:{A:1},D:{A:E}}}];stats=list(users_col.aggregate(pipeline));total_users=users_col.count_documents({});total_compressions=users_col.aggregate([{B:{_H:_C,F:{A:E}}}]);total_compressions=next(total_compressions,{}).get(F,0);response='>📊 **Estadísticas de Administrador**\n\n';response+=f">👥 **Total de usuarios:** {total_users}\n";response+=f">🔢 **Total de compresiones:** {total_compressions}\n\n";response+='>📝 **Distribución por Planes:**\n';plan_names={_L:'>🧩 Estándar',_N:'>💎 Pro',_K:'>👑 Premium'}
		for stat in stats:plan_type=stat[_H];count=stat[C];used=stat[D];plan_name=plan_names.get(plan_type,plan_type.capitalize()if plan_type else'❓ Desconocido');response+=f"\n{plan_name}:\n>  👥 Usuarios: {count}\n>  🔢 Comprs: {used}\n"
		await message.reply(response)
	except Exception as e:logger.error(f"Error en admin_stats_command: {e}",exc_info=_A);await message.reply('⚠️ **Error al generar estadísticas**')
async def broadcast_message(admin_id,message_text):
	try:
		user_ids=set()
		for user in users_col.find({},{_B:1}):user_ids.add(user[_B])
		user_ids=[uid for uid in user_ids if uid not in ban_users];total_users=len(user_ids)
		if total_users==0:await app.send_message(admin_id,'📭 No hay usuarios para enviar el mensaje.');return
		await app.send_message(admin_id,f"📤 **Iniciando difusión a {total_users} usuarios...**\n⏱ Esto puede tomar varios minutos.");success=0;failed=0;count=0
		for user_id in user_ids:
			count+=1
			try:await send_protected_message(user_id,f">🔔**Notificación:**\n\n{message_text}");success+=1;await asyncio.sleep(.5)
			except Exception as e:logger.error(f"Error enviando mensaje a {user_id}: {e}");failed+=1
		await app.send_message(admin_id,f"✅ **Difusión completada!**\n\n👥 Total de usuarios: {total_users}\n✅ Enviados correctamente: {success}\n❌ Fallidos: {failed}")
	except Exception as e:logger.error(f"Error en broadcast_message: {e}",exc_info=_A);await app.send_message(admin_id,f"⚠️ Error en difusión: {str(e)}")
@app.on_message(filters.command('msg')&filters.user(admin_users))
async def broadcast_command(client,message):
	try:
		if not message.text or len(message.text.split())<2:await message.reply('⚠️ Formato: /msg <mensaje>');return
		parts=message.text.split(maxsplit=1);broadcast_text=parts[1]if len(parts)>1 else''
		if not broadcast_text.strip():await message.reply('⚠️ El mensaje no puede estar vacío');return
		admin_id=message.from_user.id;asyncio.create_task(broadcast_message(admin_id,broadcast_text));await message.reply('📤 **Difusión iniciada!**\n⏱ Los mensajes se enviarán progresivamente a todos los usuarios.\nRecibirás un reporte final cuando se complete.')
	except Exception as e:logger.error(f"Error en broadcast_command: {e}",exc_info=_A);await message.reply('⚠️ Error al iniciar la difusión')
async def queue_command(client,message):
	'Muestra información sobre la cola de compresión';user_id=message.from_user.id;user_plan=await get_user_plan(user_id)
	if user_plan is _C or user_plan.get(_D)is _C:await send_protected_message(message.chat.id,'>➣ **Usted no tiene acceso para usar este bot.**\n\n>Por favor, adquiera un plan para poder ver la cola de compresión.');return
	if user_id in admin_users:await show_queue(client,message);return
	total=pending_col.count_documents({});user_pending=list(pending_col.find({_B:user_id}));user_count=len(user_pending)
	if total==0:response='>➣**La cola de compresión está vacía.**'
	else:
		cola=list(pending_col.find().sort([(_J,1),(_G,1)]));user_position=_C
		for(idx,item)in enumerate(cola,1):
			if item[_B]==user_id:user_position=idx;break
		if user_count==0:response=f""">📋 **Estado de la cola**

>• Total de videos en cola: {total}
>• Tus videos en cola: 0

>No tienes videos pendientes de compresión."""
		else:response=f""">📋 **Estado de la cola**

>• Total de videos en cola: {total}
>• Tus videos en cola: {user_count}
>• Posición de tu primer video: {user_position}

>⏱ Por favor ten paciencia mientras se procesa tu video."""
	await send_protected_message(message.chat.id,response)
@app.on_message(filters.video)
async def handle_video(client,message):
	try:
		user_id=message.from_user.id
		if user_id in ban_users:logger.warning(f"Intento de uso por usuario baneado: {user_id}");return
		user_plan=await get_user_plan(user_id)
		if user_plan is _C or user_plan.get(_D)is _C:await send_protected_message(message.chat.id,'>➣ **Usted no tiene acceso para usar este bot.**\n\n>👨🏻\u200d💻**Contacta con @InfiniteNetworkAdmin para actualizar tu Plan**');return
		if await has_pending_confirmation(user_id):logger.info(f"Usuario {user_id} tiene confirmación pendiente, ignorando video adicional");return
		if await check_user_limit(user_id):await send_protected_message(message.chat.id,f">⚠️ **Límite alcanzado**\n>Has usado {user_plan[_E]}/{PLAN_LIMITS[user_plan[_D]]} videos.\n\n>👨🏻‍💻**Contacta con @InfiniteNetworkAdmin para actualizar tu Plan**");return
		has_active=await has_active_compression(user_id);pending_count=pending_col.count_documents({_B:user_id})
		if user_plan[_D]==_K:
			if pending_count>=PREMIUM_QUEUE_LIMIT:await send_protected_message(message.chat.id,f">➣ Ya tienes {pending_count} videos en cola (límite: {PREMIUM_QUEUE_LIMIT}).\n>Por favor espera a que se procesen antes de enviar más.");return
		elif has_active or pending_count>0:await send_protected_message(message.chat.id,'>➣ Ya tienes un video en proceso de compresión o en cola.\n>Por favor espera a que termine antes de enviar otro video.');return
		confirmation_id=await create_confirmation(user_id,message.chat.id,message.id,message.video.file_id,message.video.file_name);keyboard=InlineKeyboardMarkup([[InlineKeyboardButton('🟢 Confirmar compresión 🟢',callback_data=f"confirm_{confirmation_id}")],[InlineKeyboardButton(_U,callback_data=f"cancel_{confirmation_id}")]]);await send_protected_message(message.chat.id,f">🎬 **Video recibido para comprimír:** `{message.video.file_name}`\n\n>¿Deseas comprimir este video?",reply_to_message_id=message.id,reply_markup=keyboard);logger.info(f"Solicitud de confirmación creada para {user_id}: {message.video.file_name}")
	except Exception as e:logger.error(f"Error en handle_video: {e}",exc_info=_A)
@app.on_message(filters.text)
async def handle_message(client,message):
	try:
		text=message.text;username=message.from_user.username;chat_id=message.chat.id;user_id=message.from_user.id
		if user_id in ban_users:return
		logger.info(f"Mensaje recibido de {user_id}: {text}")
		if text.startswith(('/calidad','.calidad')):update_video_settings(text[len('/calidad '):]);await message.reply(f">⚙️ Configuración Actualizada✅: {video_settings}")
		elif text.startswith(('/settings','.settings')):await settings_menu(client,message)
		elif text.startswith(('/banuser','.banuser','/deluser','.deluser')):
			if user_id in admin_users:await ban_or_delete_user_command(client,message)
			else:logger.warning(f"Intento no autorizado de banuser/deluser por {user_id}")
		elif text.startswith(('/cola','.cola')):
			if user_id in admin_users:await ver_cola_command(client,message)
		elif text.startswith(('/auto','.auto')):
			if user_id in admin_users:await startup_command(client,message)
		elif text.startswith(('/myplan','.myplan')):await my_plan_command(client,message)
		elif text.startswith(('/setplan','.setplan')):
			if user_id in admin_users:await set_plan_command(client,message)
		elif text.startswith(('/resetuser','.resetuser')):
			if user_id in admin_users:await reset_user_command(client,message)
		elif text.startswith(('/userinfo','.userinfo')):
			if user_id in admin_users:await user_info_command(client,message)
		elif text.startswith(('/planes','.planes')):await planes_command(client,message)
		elif text.startswith(('/generatekey','.generatekey')):
			if user_id in admin_users:await generate_key_command(client,message)
		elif text.startswith(('/listkeys','.listkeys')):
			if user_id in admin_users:await list_keys_command(client,message)
		elif text.startswith(('/delkeys','.delkeys')):
			if user_id in admin_users:await del_keys_command(client,message)
		elif text.startswith(('/user','.user')):
			if user_id in admin_users:await list_users_command(client,message)
		elif text.startswith(('/admin','.admin')):
			if user_id in admin_users:await admin_stats_command(client,message)
		elif text.startswith(('/restuser','.restuser')):
			if user_id in admin_users:await reset_all_users_command(client,message)
		elif text.startswith(('/desuser','.desuser')):
			if user_id in admin_users:await unban_user_command(client,message)
		elif text.startswith(('/deleteuser','.deleteuser')):
			if user_id in admin_users:await delete_user_command(client,message)
		elif text.startswith(('/viewban','.viewban')):
			if user_id in admin_users:await view_banned_users_command(client,message)
		elif text.startswith(('/msg','.msg')):
			if user_id in admin_users:await broadcast_command(client,message)
		elif text.startswith(('/cancel','.cancel')):await cancel_command(client,message)
		elif text.startswith(('/key','.key')):await key_command(client,message)
		if message.reply_to_message:
			original_message=sent_messages.get(message.reply_to_message.id)
			if original_message:user_id=original_message[_B];sender_info=f"Respuesta de @{message.from_user.username}"if message.from_user.username else f"Respuesta de user ID: {message.from_user.id}";await send_protected_message(user_id,f"{sender_info}: {message.text}");logger.info(f"Respuesta enviada a {user_id}")
	except Exception as e:logger.error(f"Error en handle_message: {e}",exc_info=_A)
async def notify_group(client,message,original_size,compressed_size=_C,status=_W):
	try:
		group_id=-4826894501;user=message.from_user;username=f"@{user.username}"if user.username else _P;file_name=message.video.file_name or'Sin nombre';size_mb=original_size//(1024*1024)
		if status==_W:text=f""">📤 **Nuevo video recibido para comprimir**

>👤 **Usuario:** {username}
>🆔 **ID:** `{user.id}`
>📦 **Tamaño original:** {size_mb} MB
>📁 **Nombre:** `{file_name}`"""
		elif status=='done':compressed_mb=compressed_size//(1024*1024);text=f""">📥 **Video comprimido y enviado**

>👤 **Usuario:** {username}
>🆔 **ID:** `{user.id}`
>📦 **Tamaño original:** {size_mb} MB
>📉 **Tamaño comprimido:** {compressed_mb} MB
>📁 **Nombre:** `{file_name}`"""
		await app.send_message(chat_id=group_id,text=text);logger.info(f"Notificación enviada al grupo: {user.id} - {file_name} ({status})")
	except Exception as e:logger.error(f"Error enviando notificación al grupo: {e}")
try:logger.info('Iniciando el bot...');app.run()
except Exception as e:logger.critical(f"Error fatal al iniciar el bot: {e}",exc_info=_A)