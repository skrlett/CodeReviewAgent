import aiohttp

class GitHubSession:
    _session = None

    @classmethod
    async def get_session(cls, headers):
        if cls._session is None:
            cls._session = aiohttp.ClientSession(headers=headers)
        
        return cls._session
        