import asyncio

from bot import KnowledgeBot
from bot.settings import settings


async def main() -> None:
    bot = KnowledgeBot(settings=settings)
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
