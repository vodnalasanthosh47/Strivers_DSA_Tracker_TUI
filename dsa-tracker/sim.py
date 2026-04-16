from screens.main_screen import MainScreen
from app import DSATrackerApp

import asyncio

async def run_sim():
    app = DSATrackerApp()
    async with app.run_test() as pilot:
        for _ in range(50):
            await pilot.press("down")
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    asyncio.run(run_sim())
