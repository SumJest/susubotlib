import random
import json
from vkwave.bots import SimpleLongPollBot, SimpleBotEvent, EventTypeFilter
from vkwave.bots.addons.easy.easy_handlers import SimpleBotCallback
from vkwave.types.bot_events import BotEventType
from susubotlib.api import SusuBotAPI
from susubotlib.filters import PayloadHasKeys


def get_random_id():
    return random.getrandbits(32)


class SusuBotEventHandler:
    api: SusuBotAPI
    bot: SimpleLongPollBot

    def __init__(self, api: SusuBotAPI, bot: SimpleLongPollBot):
        self.api = api
        self.bot = bot

    async def pressButtonEvent(self, event: SimpleBotEvent):

        if event.object.type == "message_event":
            payload_raw = event.object.object.payload
            is_callback = True
        elif event.object.type == "message_new":
            payload_raw = event.object.object.message.payload
            is_callback = False
        else:
            return
        payload = json.loads(payload_raw) if type(payload_raw) == str else payload_raw
        btn_type = payload['btn_type']

        if btn_type == 'msg' and 'msg_id' in payload.keys():
            msg_id = payload['msg_id']
            msg = await self.api.getMessage(msg_id)
            await event.api_ctx.messages.send(message=msg, peer_id=event.peer_id, random_id=get_random_id())
            if is_callback:
                await event.callback_answer(json.dumps({
                    "type": "show_snackbar",
                    "text": "Отправил"
                }))
        elif btn_type == 'kb' and 'kb_id' in payload.keys():
            kb_id = payload['kb_id']
            kb = await self.api.getKeyboard(kb_id)
            await event.api_ctx.messages.send(message="Ok", peer_id=event.peer_id, random_id=get_random_id(),
                                              keyboard=kb)
            if is_callback:
                await event.callback_answer(json.dumps({
                    "type": "show_snackbar",
                    "text": "Отправил"
                }))

    def register(self):
        record = self.bot.router.registrar.new()
        record.with_filters(PayloadHasKeys(["btn_type"]))
        record.filters.append(EventTypeFilter((BotEventType.MESSAGE_NEW, BotEventType.MESSAGE_EVENT)))
        record.handle(SimpleBotCallback(self.pressButtonEvent, self.bot.bot_type, SimpleBotEvent))
        self.bot.router.registrar.register(record.ready())
