import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from adblockparser import AdblockRules

with open("easylist.txt") as f:
    raw_rules = f.readlines()
    rules = AdblockRules(raw_rules)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.tab_wgt = QTabWidget()
        self.tab_wgt.addTab(self.browser, "home")
        self.tab_wgt.setTabsClosable(True)
        self.tab_wgt.tabCloseRequested.connect(lambda i: self.tab_wgt.removeTab(i))
        self.tab_wgt.currentChanged.connect(self.tab_changed)
        self.setCentralWidget(self.tab_wgt)
        self.showMaximized()

        # nav bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        new_btn = QAction('New Tab', self)
        new_btn.triggered.connect(self.newtab)
        navbar.addAction(new_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    def newtab(self):
        browser = QWebEngineView()
        self.tab_wgt.addTab(browser, "about:blank")
        self.tab_wgt.setCurrentWidget(browser)
        self.url_bar.setText("about:blank")
        browser.titleChanged.connect(self.update_title)
        browser.urlChanged.connect(self.update_url)

    def tab_changed(self, i):
        browser: QWebEngineView = self.tab_wgt.widget(i)
        if browser:
            text = browser.url().toString()
            if text:
                self.url_bar.setText(text)
            else:
                self.url_bar.setText("about:blank")

    def navigate_to_url(self):
        if "https://" in self.url_bar.text():
            url = self.url_bar.text()
        else:
            url = "https://www." + self.url_bar.text()
        browser: QWebEngineView = self.tab_wgt.currentWidget()
        browser.setUrl(QUrl(url))

    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def update_title(self, title):
        self.tab_wgt.setTabText(self.tab_wgt.currentIndex(), title)




app = QApplication(sys.argv)
QApplication.setApplicationName("Jeswwws")
window = MainWindow()
app.exec_()
