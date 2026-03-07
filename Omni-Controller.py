import os
import sys
import ctypes
import time
import threading
import atexit
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
    QObject,
    QThread,
    Qt,
    QTimer,
    Signal,
    QEvent,
    QPoint,
    QRect,
    QSize,
    QPropertyAnimation,
    QByteArray,
    QMimeData,
    QEasingCurve,
)
from PySide6.QtGui import QFont, QColor, QAction, QIcon, QPixmap, QCursor, QDrag, QDoubleValidator
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
    QTabWidget,
    QSplitter,
    QWidgetAction,
    QSpacerItem,
    QSizePolicy,
    QProxyStyle,
    QStyle,
    QStyleFactory,
    QAbstractScrollArea,
)



class _SafeDict(dict):
    """
    Безопасный dict для format_map.
    Возвращает пустую строку вместо KeyError для любого ключа,
    отсутствующего в словаре стилей. Это позволяет расширять _QSS_TEMPLATE
    новыми переменными, не ломая старые вызовы get_stylesheet.
    Должен быть объявлен ДО get_stylesheet, которая его использует.
    """
    def __missing__(self, key):
        return ''


def get_stylesheet(primary="#0078d7", secondary="#e72e2e"):
    """
    Генерирует таблицу стилей безопасно: использует _SafeDict и format_map.
    """    
    p_color = QColor(primary)
    s_color = QColor(secondary)
    
    # Расчёт умных оттенков
    p_hover = p_color.lighter(130).name()
    p_hover_bg = p_color.darker(500).name()
    p_active_bg = p_color.darker(300).name()
    p_checked_hover = p_color.darker(200).name()
    s_hover = s_color.lighter(130).name() 
    s_hover_bg = s_color.darker(500).name()
    s_active_bg = s_color.darker(300).name()
    
    # Дополнительно: прозрачный RGBA для более мягких свечений
    p_rgba = f"rgba({p_color.red()}, {p_color.green()}, {p_color.blue()}, 0.15)"

    styles = {
        "primary": primary,
        "secondary": secondary,
        "p_hover": p_hover,
        "p_hover_bg": p_hover_bg, # Добавляем в словарь
        "p_active_bg": p_active_bg,
        "p_checked_hover": p_checked_hover,
        "s_hover": s_hover,
        "s_hover_bg": s_hover_bg,  # Добавляем в словарь
        "s_active_bg": s_active_bg,
        "p_rgba": p_rgba
    }
    return _QSS_TEMPLATE.format_map(_SafeDict(styles))

# ─── QSS-шаблон ──────────────────────────────────────────────────────────────
# Правило экранирования:
#   {{ и }}  →  буквальные фигурные скобки CSS   →  { } в итоговой строке
#   {primary} и т.д. →  переменные для .format() →  реальный цвет
#
_QSS_TEMPLATE = """
/* ─── Уровень 0: Глобальный сброс outline ─────────────────────────────────── */
* {{
    outline: none;
}}
*:focus {{
    outline: none;
}}
QWidget:focus {{
    outline: none;
}}
QAbstractScrollArea:focus,
QScrollArea:focus,
QFrame:focus,
QPushButton:focus,
QLineEdit:focus {{
    outline: none;
    border: none;
}}

/* ─── Основное окно и контейнеры ───────────────────────────────────────────── */
QMainWindow,
QWidget#scrollAreaWidgetContents,
QWidget#MacroScrollContent {{
    background-color: #0d0d0d;
}}

#Container {{
    background-color: #0d0d0d;
    border: 2px solid {primary};
    border-radius: 10px;
}}

QScrollArea {{
    background-color: transparent;
    border: none;
    /* Создаёт зазор между контентом/скроллом и границей окна */
    padding-right: 8px;
}}

QFrame#Header {{
    background-color: #0d0d0d;
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

/* ─── Title Label ───────────────────────────────────────────────────────────── */
QLabel#TitleLabel {{
    color: #B7C0C9;
    font-family: 'Segoe UI';
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
}}

/* ─── Кнопки шапки ─────────────────────────────────────────────────────────── */
QPushButton#min_btn,
QPushButton#close_btn {{
    background-color: transparent;
    border: 1px solid #333;
    color: #666;
    font-size: 16px;
    font-weight: bold;
    min-width: 32px;
    max-width: 32px;
    min-height: 24px;
    outline: none;
}}
QPushButton#min_btn:focus, QPushButton#close_btn:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton#min_btn:hover {{
    color: {primary};
    border-color: {primary};
}}
QPushButton#close_btn:hover {{
    color: {secondary};
    border-color: {secondary};
}}

/* ─── Скроллбары (Stealth Gray) ────────────────────────────────────────────── */
QScrollArea#ScrollArea,
QScrollArea#MacroScroll {{
    border: none;
    background-color: #0A0A0A;
    outline: none;
}}

QScrollBar:vertical {{
    background: #0A0A0A;
    width: 12px;
    margin: 0px 4px 0px 0px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background: #222222;
    border: 1px solid #444;
    min-height: 30px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical:hover,
QScrollBar::handle:vertical:pressed {{
    background: #333333;
    border: 1px solid {primary};
}}

QScrollBar:horizontal {{
    border: none;
    background: transparent;
    height: 8px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: #333333;
    min-width: 20px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #444444;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
    background: none;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    height: 0px;
    background: none;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ─── Секция профилей ──────────────────────────────────────────────────────── */
QFrame#ProfSection {{
    background-color: #1A1A1A;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 2px;
}}
QFrame#ProfSection:focus {{
    outline: none;
    border: 1px solid #333;
}}
QFrame#ProfSection QLabel {{
    color: #C0C0C0;
    font-weight: bold;
    margin-left: 5px;
}}
QFrame#ProfSection QPushButton {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #2A2A2A;
    border-radius: 4px;
    min-width: 65px;
    padding: 5px;
    font-size: 10px;
    outline: none;
}}
QFrame#ProfSection QPushButton:focus {{
    outline: none;
    border: 1px solid #2A2A2A;
}}
QFrame#ProfSection QPushButton:hover {{
    border-color: {primary};
    color: #FFF;
}}
QFrame#ProfSection QPushButton:pressed {{
    background-color: {primary};
    color: #FFF;
}}

/* ─── QComboBox ────────────────────────────────────────────────────────────── */
QComboBox {{
    background-color: #252525;
    color: #FFF;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 5px 10px;
    min-width: 130px;
    outline: none;
}}
QComboBox:focus {{
    outline: none;
    border: 1px solid {primary};
}}
QComboBox:hover {{
    border-color: {primary};
}}
QComboBox QAbstractItemView {{
    background-color: #0d0d0d;
    color: #c2c2c2;
    selection-background-color: {primary};
    selection-color: #c2c2c2;
    border: 1px solid {primary};
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px;
    outline: none;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {primary};
    color: #c2c2c2;
    outline: none;
}}
QComboBox::drop-down {{
    border: none;
    width: 0px;
}}
QComboBox::down-arrow {{
    image: none;
}}

/* ─── MacroRowWidget (обёртка строки — прозрачная) ─────────────────────────── */
QFrame[objectName^="MacroRow_"] {{
    outline: none;
    background: transparent;
    border: none;
}}
QFrame[objectName^="MacroRow_"]:focus {{
    outline: none;
    border: none;
}}

/* ─── MacroStepWidget ──────────────────────────────────────────────────────── */
QFrame[objectName^="MacroStep_"] {{
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;
    margin: 0px;
}}
QFrame[objectName^="MacroStep_"]:hover {{
    background-color: #111111;
    border: 1px solid {primary};
    outline: none;
}}
QFrame[objectName^="MacroStep_"]:focus,
QFrame[objectName^="MacroStep_"]:focus:hover {{
    outline: none;
    border: 1px solid transparent;
    background-color: transparent;
}}
QFrame[objectName^="MacroStep_"][highlighted="true"] {{
    border: 1px solid {p_hover};
    background-color: {p_active_bg};
    outline: none;
}}
QFrame[objectName^="MacroStep_"][highlighted="true"]:focus {{
    outline: none;
    border: 2px solid {p_hover};
    background-color: {p_active_bg};
}}
QFrame[objectName^="MacroStep_"][highlighted="false"] {{
    border: 1px solid transparent;
    background-color: transparent;
    outline: none;
}}
QFrame[objectName^="MacroStep_"][highlighted="false"]:focus {{
    outline: none;
    border: 1px solid transparent;
}}
QFrame[objectName="MacroStep_drag_over"] {{
    border: 1px solid {primary};
    background-color: {p_active_bg};
    outline: none;
}}

/* ─── StepDelayInput ───────────────────────────────────────────────────────── */
QLineEdit#StepDelayInput {{
    outline: none;
    border: none;
    border-bottom: 1px solid #2a2a2a;
    background: transparent;
    color: {primary};
    font-size: 15px;
    font-weight: bold;
    padding: 0 2px;
}}
QLineEdit#StepDelayInput:hover {{
    outline: none;
    border-bottom: 1px solid {primary};
}}
QLineEdit#StepDelayInput:focus {{
    outline: none;
    border-bottom: 2px solid {p_hover};
}}

/* ─── Run buttons (Neon Blackout Style) ────────────────────────────────────── */
QPushButton#run_btn_inactive {{
    background-color: #121212;
    color: {primary};
    font-weight: bold;
    font-size: 13px;
    border: 2px solid {primary};
    border-radius: 6px;
    min-width: 140px;
    min-height: 50px;
    padding: 0 14px;
    outline: none;
}}
#run_btn_inactive:hover {{
    background-color: {p_hover_bg};
    border-color: {p_hover};
    color: {p_hover};
}}

QPushButton#run_btn_active {{
    background-color: #121212;
    color: {secondary};
    font-weight: bold;
    font-size: 13px;
    border: 2px solid {secondary};
    border-radius: 6px;
    min-width: 140px;
    min-height: 50px;
    padding: 0 14px;
    outline: none;
}}
#run_btn_active:hover {{
    background-color: {s_hover_bg};
    border-color: {s_hover};
    color: {s_hover};
}}

/* ─── SettingsBtn, CheckBox ────────────────────────────────────────────────── */
QPushButton#SettingsBtn {{
    background-color: #1A1A1A;
    color: #BBB;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
    outline: none;
}}
QPushButton#SettingsBtn:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton#SettingsBtn:hover {{
    border-color: {primary};
    color: {primary};
}}
QCheckBox {{
    color: #CCCCCC;
    spacing: 8px;
    outline: none;
}}
QCheckBox:focus {{
    outline: none;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    background-color: #1A1A1A;
    border: 2px solid #333;
    border-radius: 4px;
    outline: none;
}}
QCheckBox::indicator:checked {{
    background-color: {primary};
    border: 2px solid {primary};
}}
QCheckBox::indicator:hover {{
    border: 2px solid {primary};
}}
QCheckBox::indicator:focus {{
    outline: none;
}}

/* ─── Строки биндинга (Row_) ───────────────────────────────────────────────── */
QFrame[objectName^="Row_"] {{
    background-color: #121212;
    border: 1px solid #333333;
    border-radius: 8px;
    margin: 2px 5px;
    outline: none;
}}
QFrame[objectName^="Row_"]:focus {{
    outline: none;
    border: 1px solid #1A1A1A;
}}
QFrame[objectName^="Row_"] QLabel {{
    color: #C0C0C0;
    font-family: "Segoe UI";
    font-weight: bold;
    font-size: 13px;
    border: none;
    background: transparent;
}}

/* ─── Slot buttons ─────────────────────────────────────────────────────────── */
QPushButton[objectName^="Slot_"] {{
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 12px;
    min-height: 30px;
    outline: none;
}}
QPushButton[objectName^="Slot_"]:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton[objectName^="Slot_"]:hover {{
    border-color: {primary};
    background-color: #252525;
    color: {p_hover};
}}
QPushButton[objectName^="Slot_"]:pressed {{
    background-color: {primary};
    color: #c2c2c2;
}}
QPushButton[objectName^="Slot_"][capturing="true"] {{
    background-color: {primary};
    color: #c2c2c2;
    border: 1px solid #c2c2c2;
}}
QPushButton[objectName^="Slot_"][capturing="true"]:focus {{
    outline: none;
    border: 1px solid #c2c2c2;
}}

/* ─── Toggle / Turbo / Delay buttons ──────────────────────────────────────── */
QPushButton[objectName^="ToggleBtn_"],
QPushButton[objectName^="TurboBtn_"],
QPushButton[objectName^="DelayBtn_"] {{
    background-color: #1A1A1A;
    color: #bababa;
    border: 1px solid #333;
    border-radius: 3px;
    font-size: 12px;
    font-weight: bold;
    padding: 2px;
    outline: none;
}}
QPushButton[objectName^="ToggleBtn_"]:focus,
QPushButton[objectName^="TurboBtn_"]:focus,
QPushButton[objectName^="DelayBtn_"]:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton[objectName^="ToggleBtn_"]:disabled,
QPushButton[objectName^="TurboBtn_"]:disabled,
QPushButton[objectName^="DelayBtn_"]:disabled {{
    background-color: #0d0d0d;
    color: #444;
    border: 1px solid #222;
}}
QPushButton[objectName^="ToggleBtn_"]:hover:!checked,
QPushButton[objectName^="TurboBtn_"]:hover:!checked,
QPushButton[objectName^="DelayBtn_"]:hover:!checked {{
    border-color: {primary};
    background-color: #252525;
    color: {p_hover};
}}
QPushButton[objectName^="ToggleBtn_"]:hover:checked,
QPushButton[objectName^="TurboBtn_"]:hover:checked,
QPushButton[objectName^="DelayBtn_"]:hover:checked {{
    background-color: {p_checked_hover};
    border-color: {p_hover};
    color: #c2c2c2;
}}
QPushButton[objectName^="ToggleBtn_"]:checked,
QPushButton[objectName^="TurboBtn_"]:checked,
QPushButton[objectName^="DelayBtn_"]:checked {{
    background-color: {p_active_bg};
    color: {p_hover};
    border: 1px solid {p_hover};
}}
QPushButton[objectName^="ToggleBtn_"]:checked:focus,
QPushButton[objectName^="TurboBtn_"]:checked:focus,
QPushButton[objectName^="DelayBtn_"]:checked:focus {{
    outline: none;
    border: 1px solid {p_hover};
}}

/* ─── TurboInput / DelayInput ──────────────────────────────────────────────── */
QLineEdit[objectName^="TurboInput_"],
QLineEdit[objectName^="DelayInput_"] {{
    background-color: #0d0d0d;
    color: #444;
    border: 1px solid #222;
    border-radius: 3px;
    font-size: 12px;
    padding: 2px;
    outline: none;
}}
QLineEdit[objectName^="TurboInput_"]:enabled,
QLineEdit[objectName^="DelayInput_"]:enabled {{
    background-color: #1A1A1A;
    color: #888;
    border: 1px solid #333;
}}
QLineEdit[objectName^="TurboInput_"]:focus,
QLineEdit[objectName^="DelayInput_"]:focus {{
    outline: none;
    border: 1px solid {p_hover};
    color: #c2c2c2;
}}
QLineEdit[objectName^="TurboInput_"][active="true"], QLineEdit[objectName^="DelayInput_"][active="true"] {{
    background-color: {p_active_bg};
    border: 1px solid {p_hover};
    color: {p_hover};
}}

/* ─── QDialog (Neon Blackout Edition) ─────────────────────────────────────── */
QDialog {{
    background-color: #121212;
    border: 2px solid {primary};
    border-radius: 10px;
    outline: none;
}}
QDialog:focus {{
    outline: none;
}}
QDialog QLabel {{
    color: #c2c2c2;
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
    outline: none;
}}
QDialog QPushButton:focus {{
    outline: none;
    border: 1px solid #333;
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
    outline: none;
}}
QDialog QLineEdit:focus {{
    outline: none;
    border: 1px solid {primary};
}}

/* Кнопки выбора цветов (Специфичные) */
QPushButton#PrimaryPickBtn:focus,
QPushButton#SecondaryPickBtn:focus,
QPushButton#SaveCloseBtn:focus {{
    outline: none;
}}

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

/* ─── QMessageBox / QColorDialog ──────────────────────────────────────────── */
QMessageBox {{
    background-color: #121212;
    border: 2px solid {secondary};
}}
QMessageBox:focus {{
    outline: none;
}}
QMessageBox QLabel {{
    color: white;
}}
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
    outline: none;
}}
QColorDialog QPushButton:focus {{
    outline: none;
    border: 1px solid #333;
}}

/* ─── QTabWidget / QTabBar ─────────────────────────────────────────────────── */
QTabWidget::pane {{
    background: #0d0d0d;
    border: 1px solid #222;
    outline: none;
}}
QTabBar::tab {{
    background: #1A1A1A;
    color: #888;
    border: 1px solid #272727;
    border-bottom: none;
    padding: 6px 16px;
    font-size: 11px;
    font-weight: bold;
    min-width: 90px;
    outline: none;
}}
QTabBar::tab:focus {{
    outline: none;
}}
QTabBar::tab:selected {{
    background: {primary};
    color: #ffffff;
    border: 1px solid {primary};
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    outline: none;
}}
QTabBar::tab:hover:!selected {{
    background: #222;
    color: #bbb;
}}

/* ─── QScrollArea и viewport (устранение ghost-рамок) ─────────────────────── */
QScrollArea {{
    background-color: #0d0d0d;
    border: 1px solid #1e1e1e;
    border-radius: 5px;
    outline: none;
}}
QScrollArea:focus {{
    outline: none;
    border: 1px solid #1e1e1e;
}}
QScrollArea QWidget#qt_scrollarea_viewport {{
    background-color: #0d0d0d;
    border: none;
    outline: none;
}}
QScrollArea QWidget#qt_scrollarea_viewport:focus {{
    outline: none;
    border: none;
}}
QWidget#MacroScrollContent {{
    background-color: #0d0d0d;
    border: none;
    outline: none;
}}
QWidget#MacroScrollContent:focus {{
    outline: none;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    outline: none;
}}

/* ─── Палитра кнопок ───────────────────────────────────────────────────────── */
QPushButton[objectName^="PaletteBtn_"] {{
    background-color: #1A1A1A;
    color: #aaa;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
    padding: 4px 6px;
    min-width: 38px;
    min-height: 32px;
    outline: none;
}}
QPushButton[objectName^="PaletteBtn_"]:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton[objectName^="PaletteBtn_"]:hover {{
    background-color: {p_active_bg};
    border-color: {primary};
    color: {p_hover};
}}
QPushButton[objectName^="PaletteBtn_"]:pressed {{
    background-color: {primary};
    color: #fff;
}}

/* ─── PalettePanel / PaletteTitle ──────────────────────────────────────────── */
QFrame#PalettePanel {{
    background: #161616;
    border: 1px solid #252525;
    border-radius: 8px;
}}
QLabel#PaletteTitle {{
    color: #666;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 3px;
    margin-left: 2px;
    background: transparent;
    border: none;
}}

/* ─── PaletteScroll (горизонтальный серый скроллбар) ──────────────────────── */
QScrollArea#PaletteScroll {{
    background: transparent;
    border: none;
    outline: none;
}}
QScrollArea#PaletteScroll QWidget {{
    background: transparent;
    border: none;
    outline: none;
}}
QScrollArea#PaletteScroll QWidget#qt_scrollarea_viewport {{
    background: transparent;
    border: none;
}}

/* ─── DnD-состояние скролл-области ────────────────────────────────────────── */
QScrollArea[drag_active="true"] {{
    border: 2px solid {primary};
    outline: none;
}}

/* ─── Контентные зоны ──────────────────────────────────────────────────────── */
QWidget#TimelineContent {{
    background: #0d0d0d;
}}
QWidget#PaletteContent {{
    background: transparent;
}}
QFrame#MacroListPanel,
QFrame#ComboBuilder,
QFrame#MacroControlPanel {{
    background: #0d0d0d;
    border: 1px solid #1e1e1e;
    border-radius: 5px;
    outline: none;
}}
QFrame#MacroListPanel:focus,
QFrame#ComboBuilder:focus,
QFrame#MacroControlPanel:focus {{
    outline: none;
    border: 1px solid #1e1e1e;
}}

/* ─── AddStepBtn ───────────────────────────────────────────────────────────── */
QPushButton#AddStepBtn {{
    background: #0d0d0d;
    color: #444;
    border: 1px dashed #333;
    border-radius: 5px;
    font-size: 10px;
    font-weight: bold;
    outline: none;
}}
QPushButton#AddStepBtn:focus {{
    outline: none;
    border: 1px dashed #333;
}}
QPushButton#AddStepBtn:hover {{
    border-color: {primary};
    color: {primary};
    background: {p_active_bg};
}}

/* ─── Скроллбар палитры (серый) ────────────────────────────────────────────── */
QScrollArea#PaletteScroll QScrollBar:horizontal {{
    border: none;
    background: transparent;
    height: 8px;
    margin: 0;
}}
QScrollArea#PaletteScroll QScrollBar::handle:horizontal {{
    background: #444;
    min-width: 20px;
    border-radius: 4px;
}}
QScrollArea#PaletteScroll QScrollBar::handle:horizontal:hover {{
    background: #666;
}}
QScrollArea#PaletteScroll QScrollBar::add-line:horizontal,
QScrollArea#PaletteScroll QScrollBar::sub-line:horizontal {{
    width: 0;
    height: 0;
}}
QScrollArea#PaletteScroll QScrollBar::add-page:horizontal,
QScrollArea#PaletteScroll QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* ─── Macro Editor ───────────────────────────────────────────────────────────── */

/* Строка макроса — единый цельный блок */
QFrame#MacroRowFrame {{
    background-color: #121212;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    margin-bottom: 4px;
}}
QFrame#MacroRowFrame:hover {{
    border-color: #3a3a3a;
}}

/* Таймлайн — тёмная вставка внутри строки */
QFrame#TimelineFrame {{
    background-color: #0d0d0d;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
}}
QFrame#TimelineFrame:focus {{
    outline: none;
    border: 1px solid #1e1e1e;
}}

/* Всё внутри таймлайна прозрачно */
QScrollArea#TimelineScroll,
QWidget#TimelineViewport,
QWidget#TimelineContent {{
    background: transparent;
    border: none;
    outline: none;
}}
QFrame#TimelineFrame QWidget {{
    background: transparent;
}}

#MacroNameInput {{
    background: transparent;
    color: #cccccc;
    font-weight: bold;
    border: none;
    padding-left: 10px;
}}
#MacroNameInput:focus {{
    color: #c2c2c2;
    background: #000000;
    border-radius: 4px;
}}

/* ─── Timeline area — всё прозрачное, фон берётся от MacroRowFrame ─── */
/* ─── Timeline: полная изоляция слоёв ────────────────────────────────── */

/* ─── MacroBindBtn ──────────────────────────────────────────────────────────── */
QPushButton#MacroBindBtn {{
    background-color: #1A1A1A;
    color: #FFF;
    border: 1px solid #333;
    border-radius: 4px;
    font-size: 12px;
    min-height: 30px;
    outline: none;
}}
QPushButton#MacroBindBtn:focus {{
    outline: none;
    border: 1px solid #333;
}}
QPushButton#MacroBindBtn:hover {{
    border: 2px solid {primary};
    background-color: #252525;
    color: {primary};
}}
QPushButton#MacroBindBtn:pressed {{
    background-color: {primary};
    color: #c2c2c2;
}}
QPushButton#MacroBindBtn[capturing="true"] {{
    background-color: {primary};
    border: 1px solid #c2c2c2;
    color: #c2c2c2;
}}
QPushButton#MacroBindBtn[capturing="true"]:focus {{
    outline: none;
    border: 1px solid #c2c2c2;
}}

/* ─── MacroClearAllBtn ──────────────────────────────────────────────────────── */
QPushButton#MacroClearAllBtn {{
    background-color: #0A0A0A;
    color: {primary};
    font-size: 10px;
    font-weight: bold;
    border-width: 1px;
    border-style: solid;
    border-color: {primary};
    border-radius: 4px;
    outline: none;
}}
QPushButton#MacroClearAllBtn:hover {{
    background-color: {p_active_bg};
    border-color: {p_hover};
    color: {p_hover};
}}
QPushButton#MacroClearAllBtn:pressed {{
    background-color: {primary};
    color: #c2c2c2;
}}

/* ─── MacroDelBtn ───────────────────────────────────────────────────────────── */
QPushButton#MacroDelBtn {{
    background-color: #0A0A0A;
    color: {secondary};
    font-size: 10px;
    font-weight: bold;
    border-width: 1px;
    border-style: solid;
    border-color: {secondary};
    border-radius: 4px;
    outline: none;
    min-height: 28px;
}}
QPushButton#MacroDelBtn:hover {{
    background-color: {s_active_bg};
    border-color: {s_hover};
    color: #c2c2c2;
}}
QPushButton#MacroDelBtn:pressed {{
    background-color: {secondary};
    color: #c2c2c2;
}}

/* ─── Иконки кнопок в MacroStepWidget ──────────────────────────────────────── */
QLabel#BtnKeyIcon {{
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 4px;
}}
QLabel#BtnKeyFallback {{
    color: #00ffcc;
    font-size: 10px;
    font-weight: bold;
    background: #1a1a1a;
    border-radius: 4px;
}}

/* ─── AddMacroRow ───────────────────────────────────────────────────────────── */
QFrame#AddMacroRow {{
    background: #0d0d0d;
    border: 2px dashed #222;
    border-radius: 8px;
    margin-top: 10px;
}}
QFrame#AddMacroRow:hover {{
    border-color: #444;
    background: #0f0f0f;
}}
QFrame#AddMacroRow QLabel {{
    color: #333;
    font-weight: bold;
    font-size: 15px;
    letter-spacing: 1px;
}}

/* ─── Macro Slot buttons (Neon Style) ─────────────────────────────────── */
QPushButton[objectName^="Slot_Macro_"] {{
    background-color: #111111;
    color: #888888;
    border: 1px solid #333333;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}}
QPushButton[objectName^="Slot_Macro_"]:hover {{
    background-color: #151515;
    border: 2px solid {primary};
    color: {primary};
}}
QPushButton[objectName^="Slot_Macro_"][capturing="true"] {{
    background-color: {primary};
    color: #c2c2c2;
    border: 2px solid #c2c2c2;
}}
QPushButton#Slot_Macro_0, QPushButton#Slot_Macro_1,
QPushButton#Slot_Macro_2, QPushButton#Slot_Macro_3,
QPushButton#Slot_Macro_4, QPushButton#Slot_Macro_5 {{
    background-color: #111111;
    color: #888888;
    border: 2px solid #444444;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}}
QPushButton[objectName^="Slot_Macro_"]:hover {{
    background-color: #151515;
    border: 2px solid {primary} !important;
    color: {primary} !important;
}}

/* ─── Универсальные диалоговые окна ─────────────────────────────────────────── */
QDialog {{
    background-color: #0F0F0F;
    border: 2px solid {primary};
    border-radius: 12px;
}}
QDialog QLabel {{
    color: white;
    background: transparent;
    border: none;
}}
QDialog QLineEdit {{
    background-color: #1A1A1A;
    color: {primary};
    border: 1px solid #333;
    padding: 8px;
    border-radius: 6px;
}}
QDialog QPushButton {{
    background-color: #222;
    color: white;
    border-radius: 6px;
    padding: 8px 15px;
    border: 1px solid #444;
    font-weight: bold;
}}
QDialog QPushButton:hover {{
    background-color: {primary};
    color: white;
    border-color: white;
}}

/* ─── QMenu / TrayMenu ─────────────────────────────────────────────── */
QMenu {{
    background-color: #0b0b0b;
    border: 1px solid {primary};
    border-radius: 4px;
    padding: 4px;
    color: white;
}}
QMenu::item {{
    background-color: transparent;
    padding: 6px 30px 6px 20px;
    color: white;
    border-radius: 2px;
}}
QMenu::item:selected {{
    background-color: {primary};
    color: white;
}}
QMenu::item:pressed {{
    background-color: {primary};
    color: white;
}}
QMenu::separator {{
    height: 1px;
    background: #333333;
    margin: 4px 10px;
}}

/* ─── DonateBtn ──────────────────────────────────────────────────────────────── */
QPushButton#DonateBtn {{
    background-color: transparent;
    color: {secondary};
    border: 1px solid {secondary};
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
}}
QPushButton#DonateBtn:hover {{ background-color: {secondary}; color: white; }}

/* ─── Окно доната ────────────────────────────────────────────────────────────── */
QFrame#DonateContentFrame {{
    background-color: #0d0d0d;
    border: 2px solid {secondary};
    border-radius: 12px;
}}
QFrame#DonateContentFrame QLabel {{
    color: #666666;
    font-size: 20px;
    font-weight: bold;
    text-transform: uppercase;
    background: transparent;
    border: none;
}}

/* Исключения — заголовки не наследуют стиль QLabel внутри DonateContentFrame */
QFrame#DonateContentFrame QLabel#DonateIcon {{
    font-size: 32px;
    color: inherit;
}}
QFrame#DonateContentFrame QLabel#DonateHeaderEn,
QFrame#DonateContentFrame QLabel#DonateHeaderRu {{
    font-size: 14px;
    color: #adadad;
    letter-spacing: 1px;
}}
QFrame#DonateContentFrame QLabel#DonateWalletLabel {{
    font-size: 14px;
    color: #666666;
    letter-spacing: normal;
}}
QFrame#DonateContentFrame QLineEdit {{
    background-color: #050505;
    color: #adadad;
    border: 1px solid #222222;
    border-radius: 5px;
    padding: 8px;
    font-family: 'Consolas', 'Monospace';
    font-size: 12px;
}}
QFrame#DonateContentFrame QLineEdit:hover {{
    border: 1px solid {secondary};
    color: #ffffff;
}}
QPushButton#CloseDonateBtn {{
    background-color: #1a1a1a;
    color: #adadad;
    border: 1px solid #333333;
    border-radius: 4px;
    padding: 6px 20px;
    font-weight: bold;
    font-size: 11px;
}}
QPushButton#CloseDonateBtn:hover {{
    background-color: {s_active_bg}; 
    color: {secondary};
    border: 1px solid {secondary};
}}
QPushButton#CloseDonateBtn:pressed {{
    background-color: {s_active_bg};
}}

/* ─── Donate dialog labels ────────────────────────────────────────────────────── */
QLabel#DonateIcon {{
    font-size: 32px; 
    background: transparent; 
    border: none;
}}
QLabel#DonateHeaderEn,
QLabel#DonateHeaderRu {{
    font-weight: bold; 
    font-size: 14px; 
    color: #adadad; 
    letter-spacing: 1px; 
    border: none; 
    background: transparent;
}}

/* ─── Прочее ─────────────────────────────────────────────────────────────────── */
QLabel#SettingsInfo {{ color: #888; font-size: 11px; background: transparent; }}

QLabel#DialogTitle, QLabel#SettingsTitle {{
    color: {primary};
    font-weight: bold;
    font-size: 16px;
}}
QLabel#DialogInfo {{ color: #BBB; font-size: 13px; }}
"""


PROJECT_NAME = "Omni-Controller"
VERSION = "v3.1"
APP_ICON = resource_path("Omni-Controller.ico")

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
            # Масштабируем иконку (например, 52x52)
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
    "APPS": 0x5D,
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
    0x51: "PAGEDOWN",
    0xD2: "INSERT",
    0xD3: "DELETE",
    0x1D: "RCTRL",
    0x38: "RALT",
    0x1C: "NUM_ENTER",
    0x35: "NUM_DIVIDE",
    0x5B: "LWIN",
    0x5C: "RWIN",
    0x5D: "APPS",
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


# Стилизованный диалог ввода текста. Принимает цвета темы от родителя и применяет к себе глобальный QSS.
class CustomInputDialog(QDialog):
    def __init__(self, title, label_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedWidth(400)

        p_color = (
            parent.primary_color if hasattr(parent, "primary_color") else "#0078D7"
        )
        s_color = (
            parent.secondary_color if hasattr(parent, "secondary_color") else "#E72E2E"
        )

        self.setStyleSheet(get_stylesheet(p_color, s_color))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        title_lbl = QLabel(title.upper())
        title_lbl.setObjectName("DialogTitle")
        layout.addWidget(title_lbl, alignment=Qt.AlignCenter)

        self.label = QLabel(label_text)
        self.label.setObjectName("DialogInfo")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setMinimumHeight(35)
        self.input_field.setPlaceholderText("Enter name...")
        layout.addWidget(self.input_field)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("CONFIRM")
        self.cancel_btn = QPushButton("CANCEL")

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


# Layout с автопереносом элементов при нехватке ширины. Используется в палитре кнопок макросов.
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




VECTOR_CONFLICTS = {
    "LS_UP": "LS_DOWN", "LS_DOWN": "LS_UP",
    "LS_LEFT": "LS_RIGHT", "LS_RIGHT": "LS_LEFT",
    "RS_UP": "RS_DOWN", "RS_DOWN": "RS_UP",
    "RS_LEFT": "RS_RIGHT", "RS_RIGHT": "RS_LEFT",
}


def parse_macro_seq(s: str) -> list:
    """Парсит строку шагов макроса в список словарей.

    Новый формат  (секунды, float):  [A,B;0.100],[X;0.050]
    Старый формат (миллисекунды):    [A,B], 50, [X], 80   — обратная совместимость
    """
    import re
    result = []
    s = s.strip()
    if not s:
        return result

    if ";" in s:
        for m in re.finditer(r"\[([^\]]+)\]", s):
            content = m.group(1)
            if ";" in content:
                btn_part, delay_part = content.rsplit(";", 1)
            else:
                btn_part, delay_part = content, "0.1"
            buttons = [b.strip().upper() for b in btn_part.split(",") if b.strip()]
            try:
                delay = max(0.0, min(float(delay_part.strip()), 10.0))
            except ValueError:
                delay = 0.1
            if buttons:
                result.append({"buttons": buttons, "delay_after": delay})
        return result

    tokens = [t.strip() for t in s.split("],")]
    next_delay = 0.1
    for tok in tokens:
        tok = tok.strip().lstrip("[")
        parts = [p.strip() for p in tok.split(",")]
        buttons = []
        delay_override = None
        for p in parts:
            if not p:
                continue
            if p.isdigit():
                delay_override = int(p) / 1000.0   # мс → сек
            else:
                buttons.append(p.upper())
        if delay_override is not None:
            next_delay = delay_override
        if buttons:
            result.append({"buttons": buttons, "delay_after": next_delay})
            next_delay = 0.1
    return result


def serialize_macro_seq(steps: list) -> str:
    """Сериализует список шагов → '[A,B;0.100],[X;0.050]'."""
    parts = []
    for step in steps:
        buttons_str = ",".join(step["buttons"])
        try:
            delay = float(step.get("delay_after", 0.1))
        except (TypeError, ValueError):
            delay = 0.1
        parts.append(f"[{buttons_str};{delay:.3f}]")
    return ",".join(parts)


# Виджет одной строки макроса: имя, кнопка бинда, таймлайн шагов, кнопки CLEAR и DELETE. Поддерживает DnD-добавление кнопок из палитры.
class MacroRowWidget(QFrame):
    """Строка макроса: [Icon] + [Name] + [Bind Slot] + [Timeline] + [Delete]."""
    selected = Signal(int)
    name_changed = Signal(int, str)
    changed = Signal()
    bind_requested = Signal(int)
    delete_requested = Signal(int)
    steps_changed = Signal(int, list) # Сигнал при изменении шагов внутри строки
    bind_cleared = Signal(int) # Сигнал для очистки макроса по правому клику

    def __init__(self, idx: int, name: str, bind: str, steps: list = None, is_active: bool = False, p_color="#0078D7", s_color="#E74C3C", parent=None):
        super().__init__(parent)
        self.mw = parent
        self.idx = idx
        self.macro_steps = steps or []
        
        self._p_color = p_color
        self._s_color = s_color
        
        self.setObjectName("MacroRowFrame")
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAcceptDrops(True)
        self.setMinimumHeight(108)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)

        self.main_lay = QHBoxLayout(self)
        self.main_lay.setContentsMargins(10, 8, 10, 8)
        self.main_lay.setSpacing(8)

        left_widget = QWidget()
        left_widget.setFixedWidth(160)
        left_widget.setFocusPolicy(Qt.NoFocus)
        left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(12, 10, 8, 10)
        left_lay.setSpacing(6)
        left_lay.setAlignment(Qt.AlignVCenter)

        self.name_input = QLineEdit(name)
        self.name_input.setObjectName("MacroNameInput")
        self.name_input.setFocusPolicy(Qt.ClickFocus)
        self.name_input.editingFinished.connect(self._on_rename)
        left_lay.addWidget(self.name_input)

        self.bind_btn = QPushButton(bind or "NONE")
        self.bind_btn.setObjectName("MacroBindBtn")
        self.bind_btn.setFocusPolicy(Qt.NoFocus)
        self.bind_btn.setFixedHeight(30)
        self.bind_btn.clicked.connect(lambda: self.bind_requested.emit(self.idx))
        self.bind_btn.installEventFilter(self)
        left_lay.addWidget(self.bind_btn)

        self.main_lay.addWidget(left_widget)

        self.tl_frame = QFrame()
        self.tl_frame.setObjectName("TimelineFrame")
        self.tl_frame.setFocusPolicy(Qt.NoFocus)
        self.tl_frame.setAttribute(Qt.WA_StyledBackground, True)
        self.tl_frame.setMinimumWidth(400)
        self.tl_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        tl_frame_lay = QVBoxLayout(self.tl_frame)
        tl_frame_lay.setContentsMargins(5, 5, 5, 5)
        tl_frame_lay.setSpacing(0)

        self.tl_scroll = QScrollArea()
        self.tl_scroll.setObjectName("TimelineScroll")
        self.tl_scroll.setWidgetResizable(True)
        self.tl_scroll.setFocusPolicy(Qt.NoFocus)
        self.tl_scroll.setFrameShape(QFrame.NoFrame)
        self.tl_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tl_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tl_scroll.setAttribute(Qt.WA_StyledBackground, True)
        self.tl_scroll.viewport().setAutoFillBackground(False)
        self.tl_scroll.viewport().setObjectName("TimelineViewport")

        self.tl_content = QWidget()
        self.tl_content.setObjectName("TimelineContent")
        self.tl_content.setAttribute(Qt.WA_StyledBackground, True)
        self.tl_content.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.tl_layout = QGridLayout(self.tl_content)
        self.tl_layout.setContentsMargins(4, 4, 4, 4)
        self.tl_layout.setHorizontalSpacing(6)
        self.tl_layout.setVerticalSpacing(8)
        self.tl_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.tl_scroll.setWidget(self.tl_content)
        tl_frame_lay.addWidget(self.tl_scroll)
        self.main_lay.addWidget(self.tl_frame)

        right_widget = QWidget()
        right_widget.setFixedWidth(88)
        right_widget.setFocusPolicy(Qt.NoFocus)
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(8, 10, 12, 10)
        right_lay.setSpacing(6)
        right_lay.setAlignment(Qt.AlignTop)

        self.clear_all_btn = QPushButton("CLEAR")
        self.clear_all_btn.setObjectName("MacroClearAllBtn")
        self.clear_all_btn.setFixedHeight(28)
        self.clear_all_btn.clicked.connect(self._clear_all_steps)

        self.del_btn = QPushButton("DELETE")
        self.del_btn.setObjectName("MacroDelBtn")
        self.del_btn.setFixedHeight(28)
        self.del_btn.clicked.connect(lambda: self.delete_requested.emit(self.idx))

        right_lay.addWidget(self.clear_all_btn)
        right_lay.addWidget(self.del_btn)
        right_lay.addStretch()

        self.main_lay.addWidget(right_widget)

        self._load_steps()
        self.update_style()

    def eventFilter(self, obj, event):
        if obj == self.bind_btn and event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.RightButton:
                self.bind_btn.setText("NONE")
                
                self.bind_cleared.emit(self.idx)
                
                return True
                
        return super().eventFilter(obj, event)

    def _clear_all_steps(self):
        """
        Полная очистка таймлайна.

        Только локальные данные — никакого self.mw.
        Внешний мир узнаёт об очистке через steps_changed.
        """
        if not self.macro_steps:
            return

        self.macro_steps.clear()

        self.setFixedHeight(108)

        self._load_steps()

        QTimer.singleShot(200, lambda: self.setMinimumHeight(108))
        QTimer.singleShot(200, lambda: self.setMaximumHeight(118))

        self.steps_changed.emit(self.idx, self.macro_steps)
        self.changed.emit()
        self.updateGeometry()
    
    def update_style(self, new_primary=None, new_secondary=None):
        """
        Обновление цветов. Стили берутся из глобального _QSS_TEMPLATE,
        здесь только сохраняем цвета и перерисовываем виджет.
        """
        if new_primary is not None:
            self._p_color = new_primary
        if new_secondary is not None:
            self._s_color = new_secondary

        self.style().unpolish(self)
        self.style().polish(self)
        
        for child in self.findChildren(QPushButton):
            child.style().unpolish(child)
            child.style().polish(child)
            
        self.update()

    def _on_rename(self):
        """Переименование макроса через сигнал — без прямого self.mw."""
        new_name = self.name_input.text().strip()
        if new_name:
            self.name_changed.emit(self.idx, new_name)
        self.name_input.clearFocus()

    def adjust_row_height(self):
        """Динамически подгоняет высоту, исключая появление скроллбаров."""
        if not self.macro_steps:
            self.setFixedHeight(108)
            self.setMaximumHeight(118)
            self.updateGeometry()
            return

        self.tl_layout.activate()
        content_h = self.tl_layout.sizeHint().height()
        
        base_h = max(108, content_h + 45)
        
        self.setMinimumHeight(base_h)
        self.setMaximumHeight(base_h + 10) 
        
        self.base_h = base_h 
        self.updateGeometry()

    def _load_steps(self):
        """ Ядерная очистка + перерисовка таймлайна с нуля. """
        self._rebuilding = True
        try:
            self._load_steps_inner()
        finally:
            self._rebuilding = False

    def _load_steps_inner(self):
        for di in getattr(self, '_delay_refs', []):
            if di is not None:
                di.blockSignals(True)

        while self.tl_layout.count():
            item = self.tl_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.hide()
                w.setParent(None)
                w.deleteLater()

        self._step_refs:  list = []
        self._delay_refs: list = []

        max_cols = 6
        total    = len(self.macro_steps)

        for i, step in enumerate(self.macro_steps):
            grid_row = i // max_cols
            grid_col = i % max_cols

            step_container = QWidget()
            step_container.setContentsMargins(0, 0, 0, 0)
            step_container.setFocusPolicy(Qt.NoFocus)

            container_lay = QHBoxLayout(step_container)
            container_lay.setContentsMargins(0, 0, 0, 0)
            container_lay.setSpacing(5)
            container_lay.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            sw = MacroStepWidget(i, step.get("buttons", []))
            sw.setFocusPolicy(Qt.NoFocus)
            sw.removed.connect(self._on_step_removed)
            sw.changed.connect(self._sync_steps_to_data)
            container_lay.addWidget(sw)
            self._step_refs.append(sw)

            if i < total - 1:
                raw = step.get("delay_after", 0.1)
                try:
                    delay_sec = float(raw)
                except (TypeError, ValueError):
                    delay_sec = 0.1
                di = StepDelayInput(delay_sec)
                di.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                di.textChanged.connect(self._sync_steps_to_data)
                container_lay.addWidget(di)
                self._delay_refs.append(di)
            else:
                ph = QWidget()
                ph.setFixedSize(40, 18)
                ph.setFocusPolicy(Qt.NoFocus)
                container_lay.addWidget(ph)
                self._delay_refs.append(None)

            self.tl_layout.addWidget(step_container, grid_row, grid_col,
                                     Qt.AlignLeft | Qt.AlignVCenter)

        for _c in range(max_cols):
            self.tl_layout.setColumnStretch(_c, 0)

        QTimer.singleShot(50, self.adjust_row_height)

    def _on_step_removed(self, payload):
        """
        Безопасное удаление шага по сигналу MacroStepWidget.removed.

        payload = ("delete", sw) — sw это ссылка на виджет шага.

        Алгоритм:
          1. Ищем sw в self._step_refs по идентичности объекта (is, не ==),
             чтобы не зависеть от реализации __eq__ у MacroStepWidget.
          2. Удаляем запись из self.macro_steps (данные).
          3. Полная перерисовка через _load_steps() — она сама сделает
             ядерную очистку и пересоздаст все виджеты с правильными индексами.
          4. Уведомляем родителя через steps_changed.
        """
        _action, sw = payload

        target_idx = next(
            (i for i, ref in enumerate(self._step_refs) if ref is sw),
            None,
        )
        if target_idx is None:
            return

        if 0 <= target_idx < len(self.macro_steps):
            self.macro_steps.pop(target_idx)

        self._load_steps()

        self.steps_changed.emit(self.idx, self.macro_steps)

    def _sync_steps_to_data(self):
        """
        Пересобирает self.macro_steps из текущего состояния виджетов.

        Не трогает layout — использует self._step_refs и self._delay_refs,
        которые _load_steps() актуализирует при каждой перерисовке.
        Этот метод вызывается только при изменении значений (delay, кнопки),
        без визуальной перестройки.
        """
        if getattr(self, '_rebuilding', False):
            return
        new_steps = []
        for i, sw in enumerate(self._step_refs):
            delay_ref = self._delay_refs[i] if i < len(self._delay_refs) else None
            if isinstance(delay_ref, StepDelayInput):
                delay = delay_ref.get_delay()
            else:
                delay = self.macro_steps[i]["delay_after"] if i < len(self.macro_steps) else 0.1
            new_steps.append({
                "buttons":     list(sw.buttons),
                "delay_after": delay,
            })
        self.macro_steps = new_steps
        self.steps_changed.emit(self.idx, self.macro_steps)

    def update_appearance(self, is_dragging: bool):
        """Подсвечивает строку, когда над ней тащат кнопку."""
        self.setProperty("drag_over", "true" if is_dragging else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
            self.update_appearance(True)

    def dragLeaveEvent(self, event):
        self.update_appearance(False)
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        """
        Дроп на пустую область таймлайна (мимо шагов):
        - plain text (палитра) → сразу новый шаг
        - "MacroStep:BTN" (из другого шага) → откладываем добавление до тех пор,
          пока источник не удалит кнопку из своего шага (_finalize_move),
          иначе кнопка дублируется в обоих шагах.
        """
        self.update_appearance(False)
        txt = event.mimeData().text()

        is_step_move = txt.startswith("MacroStep:")
        btn_key = txt[len("MacroStep:"):] if is_step_move else txt

        if is_step_move:
            self._pending_drop_btn = btn_key
            event.setDropAction(Qt.MoveAction)
            event.accept()
            QTimer.singleShot(0, self._reload_after_move)
        else:
            self.macro_steps.append({"buttons": [btn_key], "delay_after": 0.1})
            self._load_steps()
            self.steps_changed.emit(self.idx, self.macro_steps)
            self.changed.emit()
            event.acceptProposedAction()

    def _reload_after_move(self):
        """
        Вызывается через QTimer после MoveAction-дропа.
        К этому моменту _finalize_move уже отработал и удалил кнопку
        из исходного шага (или весь шаг, если он опустел).
        Теперь безопасно добавляем новый шаг и перерисовываем.
        """
        btn_key = getattr(self, "_pending_drop_btn", None)
        self._pending_drop_btn = None
        if btn_key:
            self.macro_steps.append({"buttons": [btn_key], "delay_after": 0.1})
        self._load_steps()
        self.steps_changed.emit(self.idx, self.macro_steps)
        self.changed.emit()

    def focusInEvent(self, event):
        """Перехватываем получение фокуса — не даём Qt рисовать системную рамку."""
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.selected.emit(self.idx)
        super().mousePressEvent(event)


# Кнопка добавления нового макроса. Располагается в конце списка и эмитит сигнал в MacrosEditorWidget.
class AddMacroRow(QFrame):
    """Строка-кнопка 'ADD MACROS'."""
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AddMacroRow")
        lay = QVBoxLayout(self)
        lbl = QLabel("ADD MACROS")
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


# Кнопка палитры с поддержкой DnD на таймлайн. Отображает иконку кнопки геймпада и визуальный pressed-эффект.
class PaletteBtn(QPushButton):
    """Кнопка палитры. Поддерживает перетаскивание на таймлайн."""

    def __init__(self, gp_key: str, parent=None):
        super().__init__(gp_key, parent)
        self.gp_key = gp_key
        self.setObjectName(f"PaletteBtn_{gp_key}")
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.OpenHandCursor)
        
        icon_subpath = BUTTON_ICONS.get(gp_key)
        if icon_subpath:
            full_icon_path = os.path.join(ICONS_PATH, icon_subpath)
            if os.path.exists(full_icon_path):
                self.setIcon(QIcon(full_icon_path))
                self.setIconSize(QSize(32, 32))
                self.setText("")
                self.setToolTip(gp_key)

    def focusInEvent(self, event):
        """Полностью игнорим фокус, чтобы не было рамок."""
        self.clearFocus()
        event.ignore()

    def _set_pressed(self, val: bool):
        if val:
            mw = self.window()
            p = getattr(mw, 'primary_color', '#0078D7')
            self.setStyleSheet(
                f'QPushButton {{ background-color: {p}; color: #000; }}'
            )
        else:
            self.setStyleSheet("")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.position().toPoint()
            self._set_pressed(True)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._set_pressed(False)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.position().toPoint() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        self._set_pressed(False)

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.gp_key)
        drag.setMimeData(mime)

        pix = self.grab()
        drag.setPixmap(pix)
        drag.setHotSpot(event.position().toPoint())

        self.setDown(False)
        self.update()

        drag.exec(Qt.MoveAction | Qt.CopyAction)

        QTimer.singleShot(50, lambda: (self.setDown(False), self.update()))


# Поле задержки между шагами таймлайна (в секундах). Поддерживает ввод, валидацию и изменение колесом мыши.
class StepDelayInput(QLineEdit):
    """Поле задержки между шагами таймлайна.

    • Значение в секундах (float): «0.1», «0.05», «2.0»
    • По умолчанию 0.1 с.
    • Валидация QDoubleValidator 0.0–10.0, 3 знака.
    • Стиль: безрамочный, transparent bg, цвет primary из QSS.
    """

    def __init__(self, delay_sec: float = 0.1, parent=None):
        super().__init__(parent)
        self.setObjectName("StepDelayInput")
        self.setAlignment(Qt.AlignCenter)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setFixedWidth(46)
        self.setMaxLength(6)
        self.editingFinished.connect(self._on_editing_finished)
        self.setFixedHeight(22)

        validator = QDoubleValidator(0.0, 10.0, 3, self)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.setValidator(validator)

        self.setText(f"{delay_sec:.3g}")
        self.setToolTip("Задержка перед следующим шагом (сек)")
        self.setFixedWidth(40)  # Сделаем чуть уже для плотности
        self.setFixedHeight(18) # Фиксируем высоту, чтобы не раздувало ряд
        self.setContentsMargins(0, 0, 0, 0)

    def _on_editing_finished(self):
        """Очистка текста и приведение к красивому виду при потере фокуса."""
        text = self.text().replace(',', '.')
        try:
            val = float(text)
            val = max(0.0, min(val, 10.0))
            self.setText(f"{val:.3g}")
        except ValueError:
            self.setText("0.1")
            
    def wheelEvent(self, event):
        """БОНУС: изменение задержки колесиком мыши (шаг 0.05)."""
        current_val = self.get_delay()
        delta = 0.05 if event.angleDelta().y() > 0 else -0.05
        new_val = max(0.0, min(current_val + delta, 10.0))
        self.setText(f"{new_val:.2f}")
        self.textChanged.emit(self.text()) # Чтобы макрос сразу узнал об изменении
    
    def get_delay(self) -> float:
        """Возвращает delay в секундах. 0.1 только если поле пустое или сломано."""
        text = self.text().strip().replace(",", ".")
        if not text:
            return 0.1
        try:
            val = float(text)
            return max(0.0, min(val, 10.0))
        except ValueError:
            return 0.1


# Один шаг таймлайна — контейнер для набора кнопок геймпада. Поддерживает DnD-слияние и удаление.
class MacroStepWidget(QFrame):
    """Один шаг в таймлайне макроса. Принимает кнопки через DnD."""

    removed = Signal(object)   # сигнал «удалить этот шаг»
    changed = Signal()          # сигнал «данные изменились»

    def __init__(self, idx: int, buttons: list = None, parent=None):
        super().__init__(parent)
        self.idx = idx
        self.buttons: list = buttons or []
        self.setObjectName(f"MacroStep_{idx}")
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.base_h = 86
        self.setMinimumSize(72, self.base_h)
        self.setMinimumHeight(self.base_h) # Вместо setFixedHeight
        self.setMaximumWidth(200)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(6, 6, 6, 6)
        self._layout.setSpacing(4)

        self._grid_widget = QWidget()
        self._grid_widget.setMouseTracking(True)
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(4)
        self._layout.addWidget(self._grid_widget, alignment=Qt.AlignCenter)

        self._rebuild_labels()


    def _rebuild_labels(self):
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
                w.deleteLater()
            del item

        if not self.buttons:
            return

        for i, b_key in enumerate(self.buttons):
            row = i % 2
            col = i // 2
            
            lbl = QLabel()
            lbl.setProperty("btn_key", b_key)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(32, 32)
            
            icon_subpath = BUTTON_ICONS.get(b_key)
            icon_loaded = False
            
            if icon_subpath:
                full_icon_path = os.path.join(ICONS_PATH, icon_subpath)
                
                if os.path.exists(full_icon_path):
                    pix = QPixmap(full_icon_path)
                    if not pix.isNull():
                        pix = pix.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        lbl.setPixmap(pix)
                        lbl.setToolTip(b_key)
                        icon_loaded = True
                    else:
                        print(f"!!! ОШИБКА: Файл битый или не картинка: {full_icon_path}")
                else:
                    print(f"!!! ОШИБКА: Путь не найден: {full_icon_path}")

            if not icon_loaded:
                lbl.setText(b_key)
                lbl.setObjectName("BtnKeyFallback")  # стиль в _QSS_TEMPLATE QLabel#BtnKeyFallback
            else:
                lbl.setObjectName("BtnKeyIcon")       # стиль в _QSS_TEMPLATE QLabel#BtnKeyIcon

            self._grid_layout.addWidget(lbl, row, col)

        cols = (len(self.buttons) + 1) // 2
        new_width = max(72, cols * 38 + 12)
        self.setFixedWidth(new_width)


    def _is_out_of_bounds(self, global_pos) -> bool:
        """
        Проверяет, находится ли глобальная точка за пределами
        «зоны безопасности» таймлайна.

        Логика: ищем ближайший родительский MacroRowWidget и берём его
        глобальный прямоугольник. Если курсор ушёл дальше чем на 100px
        выше верхней или нижней границы строки — считаем это намеренным
        выбросом за борт.

        Это позволяет пользователю «вытащить» шаг из макроса, потянув
        его далеко вверх или вниз, без использования контекстного меню.
        """
        row_widget = self.parent()
        while row_widget is not None and not isinstance(row_widget, MacroRowWidget):
            row_widget = row_widget.parent()

        if row_widget is None:
            return False

        row_rect = row_widget.rect()
        top    = row_widget.mapToGlobal(row_rect.topLeft()).y()
        bottom = row_widget.mapToGlobal(row_rect.bottomLeft()).y()

        THRESHOLD = 100  # px за пределами строки = удаление
        return (global_pos.y() < top - THRESHOLD or
                global_pos.y() > bottom + THRESHOLD)

    def _finalize_move(self, removed_btn: str) -> None:
        """
        Завершает перемещение кнопки из этого шага.

        Вызывается после успешного drag.exec(MoveAction) или после броска
        за борт (_is_out_of_bounds). Убирает removed_btn из self.buttons.
        Если кнопок не осталось — шаг пустой, испускаем removed, чтобы
        MacroRowWidget удалил его из данных и перестроил UI.
        """
        if removed_btn in self.buttons:
            self.buttons.remove(removed_btn)

        if not self.buttons:
            self.removed.emit(("delete", self))
        else:
            self._rebuild_labels()
            self.changed.emit()

    def mouseReleaseEvent(self, event):
        """
        mouseRelease нужен только для обычных кликов (не DnD).
        Drag-удаление обрабатывается в mouseMoveEvent после drag.exec().
        """
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        
        if (event.position().toPoint() - self._drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        p = event.position().toPoint()
        child = self._grid_widget.childAt(self._grid_widget.mapFrom(self, p))
        
        if not (child and child.property("btn_key")):
            return 
            
        targeted_btn = child.property("btn_key")

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(f"MacroStep:{targeted_btn}") 
        
        pix = child.grab()
        drag.setMimeData(mime)
        drag.setPixmap(pix)
        drag.setHotSpot(QPoint(16, 16))

        child.hide() # Эффект фантома

        res = drag.exec(Qt.MoveAction | Qt.CopyAction)

        if res == Qt.MoveAction:
            self._finalize_move(targeted_btn)
        else:
            self._finalize_move(targeted_btn)

    def update_appearance(self, is_dragging: bool):
        """Управляет подсветкой рамки шага при Drag-and-Drop."""
        self.setProperty("drag_over", "true" if is_dragging else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            txt = event.mimeData().text()
            event.acceptProposedAction()
            self.update_appearance(True)

    def dragLeaveEvent(self, event):
        self.update_appearance(False)
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self.update_appearance(False)
        txt = event.mimeData().text()
        
        is_move = txt.startswith("MacroStep:")
        clean_btn = txt.replace("MacroStep:", "") if is_move else txt

        if clean_btn not in self.buttons:
            self.buttons.append(clean_btn)
            self._rebuild_labels()
            self.changed.emit()
            
            if is_move:
                event.setDropAction(Qt.MoveAction)
            event.accept()
    
    def contextMenuEvent(self, event):
        """Полностью отключаем контекстное меню для этого виджета."""
        event.accept()

    def focusInEvent(self, event):
        """Перехватываем фокус — не даём Qt рисовать системную рамку."""
        event.accept()


    def enterEvent(self, event):
        super().enterEvent(event)

    def leaveEvent(self, event):
        super().leaveEvent(event)


# Исполнитель макроса в фоновом потоке. Нажимает кнопки с заданными задержками, удерживает финальное состояние до KeyUp и не конфликтует с маппером.
class MacroRunner(QObject):
    sig_step = Signal(int)
    sig_done = Signal()

    _BTN_MAP: dict = None

    def __init__(self, steps: list, gamepad, lock, ithread=None, parent=None):
        super().__init__(parent)
        self.steps    = steps
        self.gamepad  = gamepad
        self.lock     = lock
        self._ithread = ithread   # InterceptionThread: даёт доступ к pressed_keys/bindings

        self._stop_event = threading.Event()
        self._worker: threading.Thread = None

    def start(self):
        if not self.steps:
            self.sig_done.emit()
            return
        self._stop_event.clear()
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def isRunning(self) -> bool:
        return self._worker is not None and self._worker.is_alive()

    def stop(self):
        """Прерывает ожидание между шагами. Отпускание кнопок — в _run через _release_set."""
        self._stop_event.set()

    def _run(self):
        active_buttons: set = set()
        btn_map = self._get_btn_map()
        total = len(self.steps)

        for i, step in enumerate(self.steps):
            if self._stop_event.is_set():
                break

            active_buttons.update(step.get("buttons", []))
            self.sig_step.emit(i)
            self._press_set(active_buttons, btn_map)

            if i < total - 1:
                raw = self.steps[i].get("delay_after", 0.1)
                try:
                    delay = max(0.0, min(float(raw), 10.0))
                except (TypeError, ValueError):
                    delay = 0.1
                if self._stop_event.wait(timeout=delay):
                    break

        else:
            self._stop_event.wait()

        self._release_set(active_buttons, btn_map)
        self.sig_done.emit()

    @classmethod
    def _get_btn_map(cls) -> dict:
        if cls._BTN_MAP is None:
            from vgamepad import XUSB_BUTTON as B
            cls._BTN_MAP = {
                "A":          B.XUSB_GAMEPAD_A,
                "B":          B.XUSB_GAMEPAD_B,
                "X":          B.XUSB_GAMEPAD_X,
                "Y":          B.XUSB_GAMEPAD_Y,
                "LB":         B.XUSB_GAMEPAD_LEFT_SHOULDER,
                "RB":         B.XUSB_GAMEPAD_RIGHT_SHOULDER,
                "DPAD_UP":    B.XUSB_GAMEPAD_DPAD_UP,
                "DPAD_DOWN":  B.XUSB_GAMEPAD_DPAD_DOWN,
                "DPAD_LEFT":  B.XUSB_GAMEPAD_DPAD_LEFT,
                "DPAD_RIGHT": B.XUSB_GAMEPAD_DPAD_RIGHT,
                "LTB":        B.XUSB_GAMEPAD_LEFT_THUMB,
                "RTB":        B.XUSB_GAMEPAD_RIGHT_THUMB,
                "START":      B.XUSB_GAMEPAD_START,
                "BACK":       B.XUSB_GAMEPAD_BACK,
                "GUIDE":      B.XUSB_GAMEPAD_GUIDE,
            }
        return cls._BTN_MAP

    def _press_set(self, buttons: set, btn_map: dict):
        """Нажимает кнопки текущего шага макроса.
        Не вызывает reset() — состояние маппера не трогается."""
        if not self.gamepad:
            return
        ls_x = ls_y = rs_x = rs_y = 0
        lt_val = rt_val = 0
        v = 32767
        with self.lock:
            for btn in buttons:
                if btn in btn_map:
                    self.gamepad.press_button(button=btn_map[btn])
                elif btn == "LT":       lt_val =  255
                elif btn == "RT":       rt_val =  255
                elif btn == "LS_UP":    ls_y   =  v
                elif btn == "LS_DOWN":  ls_y   = -v
                elif btn == "LS_LEFT":  ls_x   = -v
                elif btn == "LS_RIGHT": ls_x   =  v
                elif btn == "RS_UP":    rs_y   =  v
                elif btn == "RS_DOWN":  rs_y   = -v
                elif btn == "RS_LEFT":  rs_x   = -v
                elif btn == "RS_RIGHT": rs_x   =  v
            if lt_val:          self.gamepad.left_trigger(value=lt_val)
            if rt_val:          self.gamepad.right_trigger(value=rt_val)
            if ls_x or ls_y:    self.gamepad.left_joystick(x_value=ls_x, y_value=ls_y)
            if rs_x or rs_y:    self.gamepad.right_joystick(x_value=rs_x, y_value=rs_y)
            self.gamepad.update()

    def _release_set(self, buttons: set, btn_map: dict):
        """Отпускает кнопки макроса после завершения/прерывания.
        Кнопки, для которых физическая клавиша маппера всё ещё зажата, не трогаем."""
        if not self.gamepad or not buttons:
            return

        mapper_still_held: set = set()
        if self._ithread:
            pressed = getattr(self._ithread, 'pressed_keys', set())
            bindings = getattr(self._ithread, 'bindings', {})
            for gp_btn, keys in bindings.items():
                for k in keys:
                    if k != "NONE" and k in pressed:
                        mapper_still_held.add(gp_btn)
                        break

        need_ls = need_rs = False
        ls_axes = {"LS_UP", "LS_DOWN", "LS_LEFT", "LS_RIGHT"}
        rs_axes = {"RS_UP", "RS_DOWN", "RS_LEFT", "RS_RIGHT"}

        with self.lock:
            for btn in buttons:
                if btn in mapper_still_held:
                    continue
                if btn in btn_map:
                    self.gamepad.release_button(button=btn_map[btn])
                elif btn == "LT":              self.gamepad.left_trigger(value=0)
                elif btn == "RT":              self.gamepad.right_trigger(value=0)
                elif btn in ls_axes:           need_ls = True
                elif btn in rs_axes:           need_rs = True
            if need_ls and not mapper_still_held.intersection(ls_axes):
                self.gamepad.left_joystick(x_value=0, y_value=0)
            if need_rs and not mapper_still_held.intersection(rs_axes):
                self.gamepad.right_joystick(x_value=0, y_value=0)
            self.gamepad.update()


# Главный виджет вкладки MACROS: список строк макросов, палитра кнопок, захват бинда и управление MacroRunner.
class MacrosEditorWidget(QWidget):
    """Редактор макросов. Интегрируется как вкладка MACROS."""

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.mw = main_window
        self.macros: list = []      # [{name, bind, steps:[{buttons, delay_after}]}]
        self.macro_widgets: list = []
        self.current_macro_idx: int = -1
        self.runner = None # MacroRunner инициализируется позже

        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.NoFocus) 
        
        self._build_ui()


    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 15) 
        root.setSpacing(10)

        self.macro_scroll = QScrollArea()
        self.macro_scroll.setWidgetResizable(True)
        self.macro_scroll.setFocusPolicy(Qt.NoFocus)
        self.macro_scroll.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.macro_scroll.setContextMenuPolicy(Qt.NoContextMenu)
        self.macro_scroll.setObjectName("MacroListScroll")
        
        self.macro_scroll_content = QWidget()
        self.macro_scroll_content.setObjectName("MacroScrollContent")
        self.macro_scroll_content.setFocusPolicy(Qt.NoFocus)
        
        self.macro_scroll.viewport().setFocusPolicy(Qt.NoFocus)
        
        self.macro_vbox = QVBoxLayout(self.macro_scroll_content)
        self.macro_vbox.setContentsMargins(5, 5, 5, 5)
        self.macro_vbox.setSpacing(1)
        self.macro_vbox.setAlignment(Qt.AlignTop)
        self.macro_scroll.setWidget(self.macro_scroll_content)
        root.addWidget(self.macro_scroll, stretch=1)

        pal_frame = QFrame()
        pal_frame.setObjectName("PalettePanel")
        pal_frame.setFocusPolicy(Qt.NoFocus)
        pal_frame.setContextMenuPolicy(Qt.NoContextMenu)
        
        pal_lay = QVBoxLayout(pal_frame)
        pal_lay.setContentsMargins(10, 10, 10, 10) 
        pal_lay.setSpacing(8)

        pal_title = QLabel("PALETTE")
        pal_title.setObjectName("PaletteTitle")
        pal_lay.addWidget(pal_title)

        self.palette_scroll = QScrollArea()
        self.palette_scroll.setObjectName("PaletteScroll")
        
        self.palette_scroll.setFixedHeight(110) 
        self.palette_scroll.setWidgetResizable(True)
        self.palette_scroll.setFocusPolicy(Qt.NoFocus)
        self.palette_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.palette_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        pal_content = QWidget()
        pal_content.setObjectName("PaletteContent")
        pal_content.setFocusPolicy(Qt.NoFocus)
        
        self.pal_flow = FlowLayout(pal_content, margin=0, spacing=4)
        self.palette_scroll.setWidget(pal_content)
        pal_lay.addWidget(self.palette_scroll)

        root.addWidget(pal_frame)

        self._capturing_bind = False

        self._refresh_macro_list()
        self.fill_palette(GP_MAP_KEYS)

        for child in self.findChildren(QWidget):
            if isinstance(child, (QFrame, QScrollArea, QAbstractScrollArea)):
                allowed = (QLineEdit, QPushButton)
                if not isinstance(child, allowed):
                    child.setFocusPolicy(Qt.NoFocus)
                    child.setContextMenuPolicy(Qt.NoContextMenu) # УБИВАЕМ МЕНЮ ВЕЗДЕ
                    child.setAttribute(Qt.WA_MacShowFocusRect, False)

        for area in self.findChildren(QScrollArea):
            vp = area.viewport()
            if vp is not None:
                vp.setFocusPolicy(Qt.NoFocus)
                vp.setContextMenuPolicy(Qt.NoContextMenu)


    def fill_palette(self, all_keys):
        """Заполняет палитру кнопками через FlowLayout с иммунитетом к фокусу."""
        while self.pal_flow.count():
            item = self.pal_flow.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for key in all_keys:
            btn = PaletteBtn(key)
            btn.setFocusPolicy(Qt.NoFocus)
            btn.setAttribute(Qt.WA_MacShowFocusRect, False)
            self.pal_flow.addWidget(btn)


    def _refresh_macro_list(self):
        """Перестраивает вертикальный список строк макросов с передачей цветов."""
        while self.macro_vbox.count():
            item = self.macro_vbox.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.macro_widgets.clear()
        
        p_col = self.mw.primary_color if self.mw else "#0078D7"
        s_col = self.mw.secondary_color if self.mw else "#E74C3C"
        
        for i, m in enumerate(self.macros):
            is_active = (i == self.current_macro_idx)
            row = MacroRowWidget(
                i, m["name"], m["bind"], m.get("steps", []), 
                is_active, p_color=p_col, s_color=s_col
            )
            
            row.selected.connect(self._on_macro_selected)
            row.delete_requested.connect(self._del_macro)
            row.name_changed.connect(self._on_macro_name_changed)
            row.bind_requested.connect(self._start_capture_bind)
            row.steps_changed.connect(self._on_macro_steps_changed)
            row.bind_cleared.connect(self._clear_macro_bind)
            self.macro_vbox.addWidget(row)
            self.macro_widgets.append(row)

        add_row = AddMacroRow()
        add_row.clicked.connect(self._add_macro)
        self.macro_vbox.addWidget(add_row)

    def update_theme_colors(self, p_color: str, s_color: str) -> None:
        """
        Мост для проброса цветов от MainWindow.apply_theme() вниз к строкам.

        Алгоритм:
          1. Обновляем внутренние цвета редактора (используются при следующем
             вызове _refresh_macro_list — при добавлении/удалении макроса).
          2. Проходим по self.macro_widgets и вызываем update_style() у каждого.
             Список содержит только живые MacroRowWidget-ы (AddMacroRow туда
             не попадает — он добавляется в vbox, но не в macro_widgets).

        Безопасен при пустом списке макросов.
        """
        self._p_color = p_color
        self._s_color = s_color

        for row in self.macro_widgets:
            if hasattr(row, 'update_style'):
                row.update_style(p_color, s_color)

    def _on_macro_steps_changed(self, idx, new_steps):
        if 0 <= idx < len(self.macros):
            self.macros[idx]["steps"] = new_steps

    def _on_macro_name_changed(self, idx, new_name):
        if 0 <= idx < len(self.macros):
            self.macros[idx]["name"] = new_name
            self._sync_header_combo()

    def _sync_header_combo(self):
        """Синхронизирует комбобокс в хедере с текущим списком макросов."""
        if not hasattr(self.mw, "header_macro_combo"):
            return
        combo = self.mw.header_macro_combo
        combo.blockSignals(True)
        curr = combo.currentText()
        combo.clear()
        for m in self.macros:
            combo.addItem(m["name"])
        combo.setCurrentText(curr)
        combo.blockSignals(False)

    def _add_macro(self):
        name = f"Macro_{len(self.macros) + 1}"
        new_data = {"name": name, "bind": "", "steps": list()} 
        self.macros.append(new_data)
        idx = len(self.macros) - 1
        self.current_macro_idx = idx

        self.setUpdatesEnabled(False)
        
        p_col = self.mw.primary_color if self.mw else "#0078D7"
        s_col = self.mw.secondary_color if self.mw else "#E74C3C"
        
        row = MacroRowWidget(
            idx, name, "", [], 
            True, p_color=p_col, s_color=s_col
        )
        
        row.selected.connect(self._on_macro_selected)
        row.delete_requested.connect(self._del_macro)
        row.name_changed.connect(self._on_macro_name_changed)
        row.bind_requested.connect(self._start_capture_bind)
        row.steps_changed.connect(self._on_macro_steps_changed)
        row.bind_cleared.connect(self._clear_macro_bind)

        insert_pos = self.macro_vbox.count() - 1
        self.macro_vbox.insertWidget(insert_pos, row)
        self.macro_widgets.append(row)
        
        row.setFixedHeight(108) 
        
        self.setUpdatesEnabled(True)
        self._sync_header_combo()

    def _del_macro(self, idx):
        """Удаление макроса с хирургической точностью."""
        if 0 <= idx < len(self.macros):
            if getattr(self, "_capturing_bind", False) and self.current_macro_idx == idx:
                self._cancel_capture_bind()

            self.macros.pop(idx)
            
            if self.current_macro_idx == idx:
                self.current_macro_idx = min(idx, len(self.macros) - 1)
            elif self.current_macro_idx > idx:
                self.current_macro_idx -= 1
                
            self._refresh_macro_list()
            self._sync_header_combo()
            
            if hasattr(self, "mw") and hasattr(self.mw, "update_macro_triggers"):
                self.mw.update_macro_triggers()

    def _clear_macro_bind(self, idx):
        """Обрабатывает сигнал bind_cleared от MacroRowWidget: очищает словарь и шлёт апдейты драйверу."""
        if 0 <= idx < len(self.macros):
            self.macros[idx]["bind"] = ""
            
            if hasattr(self, "mw"):
                if hasattr(self.mw, "update_macro_triggers"):
                    self.mw.update_macro_triggers()
                if hasattr(self.mw, "save_config"):
                    self.mw.save_config()

    def _on_macro_selected(self, idx):
        self.current_macro_idx = idx
        for i in range(self.macro_vbox.count()):
            w = self.macro_vbox.itemAt(i).widget()
            if isinstance(w, MacroRowWidget):
                w.setProperty("active", "true" if w.idx == idx else "false")
                w.update_style()

    def _stop_macro(self):
        """Останавливает выполнение и дает команду раннеру на сброс."""
        if self.runner and self.runner.isRunning():
            print("[_stop_macro] Stopping runner...")
            self.runner.stop()
            self.runner = None

    def _play_macro(self, idx=None):
        """Запускает воспроизведение макроса по индексу или текущему."""
        if idx is not None:
            self.current_macro_idx = idx
            
        if self.current_macro_idx < 0:
            print("[_play_macro] ОШИБКА: Макрос не выбран")
            return

        for i in range(self.macro_vbox.count()):
            item = self.macro_vbox.itemAt(i)
            if not item: continue
            w = item.widget()
            if isinstance(w, MacroRowWidget) and getattr(w, 'idx', -1) == self.current_macro_idx:
                w._sync_steps_to_data()
                break

        macro = self.macros[self.current_macro_idx]
        steps = macro.get("steps", [])
        if not steps:
            print(f"[_play_macro] В макросе '{macro.get('name')}' нет шагов!")
            return

        gamepad = None
        lock = None
        
        if hasattr(self.mw, "thread") and self.mw.thread:
            gamepad = self.mw.thread.gamepad
            lock = getattr(self.mw.thread, "lock", None)

        if not gamepad:
            print("[_play_macro] КРИТИЧЕСКАЯ ОШИБКА: Геймпад в self.mw.thread не найден!")
            return

        _ithread = self.mw.thread if hasattr(self.mw, "thread") else None

        self._stop_macro()
        
        self.runner = MacroRunner(steps, gamepad, lock, ithread=_ithread)
        self.runner.sig_step.connect(self._highlight_step)
        self.runner.sig_done.connect(self._on_runner_done)
        self.runner.start()

    def _on_runner_done(self):
        self.runner = None

    def _highlight_step(self, step_idx: int):
        row_w = self._get_row_by_idx(self.current_macro_idx)
        if not row_w:
            return

        count = 0
        for i in range(row_w.tl_layout.count()):
            w = row_w.tl_layout.itemAt(i).widget()
            if isinstance(w, MacroStepWidget):
                value = "true" if count == step_idx else "false"
                w.setProperty("highlighted", value)
                w.style().unpolish(w)
                w.style().polish(w)
                w.update()
                count += 1

    def _start_capture_bind(self, idx=None):
        """Запускает режим захвата клавиши для бинда."""
        if self._capturing_bind and (idx is None or idx == self.current_macro_idx):
            self._cancel_capture_bind()
            return

        if self._capturing_bind:
            self._cancel_capture_bind()

        if idx is not None:
            self.current_macro_idx = idx
            self._on_macro_selected(idx)

        self._capturing_bind = True
        
        row_w = self._get_row_by_idx(self.current_macro_idx)
        if row_w:
            btn = row_w.bind_btn
            btn.setText("WAITING…")
            btn.setProperty("capturing", "true")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if hasattr(self.mw, "thread"):
            self.mw.thread.is_capturing = True

    def _get_row_by_idx(self, idx):
        for i in range(self.macro_vbox.count()):
            w = self.macro_vbox.itemAt(i).widget()
            if isinstance(w, MacroRowWidget) and w.idx == idx:
                return w
        return None

    def _cancel_capture_bind(self):
        self._capturing_bind = False
        
        row_w = self._get_row_by_idx(self.current_macro_idx)
        if row_w:
            btn = row_w.bind_btn
            val = self.macros[self.current_macro_idx].get("bind", "") or "NONE"
            btn.setText(val)
            btn.setProperty("capturing", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if hasattr(self.mw, "thread"):
            self.mw.thread.is_capturing = False

    def on_bind_captured(self, key_name: str):
        """Вызывается из MainWindow.on_key при активном захвате бинда."""
        if not self._capturing_bind or self.current_macro_idx < 0:
            return
        self.macros[self.current_macro_idx]["bind"] = key_name
        self._cancel_capture_bind()
        
        if hasattr(self, "mw") and hasattr(self.mw, "update_macro_triggers"):
            self.mw.update_macro_triggers()


    def load_from_config(self, config: "configparser.ConfigParser"):
        self.macros.clear()
        section_names = [s for s in config.sections() if s.startswith("Macros_")]
        for sname in sorted(section_names):
            sec = config[sname]
            name = sec.get("name", sname)
            bind = sec.get("bind", "")
            seq_str = sec.get("seq", "")
            steps = parse_macro_seq(seq_str) if seq_str else []
            self.macros.append({"name": name, "bind": bind, "steps": steps})
        
        if self.macros:
            self.current_macro_idx = 0
        else:
            self.current_macro_idx = -1

        self._refresh_macro_list()
        self._sync_header_combo()
        
        if hasattr(self, "mw") and hasattr(self.mw, "update_macro_triggers"):
            self.mw.update_macro_triggers()

    def save_to_config(self, config: "configparser.ConfigParser"):
        for s in list(config.sections()):
            if s.startswith("Macros_"):
                config.remove_section(s)
        for i, macro in enumerate(self.macros):
            sname = f"Macros_{i:03d}"
            config[sname] = {
                "name": macro["name"],
                "bind": macro.get("bind", ""),
                "seq": serialize_macro_seq(macro.get("steps", [])),
            }
    
    def mouseReleaseEvent(self, event):
        self.setFocus(Qt.OtherFocusReason)
        super().mouseReleaseEvent(event)
    
    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()
        super().mousePressEvent(event)


# Фоновый поток на базе Interception: перехватывает клавиатуру, маппит в геймпад и эмитит сигналы для макросов.
class InterceptionThread(QThread):
    key_signal = Signal(str, int, bool)
    sig_turbo_active = Signal(str, bool, int)
    sig_delay_request = Signal(str, int, bool)
    macro_activated = Signal(int, bool) 

    def __init__(self):
        super().__init__()
        self.is_running, self.enabled = True, False
        self.is_capturing = False
        self.is_typing = False
        self.gamepad = None
        self.pressed_keys: set = set()  # физически зажатые клавиши (upper-case имена)
        self.bindings = {k: ["NONE"] * 6 for k in GP_MAP_KEYS}
        self.toggles = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.turbos = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.delays = {k: [False] * 6 for k in GP_MAP_KEYS}
        self.turbo_active_state = {}
        self.gp_state = {k: False for k in GP_MAP_KEYS} # Состояние для Toggle
        self.lock = threading.Lock()
        self.context = None
        self.macro_triggers = set() # Сюда MainWindow закидывает скан-коды
        self._init_driver()

    def _init_driver(self):
        try:
            dll_path = Path(__file__).parent.resolve() / "interception.dll"
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(str(dll_path.parent))
            self.lib = ctypes.CDLL(str(dll_path))
            self.lib.interception_create_context.restype = ctypes.c_void_p
            self.lib.interception_wait.restype = ctypes.c_void_p
            self.lib.interception_wait.argtypes = [ctypes.c_void_p]
            self.lib.interception_receive.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
            self.lib.interception_send.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint]
            self.lib.interception_set_filter.argtypes = [ctypes.c_void_p, INTERCEPTION_PREDICATE, ctypes.c_ushort]
            self.lib.interception_destroy_context.argtypes = [ctypes.c_void_p]

            self.context = self.lib.interception_create_context()
            if self.context:
                self._cb = INTERCEPTION_PREDICATE(lambda d: 1 <= d <= 10)
                self.lib.interception_set_filter(self.context, self._cb, KEYBOARD_FILTER)
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
                        if not self.gamepad: return
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
                if not self.gamepad: return
                if should_press:
                    self.gamepad.press_button(button=btn_val)
                else:
                    self.gamepad.release_button(button=btn_val)
        elif gp_btn == "LT":
            with self.lock:
                if not self.gamepad: return
                self.gamepad.left_trigger(value=255 if should_press else 0)
        elif gp_btn == "RT":
            with self.lock:
                if not self.gamepad: return
                self.gamepad.right_trigger(value=255 if should_press else 0)
        elif gp_btn.startswith("LS_") or gp_btn.startswith("RS_"):
            val = 1 if should_press else 0
            self.axes[gp_btn] = val
            ls_x = (self.axes["LS_RIGHT"] - self.axes["LS_LEFT"]) * 32767
            ls_y = (self.axes["LS_UP"] - self.axes["LS_DOWN"]) * 32767
            with self.lock:
                if not self.gamepad: return
                self.gamepad.left_joystick(x_value=int(ls_x), y_value=int(ls_y))
            rs_x = (self.axes["RS_RIGHT"] - self.axes["RS_LEFT"]) * 32767
            rs_y = (self.axes["RS_UP"] - self.axes["RS_DOWN"]) * 32767
            with self.lock:
                if not self.gamepad: return
                self.gamepad.right_joystick(x_value=int(rs_x), y_value=int(rs_y))
                
        with self.lock:
            if self.gamepad:
                self.gamepad.update()

    def connect_gamepad(self):
        """Подключает виртуальный геймпад. Вызывается при START EMULATION."""
        if self.gamepad:
            return
        try:
            self.gamepad = vg.VX360Gamepad()
            print("[SYSTEM] Virtual Xbox 360 Controller connected.")
        except Exception as e:
            print(f"[ERROR] Gamepad init failed: {e}")

    def disconnect_gamepad(self):
        """Отключает виртуальный геймпад. Вызывается при STOP EMULATION."""
        if not self.gamepad:
            return
        try:
            with self.lock:
                self.gamepad.reset()
                self.gamepad.update()
            self.gamepad = None
            print("[SYSTEM] Virtual Xbox 360 Controller disconnected.")
        except Exception as e:
            print(f"[ERROR] Gamepad disconnect failed: {e}")

    def run(self):
        if not self.context: return
        stroke = Stroke()

        self.axes = {k: 0 for k in ["LS_UP", "LS_DOWN", "LS_LEFT", "LS_RIGHT", "RS_UP", "RS_DOWN", "RS_LEFT", "RS_RIGHT"]}

        while self.is_running:
            device = self.lib.interception_wait(self.context)
            if not device or not self.is_running: continue

            if self.lib.interception_receive(self.context, device, ctypes.byref(stroke), 1) > 0:
                sc, st = stroke.key.code, stroke.key.state
                is_down = not (st & 1)
                is_extended = bool(st & 2)

                if is_extended and sc in EXTENDED_KEYS:
                    name = EXTENDED_KEYS[sc]
                else:
                    name = CODE_TO_NAME.get(sc, f"KEY_{sc}")

                self.key_signal.emit(name, sc, is_down)

                if is_down:
                    self.pressed_keys.add(name)
                else:
                    self.pressed_keys.discard(name)

                should_block_windows = False

                if self.enabled and not self.is_typing and not self.is_capturing:
                    for gp_btn, keys in self.bindings.items():
                        if name in keys:
                            should_block_windows = True
                            try:
                                slot_idx = keys.index(name)
                                if self.delays[gp_btn][slot_idx]:
                                    self.sig_delay_request.emit(gp_btn, slot_idx, is_down)
                                else:
                                    self.trigger_logical_action(gp_btn, slot_idx, is_down)
                            except ValueError:
                                continue

                    if name in self.macro_triggers:
                        self.macro_activated.emit(sc, is_down)
                        should_block_windows = True

                if self.is_capturing:
                    self.lib.interception_send(self.context, device, ctypes.byref(stroke), 1)
                    continue

                if should_block_windows:
                    continue 
                else:
                    self.lib.interception_send(self.context, device, ctypes.byref(stroke), 1)

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
            self.lib.interception_destroy_context(self.context)
            self.context = None


# Главное окно приложения. Собирает все виджеты, управляет профилями, темой, трей-иконкой и глобальными событиями.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(PROJECT_NAME)
        if os.path.exists(APP_ICON):
            self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resizing = False
        self.drag_allowed = True
        self.offset = None
        self.active_slot = None

        self.setMouseTracking(True)
        self.installEventFilter(self)

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

        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.setInterval(30)  # 30мс достаточно для плавности без лагов
        self.turbo_state = False  # Переключатель вкл/выкл для мигания
        self.active_turbo_keys = set()
        self.pressed_phys_keys = set()
        
        self.thread = InterceptionThread()
        self.thread.key_signal.connect(self.on_key)
        self.thread.sig_turbo_active.connect(self.on_turbo_active)
        self.thread.sig_delay_request.connect(self.on_delay_request)
        self.thread.macro_activated.connect(self.on_macro_activated)

        self.macros_editor = MacrosEditorWidget(self)
        self.wallet_ton = None
        self.wallet_eth = None
        self.setup_ui()
        self.enable_child_tracking(self.centralWidget())
        atexit.register(self._cleanup_on_exit)

        config = configparser.ConfigParser()
        last_p = "Default"

        if os.path.exists(GLOBAL_CONFIG):
            config.read(GLOBAL_CONFIG, encoding="utf-8")
            last_p = config.get("Settings", "last_profile", fallback="Default")

        last_p = last_p.replace(".ini", "")

        self.scan_profiles(last_p)
        self.load_config(last_p)
        self.update_macro_triggers()

        self.resize(
            860, 900
        )  # Ширина увеличена с 835 до 860 для корректного отображения скроллбара
        self.load_window_state()

        is_autostart = config.getboolean("Settings", "autostart", fallback=False)
        self.autostart_cb.setChecked(is_autostart)

        if os.path.exists(GLOBAL_CONFIG):
            app_cfg = configparser.ConfigParser()
            app_cfg.read(GLOBAL_CONFIG, encoding="utf-8")
            is_hide_to_tray = app_cfg.getboolean("Appearance", "hide_to_tray", fallback=False)
            self.hide_to_tray_cb.setChecked(is_hide_to_tray)

        if is_autostart:
            self.toggle_btn.setChecked(True)
            self.toggle()

        self.thread.start()

        QApplication.instance().focusChanged.connect(self.on_focus_changed)

        self.tray_icon = QSystemTrayIcon(self)

        current_icon = self.windowIcon()
        if current_icon.isNull() and os.path.exists(APP_ICON):
            current_icon = QIcon(APP_ICON)

        if current_icon.isNull():
            from PySide6.QtWidgets import QStyle

            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        else:
            self.tray_icon.setIcon(current_icon)

        self.tray_menu = QMenu()
        self.tray_menu.setObjectName("TrayMenu")
        
        self.tray_action_toggle = QWidgetAction(self)
        self.tray_btn_toggle = QPushButton("START EMULATION")
        self.tray_btn_toggle.setObjectName("run_btn_inactive")
        self.tray_btn_toggle.setCursor(Qt.PointingHandCursor)
        self.tray_btn_toggle.setMinimumSize(140, 40)
        
        def on_tray_btn_click():
            if self.toggle_btn:
                self.toggle_btn.click()
            self.tray_menu.hide()
            
        self.tray_btn_toggle.clicked.connect(on_tray_btn_click)
        self.tray_action_toggle.setDefaultWidget(self.tray_btn_toggle)
        self.tray_menu.addAction(self.tray_action_toggle)

        self.tray_menu.addSeparator()

        show_action = self.tray_menu.addAction("Show app")
        show_action.triggered.connect(self.showNormal)

        self.tray_menu.addSeparator()  # Можно добавить разделитель для красоты

        quit_action = self.tray_menu.addAction("Exit")
        quit_action.triggered.connect(self.manual_exit)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.update_tray_menu_style()

    def enable_child_tracking(self, widget):
        """Рекурсивно заставляем всех детей сообщать о движении мыши"""
        widget.setMouseTracking(True)
        widget.installEventFilter(self)
        for child in widget.findChildren(QWidget):
            child.setMouseTracking(True)
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Перехватываем всё: Ресайз + Фокус + Копирование крипты"""
        
        if event.type() == QEvent.Type.MouseMove:
            global_pos = event.globalPosition().toPoint()
            local_pos = self.mapFromGlobal(global_pos)
            if self.resizing:
                self._handle_move(global_pos)
                return True
            self.update_cursor_appearance(local_pos)

        elif event.type() == QEvent.Type.MouseButtonPress:
            global_pos = event.globalPosition().toPoint()

            if hasattr(self, 'macros_editor') and self.macros_editor._capturing_bind:
                row_w = self.macros_editor._get_row_by_idx(self.macros_editor.current_macro_idx)
                self.macros_editor._cancel_capture_bind()

            if hasattr(self, 'wallet_ton') and obj is self.wallet_ton:
                QApplication.clipboard().setText(obj.text())
                print(f"TON скопирован: {obj.text()}")
                return True # Прерываем событие, чтобы не сбросить фокус случайно
                
            if hasattr(self, 'wallet_eth') and obj is self.wallet_eth:
                QApplication.clipboard().setText(obj.text())
                print(f"USDT скопирован: {obj.text()}")
                return True

            target = self.childAt(self.mapFromGlobal(global_pos))
            if not isinstance(target, QLineEdit):
                focused_widget = QApplication.focusWidget()
                if isinstance(focused_widget, QLineEdit):
                    focused_widget.clearFocus()

            local_pos = self.mapFromGlobal(global_pos)
            if self._check_resize_zone(local_pos):
                self._handle_press(global_pos)
                return True

        elif event.type() == QEvent.Type.MouseButtonRelease:
            if self.resizing:
                self.resizing = False
                self.offset = None
                return True

        return super().eventFilter(obj, event)

    def _start_macro(self, sc):
        idx = self.macro_scancodes.get(sc)
        macro_data = self.macros[idx]
        print(f"DEBUG: Data sent to runner: {macro_data['steps']}") 
    
        self.macro_runner = MacroRunner(macro_data, self.interceptor.gamepad)
    
    def on_macro_activated(self, scan_code: int, is_down: bool):
        """Вызывается драйвером. Теперь с защитой от 'дребезга' и автоповтора."""
        if not hasattr(self, "macros_editor") or not self.macros_editor:
            return

        for i, macro in enumerate(self.macros_editor.macros):
            if not isinstance(macro, dict):
                continue
            
            bind = macro.get("bind", "")
            if isinstance(bind, list):
                bind = bind[0] if bind else ""
            
            if not bind or NAME_TO_CODE.get(bind.upper()) != scan_code:
                continue

            if is_down:
                runner = self.macros_editor.runner
                if runner and runner.isRunning() and self.macros_editor.current_macro_idx == i:
                    return 
                
                print(f"[on_macro_activated] START: {bind} (index {i})")
                self.macros_editor.current_macro_idx = i
                self.macros_editor._play_macro(i)
            else:
                print(f"[on_macro_activated] STOP: {bind} (index {i})")
                self.macros_editor._stop_macro()
            break
    
    def mousePressEvent(self, event):
        if hasattr(self, 'active_slot') and self.active_slot:
            self.stop_active_capture()
        
        if event.button() == Qt.MouseButton.LeftButton:
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

    def setup_ui(self):
        self.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

        central = QWidget()
        central.setObjectName("Container")
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.centralWidget().setMouseTracking(True)

        self.main_layout.setContentsMargins(3, 3, 3, 3)
        self.main_layout.setSpacing(0)

        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 5, 0, 5)

        self.title_label = QLabel(PROJECT_NAME)
        self.title_label.setObjectName("TitleLabel")  # стиль в _QSS_TEMPLATE QLabel#TitleLabel
        
        title_layout.addStretch()
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        self.main_layout.addWidget(title_container)

        header = QFrame()
        header.setObjectName("Header")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(10, 0, 5, 0)

        self.toggle_btn = QPushButton("START EMULATION")
        self.toggle_btn.setObjectName("run_btn_inactive")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedSize(140, 60)
        self.toggle_btn.clicked.connect(self.toggle)
        self.toggle_btn.setFocusPolicy(Qt.NoFocus)
        h_layout.addWidget(self.toggle_btn)

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

        checks_frame = QFrame()
        checks_layout = QVBoxLayout(checks_frame)
        checks_layout.setContentsMargins(0, 0, 0, 0)
        checks_layout.setSpacing(2)

        self.autostart_cb = QCheckBox("AUTO-START")
        self.autostart_cb.setObjectName("AutostartCheck")
        self.autostart_cb.setFocusPolicy(Qt.NoFocus)
        checks_layout.addWidget(self.autostart_cb)

        self.hide_to_tray_cb = QCheckBox("HIDE TO TRAY")
        self.hide_to_tray_cb.setObjectName("HideToTrayCheck")
        self.hide_to_tray_cb.setFocusPolicy(Qt.NoFocus)
        self.hide_to_tray_cb.setToolTip("При сворачивании: скрывать окно в трей (без превью) или оставлять в таскбаре (с превью)")
        self.hide_to_tray_cb.stateChanged.connect(self.save_appearance)
        checks_layout.addWidget(self.hide_to_tray_cb)

        h_layout.addWidget(checks_frame)
        
        self.settings_btn = QPushButton("SETTINGS")
        self.settings_btn.setObjectName("SettingsBtn")
        self.settings_btn.setFixedSize(90, 30)
        self.settings_btn.setFocusPolicy(Qt.NoFocus)
        self.settings_btn.clicked.connect(self.show_settings)
        h_layout.addWidget(self.settings_btn)
        
        window_controls = QFrame()
        wc_layout = QHBoxLayout(window_controls)
        wc_layout.setContentsMargins(5, 0, 0, 0)
        wc_layout.setSpacing(8)
        
        self.donate_btn = QPushButton("🍜 Support")
        self.donate_btn.setObjectName("DonateBtn")
        self.donate_btn.setFixedSize(95, 35) # Высота вровень с кнопками управления
        self.donate_btn.setCursor(Qt.PointingHandCursor)
        self.donate_btn.setFocusPolicy(Qt.NoFocus)
        self.donate_btn.clicked.connect(self._show_donate_dialog)
        wc_layout.addWidget(self.donate_btn)

        self.min_btn = QPushButton("—")
        self.close_btn = QPushButton("X")
        for btn, name in [(self.min_btn, "min_btn"), (self.close_btn, "close_btn")]:
            btn.setObjectName(name)
            btn.setFixedSize(35, 35)
            btn.setFocusPolicy(Qt.NoFocus)
            wc_layout.addWidget(btn)

        self.min_btn.clicked.connect(self.force_minimize)
        self.close_btn.clicked.connect(self.manual_exit)

        h_layout.addWidget(window_controls, alignment=Qt.AlignRight | Qt.AlignTop)
        
        self.main_layout.addWidget(header)
        self.main_layout.addSpacing(10)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabs")
        self.tabs.setFocusPolicy(Qt.NoFocus)

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
                slot_container = QWidget()
                slot_layout = QVBoxLayout(slot_container)
                slot_layout.setContentsMargins(0, 0, 0, 0)
                slot_layout.setSpacing(1)

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

                turbo_input = QLineEdit("0")
                turbo_input.setObjectName(f"TurboInput_{btn_name}_{col}")
                turbo_input.setFixedSize(40, 24)
                turbo_input.setAlignment(Qt.AlignCenter)
                turbo_input.setEnabled(False)  # Изначально неактивно (вместо скрытия)
                turbo_input.editingFinished.connect(
                    lambda b=btn_name, i=col: self.update_turbo_interval(b, i)
                )

                turbo_layout.addWidget(turbo_btn)
                turbo_layout.addWidget(turbo_input)

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

        self.scroll.viewport().setFocusPolicy(Qt.NoFocus)
        self.scroll.viewport().setAttribute(Qt.WA_MacShowFocusRect, False)
        self.scroll.viewport().setAttribute(Qt.WA_StyledBackground, True)

        if hasattr(self, "macro_scroll"):
            self.macro_scroll.viewport().setFocusPolicy(Qt.NoFocus)
            self.macro_scroll.viewport().setAttribute(Qt.WA_MacShowFocusRect, False)
            self.macro_scroll.viewport().setAttribute(Qt.WA_StyledBackground, True)

        if hasattr(self, "palette_scroll"):
            self.palette_scroll.viewport().setFocusPolicy(Qt.NoFocus)
            self.palette_scroll.viewport().setAttribute(Qt.WA_MacShowFocusRect, False)
            self.palette_scroll.viewport().setAttribute(Qt.WA_StyledBackground, True)

        for sb in (self.scroll.verticalScrollBar(), self.scroll.horizontalScrollBar()):
            if sb:
                sb.setMouseTracking(True)

        self.tabs.addTab(self.scroll, "MAPPER")
        
        self.tabs.addTab(self.macros_editor, "MACROS")


        self.main_layout.addWidget(self.tabs, stretch=1)

    def changeEvent(self, event):
        """Отслеживание состояний окна: сворачивание и потеря фокуса"""
        if event.type() == QEvent.Type.ActivationChange:
            if not self.isActiveWindow():
                self.stop_active_capture()

        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                hide_to_tray = hasattr(self, "hide_to_tray_cb") and self.hide_to_tray_cb.isChecked()
                if hide_to_tray:
                    self.hide()
                    msg = "Программа свёрнута в трей"
                else:
                    msg = "Программа свёрнута"
                
                if hasattr(self, "tray_icon"):
                    self.tray_icon.showMessage(
                        PROJECT_NAME, msg,
                        QSystemTrayIcon.MessageIcon.Information, 1500
                    )
        super().changeEvent(event)

    def stop_active_capture(self):
        """Безопасно завершает режим захвата клавиши для любого активного слота"""
        if not hasattr(self, 'active_slot') or not self.active_slot:
            return
            
        gp_btn, idx, obj = self.active_slot
        
        if gp_btn in self.bindings and idx < len(self.bindings[gp_btn]):
            obj.setText(self.bindings[gp_btn][idx])
            
        obj.setProperty("capturing", "false")
        obj.style().unpolish(obj)
        obj.style().polish(obj)
        
        self.thread.is_capturing = False
        self.active_slot = None
        self.setFocus() # Снимаем фокус с кнопки

    def start_cap(self, gp_btn, idx, obj):
        if self.active_slot and self.active_slot[2] == obj:
            self.stop_active_capture()
            return

        if self.active_slot:
            self.stop_active_capture()

        self.active_slot = (gp_btn, idx, obj)
        self.thread.is_capturing = True
        obj.setText("???")
        obj.setProperty("capturing", "true")
        obj.style().unpolish(obj)
        obj.style().polish(obj)

    def on_key(self, name, sc, is_down):
        if self.macros_editor._capturing_bind:
            if is_down:  # Только по нажатию
                self.macros_editor.on_bind_captured(name.upper())
            return

        if self.thread.enabled:
            name_up = name.upper()
            
            is_repeat = is_down and (name_up in self.pressed_phys_keys)
            if is_down:
                self.pressed_phys_keys.add(name_up)
            else:
                self.pressed_phys_keys.discard(name_up)

            if not is_repeat:
                for i, macro in enumerate(self.macros_editor.macros):
                    if macro.get("bind") == name_up:
                        self.macros_editor.current_macro_idx = i
                        if is_down:
                            self.macros_editor._play_macro()
                        else:
                            self.macros_editor._stop_macro()
                        break

        if self.active_slot:
            gp_btn, idx, obj = self.active_slot
            name_up = name.upper()

            if name_up == "ESC":
                name_up = "NONE"

            self.bindings[gp_btn][idx] = name_up
            obj.setText(name_up)

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

        if is_active:
            self.thread.connect_gamepad()
        else:
            self.thread.disconnect_gamepad()

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

        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)

        self.toggle_btn.setEnabled(False)
        QTimer.singleShot(300, lambda: self.toggle_btn.setEnabled(True))

        if is_active:
            self.turbo_timer.start(10)
        else:
            self.turbo_timer.stop()
            self.active_turbo_keys.clear()
            self.active_t_session.clear()

    def scan_profiles(self, target_profile=None):
        """Сканирует папку Profiles на наличие .ini файлов (без расширений)"""
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
            print(f"[SYSTEM] Created directory: {PROFILES_DIR}")

        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()

        profiles = [f.stem for f in Path(PROFILES_DIR).glob("*.ini")]

        if not profiles:
            profiles = ["Default"]
            self.save_config("Default")

        self.profile_combo.addItems(profiles)

        if target_profile:
            clean_name = os.path.basename(target_profile).replace(".ini", "")
            if clean_name in profiles:
                self.profile_combo.setCurrentText(clean_name)
            else:
                self.profile_combo.setCurrentIndex(0)

        self.profile_combo.blockSignals(False)
        print(f"[SYSTEM] Profiles in '{PROFILES_DIR}': {profiles}")

    def update_macro_triggers(self):
        """Собирает ИМЕНА всех макросов и передаёт их в поток InterceptionThread."""
        if not hasattr(self, "macros_editor"):
            return
            
        names = set()
        for macro in self.macros_editor.macros:
            if not isinstance(macro, dict):
                continue

            bind = macro.get("bind", "")
            if not bind:
                continue

            if isinstance(bind, list):
                bind = bind[0] if bind else ""

            if not bind:
                continue
            
            if bind.upper() != "NONE":
                names.add(bind.upper())

        if hasattr(self, "thread"):
            self.thread.macro_triggers = names
    
    def load_config(self, profile_name=None):
        """Загрузка биндов из папки Profiles и системных настроек из корня"""
        GLOBAL_CONFIG = "System_Config.ini"

        if profile_name is None or not isinstance(profile_name, str):
            profile_name = self.profile_combo.currentText()

        if not profile_name.lower().endswith(".ini"):
            profile_name += ".ini"

        full_path = os.path.join(PROFILES_DIR, profile_name)

        for gp_btn in GP_MAP_KEYS:
            for i in range(6):
                self.bindings[gp_btn][i] = "NONE"
                self.toggles[gp_btn][i] = False
                self.turbos[gp_btn][i] = False
                self.turbo_intervals_map[gp_btn][i] = 0.1

                btn = self.ui_buttons[gp_btn][i]
                btn.setText("NONE")
                btn.style().unpolish(btn)
                btn.style().polish(btn)

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
                d_btn.style().unpolish(d_btn)
                d_btn.style().polish(d_btn)
                d_btn.blockSignals(False)

                d_input = self.ui_delay_inputs[gp_btn][i]
                d_input.setEnabled(False)
                d_input.setText("0.1")
                d_input.setProperty("active", "false")
                d_input.style().unpolish(d_input)
                d_input.style().polish(d_input)

        if os.path.exists(GLOBAL_CONFIG):
            sys_config = configparser.ConfigParser()
            sys_config.read(GLOBAL_CONFIG, encoding="utf-8")
            if "Window" in sys_config:
                geometry = sys_config.get("Window", "geometry", fallback=None)
                if geometry:
                    self.restoreGeometry(bytes.fromhex(geometry))
                    print(f"[SYSTEM] Window geometry restored from {GLOBAL_CONFIG}")

            if "Appearance" in sys_config:
                self.primary_color = sys_config.get(
                    "Appearance", "primary_color", fallback="#0078D7"
                )
                self.secondary_color = sys_config.get(
                    "Appearance", "secondary_color", fallback="#E74C3C"
                )
                self.apply_theme()

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
                        states = [bool(int(x)) for x in val.split(",")]
                        for i in range(min(len(states), 6)):
                            self.toggles[gp_btn_up][i] = states[i]
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

            if "TurboIntervals" in config:
                for gp_btn, val in config["TurboIntervals"].items():
                    gp_btn_up = gp_btn.upper()
                    if gp_btn_up in self.turbo_intervals_map:
                        vals = [float(x) for x in val.split(",")]
                        for i in range(min(len(vals), 6)):
                            self.turbo_intervals_map[gp_btn_up][i] = vals[i]
                            self.ui_turbo_inputs[gp_btn_up][i].setText(str(vals[i]))

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
                            self.ui_delays[gp_btn_up][i].style().unpolish(self.ui_delays[gp_btn_up][i])
                            self.ui_delays[gp_btn_up][i].style().polish(self.ui_delays[gp_btn_up][i])
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

            for gp_btn in GP_MAP_KEYS:
                for i in range(6):
                    is_toggle = self.toggles[gp_btn][i]
                    is_turbo = self.turbos[gp_btn][i]
                    is_delay = self.delays[gp_btn][i]
                    self.ui_turbos[gp_btn][i].setEnabled(not is_toggle and not is_delay)
                    self.ui_toggles[gp_btn][i].setEnabled(not is_turbo and not is_delay)
                    self.ui_delays[gp_btn][i].setEnabled(not is_toggle and not is_turbo)
            print(f"[SYSTEM] Profile loaded: {full_path}")
            
            self.macros_editor.load_from_config(config)
            self.update_macro_triggers()

    def save_config(self, filename=None):
        """Сохранение биндингов строго в папку Profiles"""
        if filename is None:
            filename = self.profile_combo.currentText()

        if not filename:
            filename = "Default.ini"

        if not filename.lower().endswith(".ini"):
            filename += ".ini"

        base_name = os.path.basename(filename)
        full_path = os.path.join(PROFILES_DIR, base_name)

        config = configparser.ConfigParser()
        config["Bindings"] = {k: ",".join(v) for k, v in self.bindings.items()}
        config["Toggles"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.toggles.items()
        }
        config["Turbo"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.turbos.items()
        }
        config["TurboIntervals"] = {
            k: ",".join([str(x) for x in v])
            for k, v in self.turbo_intervals_map.items()
        }
        config["Delay"] = {
            k: ",".join(["1" if x else "0" for x in v]) for k, v in self.delays.items()
        }
        config["DelayIntervals"] = {
            k: ",".join([str(x) for x in v])
            for k, v in self.delay_intervals_map.items()
        }
        
        self.macros_editor.save_to_config(config)

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
                filename = f"{name}.ini" if not name.endswith(".ini") else name

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
        confirm.setObjectName("WarningDialog")
        confirm.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        confirm.setWindowTitle("Подтверждение")
        confirm.setText(f"Delete profile {current}?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setIcon(QMessageBox.NoIcon)

        confirm.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

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

        filename = current if current.lower().endswith(".ini") else f"{current}.ini"
        source_path = os.path.join(PROFILES_DIR, filename)

        if not os.path.exists(source_path):
            print(f"[ERROR] Source profile not found: {source_path}")
            return

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

        self.ui_turbos[gp_btn][idx].setEnabled(not checked)
        self.ui_delays[gp_btn][idx].setEnabled(not checked)

        self.save_config()

    def update_turbo_state(self, gp_btn, idx, checked):
        """Обновление состояния чекбокса Turbo"""
        self.turbos[gp_btn][idx] = checked
        self.thread.turbos = {k: v[:] for k, v in self.turbos.items()}

        self.ui_toggles[gp_btn][idx].setEnabled(not checked)
        self.ui_delays[gp_btn][idx].setEnabled(not checked)

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
        btn.style().unpolish(btn)
        btn.style().polish(btn)

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
            if gp_btn in self.active_t_session:
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

                if not state and (now - last_time >= interval):
                    if gp_btn in GP_BUTTON_MAP:
                        self.thread.gamepad.press_button(button=GP_BUTTON_MAP[gp_btn])
                    elif gp_btn == "LT":
                        self.thread.gamepad.left_trigger(value=255)
                    elif gp_btn == "RT":
                        self.thread.gamepad.right_trigger(value=255)

                    params["state"] = True
                    params["last_time"] = now
                    need_update = True

                elif state and (now - last_time >= PRESS_DURATION):
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

    def get_macro_engine_style(self):
        """Возвращает сгенерированный стиль. Также обновляет глобальный QSS."""
        style = get_stylesheet(self.primary_color, self.secondary_color)
        self.setStyleSheet(style)
        return style
    
    def show_styled_message(self, title, text, is_warning=False):
        """Вспомогательный метод для показа стилизованных уведомлений"""
        msg = QMessageBox(self)
        if is_warning:
             msg.setObjectName("WarningDialog")
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        msg.setIcon(QMessageBox.NoIcon)
        msg.setText(text)
        msg.setWindowTitle(title)
        
        msg.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))
        msg.exec()

    def manual_exit(self):
        """Метод 'Ядерная кнопка' — просто запускает стандартное закрытие"""
        self.close()

    def show_settings(self):
        """Открывает диалог настроек цветов"""
        dialog = QDialog(self)
        dialog.setWindowTitle("UI COLOR SETTINGS")
        dialog.setFixedWidth(300)
        dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
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
        info.setObjectName("SettingsInfo")  # стиль в _QSS_TEMPLATE QLabel#SettingsInfo
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

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

        self.preview_timer.timeout.connect(on_preview_timeout)
        color_dialog.currentColorChanged.connect(update_preview)

        if color_dialog.exec():
            self.preview_timer.timeout.disconnect(on_preview_timeout)

            final_color = color_dialog.selectedColor()
            if final_color.isValid():
                if target == "primary":
                    self.primary_color = final_color.name()
                else:
                    self.secondary_color = final_color.name()

                self.apply_theme()
                self.save_appearance()
        else:
            self.preview_timer.timeout.disconnect(on_preview_timeout)

            self.primary_color = original_primary
            self.secondary_color = original_secondary
            self.apply_theme()
            dialog.setStyleSheet(
                get_stylesheet(self.primary_color, self.secondary_color)
            )

    def apply_theme(self):
        """
        Обновляет стили всего приложения и прокидывает цвета вниз по иерархии.

        Порядок:
          1. Глобальный QSS на весь MainWindow.
          2. ComboView (не покрывается глобальным QSS из-за особенностей Qt).
          3. Строки макросов через мост MacrosEditorWidget.update_theme_colors().
             ВАЖНО: список macro_widgets живёт в self.macros_editor, а не в self —
             поэтому прямой self.macro_widgets давал AttributeError молча.
          4. Меню трея.
        """
        self.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

        if hasattr(self, "profile_combo"):
            view = self.profile_combo.view()
            if view:
                view.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

        if hasattr(self, "macros_editor") and self.macros_editor is not None:
            self.macros_editor.update_theme_colors(
                self.primary_color,
                self.secondary_color
            )

        self.update_tray_menu_style()

    def update_tray_menu_style(self):
        """Синхронизирует стиль меню трея с основной темой через глобальный QSS"""
        stylesheet = get_stylesheet(self.primary_color, self.secondary_color)

        if hasattr(self, "tray_menu"):
            self.tray_menu.setStyleSheet(stylesheet)

        if hasattr(self, "tray_btn_toggle"):
            self.tray_btn_toggle.setStyleSheet(
                stylesheet + "\nQPushButton { margin: 4px 10px; padding: 0 10px; }"
            )

    def _show_donate_dialog(self):
        dlg = QDialog(self)
        dlg.setObjectName("DonateDialog")
        dlg.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) 
        dlg.setFixedWidth(480)
        dlg.setStyleSheet(get_stylesheet(self.primary_color, self.secondary_color))

        content_frame = QFrame(dlg)
        content_frame.setObjectName("DonateContentFrame") 
        layout = QVBoxLayout(content_frame)
        
        main_layout = QVBoxLayout(dlg)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_frame)

        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        icon_label = QLabel("🍜")
        icon_label.setObjectName("DonateIcon")  # стиль в _QSS_TEMPLATE QLabel#DonateIcon
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(icon_label)

        text_v_layout = QVBoxLayout()
        text_v_layout.setSpacing(0)

        label_en = QLabel("BUY ME A RAMEN")
        label_en.setObjectName("DonateHeaderEn")  # стиль в _QSS_TEMPLATE QLabel#DonateHeaderEn
        
        label_ru = QLabel("КУПИТЬ МНЕ ДОШИК")
        label_ru.setObjectName("DonateHeaderRu")  # стиль в _QSS_TEMPLATE QLabel#DonateHeaderRu

        text_v_layout.addWidget(label_en)
        text_v_layout.addWidget(label_ru)
        
        header_layout.addLayout(text_v_layout)
        header_layout.addStretch() # Прижимаем к левому краю
        layout.addLayout(header_layout)
        layout.addSpacing(5)

        _lbl_ton = QLabel("Telegram (TON):")
        _lbl_ton.setObjectName("DonateWalletLabel")
        layout.addWidget(_lbl_ton)
        self.wallet_ton = QLineEdit("UQCYSQvBMDBqsiWvRpuTK8wpB-wymTWTdD2SR5sWoHOQdCSt")
        self.wallet_ton.setReadOnly(True)
        self.wallet_ton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.wallet_ton.setToolTip("Click to copy / Кликни, чтобы скопировать")
        self.wallet_ton.installEventFilter(self)
        layout.addWidget(self.wallet_ton)

        _lbl_usdt = QLabel("USDT (TRC20):")
        _lbl_usdt.setObjectName("DonateWalletLabel")
        layout.addWidget(_lbl_usdt)
        self.wallet_eth = QLineEdit("TRw215Ck5UTou61FqQRXEKFhLnnoRr2L9U")
        self.wallet_eth.setReadOnly(True)
        self.wallet_eth.setCursor(Qt.CursorShape.PointingHandCursor)
        self.wallet_eth.setToolTip("Click to copy / Кликни, чтобы скопировать")
        self.wallet_eth.installEventFilter(self)
        layout.addWidget(self.wallet_eth)

        layout.addSpacing(15)

        ton_close = QPushButton("CLOSE")
        ton_close.setObjectName("CloseDonateBtn")
        ton_close.setFixedSize(100, 30)
        ton_close.clicked.connect(dlg.accept)
        
        ton_layout = QHBoxLayout()
        ton_layout.addStretch()
        ton_layout.addWidget(ton_close)
        ton_layout.addStretch()
        layout.addLayout(ton_layout)

        dlg.drag_pos = None
        def dialogMousePress(event):
            if event.button() == Qt.MouseButton.LeftButton:
                dlg.drag_pos = event.globalPosition().toPoint()
        def dialogMouseMove(event):
            if dlg.drag_pos is not None:
                delta = event.globalPosition().toPoint() - dlg.drag_pos
                dlg.move(dlg.pos() + delta)
                dlg.drag_pos = event.globalPosition().toPoint()
        def dialogMouseRelease(event):
            dlg.drag_pos = None

        dlg.mousePressEvent = dialogMousePress
        dlg.mouseMoveEvent = dialogMouseMove
        dlg.mouseReleaseEvent = dialogMouseRelease

        dlg.exec()

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

    def _cleanup_on_exit(self):
        """Метод, который вызовется автоматически при завершении процесса Python"""
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()

    def closeEvent(self, event):
        """Единая точка выхода с сохранением и чисткой драйвера"""
        print("\n[SYSTEM] Closing application...")

        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()

        if hasattr(self, "thread"):
            print("[SYSTEM] Stopping driver...")
            self.thread.stop()
            self.thread.wait(300)  # Ждем до 1 сек

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
        event.ignore()
        os._exit(0)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)
    
    app.setStyle("Fusion")

    from PySide6.QtGui import QIcon
    if os.path.exists("Omni-Controller.ico"):
        app.setWindowIcon(QIcon("Omni-Controller.ico"))

    from PySide6.QtNetwork import QLocalSocket, QLocalServer
    server_name = "Omni-Controller_V3_INSTANCE"
    
    socket = QLocalSocket()
    socket.connectToServer(server_name)
    if socket.waitForConnected(500):
        socket.write(b"WAKEUP")
        socket.waitForBytesWritten(500)
        sys.exit(0)

    QLocalServer.removeServer(server_name)
    server = QLocalServer()
    server.listen(server_name)

    try:
        ex = MainWindow()
    except Exception:
        import traceback
        traceback.print_exc()
        server.close()
        sys.exit(1)

    def on_new_connection():
        client = server.nextPendingConnection()
        if client:
            if client.waitForReadyRead(200):
                msg = client.readAll()
                if msg == b"WAKEUP":
                    ex.showNormal()
                    ex.raise_()
                    ex.activateWindow()
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
    
    exit_code = app.exec()
    server.close()
    sys.exit(exit_code)
