from modules.ChatBox import ChatBox
import asyncio
from  langdetect import detect
async def main():
    # chatBox = await ChatBox.start()
    # chatBox.askQuestion("cuanto cuesta una constancia?")
    print(detect("precio 20mxn"))

if __name__ == "__main__":
    asyncio.run(main())