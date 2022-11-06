import asyncio
import json
import logging
import os
import typing
import aiohttp
import traceback
import __main__

import susubotlib
from susubotlib.config import Config


class APIError(Exception):
    pass


class SusuBotAPI:
    url = ''
    client: aiohttp.ClientSession
    token: str
    bot_name: str
    config: Config
    cache: bool
    use_cache: bool
    base_dir: str

    def __init__(self, url: str, token: str, bot_name: str):
        self.url = url.rstrip('/')
        self.token = token
        session_timeout = aiohttp.ClientTimeout(total=None, sock_connect=5, sock_read=5)
        self.client = aiohttp.ClientSession(timeout=session_timeout)
        self.bot_name = bot_name
        self.config = Config("susubotlib.ini")
        self.cache = self.config.config.getboolean("API", "CACHE")
        self.use_cache = self.config.config.getboolean("API", "USE_CACHE")
        self.keyboards_dir = self.config.config['API']['KEYBOARDS_DIR']
        self.messages_dir = self.config.config['API']['MESSAGES_DIR']
        self.base_dir = susubotlib.base_dir

    async def _get(self, method: str, **kwargs) -> dict:
        async with self.client.get(f"{self.url}/api/{method}", params=kwargs) as resp:
            r_data = await resp.json()

        if 'ok' not in r_data.keys() or 'data' not in r_data.keys():
            raise APIError(f"Server returned bad data")
        if r_data['ok']:
            return r_data
        else:
            raise APIError(f"Server returned: {r_data['reason'] if 'reason' in r_data.keys() else 'No reason'}")

    async def _save_keyboard(self, keyboard_name: str, data: str):
        with open(os.path.join(self.base_dir, self.keyboards_dir, f"{keyboard_name}.json"), 'w') as file:
            file.write(data)
            file.close()

    async def _get_keyboard_file(self, keyboard_name):
        with open(os.path.join(self.base_dir, self.keyboards_dir, f"{keyboard_name}.json"), 'r') as file:
            data = file.read()
            file.close()
        return data

    async def _save_message(self, message_name: str, data: str):
        with open(os.path.join(self.base_dir, self.messages_dir, f"{message_name}.txt"), 'w') as file:
            file.write(data)
            file.close()

    async def _get_message_file(self, message_name):
        with open(os.path.join(self.base_dir, self.messages_dir, f"{message_name}.txt"), 'r') as file:
            data = file.read()
            file.close()
        return data

    async def _post(self, method: str, data, **kwargs):
        async with self.client.post(f"{self.url}/api/{method}", params=kwargs, data=json.dumps(data),
                                    headers={'content-type': 'application/json'}) as resp:
            r_data = await resp.json()
        if 'ok' not in r_data.keys() or 'data' not in r_data.keys():
            raise APIError(f"Server returned bad data")
        if data['ok']:
            return r_data
        else:
            raise APIError(f"Server returned: {r_data['reason'] if 'reason' in data.keys() else 'No reason'}")

    async def getKeyboard(self, keyboard) -> str:
        """
        Return json string keyboard by keyboard name
        :param keyboard: Keyboard name
        :return: str
        """
        try:
            data = await self._get("getkeyboard", token=self.token, bot_name=self.bot_name, keyboard_name=keyboard)
            json_keyboard = json.dumps(data['data'])
            if self.cache:
                asyncio.get_running_loop().create_task(self._save_keyboard(keyboard, json_keyboard))
        except:
            if self.use_cache:
                json_keyboard = await self._get_keyboard_file(keyboard)
            else:
                raise
        return json_keyboard

    async def getMessage(self, message_name) -> str:
        """
        Return string message by message name
        :param message_name: Message name
        :return: str
        """
        try:
            data = await self._get("getmessage", token=self.token, bot_name=self.bot_name, message_name=message_name)
            message = json.dumps(data['data'])
            if self.cache:
                asyncio.get_running_loop().create_task(self._save_message(message_name, json_keyboard))
        except:
            if self.use_cache:
                message = await self._get_message_file(message_name)
            else:
                raise
        return message
