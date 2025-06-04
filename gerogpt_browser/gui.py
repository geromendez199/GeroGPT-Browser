import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QSplitter,
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEnginePage,
    QWebEngineProfile,
)
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPalette, QColor

from .browser import GeroGPTBrowser
from .adblocker import AdBlocker


class GeroGPTBrowserGUI(QMainWindow):
    """Simple GUI browser with ChatGPT side panel."""

    def __init__(self, *, incognito: bool = False, dark: bool = False):
        super().__init__()
        self.setWindowTitle("GeroGPT Browser")
        self.browser = GeroGPTBrowser()

        self.profile = QWebEngineProfile()
        if incognito:
            self.profile.setOffTheRecord(True)
        self.profile.setRequestInterceptor(AdBlocker())

        if dark:
            self._enable_dark_mode()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search query")
        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self.handle_go)

        top = QWidget()
        top_layout = QHBoxLayout(top)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_btn)

        self.web_view = QWebEngineView()
        page = QWebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(page)
        self.web_view.setUrl(QUrl("https://www.google.com"))

        self.chat_output = QTextEdit()
        self.chat_output.setReadOnly(True)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Chat with GPT")
        self.chat_btn = QPushButton("Send")
        self.chat_btn.clicked.connect(self.send_chat)

        chat_controls = QWidget()
        chat_controls_layout = QHBoxLayout(chat_controls)
        chat_controls_layout.addWidget(self.chat_input)
        chat_controls_layout.addWidget(self.chat_btn)

        chat_panel = QWidget()
        chat_layout = QVBoxLayout(chat_panel)
        chat_layout.addWidget(self.chat_output)
        chat_layout.addWidget(chat_controls)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.web_view)
        splitter.addWidget(chat_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(top)
        layout.addWidget(splitter)
        self.setCentralWidget(central)

    def _enable_dark_mode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.instance().setStyle("Fusion")
        QApplication.instance().setPalette(palette)

    def handle_go(self):
        text = self.url_bar.text().strip()
        if text.startswith("http://") or text.startswith("https://"):
            self.web_view.setUrl(QUrl(text))
        else:
            results = self.browser.search_web(text, num_results=1)
            if results:
                url = results[0]["url"]
                self.web_view.setUrl(QUrl(url))
                summary = self.browser.summarize_url(
                    url, bullets=True, sentences=3
                )
                self.chat_output.append(f"Summary:\n{summary}\n")

    def send_chat(self):
        prompt = self.chat_input.text().strip()
        if not prompt:
            return
        response = self.browser.chat(prompt)
        self.chat_output.append(f"> {prompt}\n{response}\n")
        self.chat_input.clear()


def run_gui(*, incognito: bool = False, dark: bool = False):
    """Launch the GUI browser."""
    app = QApplication(sys.argv)
    window = GeroGPTBrowserGUI(incognito=incognito, dark=dark)
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Launch the GUI browser")
    parser.add_argument("--incognito", action="store_true", help="Use a private profile")
    parser.add_argument("--dark", action="store_true", help="Enable a dark theme")
    args = parser.parse_args()

    run_gui(incognito=args.incognito, dark=args.dark)
