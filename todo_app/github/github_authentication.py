import os
from todo_app.user.user import User
import requests
import random
from hashlib import sha256

class GithubAuthentication:
    def __init__(self):
        random.seed(a=None, version=2)
        self._client_id = None
        self._client_secret = None
        self.state = sha256(str(random.random()).encode('ascii')).hexdigest()
        self._authentication=None
    

    def get_client_id(self):
        if not self._client_id:
            self._client_id = os.environ["CLIENT_ID"]
        return self._client_id
    
    def get_client_secret(self):
        if not self._client_secret:
            self._client_secret = os.environ["CLIENT_SECRET"]
        return self._client_secret

    def get_github_auth_url(self):
        params={
            "client_id": self.get_client_id(),
            "state": self.state
        }
        return f"https://github.com/login/oauth/authorize?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    
    def post_github_identity(self, response):
        if not self._authentication:
            returned_state = response.args.get("state")
            if returned_state != self.state:
                raise ValueError(f"Returned state does not match internal state")
            data = {
                "code": response.args.get("code"),
                "client_id": self.get_client_id(),
                "client_secret": self.get_client_secret()
            }
            result = requests.post("https://github.com/login/oauth/access_token", data=data)
            
            self._authentication = str(result.content).split('&')[0].split('=')[-1]
        return User(self.get_user())

    def get_user(self) -> int:
        respone = requests.get("https://api.github.com/user", headers={"Authorization": f"token {self._authentication}"})
        return respone.json()['id']
    
    def authentication(self):
        return self._authentication