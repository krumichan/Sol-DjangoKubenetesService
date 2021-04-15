import copy

from core.rancher import rancher


class RancherClientExample(rancher.Client):
    """
    Rancher의 Client Class를 확장한 Class
    """

    def __init__(self, access_key=None, secret_key=None, url=None, cache=False,
                 cache_time=86400, strict=False, headers=None, token=None,
                 verify=True, **kw):
        super().__init__(access_key, secret_key, url, cache, cache_time, strict, headers, token, verify, **kw)

    def evaluate_url_then_reload_schema(self, new_url):
        """
        Client의 url을 새로 바꾸고, 이를 평가하여 새로운 Schema를 확립한다.
        """

        self._url = new_url
        self.reload_schema()

    def load_schemas(self):
        return copy.copy(self.schema)
