import asyncio
import os
from chat_deepseek_api import DeepseekAPI
from dotenv import load_dotenv

from chat_deepseek_api.model import MessageData

load_dotenv()


async def main():
    email = os.environ.get("DEEPSEEK_EMAIL")
    password = os.environ.get("DEEPSEEK_PASSWORD")
    device_id = os.environ.get("DEEPSEEK_DEVICE_ID")
    cookies = os.environ.get("DEEPSEEK_COOKIES")
    ds_pow_response = os.environ.get("DEEPSEEK_DS_POW_RESPONSE")

    app = await DeepseekAPI.create(
        email=email,
        password=password,
        save_login=True,
        device_id=device_id,
        custom_headers={
            "cookie": cookies,
            "x-ds-pow-response": ds_pow_response,
        },
    )
    chat_session_id = await app.new_chat()

    print(f"Starting chat session with id: {chat_session_id}")

    message_id = None
    async for chunk in app.chat(
        message="who are you", id=chat_session_id, parent_message_id=message_id
    ):
        chunk_data: MessageData = chunk
        print(chunk_data.choices[0].delta.content, end="")

        cur_message_id = chunk.get_message_id()
        if not cur_message_id:
            cur_message_id = 0
        if not message_id or cur_message_id > message_id:
            message_id = cur_message_id

    print()
    
    async for chunk in app.chat(
        message="what can you do", id=chat_session_id, parent_message_id=message_id
    ):
        chunk_data: MessageData = chunk
        print(chunk_data.choices[0].delta.content, end="")

        cur_message_id = chunk.get_message_id()
        if cur_message_id > message_id:
            message_id = cur_message_id

    print()
    await app.close()


if __name__ == "__main__":
    asyncio.run(main())
