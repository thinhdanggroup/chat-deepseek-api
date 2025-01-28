class API_URL:
    """Deepseek API URL constants"""

    BASE_URL = "https://chat.deepseek.com/api/v0"
    LOGIN = BASE_URL + "/users/login"
    CLEAR_CONTEXT = BASE_URL + "/chat/clear_context"
    CHAT = BASE_URL + "/chat/completion"
    CHAT_SESSION_CREATE = BASE_URL + "/chat_session/create"


class DeepseekConstants:
    """Deepseek constants"""

    BASE_HEADERS = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "content-type": "application/json",
        "cookie": "",
        "dnt": "1",
        "origin": "https://chat.deepseek.com",
        "priority": "u=1, i",
        "referer": "https://chat.deepseek.com/sign_in",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "x-app-version": "20241129.1",
        "x-client-locale": "en_US",
        "x-client-platform": "web",
        "x-client-version": "1.0.0-always",
    }

    BASE_COMPLETE_HEADERS = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "content-type": "application/json",
        "cookie": "",
        "dnt": "1",
        "origin": "https://chat.deepseek.com",
        "priority": "u=1, i",
        "referer": "https://chat.deepseek.com/a/chat/s/f8f4a0a7-8ee0-4d95-bc97-cbc7ad1add2a",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "x-app-version": "20241129.1",
        "x-client-locale": "en_US",
        "x-client-platform": "web",
        "x-client-version": "1.0.0-always",
        "x-ds-pow-response": "",
    }
