# Deepseek coder Reverse Engineered API Wrapper

Unofficial API Wrapper for Deepseek (chat.deepseek.com) in Python. This is a reverse-engineered API for the Deepseek coder and Deepseek code chatbots. This API is not affiliated with Deepseek in any way.

This repository is inpired by [deepseek-api](https://github.com/rabilrbl/deepseek-api). The original repository is not maintained anymore, so I decided to create a new one.

## Installation

```bash
pip install git+https://github.com/thinhdanggroup/chat-deepseek-api
```

## Usage

### Asynchronous CLI Example

Copy file `.env.example` to `.env` and fill in your Deepseek email, password, device id, cookies, and ds_pow_response.

```bash
DEEPSEEK_EMAIL=
DEEPSEEK_PASSWORD=
DEEPSEEK_DEVICE_ID=
DEEPSEEK_COOKIES=
DEEPSEEK_DS_POW_RESPONSE=
```

Sample code:


```python
import asyncio
import os
from deepseek_api import DeepseekAPI
from dotenv import load_dotenv

from deepseek_api.model import MessageData

load_dotenv()


async def main():
    email = os.environ.get("DEEPSEEK_EMAIL") # Your Deepseek email
    password = os.environ.get("DEEPSEEK_PASSWORD") # Your Deepseek password
    device_id = os.environ.get("DEEPSEEK_DEVICE_ID") # Your Deepseek device id
    cookies = os.environ.get("DEEPSEEK_COOKIES") # Your Deepseek cookies. You can get it by login to Deepseek and copy the cookies from the browser
    ds_pow_response = os.environ.get("DEEPSEEK_DS_POW_RESPONSE") # Your Deepseek ds_pow_response. You can get it by login to Deepseek and copy the ds_pow_response from the network tab in the browser

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
```

Output:

```bash
➜  chat-deepseek-api
 git:(main) ✗ python examples/simple_app.py
Starting chat session with id: 84ad4e3c-2cfc-45b1-9b84-61dcccd500af
Greetings! I'm DeepSeek-V3, an artificial intelligence assistant created by DeepSeek. I'm at your service and would be delighted to assist you with any inquiries or tasks you may have.
As an AI assistant, I can help answer questions, provide information, and have great conversations with you. Feel free to chat with me about any topic you'd like!
```
Enjoy!

## License

[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Disclaimer

This project is not affiliated with Deepseek in any way. Use at your own risk. This project was created for educational purposes only.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
