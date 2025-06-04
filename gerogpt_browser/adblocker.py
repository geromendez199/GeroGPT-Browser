from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class AdBlocker(QWebEngineUrlRequestInterceptor):
    """Very small request interceptor that blocks common ad URLs."""

    def __init__(self, patterns=None):
        super().__init__()
        if patterns is None:
            patterns = [
                "doubleclick",
                "googlesyndication",
                "adservice",
                "/ads",
                "tracking",
            ]
        self.patterns = patterns

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if any(p in url for p in self.patterns):
            info.block(True)
