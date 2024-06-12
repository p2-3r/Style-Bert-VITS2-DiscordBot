from typing import Any
from pathlib import Path
import json

import aiofiles


# 同期、非同期それぞれのJson読み書き用クラス
class JsonFile:
    def __init__(self, path: Path) -> None:
        self.path = path

    def read(self) -> Any:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data: Any) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    async def async_read(self) -> Any:
        async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
            data = await f.read()
            return json.loads(data)

    async def async_write(self, data: Any) -> None:
        async with aiofiles.open(self.path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, indent=4, ensure_ascii=False))
