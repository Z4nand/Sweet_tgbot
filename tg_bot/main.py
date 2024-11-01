import asyncio
from modules import bot
from modules import dp

from modules import create_table


# Запуск процесса поллинга новых апдейтов
async def main():
   
    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())