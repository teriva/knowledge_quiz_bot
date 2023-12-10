import asyncio

from django.core.management import BaseCommand

from bot.settings import settings
from bot.bot import KnowledgeBot


async def main() -> None:
    bot = KnowledgeBot(settings=settings)
    await bot.run()


class Command(BaseCommand):
    help = "Runs bot."

    def handle(self, *args, **options):
        asyncio.run(main())

