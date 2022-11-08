import json
import typing
from vkwave.bots import SimpleBotEvent
from vkwave.bots.core.dispatching.filters import base


class PayloadHasKeys(base.BaseFilter):
    """
    Проверяет наличия ключей в полезной нагрузке
    """
    keys: typing.List[str]

    def __init__(self, keys: typing.List[str]):
        self.keys = keys

    async def check(self, event: SimpleBotEvent) -> base.FilterResult:
        if event.object.type == "message_event":
            payload_raw = event.object.object.payload
        elif event.object.type == "message_new":
            payload_raw = event.object.object.message.payload
        if payload_raw is not None:
            payload = json.loads(payload_raw) if type(payload_raw) == str else payload_raw
            such = True
            for key in self.keys:
                if key not in payload.keys():
                    such = False
            return base.FilterResult(such)
        else:
            return base.FilterResult(False)