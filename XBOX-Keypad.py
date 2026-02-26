import os
import sys
import ctypes
import time
import threading
from ctypes import CDLL


def resource_path(relative_path):
    """Получает абсолютный путь к ресурсам, работает и для dev, и для PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


lib = CDLL(resource_path("interception.dll"))
import configparser
import shutil
from pathlib import Path
import vgamepad as vg
from pathlib import Path
from PySide6.QtCore import (
    QThread,
    Qt,
    QTimer,
    Signal,
    QEvent,
    QPoint,
    QRect,
    QSize,
    QTimer,
)
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
    QMenu,
    QSystemTrayIcon,
)


def get_stylesheet(primary="#0078d7", secondary="#e74c3c"):
    """Динамически генерирует таблицу стилей на основе выбранных цветов"""
    p_color = QColor(primary)
    s_color = QColor(secondary)

    # Расчет вспомогательных оттенков
    p_hover = p_color.lighter(130).name()  # Яркий для наведения (был #4db3ff)
    p_active_bg = p_color.darker(300).name()  # Темный фон активных кнопок (был #001220)
    p_checked_hover = p_color.darker(
        200
    ).name()  # Фон при наведении на активную (был #002244)
    p_border_checked = p_color.name()  # Рамка активной

    s_hover = s_color.lighter(130).name()  # Яркий для наведения (был #ff7070)
    s_active_bg = s_color.darker(300).name()  # Темный фон активных (был #2D1A1A)

    return f"""
/* Основное окно и фон */
QMainWindow, QWidget#Container, QWidget#scrollAreaWidgetContents {{ 
    background-color: #0A0A0A; 
}}

#Container {{
    background-color: #121212;
    border: 2px solid {primary}; /* Основной акцент  */
    border-radius: 10px;       
}}

QFrame#Header {{
    border-bottom: 1px solid #1A1A1A;
    background-color: #0A0A0A;
}}

QPushButton#min_btn, QPushButton#close_btn {{
    background-color: transparent;
    border: 1px solid #333;
    color: #666;
    font-size: 16px;
    font-weight: bold;
}}
QPushButton#min_btn:hover {{
    color: {primary};
    border-color: {primary};
}}
QPushButton#close_btn:hover {{
    color: {secondary};
    border-color: {secondary};
}}

/* Скролл-зона */
QScrollArea#ScrollArea {{
    border: none;
    background-color: #0A0A0A;
}}

/* Кастомный скроллбар */
QScrollBar:vertical {{
    border: none;
    background: #0A0A0A;
    width: 8px;
    margin-right: 2px;
}}
QScrollBar::handle:vertical {{
    background: #2A2A2A;
    min-height: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{ background: #3A3A3A; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}

/* Секция профилей */
QFrame#ProfSection {{ 
    background-color: #1A1A1A; 
    border: 1px solid #333; 
    border-radius: 6px; 
    padding: 2px;
}}

QFrame#ProfSection QLabel {{
    color: #C0C0C0;
    font-weight: bold;
    margin-left: 5px;
}}

/* Выпадающий список */
QComboBox {{ 
    background-color: #252525; 
    color: #FFF; 
    border: 1px solid #444; 
    border-radius: 4px; 
    padding: 5px 10px; 
    min-width: 130px;
    min-height: 10px;
}}
QComboBox:hover {{ border-color: {primary}; }}
QComboBox QAbstractItemView {{ 
    background-color: #121212; 
    color: #FFFFFF; 
    selection-background-color: {primary}; 
    selection-color: #FFFFFF;
    border: 1px solid {primary};
    outline: none;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px;
}}

QComboBox QAbstractItemView::item:selected {{
    background-color: {primary};
    color: #FFFFFF;
}}

/* Фикс для выпадающего списка (убрана стрелка по просьбе пользователя) */
QComboBox::drop-down {{
    border: none;
}}
QComboBox::down-arrow {{
    image: none;
}}


/* Кнопки профилей (ADD, DELETE и т.д.) */
QFrame#ProfSection QPushButton {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    min-width: 65px;
    padding: 5px;
    font-size: 10px;
}}

QFrame#ProfSection QPushButton:hover {{ border-color: {primary}; color: #FFF; }}
QFrame#ProfSection QPushButton:pressed {{ background-color: {primary}; color: #FFF; }}

/* Убираем пунктирную рамку фокуса со всех кнопок */
QPushButton {{ outline: none; }}
QPushButton:focus {{ border: 1px solid #333; }}

/* Кнопка запуска */
QPushButton#run_btn_inactive {{ 
    background-color: #1A1A1A; 
    color: {primary}; 
    font-weight: bold; 
    border: 2px solid {primary}; 
    border-radius: 6px; 
}}

QPushButton#SettingsBtn {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}}
QPushButton#SettingsBtn:hover {{
    border-color: {primary};
    color: {primary};
}}

QCheckBox {{
    color: #CCCCCC;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    background-color: #1A1A1A;
    border: 2px solid #333;
    border-radius: 4px;
}}
QCheckBox::indicator:checked {{
    background-color: {primary};
    border: 2px solid {primary};
}}
QCheckBox::indicator:hover {{
    border: 2px solid {primary};
}}

QPushButton#run_btn_active {{ 
    background-color: #1A1A1A; 
    color: {secondary}; 
    font-weight: bold; 
    border: 2px solid {secondary}; 
    border-radius: 6px; 
}}

/* Строки биндинга */
QFrame[objectName^="Row_"] {{
    background-color: #121212;
    border: 1px solid #1A1A1A;
    border-radius: 8px;
    margin: 2px 5px;
}}

QFrame[objectName^="Row_"] QLabel {{
    color: #C0C0C0;
    font-family: "Segoe UI";
    font-weight: bold;
    font-size: 13px;
    border: none;
}}

/* Кнопки-слоты */
QPushButton[objectName^="Slot_"] {{
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 12px;
    min-height: 30px;
}}
QPushButton[objectName^="Slot_"]:hover {{
    border-color: {primary};
    background-color: #252525;
    color: {p_hover};
}}
QPushButton[objectName^="Slot_"]:pressed {{
    background-color: {primary};
    color: #FFFFFF;
}}

/* Состояние при захвате клавиши */
QPushButton[objectName^="Slot_"][capturing="true"] {{
    background-color: {primary};
    color: #FFFFFF;
    border: 1px solid #FFFFFF;
}}


/* Эффект наведения, когда кнопка КРАСНАЯ (выключена) */
#run_btn_inactive:hover {{
    background-color: {p_active_bg}; 
    border-color: {p_hover};     
    color: {p_hover};            
}}

/* Эффект наведения, когда кнопка КРАСНАЯ (активна) */
#run_btn_active:hover {{
    background-color: {s_active_bg}; 
    border-color: {s_hover};     
    color: {s_hover};            
}}

QPushButton[objectName^="ToggleBtn_"], QPushButton[objectName^="TurboBtn_"], QPushButton[objectName^="DelayBtn_"] {{
    background-color: #1A1A1A;
    color: #bababa;
    border: 1px solid #333;
    border-radius: 3px;
    font-size: 12px;
    font-weight: bold;
    padding: 2px;
}}

QPushButton[objectName^="ToggleBtn_"]:disabled, QPushButton[objectName^="TurboBtn_"]:disabled, QPushButton[objectName^="DelayBtn_"]:disabled {{
    background-color: #0d0d0d;
    color: #444;
    border: 1px solid #222;
}}

/* Hover эффект для неактивных кнопок */
QPushButton[objectName^="ToggleBtn_"]:hover:!checked, 
QPushButton[objectName^="TurboBtn_"]:hover:!checked,
QPushButton[objectName^="DelayBtn_"]:hover:!checked {{
    border-color: {primary};
    background-color: #252525;
    color: {p_hover};
}}

/* Hover эффект для активных кнопок (checked) */
QPushButton[objectName^="ToggleBtn_"]:hover:checked,
QPushButton[objectName^="TurboBtn_"]:hover:checked,
QPushButton[objectName^="DelayBtn_"]:hover:checked {{
    background-color: {p_checked_hover};
    border-color: {p_hover};
    color: #ffffff;
}}

/* Pressed эффект */
QPushButton[objectName^="ToggleBtn_"]:pressed,
QPushButton[objectName^="TurboBtn_"]:pressed,
QPushButton[objectName^="DelayBtn_"]:pressed {{
    background-color: {primary};
    color: #FFFFFF;
}}

/* Активный Toggle */
QPushButton[objectName^="ToggleBtn_"]:checked {{
    background-color: {p_active_bg};
    color: {p_hover};
    border: 1px solid {p_hover};
}}

/* Активный Turbo */
QPushButton[objectName^="TurboBtn_"]:checked {{
    background-color: {p_active_bg};
    color: {p_hover};
    border: 1px solid {p_hover};
}}

/* Активный Delay */
QPushButton[objectName^="DelayBtn_"]:checked {{
    background-color: {p_active_bg};
    color: {p_hover};
    border: 1px solid {p_hover};
}}

/* Текстовые поля Turbo и Delay */
QLineEdit[objectName^="TurboInput_"], QLineEdit[objectName^="DelayInput_"] {{
    background-color: #0d0d0d;
    color: #444;
    border: 1px solid #222;
    border-radius: 3px;
    font-size: 12px;
    padding: 2px;
}}

QLineEdit[objectName^="TurboInput_"]:enabled, QLineEdit[objectName^="DelayInput_"]:enabled {{
    background-color: #1A1A1A;
    color: #888;
    border: 1px solid #333;
}}

QLineEdit[objectName^="TurboInput_"]:focus, QLineEdit[objectName^="DelayInput_"]:focus {{
    border: 1px solid {p_hover};
    color: #ffffff;
}}

/* Активное состояние (когда режим включен) */
QLineEdit[objectName^="TurboInput_"][active="true"], QLineEdit[objectName^="DelayInput_"][active="true"] {{
    background-color: {p_active_bg};
    border: 1px solid {p_hover};
    color: {p_hover};
}}

/* Стилизация диалогов (Settings, Input и т.д.) */
QDialog {{
    background-color: #121212;
    border: 2px solid {primary};
    border-radius: 10px;
}}

QDialog QLabel {{
    color: #FFFFFF;
    background: transparent;
}}

QDialog QLabel#SettingsTitle {{
    color: {primary};
    font-weight: bold;
    font-size: 16px;
}}


QDialog QPushButton {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px 15px;
    font-size: 12px;
}}

QDialog QPushButton:hover {{
    border-color: {primary};
    color: {primary};
    background-color: {p_active_bg};
}}

QDialog QLineEdit {{
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: {primary};
}}

QDialog QLineEdit:focus {{
    border-color: {primary};
}}

/* Специфические кнопки в настройках цветов */
QPushButton#PrimaryPickBtn:hover {{
    border-color: {primary};
    color: {p_hover};
    background-color: {p_active_bg};
}}

QPushButton#SecondaryPickBtn:hover {{
    border-color: {secondary};
    color: {s_hover};
    background-color: {s_active_bg};
}}

QPushButton#SaveCloseBtn {{
    background-color: #1A1A1A;
    color: white;
    border: 1px solid #333;
    font-weight: bold;
}}

QPushButton#SaveCloseBtn:hover {{
    background-color: {p_active_bg};
    border-color: {primary};
    color: {p_hover};
}}

/* QMessageBox (системные уведомления) */
QMessageBox {{
    background-color: #121212;
    border: 2px solid {secondary};
}}

QMessageBox QLabel {{
    color: white;
}}

/* QColorDialog (выбор цвета) */
QColorDialog {{
    background-color: #121212;
    color: white;
}}

QColorDialog QPushButton {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 5px;
}}
"""


PROJECT_NAME = "XBOX-Keypad"
VERSION = "v2.2"
APP_ICON = resource_path("XBOX-Keypad.ico")

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
        self.setFixedWidth(400)

        # Получаем цвета от родителя или ставим дефолт
        p_color = (
            parent.primary_color if hasattr(parent, "primary_color") else "#0078D7"
        )
        s_color = (
            parent.secondary_color if hasattr(parent, "secondary_color") else "#E74C3C"
        )

        # Устанавливаем общий стиль
        self.setStyleSheet(get_stylesheet(p_color, s_color))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Заголовок
        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet(
            f"font-weight: bold; color: {p_color}; font-size: 16px;"
        )
        layout.addWidget(title_lbl, alignment=Qt.AlignCenter)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("font-size: 13px; color: #BBB;")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setMinimumHeight(35)
        self.input_field.setPlaceholderText("Enter name...")
        layout.addWidget(self.input_field)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("CONFIRM")
        self.cancel_btn = QPushButton("CANCEL")

        # Кнопки наследуют стиль из get_stylesheet(p_color, s_color)
        self.ok_btn.setObjectName("ConfirmBtn")

        for b in [self.ok_btn, self.cancel_btn]:
            b.setFocusPolicy(Qt.NoFocus)
            b.setCursor(Qt.PointingHandCursor)
            b.setMinimumHeight(35)
            btn_layout.addWidget(b)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        layout.addLayout(btn_layout)

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
    sig_turbo_active = Signal(
        str, bool, int
    )  # Сигнал для активации/деактивации турбо в Main: btn, active, slot_idx
    sig_delay_request = Signal(str, int, bool)

    def __init__(self):
        super().__init__()
        self.is_running, self.enabled = True, False
        self.is_capturing = False
        self.is_typing = False  # Флаг: печатает ли пользователь в поле ввода
        self.gamepad = None  # Ссылка на геймпад для Turbo-инъекций
        self.bindings = {k: ["NONE"] * 6 for k in GP_MAP_KEYS}
        self.toggles = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.turbos = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.delays = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.turbo_active_state = {}  # {(gp_btn, slot_idx): bool} - активен ли турбо
        self.lock = threading.Lock()
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

    def trigger_logical_action(self, gp_btn, slot_idx, is_down):
        is_toggle = self.toggles[gp_btn][slot_idx]
        is_turbo = self.turbos[gp_btn][slot_idx]
        should_press = False

        if is_turbo:
            if is_down:
                turbo_key = (gp_btn, slot_idx)
                current_state = self.turbo_active_state.get(turbo_key, False)
                new_state = not current_state
                self.turbo_active_state[turbo_key] = new_state
                self.sig_turbo_active.emit(gp_btn, new_state, slot_idx)
                if not new_state:
                    with self.lock:
                        if gp_btn in GP_BUTTON_MAP:
                            self.gamepad.release_button(button=GP_BUTTON_MAP[gp_btn])
                        elif gp_btn in ["LT", "RT"]:
                            if gp_btn == "LT":
                                self.gamepad.left_trigger(value=0)
                            else:
                                self.gamepad.right_trigger(value=0)
                        self.gamepad.update()
            return
        elif is_toggle:
            if is_down:
                self.gp_state[gp_btn] = not self.gp_state[gp_btn]
                should_press = self.gp_state[gp_btn]
            else:
                should_press = self.gp_state[gp_btn]
        else:
            should_press = is_down
            self.gp_state[gp_btn] = is_down

        if gp_btn in GP_BUTTON_MAP:
            btn_val = GP_BUTTON_MAP[gp_btn]
            with self.lock:
                if should_press:
                    self.gamepad.press_button(button=btn_val)
                else:
                    self.gamepad.release_button(button=btn_val)
        elif gp_btn == "LT":
            with self.lock:
                self.gamepad.left_trigger(value=255 if should_press else 0)
        elif gp_btn == "RT":
            with self.lock:
                self.gamepad.right_trigger(value=255 if should_press else 0)
        elif gp_btn.startswith("LS_") or gp_btn.startswith("RS_"):
            val = 1 if should_press else 0
            self.axes[gp_btn] = val
            ls_x = (self.axes["LS_RIGHT"] - self.axes["LS_LEFT"]) * 32767
            ls_y = (self.axes["LS_UP"] - self.axes["LS_DOWN"]) * 32767
            with self.lock:
                self.gamepad.left_joystick(x_value=int(ls_x), y_value=int(ls_y))
            rs_x = (self.axes["RS_RIGHT"] - self.axes["RS_LEFT"]) * 32767
            rs_y = (self.axes["RS_UP"] - self.axes["RS_DOWN"]) * 32767
            with self.lock:
                self.gamepad.right_joystick(x_value=int(rs_x), y_value=int(rs_y))
                
        with self.lock:
            self.gamepad.update()

    def run(self):
        if not self.context:
            return
        stroke = Stroke()

        try:
            self.gamepad = vg.VX360Gamepad()
            print("[SYSTEM] Virtual Xbox 360 Controller connected.")
        except Exception as e:
            print(f"[ERROR] Gamepad initialization failed: {e}")
            return

        # Храним состояние осей
        self.axes = {
            "LS_UP": 0,
            "LS_DOWN": 0,
            "LS_LEFT": 0,
            "LS_RIGHT": 0,
            "RS_UP": 0,
            "RS_DOWN": 0,
            "RS_LEFT": 0,
            "RS_RIGHT": 0,
        }

        # Храним ФИЗИЧЕСКОЕ состояние кнопок геймпада (для Toggle Mode)
        # True = кнопка сейчас нажата (виртуально)
        self.gp_state = {k: False for k in GP_MAP_KEYS}

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
                if self.enabled and not self.is_typing:
                    # Проходим по всем кнопкам геймпада и их слотам
                    for gp_btn, keys in self.bindings.items():
                        if name in keys:
                            mapped = True

                            # Определяем индекс слота для текущей клавиши
                            try:
                                slot_idx = keys.index(name)
                                is_delay = self.delays[gp_btn][slot_idx]
                            except ValueError:
                                continue

                            if is_delay:
                                self.sig_delay_request.emit(gp_btn, slot_idx, is_down)
                                continue

                            self.trigger_logical_action(gp_btn, slot_idx, is_down)

                # Если нажатие не было замаплено, отправляем его дальше в систему
                if not mapped:
                    self.lib.interception_send(
                        self.context, device, ctypes.byref(stroke), 1
                    )

    def inject_turbo(self, active_keys, turbo_state):
        """Метод для внешнего вызова (из таймера Qt)"""
        if not self.gamepad:
            return

        need_update = False
        for gp_btn in active_keys:
            need_update = True
            is_pressed = turbo_state

            if gp_btn in GP_BUTTON_MAP:
                if is_pressed:
                    self.gamepad.press_button(button=GP_BUTTON_MAP[gp_btn])
                else:
                    self.gamepad.release_button(button=GP_BUTTON_MAP[gp_btn])
            elif gp_btn == "LT":
                self.gamepad.left_trigger(value=255 if is_pressed else 0)
            elif gp_btn == "RT":
                self.gamepad.right_trigger(value=255 if is_pressed else 0)

        if need_update:
            self.gamepad.update()

    def stop(self):
        """Принудительная остановка потока"""
        self.is_running = False
        self.enabled = False
        if self.context:
            # Это «выбивает» блокировку interception_wait
            self.lib.interception_destroy_context(self.context)
            self.context = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Официальное название в заголовке
        self.setWindowTitle(PROJECT_NAME)
        if os.path.exists(APP_ICON):
            self.setWindowIcon(QIcon(APP_ICON))
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
        self.bindings = {k: ["NONE"] * 6 for k in GP_MAP_KEYS}
        self.toggles = {
            k: [False] * 6 for k in GP_MAP_KEYS
        }  # Новая структура для то,гглов
        self.turbos = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.turbo_intervals_map = {
            k: [0.1] * 6 for k in GP_MAP_KEYS
        }  # Интервалы (сек)
        
        self.delays = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.delay_intervals_map = {k: [0.1] * 6 for k in GP_MAP_KEYS}

        # --- ЦВЕТОВАЯ СХЕМА (v2.0) ---
        self.primary_color = "#0078D7"
        self.secondary_color = "#E74C3C"

        self.ui_buttons = {k: [] for k in GP_MAP_KEYS}
        self.ui_toggles = {k: [] for k in GP_MAP_KEYS}
        self.ui_turbos = {k: [] for k in GP_MAP_KEYS}
        self.ui_turbo_inputs = {k: [] for k in GP_MAP_KEYS}  # Поля ввода скорости
        self.ui_delays = {k: [] for k in GP_MAP_KEYS}
        self.ui_delay_inputs = {k: [] for k in GP_MAP_KEYS}
        self.delay_timers = {}
        self.delay_fired_state = {}

        self.active_t_session = {}
        self.turbo_timer = QTimer(self)
        self.turbo_timer.timeout.connect(self.on_turbo_tick)

        # Таймер для сглаживания предпросмотра цветов (убираем лаги)
        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(30)  # 30мс достаточно для плавности без лагов
        self.turbo_state = False  # Переключатель вкл/выкл для мигания
        self.active_turbo_keys = (
            set()
        )  # Множество активных сейчас турбо-кнопок (физически зажатых)

        self.thread = InterceptionThread()
        self.thread.key_signal.connect(self.on_key)
        self.thread.sig_turbo_active.connect(self.on_turbo_active)
        self.thread.sig_delay_request.connect(self.on_delay_request)

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

        self.resize(
            860, 900
        )  # Ширина увеличена с 835 до 860 для корректного отображения скроллбара
        self.load_window_state()

        is_autostart = config.getboolean("Settings", "autostart", fallback=False)
        self.autostart_cb.setChecked(is_autostart)

        # Загружаем настройку сворачивания
        if os.path.exists(GLOBAL_CONFIG):
            app_cfg = configparser.ConfigParser()
            app_cfg.read(GLOBAL_CONFIG, encoding="utf-8")
            is_hide_to_tray = app_cfg.getboolean("Appearance", "hide_to_tray", fallback=False)
            self.hide_to_tray_cb.setChecked(is_hide_to_tray)

        if is_autostart:
            self.toggle_btn.setChecked(True)
            self.toggle()

        self.thread.start()

        # --- ОТСЛЕЖИВАНИЕ ФОКУСА (для корректной печати в полях ввода) ---
        QApplication.instance().focusChanged.connect(self.on_focus_changed)

        # --- НАСТРОЙКА ТРЕЯ ---
        self.tray_icon = QSystemTrayIcon(self)

        # Сначала пробуем иконку окна, если она пустая — лезем за файлом напрямую
        current_icon = self.windowIcon()
        if current_icon.isNull() and os.path.exists(APP_ICON):
            current_icon = QIcon(APP_ICON)

        # Если и файл не помог (например, его нет), ставим системную заглушку
        if current_icon.isNull():
            from PySide6.QtWidgets import QStyle

            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        else:
            self.tray_icon.setIcon(current_icon)

        tray_menu = QMenu()
        tray_menu.setStyleSheet(
            """
            QMenu {
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #0078d7;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 25px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #333333;
                margin: 5px 10px;
            }
        """
        )

        from PySide6.QtWidgets import QWidgetAction
        
        self.tray_action_toggle = QWidgetAction(self)
        self.tray_btn_toggle = QPushButton("START EMULATION")
        self.tray_btn_toggle.setObjectName("run_btn_inactive")
        self.tray_btn_toggle.setCursor(Qt.PointingHandCursor)
        self.tray_btn_toggle.setMinimumSize(140, 40)
        # Применяем общий стиль + отступы, чтобы кнопка реагировала на темы
        self.tray_btn_toggle.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color) + "\nQPushButton { margin: 4px 10px; padding: 0 10px; }")
        
        def on_tray_btn_click():
            if self.toggle_btn:
                self.toggle_btn.click()
            tray_menu.hide()
            
        self.tray_btn_toggle.clicked.connect(on_tray_btn_click)
        self.tray_action_toggle.setDefaultWidget(self.tray_btn_toggle)
        tray_menu.addAction(self.tray_action_toggle)

        tray_menu.addSeparator()

        show_action = tray_menu.addAction("Show app")
        show_action.triggered.connect(self.showNormal)

        tray_menu.addSeparator()  # Можно добавить разделитель для красоты

        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(self.manual_exit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def enable_child_tracking(self, widget):
        """Рекурсивно заставляем всех детей сообщать о движении мыши"""
        widget.setMouseTracking(True)
        widget.installEventFilter(self)
        for child in widget.findChildren(QWidget):
            child.setMouseTracking(True)
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Перехватываем всё для абсолютного приоритета ресайза"""
        if event.type() == QEvent.MouseMove:
            global_pos = event.globalPosition().toPoint()
            local_pos = self.mapFromGlobal(global_pos)

            if self.resizing:
                self._handle_move(global_pos)
                return True

            self.update_cursor_appearance(local_pos)

        elif event.type() == QEvent.MouseButtonPress:
            # 1. Снимаем фокус ТОЛЬКО если кликнули НЕ по полю ввода
            global_pos = event.globalPosition().toPoint()
            target = self.childAt(self.mapFromGlobal(global_pos))

            if not isinstance(target, QLineEdit):
                focused_widget = QApplication.focusWidget()
                if isinstance(focused_widget, QLineEdit):
                    focused_widget.clearFocus()

            # 2. Если в зоне ресайза - блокируем детей
            local_pos = self.mapFromGlobal(global_pos)
            if self._check_resize_zone(local_pos):
                self._handle_press(global_pos)
                return True

        elif event.type() == QEvent.MouseButtonRelease:
            if self.resizing:
                self.resizing = False
                self.offset = None
                return True

        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._handle_press(event.globalPosition().toPoint())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self._handle_move(event.globalPosition().toPoint())
        super().mouseMoveEvent(event)

    def on_focus_changed(self, old, new):
        """Когда пользователь переходит в поле ввода, отключаем перехват клавиш драйвером"""
        if isinstance(new, QLineEdit):
            self.thread.is_typing = True
        else:
            self.thread.is_typing = False

    def _check_resize_zone(self, local_pos):
        """Простая проверка: находится ли точка в 5px зоне ресайза"""
        rect = self.rect()
        m = 5
        return (
            local_pos.x() <= m
            or local_pos.x() >= rect.width() - m
            or local_pos.y() <= m
            or local_pos.y() >= rect.height() - m
        )

    def _handle_press(self, global_pos):
        local_pos = self.mapFromGlobal(global_pos)
        rect = self.rect()
        m = 5

        left = local_pos.x() <= m
        right = local_pos.x() >= rect.width() - m
        top = local_pos.y() <= m
        bottom = local_pos.y() >= rect.height() - m

        if left or right or top or bottom:
            self.resizing = True
            self.drag_allowed = False
            self.resize_dir = (left, right, bottom, top)
            self.start_geometry = self.geometry()
            self.start_pos_g = global_pos
        else:
            self.resizing = False
            self.drag_allowed = True
            self.offset = local_pos

    def _handle_move(self, global_pos):
        if self.resizing:
            left, right, bottom, top = self.resize_dir
            p = global_pos
            st = self.start_geometry
            fixed_right = st.x() + st.width()
            fixed_bottom = st.y() + st.height()

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

            final_w = max(835, new_w)
            final_h = max(450, new_h)
            final_x = fixed_right - final_w if left else st.x()
            final_y = fixed_bottom - final_h if top else st.y()

            current_geo = self.geometry()
            if (final_x, final_y, final_w, final_h) != (
                current_geo.x(),
                current_geo.y(),
                current_geo.width(),
                current_geo.height(),
            ):
                if left and new_w < 835 and current_geo.width() <= 835:
                    return
                if top and new_h < 450 and current_geo.height() <= 450:
                    return
                self.setGeometry(final_x, final_y, final_w, final_h)
        elif self.drag_allowed and self.offset is not None:
            self.move(global_pos - self.offset)

    def update_cursor_appearance(self, local_pos):
        """Меняет курсор при наведении на края"""
        rect = self.rect()
        m = 5

        left = local_pos.x() <= m
        right = local_pos.x() >= rect.width() - m
        top = local_pos.y() <= m
        bottom = local_pos.y() >= rect.height() - m

        new_cursor = Qt.ArrowCursor
        if (left and top) or (right and top):
            new_cursor = Qt.SizeFDiagCursor if left == top else Qt.SizeBDiagCursor
        elif (left and bottom) or (right and bottom):
            new_cursor = Qt.SizeBDiagCursor if left else Qt.SizeFDiagCursor
        elif left or right:
            new_cursor = Qt.SizeHorCursor
        elif bottom or top:
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

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.offset = None
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        """Пересчёт позиции уголка ресайза при изменении размеров"""
        super().resizeEvent(event)
        if hasattr(self, "sizegrip"):
            # Всегда держим уголок в самом низу справа
            self.sizegrip.move(
                self.width() - self.sizegrip.width() - 5,
                self.height() - self.sizegrip.height() - 5,
            )

    def on_tray_icon_activated(self, reason):
        """Разворачивание/сворачивание окна при клике по иконке в трее"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isMinimized() or not self.isVisible():
                self.showNormal()
                self.activateWindow()
                try:
                    import ctypes
                    ctypes.windll.user32.SetForegroundWindow(int(self.winId()))
                except Exception:
                    pass
            else:
                self.setWindowState(Qt.WindowMinimized)

    def force_minimize(self):
        """Принудительное сворачивание для безрамочного окна"""
        self.setWindowState(Qt.WindowMinimized)

    def changeEvent(self, event):
        """Ловим сворачивание — оставляем в таскбаре для нативного превью"""
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                hide_to_tray = hasattr(self, "hide_to_tray_cb") and self.hide_to_tray_cb.isChecked()
                if hide_to_tray:
                    # Полностью скрываем окно из таскбара (трей-онли)
                    self.hide()
                    if hasattr(self, "tray_icon"):
                        self.tray_icon.showMessage(
                            PROJECT_NAME,
                            "Программа свёрнута в трей",
                            QSystemTrayIcon.MessageIcon.Information,
                            1500,
                        )
                else:
                    # Остаёмся в таскбаре, DWM-превью работает
                    if hasattr(self, "tray_icon"):
                        self.tray_icon.showMessage(
                            PROJECT_NAME,
                            "Программа свёрнута",
                            QSystemTrayIcon.MessageIcon.Information,
                            1500,
                        )
        super().changeEvent(event)

    def setup_ui(self):
        self.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

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

        self.title_label = QLabel(PROJECT_NAME)
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

        # Блок AUTO-START + HIDE TO TRAY — вертикально
        checks_frame = QFrame()
        checks_layout = QVBoxLayout(checks_frame)
        checks_layout.setContentsMargins(0, 0, 0, 0)
        checks_layout.setSpacing(2)

        self.autostart_cb = QCheckBox("AUTO-START")
        self.autostart_cb.setObjectName("AutostartCheck")
        self.autostart_cb.setFocusPolicy(Qt.NoFocus)
        checks_layout.addWidget(self.autostart_cb)

        # Сворачивать в трей или в таскбар
        self.hide_to_tray_cb = QCheckBox("HIDE TO TRAY")
        self.hide_to_tray_cb.setObjectName("HideToTrayCheck")
        self.hide_to_tray_cb.setFocusPolicy(Qt.NoFocus)
        self.hide_to_tray_cb.setToolTip("При сворачивании: скрывать окно в трей (без превью) или оставлять в таскбаре (с превью)")
        self.hide_to_tray_cb.stateChanged.connect(self.save_appearance)
        checks_layout.addWidget(self.hide_to_tray_cb)

        h_layout.addWidget(checks_frame)

        # Кнопка НАСТРОЙКИ (Settings)
        self.settings_btn = QPushButton("SETTINGS")
        self.settings_btn.setObjectName("SettingsBtn")
        self.settings_btn.setFixedSize(90, 30)
        self.settings_btn.setFocusPolicy(Qt.NoFocus)
        self.settings_btn.clicked.connect(self.show_settings)
        h_layout.addWidget(self.settings_btn)

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

        self.min_btn.clicked.connect(self.force_minimize)
        self.close_btn.clicked.connect(self.manual_exit)

        h_layout.addWidget(window_controls, alignment=Qt.AlignRight | Qt.AlignTop)

        # Добавляем хедер под названием
        self.main_layout.addWidget(header)

        # --- 2. ОБЛАСТЬ СКРОЛЛА ---
        self.scroll = QScrollArea()
        self.scroll.setObjectName("ScrollArea")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFocusPolicy(Qt.NoFocus)
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn
        )  # Принудительно показываем скроллбар

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
                # Создаем контейнер для слота и кнопок режимов
                slot_container = QWidget()
                slot_layout = QVBoxLayout(slot_container)
                slot_layout.setContentsMargins(0, 0, 0, 0)
                slot_layout.setSpacing(1)

                # 1. Верхняя панель: [ TURBO ] [ INPUT ]
                turbo_container = QWidget()
                turbo_layout = QHBoxLayout(turbo_container)
                turbo_layout.setContentsMargins(0, 0, 0, 0)
                turbo_layout.setSpacing(2)
                turbo_layout.setAlignment(Qt.AlignLeft)  # Выравниваем влево

                turbo_btn = QPushButton("TURBO")
                turbo_btn.setObjectName(f"TurboBtn_{btn_name}_{col}")
                turbo_btn.setCheckable(True)
                turbo_btn.setFocusPolicy(Qt.NoFocus)
                turbo_btn.setFixedSize(79, 24)
                turbo_btn.clicked.connect(
                    lambda checked, b=btn_name, i=col: self.update_turbo_state(
                        b, i, checked
                    )
                )

                # Поле ввода скорости (сек)
                turbo_input = QLineEdit("0")
                turbo_input.setObjectName(f"TurboInput_{btn_name}_{col}")
                turbo_input.setFixedSize(40, 24)
                turbo_input.setAlignment(Qt.AlignCenter)
                turbo_input.setEnabled(False)  # Изначально неактивно (вместо скрытия)
                # Стили применяются из STYLE_SHEET
                turbo_input.editingFinished.connect(
                    lambda b=btn_name, i=col: self.update_turbo_interval(b, i)
                )

                turbo_layout.addWidget(turbo_btn)
                turbo_layout.addWidget(turbo_input)

                # DELAY PANEL
                delay_container = QWidget()
                delay_layout = QHBoxLayout(delay_container)
                delay_layout.setContentsMargins(0, 0, 0, 0)
                delay_layout.setSpacing(2)
                delay_layout.setAlignment(Qt.AlignLeft)

                delay_btn = QPushButton("DELAY")
                delay_btn.setObjectName(f"DelayBtn_{btn_name}_{col}")
                delay_btn.setCheckable(True)
                delay_btn.setFocusPolicy(Qt.NoFocus)
                delay_btn.setFixedSize(79, 24)
                delay_btn.clicked.connect(
                    lambda checked, b=btn_name, i=col: self.update_delay_state(
                        b, i, checked
                    )
                )

                delay_input = QLineEdit("0.1")
                delay_input.setObjectName(f"DelayInput_{btn_name}_{col}")
                delay_input.setFixedSize(40, 24)
                delay_input.setAlignment(Qt.AlignCenter)
                delay_input.setEnabled(False)
                delay_input.editingFinished.connect(
                    lambda b=btn_name, i=col: self.update_delay_interval(b, i)
                )

                delay_layout.addWidget(delay_btn)
                delay_layout.addWidget(delay_input)

                # 2. Основная кнопка слота
                slot_btn = QPushButton("NONE")
                slot_btn.setObjectName(f"Slot_{btn_name}_{col}")
                slot_btn.setFixedSize(79, 30)
                slot_btn.setFocusPolicy(Qt.NoFocus)

                slot_btn.clicked.connect(
                    lambda _, b=btn_name, i=col, o=slot_btn: self.start_cap(b, i, o)
                )
                slot_btn.setContextMenuPolicy(Qt.CustomContextMenu)
                slot_btn.customContextMenuRequested.connect(
                    lambda pos, b=btn_name, i=col, o=slot_btn: self.clear_slot(b, i, o)
                )

                # 3. Кнопка TOGGLE (под слотом)
                toggle_container = QWidget()
                toggle_layout = QHBoxLayout(toggle_container)
                toggle_layout.setContentsMargins(0, 0, 0, 0)
                toggle_layout.setSpacing(2)
                toggle_layout.setAlignment(Qt.AlignLeft)

                toggle_btn = QPushButton("TOGGLE")
                toggle_btn.setObjectName(f"ToggleBtn_{btn_name}_{col}")
                toggle_btn.setCheckable(True)
                toggle_btn.setFocusPolicy(Qt.NoFocus)
                toggle_btn.setFixedSize(79, 24)  # Высота 24px (по просьбе пользователя)
                toggle_container.setFixedHeight(
                    30
                )  # Фиксируем высоту для симметрии с TURBO-панелью
                toggle_btn.clicked.connect(
                    lambda checked, b=btn_name, i=col: self.update_toggle_state(
                        b, i, checked
                    )
                )
                toggle_layout.addWidget(toggle_btn)

                # Добавляем виджеты в вертикальный layout с отступами
                slot_layout.setSpacing(6)  # Увеличили отступ для четкого разделения
                slot_layout.addWidget(turbo_container)
                slot_layout.addWidget(delay_container)
                slot_layout.addWidget(slot_btn)
                slot_layout.addWidget(toggle_container)

                row_layout.addWidget(slot_container)

                self.ui_buttons[btn_name].append(slot_btn)
                self.ui_toggles[btn_name].append(toggle_btn)
                self.ui_turbos[btn_name].append(turbo_btn)
                self.ui_turbo_inputs[btn_name].append(turbo_input)
                self.ui_delays[btn_name].append(delay_btn)
                self.ui_delay_inputs[btn_name].append(delay_input)

            self.scroll_layout.addWidget(row_frame)

        self.scroll.setWidget(self.scroll_content)

        # Явно вешаем трекинг на скроллбар
        self.scroll.verticalScrollBar().setMouseTracking(True)
        self.scroll.verticalScrollBar().installEventFilter(self)
        self.scroll.horizontalScrollBar().setMouseTracking(True)
        self.scroll.horizontalScrollBar().installEventFilter(self)

        self.main_layout.addWidget(self.scroll)
        self.scan_profiles()

    def start_cap(self, gp_btn, idx, obj):
        if self.active_slot:
            old_gp, old_idx, old_obj = self.active_slot
            old_obj.setText(self.bindings[old_gp][old_idx])
            old_obj.setProperty("capturing", "false")
            old_obj.style().unpolish(old_obj)
            old_obj.style().polish(old_obj)

        self.active_slot = (gp_btn, idx, obj)
        self.thread.is_capturing = True
        obj.setText("???")
        obj.setProperty("capturing", "true")
        obj.style().unpolish(obj)
        obj.style().polish(obj)

    def on_key(self, name, sc):
        if self.active_slot:
            gp_btn, idx, obj = self.active_slot
            name_up = name.upper()

            if name_up == "ESC":
                name_up = "NONE"

            self.bindings[gp_btn][idx] = name_up
            obj.setText(name_up)

            # Сбрасываем выделение через свойство
            obj.setProperty("capturing", "false")
            obj.style().unpolish(obj)
            obj.style().polish(obj)

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
        
        if hasattr(self, "tray_btn_toggle"):
            self.tray_btn_toggle.setObjectName(
                "run_btn_active" if is_active else "run_btn_inactive"
            )
            self.tray_btn_toggle.setText("STOP EMULATION" if is_active else "START EMULATION")
            self.tray_btn_toggle.style().unpolish(self.tray_btn_toggle)
            self.tray_btn_toggle.style().polish(self.tray_btn_toggle)
            
        self.toggle_btn.style().unpolish(self.toggle_btn)  # Форсим перерисовку стиля
        self.toggle_btn.style().polish(self.toggle_btn)

        if is_active:
            self.turbo_timer.start(10)
        else:
            self.turbo_timer.stop()
            self.active_turbo_keys.clear()
            self.active_t_session.clear()

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

        # 1. RESET PHASE (Сброс перед загрузкой нового профиля)
        for gp_btn in GP_MAP_KEYS:
            for i in range(6):
                # Сброс внутренних данных
                self.bindings[gp_btn][i] = "NONE"
                self.toggles[gp_btn][i] = False
                self.turbos[gp_btn][i] = False
                self.turbo_intervals_map[gp_btn][i] = 0.1

                # Сброс UI
                btn = self.ui_buttons[gp_btn][i]
                btn.setText("NONE")
                btn.setStyleSheet("")

                toggle = self.ui_toggles[gp_btn][i]
                toggle.blockSignals(True)
                toggle.setChecked(False)
                toggle.setEnabled(True)
                toggle.blockSignals(False)

                turbo = self.ui_turbos[gp_btn][i]
                turbo.blockSignals(True)
                turbo.setChecked(False)
                turbo.setEnabled(True)
                turbo.blockSignals(False)

                t_input = self.ui_turbo_inputs[gp_btn][i]
                t_input.setEnabled(False)
                t_input.setText("0.1")
                t_input.setProperty("active", "false")
                t_input.style().unpolish(t_input)
                t_input.style().polish(t_input)

                self.delays[gp_btn][i] = False
                self.delay_intervals_map[gp_btn][i] = 0.1

                d_btn = self.ui_delays[gp_btn][i]
                d_btn.blockSignals(True)
                d_btn.setChecked(False)
                d_btn.setStyleSheet("")
                d_btn.blockSignals(False)

                d_input = self.ui_delay_inputs[gp_btn][i]
                d_input.setEnabled(False)
                d_input.setText("0.1")
                d_input.setProperty("active", "false")
                d_input.style().unpolish(d_input)
                d_input.style().polish(d_input)

        # 1. Сначала подгружаем геометрию окна из GLOBAL_CONFIG (config.ini)
        if os.path.exists(GLOBAL_CONFIG):
            sys_config = configparser.ConfigParser()
            sys_config.read(GLOBAL_CONFIG, encoding="utf-8")
            if "Window" in sys_config:
                geometry = sys_config.get("Window", "geometry", fallback=None)
                if geometry:
                    self.restoreGeometry(bytes.fromhex(geometry))
                    print(f"[SYSTEM] Window geometry restored from {GLOBAL_CONFIG}")

            # --- ЗАГРУЗКА ЦВЕТОВОЙ СХЕМЫ (v2.0) ---
            if "Appearance" in sys_config:
                self.primary_color = sys_config.get(
                    "Appearance", "primary_color", fallback="#0078D7"
                )
                self.secondary_color = sys_config.get(
                    "Appearance", "secondary_color", fallback="#E74C3C"
                )
                self.apply_theme()

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

            if "Toggles" in config:
                for gp_btn, val in config["Toggles"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.toggles:
                        # Преобразуем строку "1,0,1..." в список булевых значений
                        states = [bool(int(x)) for x in val.split(",")]
                        for i in range(min(len(states), 6)):
                            self.toggles[gp_btn_up][i] = states[i]
                            # Блокируем сигналы, чтобы не триггерить сохранение при загрузке
                            self.ui_toggles[gp_btn_up][i].blockSignals(True)
                            self.ui_toggles[gp_btn_up][i].setChecked(states[i])
                            self.ui_toggles[gp_btn_up][i].blockSignals(False)

            if "Turbo" in config:
                for gp_btn, val in config["Turbo"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.turbos:
                        states = [bool(int(x)) for x in val.split(",")]
                        for i in range(min(len(states), 6)):
                            self.turbos[gp_btn_up][i] = states[i]
                            self.ui_turbos[gp_btn_up][i].blockSignals(True)
                            self.ui_turbos[gp_btn_up][i].setChecked(states[i])
                            self.ui_turbos[gp_btn_up][i].blockSignals(False)

            # Загрузка интервалов
            if "TurboIntervals" in config:
                for gp_btn, val in config["TurboIntervals"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.turbo_intervals_map:
                        vals = [float(x) for x in val.split(",")]
                        for i in range(min(len(vals), 6)):
                            self.turbo_intervals_map[gp_btn_up][i] = vals[i]
                            self.ui_turbo_inputs[gp_btn_up][i].setText(str(vals[i]))

                             # Активируем поле только если турбо активен
                            is_active = self.turbos[gp_btn_up][i]
                            self.ui_turbo_inputs[gp_btn_up][i].setEnabled(is_active)
                            self.ui_turbo_inputs[gp_btn_up][i].setProperty(
                                "active", "true" if is_active else "false"
                            )

            if "Delay" in config:
                for gp_btn, val in config["Delay"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.delays:
                        states = [bool(int(x)) for x in val.split(",")]
                        for i in range(min(len(states), 6)):
                            self.delays[gp_btn_up][i] = states[i]
                            self.ui_delays[gp_btn_up][i].blockSignals(True)
                            self.ui_delays[gp_btn_up][i].setChecked(states[i])
                            if states[i]:
                                self.ui_delays[gp_btn_up][i].setStyleSheet(f"background-color: {self.primary_color}; color: white;")
                            self.ui_delays[gp_btn_up][i].blockSignals(False)

            if "DelayIntervals" in config:
                for gp_btn, val in config["DelayIntervals"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.delay_intervals_map:
                        vals = [float(x) for x in val.split(",")]
                        for i in range(min(len(vals), 6)):
                            self.delay_intervals_map[gp_btn_up][i] = vals[i]
                            self.ui_delay_inputs[gp_btn_up][i].setText(str(vals[i]))
                            is_active = self.delays[gp_btn_up][i]
                            self.ui_delay_inputs[gp_btn_up][i].setEnabled(is_active)
                            self.ui_delay_inputs[gp_btn_up][i].setProperty("active", "true" if is_active else "false")

            self.thread.bindings = {k: v[:] for k, v in self.bindings.items()}
            self.thread.toggles = {k: v[:] for k, v in self.toggles.items()}
            self.thread.turbos = {k: v[:] for k, v in self.turbos.items()}
            self.thread.delays = {k: v[:] for k, v in self.delays.items()}

            # Обновляем состояние блокировок
            for gp_btn in GP_MAP_KEYS:
                for i in range(6):
                    is_toggle = self.toggles[gp_btn][i]
                    is_turbo = self.turbos[gp_btn][i]
                    is_delay = self.delays[gp_btn][i]
                    self.ui_turbos[gp_btn][i].setEnabled(not is_toggle and not is_delay)
                    self.ui_toggles[gp_btn][i].setEnabled(not is_turbo and not is_delay)
                    self.ui_delays[gp_btn][i].setEnabled(not is_toggle and not is_turbo)
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
        # Сохраняем состояние тогглов как 1/0
        config["Toggles"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.toggles.items()
        }
        # Сохраняем Turbo
        config["Turbo"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.turbos.items()
        }
        # Сохраняем Интервалы
        config["TurboIntervals"] = {
            k: ",".join([str(x) for x in v])
            for k, v in self.turbo_intervals_map.items()
        }
        # Сохраняем Delay
        config["Delay"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.delays.items()
        }
        # Сохраняем интервалы Delay
        config["DelayIntervals"] = {
            k: ",".join([str(x) for x in v])
            for k, v in self.delay_intervals_map.items()
        }

        try:
            with open(full_path, "w", encoding="utf-8") as f:
                config.write(f)
            print(f"[SYSTEM] Config saved to: {full_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save {full_path}: {e}")

    def add_profile(self):
        """Создание профиля через наш личный тёмный диалог"""
        dialog = CustomInputDialog("New Profile", self)

        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_value()
            if name:
                # Имя файла может прийти как с путём, так и без
                filename = f"{name}.ini" if not name.endswith(".ini") else name

                # Полный путь к файлу в папке Profiles
                full_path = os.path.join(PROFILES_DIR, filename)

                if not os.path.exists(full_path):
                    self.save_config(full_path)
                    self.scan_profiles(filename)
                    print(f"[SYSTEM] Profile '{filename}' created.")
                else:
                    self.show_styled_message(
                        "Error",
                        f"Profile '{filename}' already exists!",
                        is_warning=True,
                    )

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

        # Расчет вспомогательных оттенков для QMessageBox
        s_color = QColor(self.secondary_color)
        s_hover = s_color.lighter(130).name()
        s_active_bg = s_color.darker(300).name()

        # Используем динамический стиль, настроенный на вторичный цвет
        # Передаем secondary_color как основной, чтобы все рамки и ховеры в диалоге стали "опасного" цвета
        confirm.setStyleSheet(
            get_stylesheet(self.secondary_color, self.secondary_color)
            + f"""
            QMessageBox {{
                background-color: #121212;
                border: 2px solid {self.secondary_color};
                border-radius: 10px;
            }}
            QLabel {{
                color: {self.secondary_color};
                font-weight: bold;
                font-size: 15px;
                padding: 20px;
            }}
            QPushButton {{
                background-color: #1A1A1A;
                color: #BBB;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 8px 20px;
                margin-bottom: 10px;
                min-width: 80px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                border-color: {self.secondary_color};
                color: {self.secondary_color};
                background-color: #252525;
            }}
            QPushButton:focus {{
                border: 1px solid #333;
            }}
        """
        )

        if confirm.exec() == QMessageBox.Yes:
            try:
                filename = (
                    current if current.lower().endswith(".ini") else f"{current}.ini"
                )
                full_path = os.path.join(PROFILES_DIR, filename)

                if os.path.exists(full_path):
                    os.remove(full_path)
                    print(f"[SYSTEM] Profile {filename} deleted.")
                    self.scan_profiles()
                else:
                    print(f"[ERROR] File not found for deletion: {full_path}")
            except Exception as e:
                print(f"[ERROR] {e}")

    def import_profile(self):
        """Копирование внешнего .ini файла в папку программы"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select profile", "", "INI Files (*.ini)"
        )
        if file_path:
            # Копируем файл ВНУТРЬ папки Profiles
            try:
                shutil.copy(file_path, PROFILES_DIR)
                print(f"[SYSTEM] Imported profile from {file_path}")
                self.scan_profiles()
            except Exception as e:
                self.show_styled_message(
                    "Import Error", f"Failed to import profile:\n{e}", is_warning=True
                )

    def export_profile(self):
        """Сохранение текущего выбранного профиля в любое место на диске"""
        current = self.profile_combo.currentText()
        if not current:
            return

        # Убеждаемся, что расширение .ini присутствует для поиска файла
        filename = current if current.lower().endswith(".ini") else f"{current}.ini"
        source_path = os.path.join(PROFILES_DIR, filename)

        # Проверяем, существует ли файл в папке Profiles
        if not os.path.exists(source_path):
            print(f"[ERROR] Source profile not found: {source_path}")
            return

        # Открываем диалог сохранения
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Export profile", filename, "INI Files (*.ini)"
        )

        if save_path:
            try:
                shutil.copy(source_path, save_path)
                print(f"[SYSTEM] Profile exported to: {save_path}")
            except Exception as e:
                print(f"[ERROR] Failed to export: {e}")

    def update_toggle_state(self, gp_btn, idx, checked):
        """Обновление состояния чекбокса Toggle"""
        self.toggles[gp_btn][idx] = checked
        self.thread.toggles = {k: v[:] for k, v in self.toggles.items()}

        # Блокируем Turbo и Delay если Toggle активен
        self.ui_turbos[gp_btn][idx].setEnabled(not checked)
        self.ui_delays[gp_btn][idx].setEnabled(not checked)

        self.save_config()

    def update_turbo_state(self, gp_btn, idx, checked):
        """Обновление состояния чекбокса Turbo"""
        self.turbos[gp_btn][idx] = checked
        self.thread.turbos = {k: v[:] for k, v in self.turbos.items()}

        # Блокируем Toggle и Delay если Turbo активен
        self.ui_toggles[gp_btn][idx].setEnabled(not checked)
        self.ui_delays[gp_btn][idx].setEnabled(not checked)

        # Включаем/выключаем текстовое поле (всегда видимо)
        turbo_input = self.ui_turbo_inputs[gp_btn][idx]
        turbo_input.setEnabled(checked)
        if checked:
            turbo_input.setProperty("active", "true")
        else:
            turbo_input.setProperty("active", "false")
        turbo_input.style().unpolish(turbo_input)
        turbo_input.style().polish(turbo_input)

        self.save_config()

    def update_turbo_interval(self, gp_btn, idx):
        """Обновление интервала из текстового поля"""
        inp = self.ui_turbo_inputs[gp_btn][idx]
        text = inp.text().replace(",", ".")
        try:
            val = float(text)
            if val < 0.01:
                val = 0.01
            self.turbo_intervals_map[gp_btn][idx] = val
        except ValueError:
            inp.setText(str(self.turbo_intervals_map[gp_btn][idx]))
        self.save_config()

    def update_delay_state(self, gp_btn, idx, checked):
        """Обновление состояния чекбокса Delay"""
        self.delays[gp_btn][idx] = checked
        self.thread.delays = {k: v[:] for k, v in self.delays.items()}
        
        # Блокируем Toggle и Turbo если Delay активен
        self.ui_toggles[gp_btn][idx].setEnabled(not checked)
        self.ui_turbos[gp_btn][idx].setEnabled(not checked)
        
        delay_input = self.ui_delay_inputs[gp_btn][idx]
        delay_input.setEnabled(checked)
        if checked:
            delay_input.setProperty("active", "true")
        else:
            delay_input.setProperty("active", "false")
        delay_input.style().unpolish(delay_input)
        delay_input.style().polish(delay_input)
        
        btn = self.ui_delays[gp_btn][idx]
        if checked:
            btn.setStyleSheet(f"background-color: {self.primary_color}; color: white;")
        else:
            btn.setStyleSheet("")

        self.save_config()

    def update_delay_interval(self, gp_btn, idx):
        """Обновление интервала из текстового поля Delay"""
        inp = self.ui_delay_inputs[gp_btn][idx]
        text = inp.text().replace(",", ".")
        try:
            val = float(text)
            if val < 0.0:
                val = 0.0
            self.delay_intervals_map[gp_btn][idx] = val
        except ValueError:
            inp.setText(str(self.delay_intervals_map[gp_btn][idx]))
        self.save_config()

    def on_delay_request(self, gp_btn, slot_idx, is_down):
        """Слот для сигнала Delay из InterceptionThread (нажатие/отпускание)"""
        key = (gp_btn, slot_idx)
        if is_down:
            if key in self.delay_timers:
                # Игнорируем автоповторы нажатия от системы, если таймер уже запущен
                return
            delay_sec = self.delay_intervals_map[gp_btn][slot_idx]
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(lambda b=gp_btn, i=slot_idx: self.on_delay_fired(b, i))
            self.delay_timers[key] = timer
            self.delay_fired_state[key] = False
            timer.start(int(delay_sec * 1000))
        else:
            if key in self.delay_timers:
                timer = self.delay_timers.pop(key)
                timer.stop()
                has_fired = self.delay_fired_state.get(key, False)
                if has_fired:
                    # Раз запущен, нужно его корректно "отпустить"
                    self.thread.trigger_logical_action(gp_btn, slot_idx, False)

    def on_delay_fired(self, gp_btn, slot_idx):
        key = (gp_btn, slot_idx)
        self.delay_fired_state[key] = True
        self.thread.trigger_logical_action(gp_btn, slot_idx, True)

    def on_turbo_active(self, gp_btn, is_active, slot_idx):
        """Слот для сигнала из потока Interception"""
        if is_active:
            interval = self.turbo_intervals_map[gp_btn][slot_idx]
            self.active_t_session[gp_btn] = {
                "interval": interval,
                "last_time": 0,
                "state": False,
            }
        else:
            # Перед удалением сессии убеждаемся, что кнопка отпущена
            if gp_btn in self.active_t_session:
                # Принудительно отпускаем кнопку
                with self.thread.lock:
                    if gp_btn in GP_BUTTON_MAP:
                        self.thread.gamepad.release_button(button=GP_BUTTON_MAP[gp_btn])
                    elif gp_btn == "LT":
                        self.thread.gamepad.left_trigger(value=0)
                    elif gp_btn == "RT":
                        self.thread.gamepad.right_trigger(value=0)
                    self.thread.gamepad.update()

                del self.active_t_session[gp_btn]

    def on_turbo_tick(self):
        """Тик таймера для турбо-режима (краткие нажатия с заданным интервалом)"""
        if not self.thread.enabled or not self.active_t_session:
            return

        now = time.time()
        need_update = False

        if not self.thread.gamepad:
            return

        PRESS_DURATION = 0.1  # Кнопка нажата 00мс

        with self.thread.lock:
            for gp_btn, params in list(self.active_t_session.items()):
                interval = params["interval"]
                last_time = params["last_time"]
                state = params["state"]

                # Если пора делать новое нажатие
                if not state and (now - last_time >= interval):
                    # Нажимаем кнопку
                    if gp_btn in GP_BUTTON_MAP:
                        self.thread.gamepad.press_button(button=GP_BUTTON_MAP[gp_btn])
                    elif gp_btn == "LT":
                        self.thread.gamepad.left_trigger(value=255)
                    elif gp_btn == "RT":
                        self.thread.gamepad.right_trigger(value=255)

                    params["state"] = True
                    params["last_time"] = now
                    need_update = True

                # Если кнопка нажата и пора отпустить (прошло 50мс)
                elif state and (now - last_time >= PRESS_DURATION):
                    # Отпускаем кнопку
                    if gp_btn in GP_BUTTON_MAP:
                        self.thread.gamepad.release_button(button=GP_BUTTON_MAP[gp_btn])
                    elif gp_btn == "LT":
                        self.thread.gamepad.left_trigger(value=0)
                    elif gp_btn == "RT":
                        self.thread.gamepad.right_trigger(value=0)

                    params["state"] = False
                    need_update = True

            if need_update:
                self.thread.gamepad.update()

    def clear_slot(self, gp_btn, idx, obj):
        """Очистка слота по правому клику мыши"""
        self.bindings[gp_btn][idx] = "NONE"
        obj.setText("NONE")

        self.thread.bindings = {k: v[:] for k, v in self.bindings.items()}
        self.save_config()

        if self.active_slot and self.active_slot[2] == obj:
            self.thread.is_capturing = False
            self.active_slot = None

    def show_styled_message(self, title, text, is_warning=False):
        """Вспомогательный метод для показа стилизованных уведомлений"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        color = self.secondary_color if is_warning else self.primary_color
        p_color = QColor(color)
        hover = p_color.lighter(130).name()
        bg = p_color.darker(300).name()

        style = (
            get_stylesheet(self.primary_color, self.secondary_color)
            + f"""
            QMessageBox {{
                background-color: #121212;
                border: 2px solid {color};
                border-radius: 10px;
            }}
            QLabel {{ color: white; padding: 20px; font-size: 14px; }}
            QPushButton {{
                background-color: #1A1A1A;
                color: white;
                border: 1px solid #333;
                border-radius: 4px;
                padding: 8px 20px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                border-color: {color};
                background-color: {bg};
                color: {hover};
            }}
        """
        )
        msg.setStyleSheet(style)
        msg.exec()

    def closeEvent(self, event):
        """Единая точка выхода с сохранением и чисткой драйвера"""
        print("\n[SYSTEM] Closing application...")

        # 1. Сначала скрываем иконку в трее, чтобы не висела
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()

        # 2. Гасим драйвер и ждем его завершения
        if hasattr(self, "thread"):
            print("[SYSTEM] Stopping driver...")
            self.thread.stop()
            self.thread.wait(1000)  # Ждем до 1 сек

        # 3. Сохраняем всё
        try:
            target_config = "System_Config.ini"
            config = configparser.ConfigParser()
            if os.path.exists(target_config):
                config.read(target_config, encoding="utf-8")

            if "Settings" not in config:
                config.add_section("Settings")
            if "Window" not in config:
                config.add_section("Window")
            if "Appearance" not in config:
                config.add_section("Appearance")

            current_prof_name = self.profile_combo.currentText()
            config.set("Settings", "last_profile", f"{current_prof_name}.ini")
            config.set("Settings", "autostart", str(self.autostart_cb.isChecked()))
            config.set(
                "Window", "geometry", self.saveGeometry().toHex().data().decode()
            )
            config.set("Appearance", "primary_color", self.primary_color)
            config.set("Appearance", "secondary_color", self.secondary_color)
            config["Bindings"] = {k: ",".join(v) for k, v in self.bindings.items()}

            with open(target_config, "w", encoding="utf-8") as f:
                config.write(f)

            if current_prof_name:
                self.save_config(current_prof_name)

            print("[SYSTEM] All settings saved.")
        except Exception as e:
            print(f"[ERROR] Save failed: {e}")

        print("[SYSTEM] Shutdown complete. Goodbye!")
        # Игнорируем стандартное закрытие и выходим жестко, чтобы процесс не висел
        event.ignore()
        os._exit(0)

    # 2. А вот этот метод мы вызываем ИЗ ТРЕЯ
    def manual_exit(self):
        """Метод 'Ядерная кнопка' — просто запускает стандартное закрытие"""
        self.close()

    # --- COLOR CUSTOMIZATION METHODS (v2.0) ---
    def show_settings(self):
        """Открывает диалог настроек цветов"""
        dialog = QDialog(self)
        dialog.setWindowTitle("UI COLOR SETTINGS")
        dialog.setFixedWidth(300)
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        # Применяем текущую тему к самому диалогу
        dialog.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title = QLabel("COLOR CUSTOMIZATION")
        title.setObjectName("SettingsTitle")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        info = QLabel(
            "Pick base colors, highlights\\nwill be calculated automatically."
        )
        info.setStyleSheet("color: #888; font-size: 11px; background: transparent;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # Кнопки цветов
        p_btn = QPushButton("PRIMARY (REPLACES BLUE)")
        p_btn.setObjectName("PrimaryPickBtn")
        p_btn.setMinimumHeight(45)
        p_btn.setCursor(Qt.PointingHandCursor)
        p_btn.clicked.connect(lambda: self.pick_color("primary", dialog))
        layout.addWidget(p_btn)

        s_btn = QPushButton("SECONDARY (REPLACES RED)")
        s_btn.setObjectName("SecondaryPickBtn")
        s_btn.setMinimumHeight(45)
        s_btn.setCursor(Qt.PointingHandCursor)
        s_btn.clicked.connect(lambda: self.pick_color("secondary", dialog))
        layout.addWidget(s_btn)

        layout.addSpacing(10)

        # Кнопка закрытия
        close_btn = QPushButton("SAVE and CLOSE")
        close_btn.setObjectName("SaveCloseBtn")
        close_btn.setMinimumHeight(40)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec()

    def pick_color(self, target, dialog):
        """Вызов кастомного диалога выбора цвета с предпросмотром в реальном времени (v2.0)"""
        from PySide6.QtWidgets import QColorDialog

        # Сохраняем исходные цвета на случай отмены
        original_primary = self.primary_color
        original_secondary = self.secondary_color
        current = self.primary_color if target == "primary" else self.secondary_color

        color_dialog = QColorDialog(QColor(current), self)
        color_dialog.setOptions(QColorDialog.DontUseNativeDialog)
        color_dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        color_dialog.setStyleSheet(
            get_stylesheet(self.primary_color, self.secondary_color)
        )

        def update_preview(color):
            if color.isValid():
                if target == "primary":
                    self.primary_color = color.name()
                else:
                    self.secondary_color = color.name()

                # Используем таймер для троттлинга (сглаживания)
                if not self.preview_timer.isActive():
                    self.preview_timer.start()

        def on_preview_timeout():
            self.apply_theme()
            dialog.setStyleSheet(
                get_stylesheet(self.primary_color, self.secondary_color)
            )
            color_dialog.setStyleSheet(
                get_stylesheet(self.primary_color, self.secondary_color)
            )

        # Подключаем таймер для этого сеанса
        self.preview_timer.timeout.connect(on_preview_timeout)
        color_dialog.currentColorChanged.connect(update_preview)

        if color_dialog.exec():
            # На всякий случай отключаем временные коннекты
            self.preview_timer.timeout.disconnect(on_preview_timeout)

            # Если нажали OK, сохраняем финальный результат
            final_color = color_dialog.selectedColor()
            if final_color.isValid():
                if target == "primary":
                    self.primary_color = final_color.name()
                else:
                    self.secondary_color = final_color.name()

                self.apply_theme()
                self.save_appearance()
        else:
            # Напоследок отключаем наш временный коннект таймера
            self.preview_timer.timeout.disconnect(on_preview_timeout)

            # Если отмена — возвращаем как было
            self.primary_color = original_primary
            self.secondary_color = original_secondary
            self.apply_theme()
            dialog.setStyleSheet(
                get_stylesheet(self.primary_color, self.secondary_color)
            )

    def apply_theme(self):
        """Обновляет стили всего приложения"""
        new_style = get_stylesheet(self.primary_color, self.secondary_color)
        self.setStyleSheet(new_style)

        # Принудительно обновляем вид выпадающего списка (целевой стиль)
        if hasattr(self, "profile_combo"):
            view = self.profile_combo.view()
            if view:
                view.setStyleSheet(
                    f"""
                    QListView {{ 
                        background-color: #121212; 
                        color: white; 
                        selection-background-color: {self.primary_color}; 
                        selection-color: white;
                        border: 1px solid {self.primary_color};
                        outline: none;
                    }}
                    QListView::item {{ padding: 8px; }}
                """
                )

        self.update_tray_menu_style()

    def update_tray_menu_style(self):
        """Синхронизирует стиль меню трея с основной темой"""
        style = f"""
            QMenu {{
                background-color: #1a1a1a;
                color: white;
                border: 1px solid {self.primary_color};
                padding: 5px;
            }}
            QMenu::item {{
                padding: 8px 25px;
                background-color: transparent;
            }}
            QMenu::item:selected {{
                background-color: {self.primary_color};
                color: white;
            }}
            QMenu::separator {{
                height: 1px;
                background: #333333;
                margin: 5px 10px;
            }}
        """
        if hasattr(self, "tray_icon") and self.tray_icon.contextMenu():
            self.tray_icon.contextMenu().setStyleSheet(style)
            
        if hasattr(self, "tray_btn_toggle"):
            self.tray_btn_toggle.setStyleSheet(
                get_stylesheet(self.primary_color, self.secondary_color) + "\nQPushButton { margin: 4px 10px; padding: 0 10px; }"
            )

    def save_appearance(self):
        """Сохраняет цвета в System_Config.ini"""
        config = configparser.ConfigParser()
        if os.path.exists(GLOBAL_CONFIG):
            config.read(GLOBAL_CONFIG, encoding="utf-8")

        if "Appearance" not in config:
            config["Appearance"] = {}

        config["Appearance"]["primary_color"] = self.primary_color
        config["Appearance"]["secondary_color"] = self.secondary_color
        if hasattr(self, "hide_to_tray_cb"):
            config["Appearance"]["hide_to_tray"] = "true" if self.hide_to_tray_cb.isChecked() else "false"

        with open(GLOBAL_CONFIG, "w", encoding="utf-8") as f:
            config.write(f)
        print(f"[SYSTEM] Colors saved to {GLOBAL_CONFIG}")


if __name__ == "__main__":
    import multiprocessing
    # 1. Freeze Support: Обязательно для корректной работы PyInstaller с мультипроцессами (onefile)
    multiprocessing.freeze_support()

    # 2. App ID Integration: Удалено, так как явное задание AppID ломает группировку ярлыка в EXE.
    # Windows автоматически сгруппирует процесс с ярлыком на таскбаре по пути к исполняемому файлу.

    app = QApplication(sys.argv)
    
    # Глобальная иконка приложения для таскбара
    from PySide6.QtGui import QIcon
    if os.path.exists("XBOX-Keypad.ico"):
        app.setWindowIcon(QIcon("XBOX-Keypad.ico"))

    # 3. Single Instance / Window Restore Communication
    from PySide6.QtNetwork import QLocalSocket, QLocalServer
    server_name = "XBOX_KEYPAD_V2_INSTANCE"
    
    # Пытаемся подключиться к уже запущенному приложению
    socket = QLocalSocket()
    socket.connectToServer(server_name)
    if socket.waitForConnected(500):
        # Если удалось — шлём команду развернуть окно и тихо выходим
        socket.write(b"WAKEUP")
        socket.waitForBytesWritten(500)
        sys.exit(0)

    # Если мы здесь, значит мы первые. Удаляем старый сокет (если был краш) и слушаем.
    QLocalServer.removeServer(server_name)
    server = QLocalServer()
    server.listen(server_name)

    ex = MainWindow()
    
    def on_new_connection():
        client = server.nextPendingConnection()
        if client:
            if client.waitForReadyRead(200):
                msg = client.readAll()
                if msg == b"WAKEUP":
                    ex.showNormal()
                    ex.raise_()
                    ex.activateWindow()
                    # SetForegroundWindow принудительно поднимает окно,
                    # даже если Windows заблокировала обычный захват фокуса
                    try:
                        import ctypes
                        hwnd = int(ex.winId())
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                    except Exception:
                        pass
            client.disconnectFromServer()
            client.deleteLater()
            
    server.newConnection.connect(on_new_connection)

    ex.show()
    
    # 4. Cleanup
    exit_code = app.exec()
    server.close()
    sys.exit(exit_code)
