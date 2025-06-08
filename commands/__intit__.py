# commands/__init__.py

from .covid import setup as setup_covid
from .lotto import setup as setup_lotto
from .check_lotto import setup as setup_check_lotto
from .help import setup as setup_help
from .ping import setup as setup_ping

async def setup(bot):
    await setup_covid(bot)
    await setup_lotto(bot)
    await setup_check_lotto(bot)
    await setup_help(bot)
    await setup_ping(bot)