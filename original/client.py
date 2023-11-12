import json
from typing import Any, Callable, Dict

import requests

from original.__pkg__ import __version__
from original.base.client import OriginalInterface
from original.base.exceptions import OriginalAPIException
from original.types.original_response import OriginalResponse


def get_user_agent() -> str:
    return f"original-python-client-{__version__}"


def get_default_header() -> Dict[str, str]:
    base_headers = {
        "Content-type": "application/json",
        "X-ORIGINAL-Client": get_user_agent(),
    }
    return base_headers


class Original(OriginalInterface):
    def __init__(
        self, api_key: str, api_secret: str, timeout: float = 6.0, **options: Any
    ):
        super().__init__(
            api_key=api_key, api_secret=api_secret, timeout=timeout, **options
        )
        self.session = requests.Session()
        self.session.mount("http://", requests.adapters.HTTPAdapter(max_retries=1))
        self.session.mount("https://", requests.adapters.HTTPAdapter(max_retries=1))

    def set_http_session(self, session: requests.Session) -> None:
        """
        You can use your own `requests.Session` instance. This instance
        will be used for underlying HTTP requests.
        """
        self.session = session

    def _parse_response(self, response: requests.Response) -> OriginalResponse:
        try:
            parsed_result = json.loads(response.text) if response.text else {}
        except ValueError:
            raise OriginalAPIException(response.text, response.status_code)
        if response.status_code >= 399:
            raise OriginalAPIException(response.text, response.status_code)

        return OriginalResponse(
            parsed_result, dict(response.headers), response.status_code
        )

    def _make_request(
        self,
        method: Callable[..., requests.Response],
        relative_url: str,
        params: Dict = None,
        data: Any = None,
    ) -> OriginalResponse:
        params = params or {}
        data = data or {}
        serialized = None
        default_params = self.get_default_params()
        default_params.update(params)
        headers = get_default_header()
        headers["Authorization"] = self.auth_token
        headers["original-auth-type"] = "jwt"

        url = f"{self.base_url}/{relative_url}"

        if method.__name__ in ["post", "put", "patch"]:
            serialized = json.dumps(data)

        response = method(
            url,
            data=serialized,
            headers=headers,
            params=default_params,
            timeout=self.timeout,
        )
        return self._parse_response(response)

    def put(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.put, relative_url, params, data)

    def post(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.post, relative_url, params, data)

    def get(self, relative_url: str, params: Dict = None) -> OriginalResponse:
        return self._make_request(self.session.get, relative_url, params, None)

    def delete(self, relative_url: str, params: Dict = None) -> OriginalResponse:
        return self._make_request(self.session.delete, relative_url, params, None)

    def patch(
        self, relative_url: str, params: Dict = None, data: Any = None
    ) -> OriginalResponse:
        return self._make_request(self.session.patch, relative_url, params, data)

    def create_user(self, **user_data: Any) -> OriginalResponse:
        return self.post("user", data=user_data)

    def get_user(self, user_id: str) -> OriginalResponse:
        return self.get(f"users/{user_id}")

    def get_user_by_email(
        self, email: str
    ) -> OriginalResponse:
        return self.get("user", params={"email": email})

    def get_user_by_client_id(
        self, client_id: str
    ) -> OriginalResponse:
        return self.get("user", params={"client_id": client_id})

    def get_collection(
        self, uid: str
    ) -> OriginalResponse:
        return self.get(f"collections/{uid}")

    def create_asset(self, **asset_data: Any) -> OriginalResponse:
        return self.post("asset", data=asset_data)

    def edit_asset(self, uid: str, **asset_data: Any) -> OriginalResponse:
        return self.put(f"assets/{uid}", data=asset_data)

    def get_asset(self, uid: str) -> OriginalResponse:
        return self.get(f"assets/{uid}")

    def get_assets_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("assets", params={"user_uid": user_uid})

    def create_transfer(self, **transfer_data: Any) -> OriginalResponse:
        return self.post("transfer", data=transfer_data)

    def get_transfer(self, uid: str) -> OriginalResponse:
        return self.get(f"transfers/{uid}")

    def get_transfers_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("transfers", params={"user_uid": user_uid})

    def create_burn(self, **burn_data: Any) -> OriginalResponse:
        return self.post("burn", data=burn_data)

    def get_burn(self, uid: str) -> OriginalResponse:
        return self.get(f"burns/{uid}")

    def get_burns_by_user_uid(self, user_uid: str) -> OriginalResponse:
        return self.get("burns", params={"user_uid": user_uid})


