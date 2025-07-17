# scan.py

Утилита для Windows: ищет все .exe-файлы в указанных директориях и генерирует блок rules для конфига **nekoray**, чтобы трафик этих процессов шёл напрямую.

## Содержание

* [Требования](#требования)
* [Установка](#установка)
* [Формат конфигурации](#формат-конфига)
* [Запуск](#запуск)
* [Пример вывода](#пример-вывода)
* [Интеграция в nekoray](#интеграция-в-nekoray)
* [Лицензия](#лицензия)

---

## Запуск

```PowerShell
git clone git@github.com:belousotroll/process-to-nekoray.git
cd process-to-nekoray
python scan.py --config settings.json
```

---

## Формат конфигурации

Создайте JSON-файл, например `settings.json`, со списком директорий, процессы в которых вы хотите "защитить" от туннелирования:

```json
{
  "scanning_dirs": [
    "C:\\Program Files (x86)\\Steam\\steamapps\\common",
    "D:\\Games",
    "C:\\Users\\%USERNAME%\\Games"
  ]
}
```

Пути указываются через двойной обратный слэш `\\`.

Каждый путь должен существовать и быть директорией.

---

## Запуск

Откройте PowerShell и выполните:

```powershell
# Вывести результат в консоль (по умолчанию формат JSON для Route settings)
python scan.py --config settings.json

# Записать в файл nekoray_games.json
python scan.py --config settings.json --out nekoray_games.json

# Записать как список процессов
python scan.py --config settings.json -f tun

# Записать как правило для маршрутизации
python scan.py --config settings.json -f route
```

Краткие опции:

* `-c, --config` — путь к JSON-конфигу.
* `-o, --out` — необязательный файл для сохранения результата.
* `-f, --format` — формат вывода:

  * `route` — генерирует JSON-блок для вставки в **Route settings**.
  * `tun` — генерирует список процессов для вставки в **Tun settings** (Bypass Process Name).

---

## Пример вывода

При запуске:

```powershell
python scan.py -c settings.json -f json
```

получите файл с блоком для **Route settings**:

```json
{
  "rules": [
    {
      "process_name": [
        "MonsterHunterWorld.exe",
        "Overwatch.exe",
        "PathOfExile.exe",
        "tModLoader.exe",
        "...и другие"
      ],
      "outbound": "direct"
    }
  ]
}
```

При запуске:

```powershell
python scan.py -c settings.json -f tun
```

будет сгенерирован простой список для **Tun settings** (каждый процесс на новой строке, без кавычек):

```
MonsterHunterWorld.exe
Overwatch.exe
PathOfExile.exe
tModLoader.exe
...и другие
```

---

## Интеграция в nekoray

### Route settings

1. Откройте `nekoray`.
2. Перейдите во вкладку **Preferences** → **Routing Settings**.
3. Откройте вкладку **Simple Route**.
4. Нажмите на кнопку **Custom route** слева снизу окна.
5. Вставьте сгенерированный JSON-блок из `route` в массив `rules`.
6. Перезапустите `nekoray`.

### Tun settings

1. Откройте `nekoray`.
2. Перейдите во вкладку **Preferences** → **Tun Settings**.
3. Откройте раздел **Bypass Process Name**.
4. Вставьте сгенерированный список из режима `tun` в раздел **Bypass Process Name**.
5. Перезапустите `nekoray`.
