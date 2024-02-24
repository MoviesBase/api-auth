class RedlockMock:
    def __init__(self, *args, **kwargs):
        pass


def mock_redlock(retry_count=20, retry_delay=0.2):
    return None
