import os
import sys
import ctypes
from ctypes import CDLL
def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсам, работает и для dev, и для PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
lib = CDLL(resource_path("interception.dll"))
import configparser
from pathlib import Path
import vgamepad as vg
from pathlib import Path
from PySide6.QtCore import QThread, Qt, QTimer, Signal, QEvent, QPoint, QRect, QSize
from PySide6.QtGui import QFont, QColor, QAction, QIcon, QPixmap, QCursor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QMessageBox,
    QListWidget,
    QInputDialog,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QScrollArea,
    QGridLayout,
    QLayout,
    QCheckBox,
    QDialog,
    QLineEdit,
    QSizeGrip,
)

STYLE_SHEET = """
/* Основное окно и фон */
QMainWindow, QWidget#Container, QWidget#scrollAreaWidgetContents { 
    background-color: #0A0A0A; 
}

#Container {
    background-color: #121212;
    border: 2px solid #0078d7; /* Синяя рамка в стиле ADD/START  */
    border-radius: 10px;       /* Мягкие углы  */
}

QFrame#Header {
    border-bottom: 1px solid #1A1A1A;
    background-color: #0A0A0A;
}

QPushButton#min_btn, QPushButton#close_btn {
    background-color: transparent;
    border: 1px solid #333;
    color: #666;
    font-size: 16px;
    font-weight: bold;
}
QPushButton#min_btn:hover {
    color: #0078d7;
    border-color: #0078d7;
}
QPushButton#close_btn:hover {
    color: #ff4b4b; /* Красный акцент при наведении на закрытие  */
    border-color: #ff4b4b;
}

/* Скролл-зона */
QScrollArea#ScrollArea {
    border: none;
    background-color: #0A0A0A;
}

/* Кастомный скроллбар */
QScrollBar:vertical {
    border: none;
    background: #0A0A0A;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #2A2A2A;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover { background: #3A3A3A; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

/* Секция профилей */
QFrame#ProfSection { 
    background-color: #1A1A1A; 
    border: 1px solid #333; 
    border-radius: 6px; 
    padding: 2px;
}

QFrame#ProfSection QLabel {
    color: #C0C0C0;
    font-weight: bold;
    margin-left: 5px;
}

/* Выпадающий список */
QComboBox { 
    background-color: #252525; 
    color: #FFF; 
    border: 1px solid #444; 
    border-radius: 4px; 
    padding: 2px 10px; 
    min-width: 120px;
}
QComboBox:hover { border-color: #0078d7; }
QComboBox QAbstractItemView { 
    background-color: #1A1A1A; 
    color: #BBB; 
    selection-background-color: #0078d7; 
}

QComboBox QAbstractItemView { 
    background-color: #1A1A1A; 
    color: #FFFFFF; 
    selection-background-color: #0078d7;
    border: 1px solid #444;
}

/* Фикс для выпадающего списка */
QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none; /* Убираем стандартную стрелку */
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #0078d7; /* Рисуем свою синюю стрелочку */
    margin-right: 5px;
}

QComboBox QListView {
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #333;
    selection-background-color: #0078d7;
}

/* Кнопки профилей (ADD, DELETE и т.д.) */
QFrame#ProfSection QPushButton {
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    min-width: 65px;
    padding: 5px;
    font-size: 10px;
}

QFrame#ProfSection QPushButton:hover { border-color: #0078d7; color: #FFF; }

QFrame#ProfSection QPushButton:pressed { background-color: #0078d7; color: #FFF; }

/* Убираем пунктирную рамку фокуса со всех кнопок */
QPushButton {
    outline: none;
}

/* Дополнительно для слотов, если они выделяются отдельно */
QPushButton:focus {
    border: 1px solid #333; /* Оставляем стандартную границу, но без пунктира */
}

/* Кнопка запуска (Два состояния) */
QPushButton#run_btn_inactive { 
    background-color: #1A1A1A; 
    color: #0078d7; 
    font-weight: bold; 
    border: 2px solid #0078d7; 
    border-radius: 6px; 
}

QCheckBox {
    color: #CCCCCC;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #1A1A1A;
    border: 2px solid #333;
    border-radius: 4px;
}
QCheckBox::indicator:checked {
    background-color: #0078d7;
    border: 2px solid #005a9e;
}
QCheckBox::indicator:hover {
    border: 2px solid #0078d7;
}

QPushButton#run_btn_active { 
    background-color: #1A1A1A; 
    color: #e74c3c; 
    font-weight: bold; 
    border: 2px solid #e74c3c; 
    border-radius: 6px; 
}

/* Строки биндинга */
QFrame[objectName^="Row_"] {
    background-color: #121212;
    border: 1px solid #1A1A1A;
    border-radius: 8px;
    margin: 2px 5px;
}

QFrame[objectName^="Row_"] QLabel {
    color: #C0C0C0;
    font-family: "Segoe UI";
    font-weight: bold;
    font-size: 13px;
    border: none;
}

/* Кнопки-слоты */
QPushButton[objectName^="Slot_"] {
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 10px;
    min-height: 30px;
}
QPushButton[objectName^="Slot_"]:hover {
    border-color: #0078d7;
    background-color: #252525;
    color: #00aaff;
}
QPushButton[objectName^="Slot_"]:pressed {
    background-color: #0078d7;
    color: #FFFFFF;
}

/* Эффект наведения, когда кнопка КРАСНАЯ (выключена) */
#run_btn_inactive:hover {
    background-color: #001220; /* Тот самый синий, уходящий в черноту */
    border-color: #4db3ff;     /* Светло-голубая рамка */
    color: #4db3ff;            /* Светло-голубой текст */
}

/* Эффект наведения, когда кнопка СИНЯЯ (активна) */
#run_btn_active:hover {
background-color: #2D1A1A; /* Тёмно-красный фон */
    border-color: #ff7070;     /* Ярко-красная рамка */
    color: #ff7070;            /* Яркий текст */
}
"""

PROJECT_NAME = "XBOX-Kepad"
VERSION = "v1.0"

# --- PROFILES SETTINGS ---
GLOBAL_CONFIG = "System_Config.ini"
PROFILES_DIR = "Profiles"
# Теперь это имя файла
DEFAULT_PROFILE = "Default.ini"
# А это полный путь для работы внутри кода
DEFAULT_PROFILE_PATH = os.path.join(PROFILES_DIR, DEFAULT_PROFILE)

# Проверяем, существует ли папка, чтобы не было ошибок при старте
if not os.path.exists(PROFILES_DIR):
    os.makedirs(PROFILES_DIR)

ICONS_PATH = resource_path("XBOX ICONS")

BUTTON_ICONS = {
    # Основные кнопки
    "A": "ABXY/A.png",
    "B": "ABXY/B.png",
    "X": "ABXY/X.png",
    "Y": "ABXY/Y.png",
    # Бамперы и Триггеры
    "RT": "BUMPERS_TRIGGERS/RT.png",
    "LT": "BUMPERS_TRIGGERS/LT.png",
    "RB": "BUMPERS_TRIGGERS/RB.png",
    "LB": "BUMPERS_TRIGGERS/LB.png",
    # Крестовина (D-Pad)
    "DPAD_UP": "DPAD/DPAD_UP.png",
    "DPAD_DOWN": "DPAD/DPAD_DOWN.png",
    "DPAD_LEFT": "DPAD/DPAD_LEFT.png",
    "DPAD_RIGHT": "DPAD/DPAD_RIGHT.png",
    # Стики (LS/RS)
    "LS_UP": "STICKS/LS_UP.png",
    "LS_DOWN": "STICKS/LS_DOWN.png",
    "LS_LEFT": "STICKS/LS_LEFT.png",
    "LS_RIGHT": "STICKS/LS_RIGHT.png",
    "LTB": "STICKS/LTB.png",
    "RS_UP": "STICKS/RS_UP.png",
    "RS_DOWN": "STICKS/RS_DOWN.png",
    "RS_LEFT": "STICKS/RS_LEFT.png",
    "RS_RIGHT": "STICKS/RS_RIGHT.png",
    "RTB": "STICKS/RTB.png",
    # Системные
    "START": "SYSTEM/START.png",
    "BACK": "SYSTEM/BACK.png",
    "GUIDE": "SYSTEM/GUIDE.png",
}


def setup_button_icon(label_widget, gp_key):
    icon_subpath = BUTTON_ICONS.get(gp_key)
    if icon_subpath:
        full_icon_path = os.path.join(ICONS_PATH, icon_subpath)
        if os.path.exists(full_icon_path):
            pixmap = QPixmap(full_icon_path)
            # Масштабируем иконку (например, 24x24 или 32x32)
            label_widget.setPixmap(
                pixmap.scaled(52, 52, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            label_widget.setText("")  # Убираем текст, если есть картинка
            return

    label_widget.setText(gp_key)  # Если иконки нет — пишем текст


# --- INTERCEPTION STRUCTURES (x64 Ready) ---
class KeyStroke(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("code", ctypes.c_ushort),
        ("state", ctypes.c_ushort),
        ("rolling", ctypes.c_ushort),
    ]


class Stroke(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("key", KeyStroke)]


INTERCEPTION_PREDICATE = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)

# --- KEYBOARD DATABASE ---
NAME_TO_CODE = {
    # Основные буквы
    "A": 0x1E,
    "B": 0x30,
    "C": 0x2E,
    "D": 0x20,
    "E": 0x12,
    "F": 0x21,
    "G": 0x22,
    "H": 0x23,
    "I": 0x17,
    "J": 0x24,
    "K": 0x25,
    "L": 0x26,
    "M": 0x32,
    "N": 0x31,
    "O": 0x18,
    "P": 0x19,
    "Q": 0x10,
    "R": 0x13,
    "S": 0x1F,
    "T": 0x14,
    "U": 0x16,
    "V": 0x2F,
    "W": 0x11,
    "X": 0x2D,
    "Y": 0x15,
    "Z": 0x2C,
    # Цифры (основной ряд)
    "1": 0x02,
    "2": 0x03,
    "3": 0x04,
    "4": 0x05,
    "5": 0x06,
    "6": 0x07,
    "7": 0x08,
    "8": 0x09,
    "9": 0x0A,
    "0": 0x0B,
    # Функциональные клавиши
    "F1": 0x3B,
    "F2": 0x3C,
    "F3": 0x3D,
    "F4": 0x3E,
    "F5": 0x3F,
    "F6": 0x40,
    "F7": 0x41,
    "F8": 0x42,
    "F9": 0x43,
    "F10": 0x44,
    "F11": 0x57,
    "F12": 0x58,
    "F13": 0x64,
    "F14": 0x65,
    "F15": 0x66,
    # Управление
    "ESC": 0x01,
    "ENTER": 0x1C,
    "SPACE": 0x39,
    "TAB": 0x0F,
    "BACKSPACE": 0x0E,
    "CAPSLOCK": 0x3A,
    "PRINTSCREEN": 0x37,
    "SCROLLLOCK": 0x46,
    "PAUSE": 0x45,
    # Модификаторы
    "LSHIFT": 0x2A,
    "RSHIFT": 0x36,
    "LCTRL": 0x1D,
    "RCTRL": 0x9D,
    "LALT": 0x38,
    "RALT": 0xB8,
    "LWIN": 0xDB,
    "RWIN": 0xDC,
    "APPS": 0xDD,
    # NumPad (Цифровая клавиатура)
    "NUM0": 0x52,
    "NUM1": 0x4F,
    "NUM2": 0x50,
    "NUM3": 0x51,
    "NUM4": 0x4B,
    "NUM5": 0x4C,
    "NUM6": 0x4D,
    "NUM7": 0x47,
    "NUM8": 0x48,
    "NUM9": 0x49,
    "NUM_ENTER": 0x9C,
    "NUM_PLUS": 0x4E,
    "NUM_MINUS": 0x4A,
    "NUM_MULTIPLY": 0x37,
    "NUM_DIVIDE": 0xB5,
    "NUM_PERIOD": 0x53,
    "NUMLOCK": 0x45,
    # Символы
    "MINUS": 0x0C,
    "EQUALS": 0x0D,
    "LBRACKET": 0x1A,
    "RBRACKET": 0x1B,
    "SEMICOLON": 0x27,
    "APOSTROPHE": 0x28,
    "GRAVE": 0x29,
    "BACKSLASH": 0x2B,
    "COMMA": 0x33,
    "DOT": 0x34,
    "SLASH": 0x35,
    # OEM Символы (могут варьироваться, но это стандарты)
    "OEM_1": 0x27,  # ; :
    "OEM_PLUS": 0x0D,  # = +
    "OEM_COMMA": 0x33,  # , <
    "OEM_MINUS": 0x0C,  # - _
    "OEM_PERIOD": 0x34,  # . >
    "OEM_2": 0x35,  # / ?
    "OEM_3": 0x29,  # ` ~ (Тильда/Ё)
    "OEM_4": 0x1A,  # [ {
    "OEM_5": 0x2B,  # \ |
    "OEM_6": 0x1B,  # ] }
    "OEM_7": 0x28,  # ' "
    "OEM_102": 0x56,  # Дополнительная клавиша на ISO-клавиатурах (возле Shift)
    # Мультимедиа (могут работать не на всех клавиатурах)
    "MUTE": 0xA0,
    "VOL_DOWN": 0xAE,
    "VOL_UP": 0xB0,
    "MEDIA_PLAY": 0xA2,
    "MEDIA_STOP": 0xA4,
    "MEDIA_PREV": 0x90,
    "MEDIA_NEXT": 0x99,
    "BROWSER_HOME": 0xB2,
    "MAIL": 0x6C,
    "CALCULATOR": 0xA1,
}

# Инвертируем для быстрого поиска
# ВАЖНО: Коды стрелок и т.д. в Interception приходят как 0x48 + INTERCEPTION_KEY_E0
CODE_TO_NAME = {v: k for k, v in NAME_TO_CODE.items()}

# Список клавиш, которые драйвер помечает как E0 (Extended)
EXTENDED_KEYS = {
    0x48: "UP",
    0x50: "DOWN",
    0x4B: "LEFT",
    0x4D: "RIGHT",
    0x47: "HOME",
    0x4F: "END",
    0x53: "DELETE",
    0x49: "PAGEUP",
    0x51: "PAGEDOWN",  # <- Добавили эти
    0xD2: "INSERT",
    0xD3: "DELETE",
    0x1D: "RCTRL",
    0x38: "RALT",
    0x1C: "NUM_ENTER",
    0x35: "NUM_DIVIDE",
    0x5B: "LWIN",
    0x5C: "RWIN",
}

# --- GAMEPAD MAPPING DATABASE ---
GP_BUTTON_MAP = {
    "A": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
    "B": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
    "X": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
    "Y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
    "LB": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
    "RB": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
    "DPAD_UP": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
    "DPAD_DOWN": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
    "DPAD_LEFT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
    "DPAD_RIGHT": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
    "LTB": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
    "RTB": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
    "START": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
    "BACK": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
    "GUIDE": vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE,
}

GP_ANALOG = [
    "LT",
    "RT",
    "LS_UP",
    "LS_DOWN",
    "LS_LEFT",
    "LS_RIGHT",
    "RS_UP",
    "RS_DOWN",
    "RS_LEFT",
    "RS_RIGHT",
]

GP_MAP_KEYS = list(GP_BUTTON_MAP.keys()) + GP_ANALOG

# Строгий порядок отображения в UI
GP_MAP_KEYS = [
    "A",
    "B",
    "X",
    "Y",
    "LB",
    "RB",
    "LT",
    "RT",
    "DPAD_UP",
    "DPAD_DOWN",
    "DPAD_LEFT",
    "DPAD_RIGHT",
    "LS_UP",
    "LS_DOWN",
    "LS_LEFT",
    "LS_RIGHT",
    "LTB",
    "RS_UP",
    "RS_DOWN",
    "RS_LEFT",
    "RS_RIGHT",
    "RTB",
    "GUIDE",
    "START",
    "BACK",
]

# Флаги состояний клавиш
INTERCEPTION_FILTER_KEY_NONE = 0x0000
INTERCEPTION_FILTER_KEY_ALL = 0xFFFF
INTERCEPTION_FILTER_KEY_DOWN = 0x0001
INTERCEPTION_FILTER_KEY_UP = 0x0002
INTERCEPTION_FILTER_KEY_E0 = 0x0004  # Для стрелок и системных клавиш
INTERCEPTION_FILTER_KEY_E1 = 0x0008
INTERCEPTION_FILTER_KEY_TERMSRV_SET_LED = 0x0010
INTERCEPTION_FILTER_KEY_TERMSRV_SHADOW = 0x0020
INTERCEPTION_FILTER_KEY_TERMSRV_VKPACKET = 0x0040

# Собираем маску для фильтра
KEYBOARD_FILTER = (
    INTERCEPTION_FILTER_KEY_DOWN
    | INTERCEPTION_FILTER_KEY_UP
    | INTERCEPTION_FILTER_KEY_E0
)


class CustomInputDialog(QDialog):
    def __init__(self, title, label_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedWidth(380)

        # Насильно впихиваем стиль, но уточняем детали для внутренних виджетов 
        self.setStyleSheet(parent.styleSheet() if parent else STYLE_SHEET)

        # Основной контейнер с рамкой
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("CustomDialogFrame")
        self.main_frame.setStyleSheet(
            """
            QFrame#CustomDialogFrame { 
                border: 2px solid #0078d7; 
                background-color: #121212; 
                border-radius: 5px;
            }
            QLabel { 
                color: #cccccc; 
                font-size: 14px; 
            }
            QLineEdit { 
                background-color: #1a1a1a; 
                border: 1px solid #333; 
                color: white; 
                padding: 5px;
                border-radius: 3px;
            }
            QLineEdit:focus { 
                border-color: #0078d7; 
            }
            QPushButton { 
                background-color: #222; 
                color: #0078d7; 
                border: 1px solid #0078d7; 
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #001220; 
                color: #4db3ff; 
                border-color: #4db3ff;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_frame)

        inner_layout = QVBoxLayout(self.main_frame)
        inner_layout.setContentsMargins(20, 20, 20, 20)
        inner_layout.setSpacing(15)

        # Заголовок (чуть ярче)
        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet("font-weight: bold; color: #0078d7; font-size: 16px;")
        inner_layout.addWidget(title_lbl)

        self.label = QLabel(label_text)
        inner_layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setMinimumHeight(35)
        inner_layout.addWidget(self.input_field)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("СОЗДАТЬ")
        self.cancel_btn = QPushButton("ОТМЕНА")

        for b in [self.ok_btn, self.cancel_btn]:
            b.setFocusPolicy(Qt.NoFocus)
            b.setCursor(Qt.PointingHandCursor)
            btn_layout.addWidget(b)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        inner_layout.addLayout(btn_layout)

    def get_value(self):
        return self.input_field.text().strip()


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.items = []

    def __del__(self):
        del self.items

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.items:
            size = size.expandedTo(item.minimumSize())
        size += QSize(
            2 * self.contentsMargins().top(), 2 * self.contentsMargins().top()
        )
        return size

    def _do_layout(self, rect, test_only):
        x, y, line_height = rect.x(), rect.y(), 0
        for item in self.items:
            wid = item.widget()
            space_x, space_y = self.spacing(), self.spacing()
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        return y + line_height - rect.y()


class InterceptionThread(QThread):
    key_signal = Signal(str, int)

    def __init__(self):
        super().__init__()
        self.is_running, self.enabled = True, False
        self.is_capturing = False
        self.bindings = {k: ["NONE"] * 6 for k in GP_MAP_KEYS}
        self.context = None
        self._init_driver()

    def _init_driver(self):
        try:
            dll_path = Path(__file__).parent.resolve() / "interception.dll"
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(str(dll_path.parent))
            self.lib = ctypes.CDLL(str(dll_path))

            # Жёсткая настройка типов для x64
            self.lib.interception_create_context.restype = ctypes.c_void_p

            self.lib.interception_wait.restype = (
                ctypes.c_void_p
            )  # Возвращает указатель на девайс
            self.lib.interception_wait.argtypes = [ctypes.c_void_p]

            self.lib.interception_receive.argtypes = [
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_uint,
            ]
            self.lib.interception_send.argtypes = [
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_uint,
            ]
            self.lib.interception_set_filter.argtypes = [
                ctypes.c_void_p,
                INTERCEPTION_PREDICATE,
                ctypes.c_ushort,
            ]
            self.lib.interception_destroy_context.argtypes = [ctypes.c_void_p]

            self.context = self.lib.interception_create_context()
            if self.context:
                # Предикат ловит устройства 1-10 (клавиатуры)
                self._cb = INTERCEPTION_PREDICATE(lambda d: 1 <= d <= 10)
                self.lib.interception_set_filter(
                    self.context, self._cb, KEYBOARD_FILTER
                )
                print(f"[SYSTEM] Driver loaded. Context: {self.context}")
        except Exception as e:
            print(f"[CRITICAL] Driver Error: {e}")

    def run(self):
        if not self.context:
            return
        stroke = Stroke()

        try:
            gamepad = vg.VX360Gamepad()
            print("[SYSTEM] Virtual Xbox 360 Controller connected.")
        except Exception as e:
            print(f"[ERROR] Gamepad initialization failed: {e}")
            return

        # Храним состояние осей
        axes = {
            "LS_UP": 0,
            "LS_DOWN": 0,
            "LS_LEFT": 0,
            "LS_RIGHT": 0,
            "RS_UP": 0,
            "RS_DOWN": 0,
            "RS_LEFT": 0,
            "RS_RIGHT": 0,
        }

        while self.is_running:
            device = self.lib.interception_wait(self.context)
            if not device:
                continue

            if (
                self.lib.interception_receive(
                    self.context, device, ctypes.byref(stroke), 1
                )
                > 0
            ):
                sc, st = stroke.key.code, stroke.key.state
                is_down = not (st & 1)
                is_extended = bool(st & 2)

                if is_extended and sc in EXTENDED_KEYS:
                    name = EXTENDED_KEYS[sc]
                else:
                    name = CODE_TO_NAME.get(sc, f"KEY_{sc}")

                self.key_signal.emit(name, sc)

                if self.is_capturing:
                    self.lib.interception_send(
                        self.context, device, ctypes.byref(stroke), 1
                    )
                    continue

                mapped = False
                if self.enabled:
                    # Проходим по всем кнопкам геймпада и их слотам
                    for gp_btn, keys in self.bindings.items():
                        if name in keys:
                            mapped = True

                            # Обработка кнопок
                            if gp_btn in GP_BUTTON_MAP:
                                btn_val = GP_BUTTON_MAP[gp_btn]
                                if is_down:
                                    gamepad.press_button(button=btn_val)
                                else:
                                    gamepad.release_button(button=btn_val)

                            # Обработка триггеров
                            elif gp_btn == "LT":
                                gamepad.left_trigger(value=255 if is_down else 0)
                            elif gp_btn == "RT":
                                gamepad.right_trigger(value=255 if is_down else 0)

                            # Обработка стиков
                            elif gp_btn.startswith("LS_") or gp_btn.startswith("RS_"):
                                val = 1 if is_down else 0
                                axes[gp_btn] = val

                                ls_x = (axes["LS_RIGHT"] - axes["LS_LEFT"]) * 32767
                                ls_y = (axes["LS_UP"] - axes["LS_DOWN"]) * 32767
                                gamepad.left_joystick(
                                    x_value=int(ls_x), y_value=int(ls_y)
                                )

                                rs_x = (axes["RS_RIGHT"] - axes["RS_LEFT"]) * 32767
                                rs_y = (axes["RS_UP"] - axes["RS_DOWN"]) * 32767
                                gamepad.right_joystick(
                                    x_value=int(rs_x), y_value=int(rs_y)
                                )

                    if mapped:
                        gamepad.update()

                # Если нажатие не было замаплено, отправляем его дальше в систему
                if not mapped:
                    self.lib.interception_send(
                        self.context, device, ctypes.byref(stroke), 1
                    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Официальное название в заголовке 
        self.setWindowTitle("Keyboard2Xinput UI")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ПЕРЕМЕННЫЕ ДЛЯ ПЕРЕМЕЩЕНИЯ ОКНА (Устраняем AttributeError) 
        self.resizing = False
        self.drag_allowed = True
        self.offset = None
        self.active_slot = None

        # Глобальный трекинг мыши 
        self.setMouseTracking(True)
        self.installEventFilter(self)

        self.bindings = {k: ["NONE"] * 6 for k in GP_MAP_KEYS}
        self.ui_buttons = {k: [] for k in GP_MAP_KEYS}

        self.thread = InterceptionThread()
        self.thread.key_signal.connect(self.on_key)

        self.setup_ui()
        self.enable_child_tracking(self.centralWidget())

        # ЗАГРУЗКА СИСТЕМНОГО КОНФИГА 
        config = configparser.ConfigParser()
        last_p = "Default"

        if os.path.exists(GLOBAL_CONFIG):
            config.read(GLOBAL_CONFIG, encoding="utf-8")
            last_p = config.get("Settings", "last_profile", fallback="Default")

        # Очищаем имя профиля от расширения для загрузки 
        last_p = last_p.replace(".ini", "")

        self.scan_profiles(last_p)
        self.load_config(last_p)

        self.resize(835, 900)
        self.load_window_state()

        is_autostart = config.getboolean("Settings", "autostart", fallback=False)
        self.autostart_cb.setChecked(is_autostart)

        if is_autostart:
            self.toggle_btn.setChecked(True)
            self.toggle()

        self.thread.start()

    def enable_child_tracking(self, widget):
        """Рекурсивно заставляем всех детей сообщать о движении мыши"""
        widget.setMouseTracking(True)
        widget.installEventFilter(self)
        for child in widget.findChildren(QWidget):
            child.setMouseTracking(True)
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Перехватываем движение мыши над любым виджетом окна"""
        if event.type() == QEvent.MouseMove:
            # Превращаем глобальные координаты в локальные относительно окна
            pos = self.mapFromGlobal(event.globalPosition().toPoint())
            self.update_cursor_appearance(pos)
        return super().eventFilter(obj, event)

    def update_cursor_appearance(self, pos):
        rect = self.rect()
        margin = 12

        right = pos.x() >= rect.width() - margin
        bottom = pos.y() >= rect.height() - margin
        left = pos.x() <= margin
        top = pos.y() <= margin

        new_cursor = Qt.ArrowCursor
        if (left and top) or (right and top):
            new_cursor = Qt.SizeFDiagCursor if left == top else Qt.SizeBDiagCursor
        elif (left and bottom) or (right and bottom):
            new_cursor = Qt.SizeBDiagCursor if left else Qt.SizeFDiagCursor
        elif left or right:
            new_cursor = Qt.SizeHorCursor
        elif bottom or top:  # Теперь и верх меняет курсор
            new_cursor = Qt.SizeVerCursor

        if self.cursor().shape() != new_cursor:
            self.setCursor(new_cursor)

    def load_window_state(self):
        """Восстановление размеров и позиции из конфига"""
        config = configparser.ConfigParser()
        if os.path.exists(DEFAULT_PROFILE):
            config.read(DEFAULT_PROFILE)
            if "Window" in config:
                geometry = config.get("Window", "geometry", fallback=None)
                if geometry:
                    print(f"[SYSTEM] Restoring geometry...")
                    self.restoreGeometry(bytes.fromhex(geometry))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.position()
            rect = self.rect()
            margin = 20  # Увеличим зону захвата для надёжности 

            self.resize_dir = None
            right = pos.x() >= rect.width() - margin
            bottom = pos.y() >= rect.height() - margin
            left = pos.x() <= margin
            top = pos.y() <= margin

            if right or bottom or left or top:
                self.resizing = True
                self.drag_allowed = False  # ЗАПРЕЩАЕМ ТАСКАТЬ 
                self.resize_dir = (left, right, bottom, top)
                self.start_geometry = self.geometry()
                self.start_pos_g = event.globalPosition().toPoint()
            else:
                self.resizing = False
                self.drag_allowed = True  # РАЗРЕШАЕМ ТАСКАТЬ 
                self.offset = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # 1. РЕСАЙЗ С ФИЗИЧЕСКОЙ БЛОКИРОВКОЙ ВЫЗОВА 
            if self.resizing:
                left, right, bottom, top = self.resize_dir
                p = event.globalPosition().toPoint()
                st = self.start_geometry

                fixed_right = st.x() + st.width()
                fixed_bottom = st.y() + st.height()

                # Считаем желаемые размеры 
                if left:
                    new_w = fixed_right - p.x()
                elif right:
                    new_w = p.x() - st.x()
                else:
                    new_w = st.width()

                if top:
                    new_h = fixed_bottom - p.y()
                elif bottom:
                    new_h = p.y() - st.y()
                else:
                    new_h = st.height()

                # ЖЁСТКАЯ КОРРЕКЦИЯ 
                final_w = max(835, new_w)
                final_h = max(450, new_h)

                # РАССЧИТЫВАЕМ X и Y 
                # Если тянем лево/верх, позиция зависит от ширины/высоты 
                final_x = fixed_right - final_w if left else st.x()
                final_y = fixed_bottom - final_h if top else st.y()

                # АТОМАРНАЯ ПРОВЕРКА: вызываем setGeometry только если 
                # текущий размер еще НЕ минимальный ИЛИ мышь движется в сторону расширения 
                current_geo = self.geometry()
                if (final_x, final_y, final_w, final_h) != (
                    current_geo.x(),
                    current_geo.y(),
                    current_geo.width(),
                    current_geo.height(),
                ):
                    # Дополнительный предохранитель для левой стороны 
                    if left and new_w < 835 and current_geo.width() <= 835:
                        return  # Просто игнорируем событие, не давая винде повода двинуть окно 
                    if top and new_h < 450 and current_geo.height() <= 450:
                        return

                    self.setGeometry(final_x, final_y, final_w, final_h)
                return

            # 2. ПЕРЕМЕЩЕНИЕ 
            elif self.drag_allowed and self.offset is not None:
                self.move(self.pos() + event.position().toPoint() - self.offset)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.offset = None

    def resizeEvent(self, event):
        """Пересчёт позиции уголка ресайза при изменении размеров """
        super().resizeEvent(event)
        if hasattr(self, "sizegrip"):
            # Всегда держим уголок в самом низу справа
            self.sizegrip.move(
                self.width() - self.sizegrip.width() - 5,
                self.height() - self.sizegrip.height() - 5,
            )

    def setup_ui(self):
        self.setStyleSheet(STYLE_SHEET)

        central = QWidget()
        central.setObjectName("Container")
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.centralWidget().setMouseTracking(True)

        # Убираем лишние отступы
        self.main_layout.setContentsMargins(3, 3, 3, 3)
        self.main_layout.setSpacing(0)

        # --- 0. ВЕРХНЯЯ ПОЛОСА (Title Bar) ---
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 5, 0, 5)

        self.title_label = QLabel("XBOX-Keypad")
        self.title_label.setStyleSheet(
            """
            QLabel {
                color: #B7C0C9; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px; 
                font-weight: bold;
                letter-spacing: 2px;
            }
        """
        )
        # Центрируем название 
        title_layout.addStretch()
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        self.main_layout.addWidget(title_container)

        # --- 1. ВЕРХНЯЯ ПАНЕЛЬ УПРАВЛЕНИЯ (Header) ---
        header = QFrame()
        header.setObjectName("Header")
        h_layout = QHBoxLayout(header)

        # Кнопка СТАРТ
        self.toggle_btn = QPushButton("START EMULATION")
        self.toggle_btn.setObjectName("run_btn_inactive")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedSize(140, 60)
        self.toggle_btn.clicked.connect(self.toggle)
        self.toggle_btn.setFocusPolicy(Qt.NoFocus)
        h_layout.addWidget(self.toggle_btn)

        # Секция профилей
        prof_section = QFrame()
        prof_section.setObjectName("ProfSection")
        p_layout = QHBoxLayout(prof_section)
        p_layout.setContentsMargins(10, 0, 10, 0)

        p_layout.addWidget(QLabel("PROFILE:"))
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumWidth(250)
        self.profile_combo.setFocusPolicy(Qt.NoFocus)
        p_layout.addWidget(self.profile_combo)

        self.add_btn = QPushButton("ADD")
        self.del_btn = QPushButton("DELETE")
        self.imp_btn = QPushButton("IMPORT")
        self.exp_btn = QPushButton("EXPORT")

        self.add_btn.clicked.connect(self.add_profile)
        self.del_btn.clicked.connect(self.delete_profile)
        self.imp_btn.clicked.connect(self.import_profile)
        self.exp_btn.clicked.connect(self.export_profile)
        self.profile_combo.currentTextChanged.connect(self.load_config)

        for btn in [self.add_btn, self.del_btn, self.imp_btn, self.exp_btn]:
            btn.setFocusPolicy(Qt.NoFocus)
            p_layout.addWidget(btn)

        h_layout.addWidget(prof_section, stretch=1)

        # Автостарт
        self.autostart_cb = QCheckBox("AUTO-START")
        self.autostart_cb.setObjectName("AutostartCheck")
        self.autostart_cb.setFocusPolicy(Qt.NoFocus)
        h_layout.addWidget(self.autostart_cb)

        # Управление окном
        window_controls = QFrame()
        wc_layout = QHBoxLayout(window_controls)
        wc_layout.setContentsMargins(5, 0, 0, 0)
        wc_layout.setSpacing(5)

        self.min_btn = QPushButton("_")
        self.close_btn = QPushButton("×")

        for btn, name in [(self.min_btn, "min_btn"), (self.close_btn, "close_btn")]:
            btn.setObjectName(name)
            btn.setFixedSize(35, 35)
            btn.setFocusPolicy(Qt.NoFocus)
            wc_layout.addWidget(btn)

        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        h_layout.addWidget(window_controls, alignment=Qt.AlignRight | Qt.AlignTop)

        # Добавляем хедер под названием
        self.main_layout.addWidget(header)

        # --- 2. ОБЛАСТЬ СКРОЛЛА ---
        self.scroll = QScrollArea()
        self.scroll.setObjectName("ScrollArea")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFocusPolicy(Qt.NoFocus)

        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("scrollAreaWidgetContents")
        self.scroll_content.setFocusPolicy(Qt.NoFocus)

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        for btn_name in GP_MAP_KEYS:
            row_frame = QFrame()
            row_frame.setObjectName(f"Row_{btn_name}")
            row_layout = QHBoxLayout(row_frame)

            lbl = QLabel()
            lbl.setFixedWidth(70)
            lbl.setAlignment(Qt.AlignCenter)
            setup_button_icon(lbl, btn_name)
            row_layout.addWidget(lbl)

            for col in range(6):
                slot_btn = QPushButton("NONE")
                slot_btn.setObjectName(f"Slot_{btn_name}_{col}")
                slot_btn.setFixedSize(75, 35)
                slot_btn.setFocusPolicy(Qt.NoFocus)

                slot_btn.clicked.connect(
                    lambda _, b=btn_name, i=col, o=slot_btn: self.start_cap(b, i, o)
                )
                slot_btn.setContextMenuPolicy(Qt.CustomContextMenu)
                slot_btn.customContextMenuRequested.connect(
                    lambda pos, b=btn_name, i=col, o=slot_btn: self.clear_slot(b, i, o)
                )

                row_layout.addWidget(slot_btn)
                self.ui_buttons[btn_name].append(slot_btn)

            self.scroll_layout.addWidget(row_frame)

        self.scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll)
        self.scan_profiles()

    def start_cap(self, gp_btn, idx, obj):
        if self.active_slot:
            old_gp, old_idx, old_obj = self.active_slot
            old_obj.setText(self.bindings[old_gp][old_idx])
            old_obj.setStyleSheet("")

        self.active_slot = (gp_btn, idx, obj)
        self.thread.is_capturing = True
        obj.setText("???")
        obj.setStyleSheet(
            """
            background-color: #0078d7; 
            color: white; 
            border: 1px solid #ffffff;
        """
        )

    def on_key(self, name, sc):
        if self.active_slot:
            gp_btn, idx, obj = self.active_slot
            name_up = name.upper()

            if name_up == "ESC":
                name_up = "NONE"

            self.bindings[gp_btn][idx] = name_up
            obj.setText(name_up)

            # --- ВОТ ЭТА СТРОКА СБРАСЫВАЕТ ВЫДЕЛЕНИЕ ---
            obj.setStyleSheet("")
            # ------------------------------------------

            self.thread.bindings = {k: v[:] for k, v in self.bindings.items()}
            self.thread.is_capturing = False
            self.save_config()
            self.active_slot = None

    def toggle(self):
        is_active = self.toggle_btn.isChecked()
        self.thread.enabled = is_active
        # Меняем ID для смены стиля (подхват из QSS)
        self.toggle_btn.setObjectName(
            "run_btn_active" if is_active else "run_btn_inactive"
        )
        self.toggle_btn.setText("STOP EMULATION" if is_active else "START EMULATION")
        self.toggle_btn.style().unpolish(self.toggle_btn)  # Форсим перерисовку стиля
        self.toggle_btn.style().polish(self.toggle_btn)

    def scan_profiles(self, target_profile=None):
        """Сканирует папку Profiles на наличие .ini файлов (без расширений)"""
        # Гарантируем наличие папки 
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
            print(f"[SYSTEM] Created directory: {PROFILES_DIR}")

        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()

        # Получаем имена файлов из папки Profiles без расширения .ini 
        # Используем f.stem для чистого имени без расширения 
        profiles = [f.stem for f in Path(PROFILES_DIR).glob("*.ini")]

        if not profiles:
            # Если папка пуста, создаём там стартовый профиль через системный путь 
            profiles = ["Default"]
            # ВАЖНО: save_config должен уметь работать с PROFILES_DIR 
            self.save_config("Default")

        self.profile_combo.addItems(profiles)

        # Если передан профиль для автовыбора 
        if target_profile:
            # Очищаем имя от путей и расширений на случай, если в конфиге записан полный путь 
            clean_name = os.path.basename(target_profile).replace(".ini", "")
            if clean_name in profiles:
                self.profile_combo.setCurrentText(clean_name)
            else:
                self.profile_combo.setCurrentIndex(0)

        self.profile_combo.blockSignals(False)
        print(f"[SYSTEM] Profiles in '{PROFILES_DIR}': {profiles}")

    def load_config(self, profile_name=None):
        """Загрузка биндов из папки Profiles и системных настроек из корня"""
        # 0. ОПРЕДЕЛЯЕМ ПУТИ 
        # Глобальный конфиг для геометрии окна (в корне)
        GLOBAL_CONFIG = "System_Config.ini"

        if profile_name is None or not isinstance(profile_name, str):
            profile_name = self.profile_combo.currentText()

        if not profile_name.lower().endswith(".ini"):
            profile_name += ".ini"

        # Путь к игровому профилю в папке Profiles 
        full_path = os.path.join(PROFILES_DIR, profile_name)

        # 1. Сначала подгружаем геометрию окна из GLOBAL_CONFIG (config.ini) 
        if os.path.exists(GLOBAL_CONFIG):
            sys_config = configparser.ConfigParser()
            sys_config.read(GLOBAL_CONFIG, encoding="utf-8")
            if "Window" in sys_config:
                geometry = sys_config.get("Window", "geometry", fallback=None)
                if geometry:
                    self.restoreGeometry(bytes.fromhex(geometry))
                    print(f"[SYSTEM] Window geometry restored from {GLOBAL_CONFIG}")

        # 2. Теперь загружаем бинды из файла в папке Profiles 
        if os.path.exists(full_path):
            config = configparser.ConfigParser()
            config.read(full_path, encoding="utf-8")
            if "Bindings" in config:
                for gp_btn, val in config["Bindings"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.bindings:
                        keys = [k.strip().upper() for k in val.split(",")]
                        for i in range(min(len(keys), 6)):
                            self.bindings[gp_btn_up][i] = keys[i]
                            self.ui_buttons[gp_btn_up][i].setText(keys[i])

            self.thread.bindings = {k: v[:] for k, v in self.bindings.items()}
            print(f"[SYSTEM] Profile loaded: {full_path}")

    def save_config(self, filename=None):
        """Сохранение биндингов строго в папку Profiles"""
        if filename is None:
            filename = self.profile_combo.currentText()

        if not filename:
            filename = "Default.ini"

        if not filename.lower().endswith(".ini"):
            filename += ".ini"

        # Имя файла может прийти как с путём, так и без — берём только хвост
        base_name = os.path.basename(filename)
        full_path = os.path.join(PROFILES_DIR, base_name)

        config = configparser.ConfigParser()
        config["Bindings"] = {k: ",".join(v) for k, v in self.bindings.items()}

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                config.write(f)
            print(f"[SYSTEM] Config saved to: {full_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save {full_path}: {e}")

    def add_profile(self):
        """Создание профиля через наш личный тёмный диалог"""
        dialog = CustomInputDialog("New Profile", "Имя нового профиля:", self)

        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_value()
            if name:
                filename = f"{name}.ini" if not name.endswith(".ini") else name
                if not os.path.exists(filename):
                    self.save_config(filename)
                    self.scan_profiles(filename)
                    print(f"[SYSTEM] Profile '{filename}' created.")
                else:
                    print(f"[ERROR] Profile '{filename}' already exists.")

    def delete_profile(self):
        current = self.profile_combo.currentText()
        if current == DEFAULT_PROFILE:
            return

        confirm = QMessageBox(self)
        # УБИРАЕМ СИСТЕМНУЮ РАМКУ (Заголовок Windows) 
        confirm.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        confirm.setWindowTitle("Подтверждение")
        confirm.setText(f"Delete profile {current}?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setIcon(QMessageBox.NoIcon)

        # Немного подправим отступы, чтобы текст не лип к краям без рамки 
        confirm.setStyleSheet(
            STYLE_SHEET
            + """
            QMessageBox {
                background-color: #1a1a1a;
                border: 2px solid #ff4444;
            }
            QLabel {
                color: #ff4444;
                font-weight: bold;
                font-size: 15px;
                padding: 20px;
            }
            QPushButton {
                background-color: #333333;
                color: white;
                border: 1px solid #ff4444;
                border-radius: 4px;
                padding: 6px 20px;
                margin-bottom: 10px;
                min-width: 80px;
                font-weight: bold;
                outline: none; /* Убирает пунктирную рамку фокуса  */
            }
            /* Убираем специфическую подсветку кнопок по умолчанию  */
            QPushButton:default, QPushButton:focus {
                border: 1px solid #ff4444; 
            }
            QPushButton:hover {
                background-color: #ff4444;
                color: white;
            }
        """
        )

        if confirm.exec() == QMessageBox.Yes:
            try:
                full_path = os.path.join(PROFILES_DIR, current)
                if os.path.exists(full_path):
                    os.remove(full_path)
                    self.scan_profiles()
            except Exception as e:
                print(f"[ERROR] {e}")

    def import_profile(self):
        """Копирование внешнего .ini файла в папку программы"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать конфиг", "", "INI Files (*.ini)"
        )
        if file_path:
            shutil.copy(file_path, os.getcwd())  # Копируем в рабочую директорию
            self.scan_profiles()

    def export_profile(self):
        """Сохранение текущего профиля в выбранное место"""
        current = self.profile_combo.currentText()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт профиля", current, "INI Files (*.ini)"
        )
        if save_path:
            shutil.copy(current, save_path)

    def clear_slot(self, gp_btn, idx, obj):
        """Очистка слота по правому клику мыши"""
        self.bindings[gp_btn][idx] = "NONE"
        obj.setText("NONE")
        obj.setStyleSheet("")  # Сбрасываем стили, если кнопка была в режиме захвата

        # Обновляем биндинги в потоке
        self.thread.bindings = {k: v[:] for k, v in self.bindings.items()}
        self.save_config()

        # Если очистили тот слот, который сейчас захватывался
        if self.active_slot and self.active_slot[2] == obj:
            self.thread.is_capturing = False
            self.active_slot = None

    def closeEvent(self, event):
        # 1. СРАЗУ ГАСИМ ДРАЙВЕР 
        self.thread.enabled = False
        print("[SYSTEM] Driver disabled immediately.")

        # 2. Теперь сохраняем системные настройки в config.ini (вместо Default.ini) 
        GLOBAL_CONFIG = "System_Config.ini"
        config = configparser.ConfigParser()

        if os.path.exists(GLOBAL_CONFIG):
            sys_config = configparser.ConfigParser()
            sys_config.read(GLOBAL_CONFIG, encoding="utf-8")

        if "Settings" not in config:
            config.add_section("Settings")
        if "Window" not in config:
            config.add_section("Window")

        # Записываем системные данные 
        config.set(
            "Settings", "last_profile", self.profile_combo.currentText() + ".ini"
        )
        config.set("Settings", "autostart", str(self.autostart_cb.isChecked()))
        config.set("Window", "geometry", self.saveGeometry().toHex().data().decode())

        # Биндинги текущего профиля (дублируем в config.ini для сохранности) 
        config["Bindings"] = {k: ",".join(v) for k, v in self.bindings.items()}

        # СОХРАНЯЕМ В КОРНЕВОЙ config.ini 
        with open(GLOBAL_CONFIG, "w", encoding="utf-8") as f:
            config.write(f)

        # 3. Дополнительно сохраняем в файл профиля внутри папки Profiles 
        # Чтобы изменения не пропали из самой папки профилей
        current_profile = self.profile_combo.currentText()
        if current_profile:
            self.save_config(current_profile)

        print(f"[SYSTEM] Settings saved to {GLOBAL_CONFIG}. Exiting...")
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
