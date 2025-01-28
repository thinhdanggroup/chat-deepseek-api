from typing import Optional
import aiohttp
import aiofiles
import json
from abc import ABC, abstractmethod
from chat_deepseek_api.constants import API_URL, DeepseekConstants, DeepseekHeaderKey
from chat_deepseek_api.errors import (
    EmptyEmailOrPasswordError,
    MissingHeaderConfigError,
    NotLoggedInError,
)
from chat_deepseek_api.model import MessageData


class DeepSeekBase(ABC):
    """
    A base class to create DeepseekAPI instances.
    """

    def __init__(
        self,
        email: str,
        password: str,
        save_login: bool = False,
        device_id: str = "",
        verbose_level: int = 0,
        custom_headers: dict = {},
    ):
        """
        Constructor method for DeepseekAPI class.

        Initializes a DeepseekAPI instance with provided credentials and settings.

        Parameters:
        email (str): User's email for Deepseek account
        password (str): Password for user's Deepseek account
        save_login (bool): Whether to save credentials to login.json to avoid re-login

        """
        self.email = email
        self.password = password

        if not email or not password:
            raise EmptyEmailOrPasswordError

        self.save_login = save_login

        if (
            not custom_headers
            or custom_headers.get(DeepseekHeaderKey.COOKIE) is None
            or custom_headers.get(DeepseekHeaderKey.X_DS_POW_RESPONSE) is None
        ):
            raise MissingHeaderConfigError

        self.headers = DeepseekConstants.BASE_HEADERS.copy()
        self.headers.update(custom_headers)

        self.completion_headers = DeepseekConstants.BASE_COMPLETE_HEADERS.copy()
        self.completion_headers.update(custom_headers)

        self.credentials = {}
        self._thread_timer = None  # Initialized in the _schedule_update_token method
        self.session = None
        self.device_id = device_id
        self.verbose_level = verbose_level

    def set_authorization_header(self):
        """Sets the authorization header to a JWT token.

        Gets the JWT token by calling get_token() and prepends 'Bearer '
        to set the authorization header.
        """
        self.headers["authorization"] = "Bearer " + self.get_token()

    def get_token(self):
        """Get token

        Returns:
            str: JWT Authorization token
        """
        return self.get_credentials()["data"]["user"]["token"]

    def get_credentials(self):
        """Get credentials

        Returns:
            dict: Credentials JSON data from login response
        """
        return self.credentials

    def _schedule_update_token(self):
        """Schedules a timer to refresh the JWT token before it expires.

        Decodes the current JWT token to get the 'exp' expiration time.
        Subtracts 1 hour from the 'exp' time to refresh the token early.
        Starts a Timer thread to call the _login() method when the expiration
        time is reached. This will refresh the token and update the authorization
        header with the new token.
        """
        # Decode the JWT token
        # token = self.get_token()
        # decoded_token = jwt.decode(token, options={"verify_signature": False})

        # # Fetch the 'exp' value and subtract 1 hour (to be safe)
        # exp_time = datetime.datetime.fromtimestamp(
        #     decoded_token["exp"]
        # ) - datetime.timedelta(hours=1)

        # self._thread_timer = threading.Timer(
        #     (exp_time - datetime.datetime.now()).total_seconds(), self._login
        # )
        # self._thread_timer.start()
        pass

    def is_logged_in(self):
        """Check if user is logged in

        Returns:
            bool: True if logged in, False otherwise
        """
        if self.credentials:
            return True
        else:
            return False

    def raise_for_not_logged_in(self):
        """Raise NotLoggedInError if user is not logged in

        Raises:
            NotLoggedInError: If user is not logged in
        """
        if not self.is_logged_in():
            raise NotLoggedInError

    @abstractmethod
    def login(self):
        """Logs the user in by loading credentials from file or calling login API.

        If save_login is True, tries to load credentials from the login.json file.
        If file not found, calls _login() to login via API.

        If save_login is False, calls _login() to always login via API.

        Schedules an update token callback to refresh the token periodically.
        """
        pass

    @abstractmethod
    def close(self):
        """Call destructor method"""
        pass

    @abstractmethod
    def new_chat(self):
        """Start a new chat"""
        pass

    @abstractmethod
    def chat(self, message: str):
        """Chat with the Deepseek API.

        Sends a chat message to the Deepseek API and yields the response.

        Args:
            message (str): The chat message to send.

        Yields:
            dict: The JSON response from the API for each chat message.
        """
        pass

    @abstractmethod
    def _login(self):
        """Logs in the user by sending a POST request to the login API endpoint.

        Sends the login request with email, password and other required fields.
        Saves the credentials to a file if save_login is True.
        Returns the JSON response from the API.

        Raises:
            EmptyEmailOrPasswordError: If the email or password is not provided.
            HTTP Error: If the login request fails.

        Returns:
            dict: Credentials JSON data from login response
        """
        pass


class DeepseekAPI(DeepSeekBase):
    """
    An asynchronous class to interact with the Deepseek API.
    """

    async def __aenter__(self):
        """Initializes an aiohttp ClientSession and logs in.

        This method is called when entering an async context manager.
        It creates the aiohttp ClientSession used for making requests.
        It also calls the login() method to authenticate with Deepseek.

        Returns:
            Self - Returns itself to enable use as an async context manager.
        """
        self.session = aiohttp.ClientSession()
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Closes the aiohttp ClientSession and cancels the scheduled token update.

        This method is called when exiting the async context manager. It closes
        the aiohttp ClientSession that was used for making requests to the API.

        It also cancels the scheduled token update that was created in
        __schedule_update_token() to periodically refresh the auth token.
        """
        await self.session.close()
        if self._thread_timer:
            self._thread_timer.cancel()

    @staticmethod
    async def create(*args, **kwargs):
        """Creates a new DeepseekAPI instance and enters the context manager.

        This static method initializes a new DeepseekAPI instance with the given
        arguments and enters the async context manager by calling __aenter__().

        Args:
            *args: Positional arguments to pass to DeepseekAPI constructor.
            **kwargs: Keyword arguments to pass to DeepseekAPI constructor.

        Returns:
            DeepseekAPI instance that has entered the context manager.
        """
        self = DeepseekAPI(*args, **kwargs)
        await self.__aenter__()
        return self

    async def close(self):
        """Closes the DeepseekAPI instance by exiting the context manager.

        Calls __aexit__ to close the aiohttp session and cancel the token update.
        """
        await self.__aexit__(None, None, None)

    async def _login(self):
        if self.email == "" or self.password == "":
            raise EmptyEmailOrPasswordError

        json_data = {
            "email": self.email,
            "mobile": "",
            "password": self.password,
            "area_code": "",
            "device_id": self.device_id,
            "os": "web",
        }

        async with self.session.post(
            API_URL.LOGIN, headers=self.headers, json=json_data
        ) as response:
            self.credentials = await response.json()
            if response.status != 200:
                raise Exception("Login failed")

            self.headers["authorization"] = "Bearer " + self.get_token()

            if self.save_login:
                async with aiofiles.open("login.json", "w") as file:
                    await file.write(json.dumps(self.credentials))

            return await response.json()

    async def login(self):
        """Logs the user in by loading credentials from file or calling login API.

        If save_login is True, tries to load credentials from the login.json file.
        If file not found, calls _login() to login via API.

        If save_login is False, calls _login() to always login via API.

        Schedules an update token callback to refresh the token periodically.
        """
        if self.save_login:
            try:
                async with aiofiles.open("login.json", "r") as file:
                    content = await file.read()
                    self.credentials = json.loads(content)

                    self.set_authorization_header()
            except FileNotFoundError:
                await self._login()
        else:
            await self._login()
        # Schedule a callback to update the token periodically
        self._schedule_update_token()

    async def new_chat(self):
        """Start a new chat asynchronously"""

        json_data = {"character_id": None}

        async with self.session.post(
            API_URL.CHAT_SESSION_CREATE, headers=self.headers, json=json_data
        ) as response:
            if response.status != 200:
                json_response = await response.text()
                raise Exception(f"Failed to start new chat response: {json_response}")

            res = await response.json()

            if "data" not in res or "biz_data" not in res["data"]:
                raise Exception("Failed to start new chat")

            id = res["data"]["biz_data"]["id"]
            if id is None:
                raise Exception("There is no chat id")
            return id

    async def chat(
        self,
        message: str,
        id: str = None,
        parent_message_id: Optional[str] = None,
        thinking_enabled: bool = False,
        search_enabled: bool = False,
    ):
        """Chat asynchronously with the Deepseek API.

        Sends a chat message to the Deepseek API and yields the response.

        Args:
            message (str): The chat message to send.
            id (str): The chat session id to use. If None, a new chat session is started.
            message_id (str): The message id to use. If None, the chat session is started.

        Yields:
            dict: The JSON response from the API for each chat message.
        """

        if id is None:
            id = await self.new_chat()
            parent_message_id = None

        json_data = {
            "chat_session_id": id,
            "parent_message_id": parent_message_id,
            "prompt": message,
            "ref_file_ids": [],
            "thinking_enabled": thinking_enabled,
            "search_enabled": search_enabled,
        }

        self.completion_headers.update({"Authorization": "Bearer " + self.get_token()})

        async with self.session.post(
            API_URL.CHAT, headers=self.completion_headers, json=json_data
        ) as response:
            if response.status != 200:
                res = await response.text()
                raise Exception(
                    f"Failed to send chat message with status {response.status}, response: {res}"
                )

            # Iterate over the content asynchronously
            async for data in response.content:
                line = data.decode().strip().replace("data: ", "")

                if line:
                    if "[DONE]" in line:
                        continue

                    try:
                        line = json.loads(line)
                        data = MessageData.model_validate(line)
                        if data.has_content():
                            yield data
                        else:
                            self._log_message(f"No content {line}")
                    except json.JSONDecodeError:
                        self._log_message(f"Invalid JSON data {line}")

    def _log_message(self, message: str, level: int = 1):
        """Log message if verbose level is greater than or equal to the level"""
        if self.verbose_level >= level:
            print(message)
