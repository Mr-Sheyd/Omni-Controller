# ENG:

# 🟦 Omni-Controller
Gamepad emulator with block keys.

**Omni-Controller** is a powerful tool designed to transform your keyboard into a virtual Xbox controller. Unlike basic mappers, this project utilizes a low-level driver for complete input isolation, enabling complex macro sequences and specialized input modes that standard software cannot handle.

---

## ✨ Key Features
* **Full XInput Emulation**: Identified as a genuine Xbox 360 controller for 100% game compatibility.
* **Custom Mapping**: Freely assign any keyboard keys to ABXY, sticks, triggers, and D-pad.
* **Low Latency**: Powered by the `Interception` driver for the fastest possible response time at the kernel level.
* **Neon UI**: A modern, minimalist interface featuring a deep blue neon aesthetic with real-time visual feedback.
* **Smart Tray Integration**: Full control via the system tray, including a dynamic START/STOP toggle and "Hide to Tray" functionality.
* **Portability**: A single standalone `.exe` file—no Python or extra libraries required on the host PC.

---

## ⚙️ Button Operation Modes
Beyond simple mapping, you can assign specialized behaviors to any button:

* **NORMAL**: Standard 1:1 mapping—the button is active only while the key is held down.
* **TURBO**: Press once to start a continuous rapid-fire loop; press again to stop. Perfect for spamming actions without fatigue.
* **TOGGLE**: Press once to keep the button held down (latched); press again to release.
* **DELAY**: Press and hold to trigger an action after a set delay (0.1s+). Releasing the key early cancels the action.

---

### 🛠 Application Control
- **One-Tap Clear**: Instant bind removal in both the mapper and macro editor via **Right-Click**.
- **Geometry Memory**: The app remembers its window position and size across sessions.
- **Safe Save**: Settings management is now isolated from window positioning to prevent config corruption.

---

## 🚀 What's New in v3.0 (Phase 1 Final)

### 🧠 Advanced Macro Engine
Create and execute sophisticated input chains with ease.
- **Sticky Sequences**: Accumulated button presses that hold until the activator key is released.
- **Input Suppression**: Full interception of physical keys to prevent "ghost typing" in Windows while a macro or bind is active. Even the notorious `APPS` key is now fully suppressed.
- **Dynamic Sync**: Direct real-time synchronization between the UI timeline and emulation data.

### 🎨 Neo-Style UI v2.0
- **Dynamic Hover**: Automatic shade calculation for buttons and interactive elements.
- **Custom Scrollbars**: Sleek 8px neon-style scrollbars for a modern look.
- **Zero-Focus Logic**: Automatic focus clearing after interaction to prevent accidental double-inputs.

---

## 🛠 Technical Specs
- **Driver**: `Interception` (Kernel-space filtering).
- **Emulation**: `vgamepad` library.
- **Standalone**: Compiled via PyInstaller (`onefile`) — all resources and DLLs are packed inside.

## 📦 Installation & Quick Start
1. Download the latest release.
2. Ensure the **Interception driver** is installed on your system.
3. Run `Omni-Controller.exe`. It works perfectly with a simple double-click or when run as Administrator.

---

## 🛠 Build Command (For Developers)
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "Omni-Controller" --icon="Omni-Controller.ico" --add-data "XBOX ICONS;XBOX ICONS" --add-data "interception.dll;." --collect-all vgamepad "Omni-Controller.py"
```


## 📜 Credits
This project uses the following resources and libraries:

* **Icons (Assets):** [Free Input Prompts](https://juliocacko.itch.io/free-input-prompts) by **JulioCacko**. Special thanks for the high-quality visual assets.
* **Driver:** [Interception](https://github.com/oblitum/Interception) by Francisco Lopes.
* **Emulation Engine:** [vgamepad](https://github.com/yannbouteiller/vgamepad).
* **UI Framework:** PySide6 (Qt for Python).


## ⚖️ License
Distributed under the **MIT License**. Feel free to use, modify, and distribute this software.


---
<img width="1171" height="1175" alt="Omni-Controller v3 1 (Mapper)" src="https://github.com/user-attachments/assets/5297fee7-72f6-4556-955c-9f6a22c6fdba" />

<img width="1171" height="1176" alt="Omni-Controller v3 1 (Macros)" src="https://github.com/user-attachments/assets/c84a98a6-3e4a-4f81-a6f5-ba05b7647b99" />

<img width="1171" height="1176" alt="Omni-Controller v3 1 (Support)" src="https://github.com/user-attachments/assets/6867520b-7098-4abd-94e5-e301d0fcff7f" />


---


# RUS:

# 🟦 Omni-Controller
Эмулятор геймпада с блокировкой клавиш.

**Omni-Controller** — это мощный инструмент, предназначенный для превращения вашей клавиатуры в виртуальный контроллер Xbox. В отличие от простых мапперов, этот проект использует низкоуровневый драйвер для полной изоляции ввода, позволяя создавать сложные макросы и специализированные режимы нажатий, которые недоступны обычному софту.

---

## ✨ Ключевые особенности
* **Полная эмуляция XInput**: Система распознаёт устройство как настоящий контроллер Xbox 360, что гарантирует 100% совместимость с играми.
* **Кастомный маппинг**: Свободно назначайте любые клавиши клавиатуры на кнопки ABXY, стики, триггеры и D-pad.
* **Минимальная задержка**: Работает через драйвер `Interception`, обеспечивающий максимально быстрый отклик на уровне ядра системы.
* **Neon UI**: Современный минималистичный интерфейс в глубоких неоновых тонах с визуальной обратной связью в реальном времени.
* **Интеграция с треем**: Полное управление через иконку в системном трее, включая динамическое переключение START/STOP и функцию «Hide to Tray».
* **Портативность**: Один автономный `.exe` файл — не требует установки Python или дополнительных библиотек на ПК пользователя.

---

### 🛠 Управление программоой.
- **One-Tap Clear**: Мгновенное удаление бинда в маппере и редакторе макросов через **правый клик мыши**.
- **Geometry Memory**: Программа запоминает положение и размер окна между сессиями.
- **Safe Save**: Система сохранения настроек теперь изолирована от данных о положении окна, что исключает порчу конфига.

---

## ⚙️ Режимы работы кнопок
Помимо обычного маппинга, вы можете назначать кнопкам особое поведение:

* **NORMAL**: Стандартный режим 1:1 — кнопка активна только пока клавиша удерживается.
* **TURBO**: Одно нажатие запускает цикл непрерывной стрельбы (rapid-fire); повторное нажатие останавливает его.
* **TOGGLE**: Одно нажатие «зажимает» кнопку геймпада; второе — отпускает её.
* **DELAY**: Нажатие срабатывает только после заданной задержки (от 0.1 сек). Если отпустить клавишу раньше, действие отменяется.

---

## 🚀 Что нового в v3.0 (Финал Фазы 1)

### 🧠 Продвинутый Macro Engine
Создавайте и исполняйте сложные цепочки команд с легкостью.
- **Sticky Sequences**: Накопительные последовательности кнопок, которые удерживаются до тех пор, пока не будет отпущена клавиша-активатор.
- **Input Suppression (Блокировка)**: Полный перехват физических клавиш. Буквы не печатаются в Windows, пока работает макрос или бинд. Даже «вредная» клавиша `APPS` теперь полностью блокируется.
- **Dynamic Sync**: Прямая синхронизация таймлайна в интерфейсе с данными эмуляции в реальном времени.

### 🎨 Neo-Style UI v2.0
- **Dynamic Hover**: Автоматический расчет оттенков для кнопок и интерактивных элементов.
- **Custom Scrollbars**: Элегантные неоновые полосы прокрутки шириной 8px.
- **Zero-Focus Logic**: Автоматический сброс фокуса после взаимодействия, чтобы избежать случайных повторных вводов.

---

## 🛠 Технические характеристики
- **Драйвер**: `Interception` (фильтрация в пространстве ядра).
- **Эмуляция**: Библиотека `vgamepad`.
- **Сборка**: Скомпилировано через PyInstaller (`onefile`) — все ресурсы и DLL упакованы внутри.

## 📦 Установка и быстрый запуск
1. Скачайте последний релиз.
2. Убедитесь, что в вашей системе установлен драйвер **Interception**.
3. Запустите `Omni-Controller.exe`. Программа отлично работает как при обычном запуске, так и от имени администратора.

---

## 🛠 Команда сборки (для разработчиков)
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "Omni-Controller" --icon="Omni-Controller.ico" --add-data "XBOX ICONS;XBOX ICONS" --add-data "interception.dll;." --collect-all vgamepad "Omni-Controller.py"
```


## 📜 Благодарности
В проекте использованы следующие ресурсы и библиотеки:

* **Иконки (Assets):** [Free Input Prompts](https://juliocacko.itch.io/free-input-prompts) от **JulioCacko**. Огромное спасибо автору за качественные ассеты.
* **Драйвер:** [Interception](https://github.com/oblitum/Interception) за авторством Francisco Lopes.
* **Движок эмуляции:** [vgamepad](https://github.com/yannbouteiller/vgamepad).
* **UI фреймворк:** PySide6 (Qt for Python).


## ⚖️ Лицензия
Распространяется под лицензией **MIT**. Вы можете свободно использовать, изменять и распространять данное ПО.
