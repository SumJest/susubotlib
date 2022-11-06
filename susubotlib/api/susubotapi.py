import json
import logging
import typing
import aiohttp
import traceback


class APIError(Exception):
    pass


class SusuBotAPI:
    url = ''
    client: aiohttp.ClientSession
    token: str
    bot_name: str

    def __init__(self, url: str, token: str, bot_name: str):
        self.url = url.rstrip('/')
        self.token = token
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=5, sock_read=5)
        self.client = aiohttp.ClientSession(timeout=session_timeout)
        self.bot_name = bot_name

    async def _get(self, method: str, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/api/{method}", params=kwargs) as resp:
            r_data = await resp.json()
        return r_data

    async def _post(self, method: str, data, **kwargs):
        async with self.client.post(f"{self.url}/api/{method}", params=kwargs, data=json.dumps(data),
                                    headers={'content-type': 'application/json'}) as resp:
            r_data = await resp.text()
        return r_data

    async def getKeyboard(self, keyboard) -> str:
        """
        Return json string keyboard by keyboard name
        :param keyboard: Keyboard name
        :return: str
        """
        data = await self._get("getkeyboard", token=self.token, bot_name=self.bot_name, keyboard_name=keyboard)
        if 'ok' in data.keys() and data['ok']:
            return json.dumps(data['data'])
        else:
            raise APIError(f"Server returned: {data['reason']}")
