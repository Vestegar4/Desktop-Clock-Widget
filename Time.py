import sys
import ctypes
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QSystemTrayIcon, QMenu, QAction, QStyle
from PyQt5.QtCore import QTimer, Qt, QTime, QDate
from PyQt5.QtGui import QFontDatabase, QFont, QIcon

def enable_blur(hwnd):
    class ACCENT_POLICY(ctypes.Structure):
        _fields_ = [
            ("AccentState", ctypes.c_int),
            ("AccentFlags", ctypes.c_int),
            ("GradientColor", ctypes.c_int),
            ("AnimationId", ctypes.c_int)
        ]

    class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ACCENT_POLICY)),
            ("SizeOfData", ctypes.c_size_t)
        ]

    accent = ACCENT_POLICY()
    accent.AccentState = 4
    accent.GradientColor = 0x01000000

    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = 19
    data.Data = ctypes.pointer(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

app = QApplication(sys.argv)

window = QWidget()
window.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
window.setAttribute(Qt.WA_TranslucentBackground)

window.setStyleSheet("""
    QWidget {
        color: rgba(255,255,255,230);
        background-color: rgba(0,0,0,10);
        border-radius: 22px;
    }
""")

layout = QVBoxLayout(window)
layout.setContentsMargins(30, 30, 30, 30)

label_time = QLabel()
label_time.setAlignment(Qt.AlignCenter)
label_time.setStyleSheet("background: transparent;")

label_date = QLabel()
label_date.setAlignment(Qt.AlignCenter)
label_date.setStyleSheet("background: transparent;")

layout.addWidget(label_time)
layout.addWidget(label_date)

font_id = QFontDatabase.addApplicationFont("LEMONMILK-LIGHT.otf")
if font_id != -1:
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
else:
    font_family = "Arial" 

font_time = QFont(font_family, 30)
font_date = QFont(font_family, 14)

label_time.setFont(font_time)
label_date.setFont(font_date)

def update_time():
    time = QTime.currentTime().toString("hh:mm:ss")
    date = QDate.currentDate().toString("dddd, dd MMMM yyyy")

    label_time.setText(time)
    label_date.setText(date)
    
    window.adjustSize()

timer = QTimer()
timer.timeout.connect(update_time)
timer.start(1000)

update_time()

screen = QApplication.primaryScreen().geometry()

x = screen.width() - window.width() - 10
y = 20

window.move(x, y)
window.show()

hwnd = int(window.winId())
enable_blur(hwnd)

tray_icon_image = app.style().standardIcon(QStyle.SP_DesktopIcon)
tray_icon = QSystemTrayIcon(tray_icon_image, app)
tray_icon.setToolTip("Aesthetic Clock Widget")

menu = QMenu()

quit_action = QAction("Keluar", app)
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

tray_icon.setContextMenu(menu)
tray_icon.show()

sys.exit(app.exec_())