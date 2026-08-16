---
type: note
description: CV_Monitoring_Retail_Outlets_System — video analytics for retail outlets (Camhi cameras, YOLOv10 detection, Windows exe modules)
tags:
id: 20260816125403
---

# Система видео-аналитики для контроля розничных точек

## 1. Обзор и назначение

Система расширяет возможности IP-камер Camhi до решения бизнес-задач розничной сети. Работает под Windows (64-bit, от Windows 10), на обычном офисном ПК (8 ГБ RAM). Камеры отправляют на FTP-сервер не видеопоток, а статистическую выборку фотографий (по одному кадру каждые 45 секунд), что позволяет работать на узком канале связи (0.1 Мбит/с).

**Автоматически (Computer Vision):**
- оценка количества посетителей (проходимости) каждой торговой точки;
- контроль присутствия продавца на рабочем месте (время отсутствия человека в кадре);
- оценка покупателей в кассовой зоне с расчётом конверсии (опционально, не в текущей версии);
- сведение данных в Dashboard (книга Excel).

**Автоматизировано (без CV):**
- обзор статистической выборки фотографий;
- фильтрация фотографий по наличию людей и их размещению в зале;
- визуализация работы системы.

**Служебно:**
- поиск пропусков в фотографиях;
- оценка точности алгоритма подсчёта посетителей;
- подбор параметров алгоритма (средний порог, окно) и зон детекции;
- архивирование и бэкап базы;
- мониторинг работоспособности камер с оповещением в Telegram.

Детекция силуэтов людей выполняется моделью **YOLOv10 (yolov10x.pt, PyTorch / Ultralytics)**. Каждый кадр обрабатывается независимо: детектируются люди (класс 0 COCO, уверенность ≥ 0.5), отсеиваются дубликаты bbox, вычисляется принадлежность силуэта зоне детекции и зоне кассы.

---

## 2. Цели проекта (зафиксировано 2026-08-16)

1. Привести проект к профессиональному, поддерживаемому виду.
2. Подготовить репозиторий для передачи будущему работодателю.
3. **Сохранить всю протестированную логику работоспособной** — это действующий живой проект, работающий годами.
4. **Перевести хранение данных с CSV на SQLite** (вся система сейчас работает на CSV-файлах в папке `db/`).
5. Устранить технический долг (см. раздел 11), не ломая работу системы.
6. **Унифицировать текстовый интерфейс всех модулей**: первый запуск exe создаёт файл-запрос с описанием и параметрами (программа завершается), повторный запуск читает сохранённые параметры и стартует. Привести к этому все текстовые модули.
7. **Очистить комментарии в коде**: ~~убрать простые/очевидные, оставить только в сложных местах~~; единый язык комментариев — английский. **Выполнено 2026-08-16 (язык):** все русские комментарии переведены на английский. Удаление очевидных комментариев — опционально, не выполнялось.

---

## 3. Архитектура и поток данных

Система двухконтурная и разделена на независимые модули, упакованные в одиночные Windows-`.exe` (PyInstaller). Каждый модуль может работать как часть системы или автономно (загрузчики также распространяются отдельно для простого скачивания медиа с камер).

### Контур 1 — сбор фотографий (загрузчики)
- `00_hiSDloader` скачивает медиа с SD-карты камеры по HTTP (веб-интерфейс Camhi).
- `01_hiFTPDloader` скачивает медиа с FTP-сервера (Beget), куда камеры сами выгружают фотографии.
- Загрузчики формируют базу фотографий: `cams_media/<камера>_photos/<день>/<файл>.jpg` (и `<камера>_videos/<день>/` для видео).
- `02_hiFTPCleaner` и `03_CVloadAntifreeze` обслуживают этот контур (очистка FTP от старых дней, защита загрузчиков от «зависания»).

### Контур 2 — обработка (ядро CV_SYS)
- `CV_SYS_v1.py` (ядро) в непрерывном цикле обходит камеры, прогоняет новые фотографии через YOLOv10 и пишет метаданные силуэтов в `db/<камера>_shapes_locs.csv`.
- По завершении дня запускаются алгоритмы второго уровня:
  - `visitors_counting` — оценка посетителей → `db/<короткое_имя>_visitors.csv`;
  - `noSeller_time` — время отсутствия человека в кадре → `db/<короткое_имя>_noSeller_time.csv`.
- Производные таблицы сводятся в Dashboard (`0_VA_Dashboard.xlsx`) и панель оценки (`1_Sys_viscount_eval.xlsx`).

### Вспомогательный контур
`04_CVdbViewer` (визуализация/фильтры), `05_CVsetCam` (настройка), `06_MissingPhotoFinder` (пропуски), `07_SysViscountEval` (оценка точности), `08_CVdbArchivator` (архивация), `09_CVdbUpdater` (синхронизация/бэкап), `10_hiSampler` (выборка), `11_FTPDataAlert` (мониторинг камер в Telegram).

**Поток:** камеры → FTP-сервер → загрузчики → `cams_media/` → CV_SYS (YOLOv10) → `db/` (таблицы силуэтов) → алгоритмы 2-го уровня → `db/` (посетители / отсутствие) → Dashboard Excel.

---

## 4. Структура проекта

```
CV_Monitoring_Retail_Outlets_System/
├── CV_SYS_v1.py                      # ядро системы (PyTorch/Ultralytics YOLOv10)
├── 00_hiSDloader_v4.py               # загрузчик с SD-карты (HTTP, GUI)
├── 01_hiFTPDloader_v3.py             # загрузчик с FTP (GUI)
├── 02_hiFTPCleaner_v3.py             # очистка FTP (текстовый UI)
├── 03_CVloadAntifreeze_v2.py         # перезапуск загрузчиков (текстовый UI)
├── 04_CVdbViewer_v2.py               # визуализация/фильтры фото (GUI)
├── 05_CVsetCam_v2.py                 # настройка камер/зон (GUI)
├── 06_MissingPhotoFinder_v1.py       # поиск пропусков фото (текстовый UI)
├── 07_SysViscountEval_v1.py          # оценка точности подсчёта (текстовый UI)
├── 08_CVdbArchivator_v2.py           # архивация таблиц силуэтов (GUI)
├── 09_CVdbUpdater_v2.py              # синхронизация/бэкап папок (текстовый UI)
├── 10_hiSampler_v2.py                # выборка фотографий (GUI)
├── 11_FTPDataAlert_v1.py             # мониторинг камер → Telegram (текстовый UI)
├── utils/
│   ├── funcs_CV.py                   # детекция, зоны, дубликаты, сохранение
│   ├── funcs_vis_count_noseller_time.py  # алгоритмы посетителей/отсутствия
│   ├── funcs_initializer_camconfig_getcamframe.py  # инициализация, camconfig
│   ├── funcs_FTP_access_cams_media_structure.py    # доступ к FTP, структура медиа
│   └── funcs_TxtUI_request_app_description.py      # текстовый UI, логи, утилиты
├── ui/                               # 6 .ui файлов Qt Designer (модули 00,01,04,05,08,10)
├── bin/                              # готовые exe + комплекты VA_PC_CV / VA_PC_client (НЕ публиковать)
├── temp/                             # PyInstaller: build/, spec/ + образцы данных для анализа (НЕ публиковать)
├── archive/                          # старые версии, руководство пользователя (НЕ публиковать)
├── build_pyinstaller_commands.ps1    # скрипт сборки всех exe
├── Dockerfile.script                 # контейнер для 11_FTPDataAlert
├── tests/                            # песочница (реальные доступы, модель, cams_media/db) — НЕ публиковать
├── requirements.txt                  # зависимости (UTF-8)
├── README.md                         # краткое описание системы
├── AGENTS.md                         # заметки для агента (среда исполнения)
└── SPEC.md                           # этот файл
```

**Соглашение об именовании модулей:** порядковый номер в начале (`00`–`11`) и версия в конце (`_v1`, `_v2`, ...). Имена переносятся в исполняемые файлы и далее в комплекты установки.

**Scope публикации (зафиксировано):** наружу идут только `ui/`, `utils/` и корневые `.py` (+ README, requirements, SPEC, AGENTS). `bin/`, `temp/`, `tests/`, `archive/`, `dist/`, `.idea/`, `.venv/` — не публикуются (уже в `.gitignore`).

---

## 5. Каталог данных и форматы

### `cams_media/` — база фотографий (создаётся загрузчиками)
```
cams_media/
├── <камера>_photos/<ГГГГММДД>/<ГГММДДЧЧММСС>.jpg   # фотографии (для CV_SYS)
└── <камера>_videos/<ГГГГММДД>/...                  # видео (не обрабатывается CV_SYS)
```
Имя файла фото кодирует время: `ГГММДДЧЧММСС` в начале имени (иногда с префиксом-статусом кадра). `initializer()` находит камеры по папкам с суффиксом `_images`/`_photos`.

### `db/` — база данных системы (CSV; направление развития — SQLite)

| Файл | Назначение |
|---|---|
| `camconfig.csv` | Конфигурация камер: `cam_name, shape_zone, face_zone, frame, work_hours, vis_count_alg` |
| `<камера>_shapes_locs.csv` | Метаданные силуэтов: `origin_file_name, uid8, shape_location, shape_zone_coords, shape_zone, face_zone_coords, face_zone` |
| `<короткое_имя>_visitors.csv` | Посетители по часам: `date, <часы...>, sum, s` (`s` = auto/real) |
| `<короткое_имя>_noSeller_time.csv` | Время отсутствия по часам: `date, <часы...>, sum, photos` |
| `<короткое_имя>_evstat.csv` | Оценка точности: строки real/auto с `err`, `mape` |
| `visitor_forecast.csv` | Прогноз/оценка посетителей: `date, <камера>_pred, <камера>_real, <камера>_mape` |
| `<камера>_last_day_processed_imgs.csv` | Маркер прогресса обработки (список обработанных файлов) |
| `shape_db_info.csv` | Сводка баз силуэтов: `Camera, File_name, First_day, Last_day, Number_of_lines` |
| `1_real_viscount.xlsx` | Ручной подсчёт посетителей (листы по камерам, заполняется вручную в Excel) |
| `0_VA_Dashboard.xlsx` | Dashboard — сводная панель (выходная) |
| `1_Sys_viscount_eval.xlsx` | Панель оценки работы системы (выходная, листы `<камера>_evstat`) |

`db_backups/` — ежедневные копии `db/` (ротация до 180 дней).

**Реальный срез данных лежит в `temp/db/`** (образцы для анализа типов, не публикуются). По нему подтверждено: `shapes_locs` — самая большая таблица (сотни тысяч строк, десятки МБ), хранится **отдельно для каждой камеры** (магазины добавляются/убираются — это требование, сохраняется и в SQLite).

### Именование камер
- Одна камера в точке → имя без цифр (`tlt`).
- Основная + дополнительная → цифры в конце: `chm1` (основная), `chm2` (дополнительная).
- Для оценки трафика используются данные **только основной камеры** (без цифры, либо с цифрой `1`). Дополнительные камеры уточняют контроль присутствия продавца. `short_name()` отбрасывает конечную цифру для группировки камер одной точки.

### Типы данных для SQLite (проекция, зафиксировано 2026-08-16)

Конвенция: **только INTEGER и TEXT, без REAL/DECIMAL**. Дробные значения — целыми (×100 и т.п.).

| Поле (источник) | Тип SQLite | Примечание |
|---|---|---|
| `cam_name`, `origin_file_name`, имена | TEXT | ключи/идентификаторы |
| `uid8` | TEXT | 22 цифры — не помещается в INTEGER (64-bit) |
| `shape_location` | 4× INTEGER | `shape_y1, shape_y2, shape_x1, shape_x2` |
| `shape_zone_coords`, `face_zone_coords`, `frame` | TEXT (JSON) | 1–3 прямоугольника, переменная длина |
| `shape_zone`, `face_zone` | INTEGER | флаги 0/1 (в CSV `face_zone` пишется как float — артефакт pandas) |
| счётчики посетителей, часы, `sum`, `err`, `photos`, `Number_of_lines` | INTEGER | |
| минуты отсутствия продавца | INTEGER | |
| `work_hours` | 2× INTEGER | `hour_start`, `hour_end` |
| `vis_count_alg` | 2× INTEGER | `mean_threshold`, `window_next` |
| даты (`date`, `First_day`, `Last_day`) | TEXT | ISO `YYYY-MM-DD` |
| `s` (auto/real) | TEXT | |
| `mape` | INTEGER | сотые доли (×100): «0,07» → 7; сейчас в CSV хранится строкой с запятой |

**Решение (зафиксировано 2026-08-16):** таблицы `visitors` / `noSeller_time` / `evstat` переводятся в **long-формат** `(cam_name, date, hour, value)` — это устраняет динамические колонки (число часов зависит от `work_hours` камеры). Широкое представление для Dashboard собирается на лету в слое доступа (pivot).

### Схема SQLite (проект, зафиксировано 2026-08-16)

Единая база `db/cv.db` (WAL). `shapes_locs` — отдельная таблица на камеру (создаётся динамически при добавлении камеры).

```sql
PRAGMA journal_mode = WAL;

-- Камеры (бывш. camconfig.csv)
CREATE TABLE cameras (
    cam_name        TEXT PRIMARY KEY,
    shape_zone      TEXT NOT NULL,          -- JSON: 1..3 прямоугольника [[y1,y2,x1,x2],...]
    face_zone       TEXT NOT NULL,          -- JSON [y1,y2,x1,x2]
    frame           TEXT NOT NULL,          -- JSON [y1,y2,x1,x2]
    hour_start      INTEGER NOT NULL,       -- из work_hours
    hour_end        INTEGER NOT NULL,       -- из work_hours
    mean_threshold  INTEGER NOT NULL,       -- из vis_count_alg
    window_next     INTEGER NOT NULL        -- из vis_count_alg
);

-- Силуэты — отдельная таблица на камеру (шаблон, имя подставляется)
CREATE TABLE "<cam_name>_shapes_locs" (
    origin_file_name  TEXT NOT NULL,        -- YYMMDDHHMMSS.jpg
    uid8              TEXT NOT NULL,        -- 22 цифры
    day               TEXT NOT NULL,        -- YYMMDD (денормализовано для срезов)
    shape_y1          INTEGER NOT NULL,
    shape_y2          INTEGER NOT NULL,
    shape_x1          INTEGER NOT NULL,
    shape_x2          INTEGER NOT NULL,
    shape_zone_coords TEXT,                 -- JSON
    shape_zone        INTEGER NOT NULL,     -- 0/1
    face_zone_coords  TEXT,                 -- JSON
    face_zone         INTEGER NOT NULL      -- 0/1
);
CREATE INDEX "idx_<cam_name>_day"  ON "<cam_name>_shapes_locs" (day);
CREATE INDEX "idx_<cam_name>_uid8" ON "<cam_name>_shapes_locs" (uid8);

-- Дни (сводка по камере и дню: источник данных и кол-во фото)
CREATE TABLE days (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,                 -- ISO YYYY-MM-DD
    photos   INTEGER NOT NULL DEFAULT 0,    -- кол-во фото за день
    s        TEXT NOT NULL DEFAULT 'auto',  -- auto|real (источник посетителей)
    PRIMARY KEY (cam_name, date)
);

-- Посетители по часам (long)
CREATE TABLE visitors (
    cam_name TEXT NOT NULL,   -- короткое имя (short_name)
    date     TEXT NOT NULL,
    hour     INTEGER NOT NULL,
    count    INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);

-- Время отсутствия продавца по часам (long)
CREATE TABLE no_seller_time (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    hour     INTEGER NOT NULL,
    absence_minutes INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);

-- Оценка точности: почасовые real/auto
CREATE TABLE evstat (
    cam_name   TEXT NOT NULL,
    date       TEXT NOT NULL,
    hour       INTEGER NOT NULL,
    count_real INTEGER NOT NULL,
    count_auto INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);

-- Оценка точности: итоги дня
CREATE TABLE evstat_day (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    sum_real INTEGER NOT NULL,
    sum_auto INTEGER NOT NULL,
    err      INTEGER NOT NULL,   -- sum_real - sum_auto
    mape     INTEGER NOT NULL,   -- сотые доли (×100): 0.07 -> 7
    PRIMARY KEY (cam_name, date)
);

-- Сводка баз силуэтов (shape_db_info)
CREATE TABLE shape_db_info (
    cam_name        TEXT NOT NULL,
    file_name       TEXT NOT NULL,
    first_day       TEXT NOT NULL,  -- ISO
    last_day        TEXT NOT NULL,  -- ISO
    number_of_lines INTEGER NOT NULL
);

-- Прогресс обработки (last_day_processed_imgs)
CREATE TABLE processed_images (
    cam_name  TEXT NOT NULL,
    file_name TEXT NOT NULL,
    PRIMARY KEY (cam_name, file_name)
);

-- Ручной подсчёт (1_real_viscount.xlsx)
CREATE TABLE real_viscount (
    cam_name TEXT NOT NULL,
    date     TEXT NOT NULL,
    hour     INTEGER NOT NULL,
    count    INTEGER NOT NULL,
    PRIMARY KEY (cam_name, date, hour)
);
```

Примечания к схеме:
- `visitor_forecast` — генерируется отдельным модулем (запускался вручную), будет добавлен в схему в конце.
- Слой доступа (data access layer) конвертирует текущие DataFrame/CSV-структуры в эту схему и обратно, чтобы алгоритмы (`shape_detection`, `visitors_counting`, `noSeller_time`) не менялись.

---

## 6. Ядро системы — CV_SYS

`CV_SYS_v1.py` — единственный компонент, который запускается как `.py` (в среде PyCharm), а не как exe.

### Инициализация
- Читает параметры через текстовый запрос `CV_SYS_request_app_description.txt` (`bot_token`, `chat_id`, флаг журнала).
- `initializer()` сканирует `cams_media/`, формирует словарь `{имя_камеры: путь_к_фото}` и актуализирует `camconfig.csv` (добавляет новые камеры с зоной по умолчанию на весь кадр, `work_hours=(10,21)`, `vis_count_alg=(2,2)`).
- Запускает процесс `CVloadAntifreeze` (антифриз загрузчиков), ждёт 30 минут.
- Загружает модель `YOLO(venv/neural_network_models/yolov10x.pt)`.

### Главный цикл
Бесконечно обходит камеры в алфавитном порядке, для каждой вызывает `shape_detection(...)`, затем пауза 5 секунд. При ошибке — логирует, отправляет сообщение в Telegram, завершает вспомогательные процессы и пробрасывает исключение.

### Алгоритм `shape_detection` (utils/funcs_CV.py)
1. Загружает список уже обработанных файлов (`<камера>_last_day_processed_imgs.csv`), определяет последний обработанный день.
2. Собирает новые файлы по дням (начиная с последнего обработанного дня).
3. Для каждого нового файла:
   - `cv2.imread` (BGR; конвертация в RGB не нужна — YOLO принимает BGR);
   - инференс `shape_detector(img, verbose=False)` (NMS уже внутри YOLO);
   - фильтр людей (класс 0, confidence ≥ 0.5);
   - фильтр дубликатов `is_duplicate_detection` (IoU > 0.9, либо близкие центры < 20 px + похожие размеры + IoU > 0.6);
   - для каждого силуэта — проверка пересечения с `shape_zone` и `face_zone` (`detection_zone_intersection`), генерация уникального `uid8`.
4. Дописывает строки в `<камера>_shapes_locs.csv` (или пересчитывает прошлые дни при `change_past`).
5. При переходе на новый день — запускает `vis_count_noseller_pipeline` и `save_shape_db_info`.

### Алгоритмы 2-го уровня (utils/funcs_vis_count_noseller_time.py)

**`visitors_counting`** — оценка посетителей:
- Берёт силуэты в `shape_zone`, считает число людей в кадре (по `origin_file_name`);
- Строит ряд «людей в кадре» по времени, берёт разность со сдвигом (прирост/убыль), отрицательную разность обнуляет;
- Применяет адаптивное скользящее среднее `custom_rolling_mean` (параметры `mean_threshold`, `window_next` из `vis_count_alg`): пока среднее ≤ порога — окно 1, иначе окно `window_next`;
- Сводит приросты в таблицу по часам (pivot), суммирует за день, помечает `s='auto'`.

**`noSeller_time`** — время отсутствия человека:
- Берёт фото с людьми в `shape_zone`, сортирует по времени;
- Достраивает «вехи» для часов без данных (`auto_insert`);
- Считает разницу во времени между соседними кадрами, порог отсутствия — 10 минут (`absence_threshold`);
- Агрегирует время отсутствия по часам (свыше 60 минут переносится на следующий час);
- Добавляет утреннее опоздание (появление первого человека позже открытия);
- Считает количество фото за день (`add_photos_to_noSeller`).

**`vis_count_noseller_pipeline`** — связка: определяет последний посчитанный день, берёт новые силуэты, вызывает `visitors_counting` и `noSeller_time`, дописывает в `_visitors.csv` и `_noSeller_time.csv`.

**`update_visitors`** — пересчёт посетителей за период при изменении зон (используется из `05_CVsetCam`): пересчитывает только строки `s != 'real'`, сохраняя ручные значения.

### Остановка (Ctrl+C / KeyboardInterrupt)
Для каждой камеры, у которой рабочий день завершён, запускается `vis_count_noseller_pipeline`; затем `save_shape_db_info`, `backup_db`, остановка вспомогательных процессов, очистка `_MEI*`.

---

## 7. Модули системы

### 00_hiSDloader_v4 (GUI, PyQt5)
Загрузчик медиа с SD-карты камеры через HTTP-интерфейс Camhi (`http://admin:<пароль>@<ip>/sd/`). Парсит HTML-страницы (`BeautifulSoup` + `html5lib`), извлекает ссылки на файлы по дням и папкам.
- **Режимы контента:** `alarm` (тревожные видео, статус `A`), `plan` (плановые, статус `P`), `images` (фото).
- **Два диапазона времени** (`ftr` и опциональный `str`), фильтр по часам/минутам.
- **`refresh`** — докачка начиная с последнего уже скачанного дня.
- **`auto`** — бесконечный режим автообновления архива (~каждые 20 минут), при недоступности SD — уведомление в Telegram.
- Настройки сохраняются в `<app>_hiSDconfig.dat` (pickle).
- Три потока: `GetDays` (подключение/список дней), `EstimateThread` (оценка объёма), `ParseThread` (скачивание, 100 попыток переподключения).

### 01_hiFTPDloader_v3 (GUI, PyQt5)
Загрузчик медиа с FTP-сервера (Beget) по протоколу FTP (`ftplib`). Логика аналогична 00, но вместо HTTP — FTP, есть список камер (кнопка «Камеры») и выбор камеры.
- Режимы `alarm`/`images`; поддержка двух временных диапазонов; `refresh` и `auto`.
- **`with_deletion`** — после скачивания удаляет файлы с FTP (двухпроходная логика: основной проход без удаления, затем контрольный с удалением; нулевые файлы удаляются локально).
- Отдельный `DeleteThread` — удаление файлов с FTP в выбранном диапазоне без скачивания.
- Русский/английский интерфейс (`self.language`).
- Настройки в `<app>_hiFTPconfig.dat` (pickle) — источник FTP-реквизитов для 02 и 11.

### 02_hiFTPCleaner_v3 (текстовый UI)
Очистка FTP-пространства от «старых» дней, не входящих в заданное окно (N последних дней). Работает в цикле: проверка через заданный период часов и дополнительно в 10:01. Удаляет файлы, затем пустые папки `images`/`record`/день/камера. Параметры — через `request_app_description` (окно в днях, период проверки).

### 03_CVloadAntifreeze_v2 (текстовый UI)
Защита загрузчиков от «зависания» при потере связи. Сначала запускает все `hiSDloader*` и `hiFTPDloader*` из текущей папки с заданным интервалом, затем периодически (период перезапуска) убивает и перезапускает их. При >3 последовательных ошибках — аварийный выход.

### 04_CVdbViewer_v2 (GUI, PyQt5)
Визуализация работы системы и фильтрация фотографий. Накладывает базу силуэтов на фотографии: рисует bbox силуэтов (жёлтый/красный — см. `red`-вариант), зону детекции и зону кассы. Результат складывает в `imgs_cvdb/`.
- **Фильтры:** общая зона детекции (`shape_zone==1`), «более двух людей в кадре», «у кассы» (`face_zone==1`), произвольная зона (рисуется мышью).
- Оценка количества подходящих кадров в диапазоне дат (без генерации изображений).
- Потоки: `EstimateThread` (подсчёт), `ParseThread` (генерация изображений с прогресс-баром).
- **`bin/04_CVdbViewer_v2_red.exe`** — вариант «red»: красные прямоугольники для силуэтов людей.

### 05_CVsetCam_v2 (GUI, PyQt5)
Настройка системы под особенности торговой точки.
- **Рабочие часы** (`work_hours`) — запись в `camconfig.csv`.
- **Зоны детекции** — до 3 зон `shape_zone` (рисуются мышью по кадру), сохранение в `camconfig.csv` или пересчёт `shapes_locs.csv` за выбранный период (`change_df_cam_shape_zone`), затем пересчёт посетителей `update_visitors`.
- **Зона кассы** (`face_zone` / register zone) — аналогично.
- Поток `SaveRecalculateThread` выполняет пересчёт без блокировки UI.

### 06_MissingPhotoFinder_v1 (текстовый UI)
Поиск пропусков в фотографиях: находит временные промежутки (≥ 1 минуты) без кадров в рабочем диапазоне и пишет их в `<app>_respond.txt`. **Использует собственный формат запроса** (`<app>_request.txt` с полями `path:` и `working hours (10-20):`) вместо общего `request_app_description` — см. раздел 11.

### 07_SysViscountEval_v1 (текстовый UI)
Оценка точности подсчёта посетителей. Берёт ручные данные из `db/1_real_viscount.xlsx`, сравнивает с расчётом алгоритма (`visitors_counting`) за те же дни, вычисляет ошибку (`err`) и `mape`. Пишет `<короткое_имя>_evstat.csv` (чередующиеся строки real/auto) и обновляет `_visitors.csv` ручными значениями (`s='real'`). Параметры алгоритма задаются в `<app>_current_params.txt` (свой формат — см. раздел 11) и после оценки записываются в `camconfig.csv`.

### 08_CVdbArchivator_v2 (GUI, PyQt5)
Архивация длинных таблиц силуэтов `shapes_locs.csv`. По дате отсечения (`cutoff_day`) делит таблицу: старые строки переносятся в `db_shapes_archive/<камера>/<первый_день>_<последний_день>/`, в `db/` остаётся «хвост». Потоки `EstimateThread` (предпросмотр границ) и `LetsArchiveThread` (архивация).

### 09_CVdbUpdater_v2 (текстовый UI)
Синхронизация/обновление файлов при изменениях. Рекурсивно копирует дерево папок (источник → цель, с игнор-списком), затем мониторит `mtime` источника и пересинхронизирует при изменениях. Назначение:
- на ПК-клиенте — забрать базу из локального Google Диска в папку с базой фотографий;
- на обрабатывающем ПК — дублирование базы на другой диск (дополнительный бэкап).

### 10_hiSampler_v2 (GUI, PyQt5)
Выборка (семплирование) фотографий: берёт каждый N-й файл (N = 3/5/10) из текущей папки и копирует (или перемещает) в подпапку `<папка>_xN`. Два потока: `EstimateThread` (подсчёт объёма) и `ParseThread` (выборка).

### 11_FTPDataAlert_v1 (текстовый UI)
Мониторинг равномерности потока кадров с FTP → контроль работоспособности камер. Каждые 45 секунд в рабочие часы сравнивает последний кадр каждой камеры с текущим временем: если отставание > 3 минут — «камера не в сети» в Telegram; при восстановлении — «снова в сети» с длительностью простоя. В конце рабочего дня шлёт итоговое количество непустых кадров. Использует локальный сервер Telegram Bot API (обход блокировок), асинхронный фоновый отправитель (python-telegram-bot + httpx). Работает и в Docker (`Dockerfile.script`). Параметры через `request_app_description` (bot_token, chat_id).

---

## 8. Служебные модули (utils)

- **funcs_CV.py** — `get_coords_from_text` (парсинг 1/2/3-зонных координат), `detection_zone_intersection` (пересечение bbox с зоной), `is_duplicate_detection`, `plus_random_8` (генерация uid), `save_shape_db_info`, `change_past_process`, `shape_detection`.
- **funcs_vis_count_noseller_time.py** — `backup_db`, `base_columns_hours`, `short_name`, `find_new_shapes`, `visitors_counting`, `noSeller_time`, `add_photos_to_noSeller`, `vis_count_noseller_pipeline`, `update_visitors`. Содержит хардкод `cam_name == 'tlt'` (см. раздел 11).
- **funcs_initializer_camconfig_getcamframe.py** — `initializer`, `load_camconfig`, `save_camconfig`, `get_cam_frame`, `dt_slice_shape_df` (срез таблицы силуэтов по датам), `load/save_last_day_processed_imgs`.
- **funcs_FTP_access_cams_media_structure.py** — `load_hiFTPconfig`, `get_ftp_host_user_pas` (чтение FTP-реквизитов из `.dat`), `get_cam_names`, `get_days_dd`, `get_day_folders`, `get_cams_days_dict`, `get_dt_last_day`.
- **funcs_TxtUI_request_app_description.py** — `get_path` (ресурсы при PyInstaller), `request_app_description` (двухэтапный текстовый запрос параметров), `log_event` (CSV-журнал `<app>_event_log.csv`), `txt_notification`, `cleanup_mei_folders` (очистка `hi_temp/_MEI*`).

**Паттерн текстового UI:** при первом запуске создаётся файл-запрос `<app>_request_app_description.txt` (шаблон для заполнения) и программа завершается; при втором запуске параметры читаются из файла и программа работает. Журнал — `<app>_event_log.csv`. Такое именование группирует файлы одного модуля в проводнике.

**Форматы конфигов загрузчиков (`.dat`, pickle):** `hiFTPconfig` = `{ftp_host, ftp_user, ftp_pas, cam_name, day_start, day_end, rb_refresh, ftr_from, ftr_from_min, ftr_to, ftr_to_min, rb_str, str_from, str_from_min, str_to, str_to_min, rb_alarm, rb_images, with_deletion, rb_auto}`; `hiSDconfig` = `{ip_num, password, cam_name, day_start, day_end, rb_refresh, ftr_*, str_*, rb_alarm, rb_plan, rb_images, rb_auto, token, chat_id}`. Образцы лежат в `temp/` (не публикуются).

---

## 9. Сборка и развёртывание

- **PyInstaller**: `build_pyinstaller_commands.ps1` собирает каждый модуль в `--onefile -w` exe с массовым `--exclude-module` (для облегчения), `--add-data ui`, `--runtime-tmpdir=hi_temp`. Артефакты: `temp/build/`, `temp/spec/`.
- **Готовые exe** лежат в `bin/` (исключены из git через `.gitignore`), включая два комплекта:
  - `bin/VA_PC_CV/` — ПК с Computer Vision (все модули + `CV_SYS.py` + модель `neural_network_models/efficientdet_d5_coco17_tpu-32` для старой TF-версии);
  - `bin/VA_PC_client/` — ПК-клиент (просмотр базы, без обработки).
- **Docker**: `Dockerfile.script` (python:3.10-slim) — контейнер для `11_FTPDataAlert_v1.py`.
- **Старые версии и документация** — в `archive/` (`Видео-аналитика_руководство_пользователя.docx/pdf`, `Описание_системы.docx`, async-вариант загрузчика, `send_whatsapp_message.py`).

---

## 10. Зависимости и окружение

`requirements.txt` (в кодировке UTF-8): torch/torchvision (cu126), ultralytics, pandas, matplotlib, opencv-python, openpyxl, PyQt5, pyTelegramBotAPI, requests, tqdm, html5lib, pyinstaller. Для `11_FTPDataAlert` дополнительно: python-telegram-bot, httpx, httpcore.

`bin/VA_PC_CV/Настройка_среды.txt` описывает **устаревшее** окружение TensorFlow (EfficientDet). Актуальный движок — PyTorch/Ultralytics YOLOv10 (см. раздел 11, п.1).

Пользовательская среда разработки — PyCharm с venv `.venv` (не трогать). Для агента — `.venv-linux` (см. раздел 12).

---

## 11. Нестыковки и технический долг (зафиксировано 2026-08-16)

1. **Два движка детекции.** Каноническая версия — `CV_SYS_v1.py` (YOLOv10 / PyTorch). `bin/VA_PC_CV/CV_SYS.py` — старая версия v1.2 на TensorFlow/EfficientDet (устаревший артефакт, не публиковать). ~~Путь к `yolov10x.pt` будет определён.~~ **Решено 2026-08-16:** путь зафиксирован константой `MODEL_REL_PATH = venv/neural_network_models/yolov10x.pt` в `CV_SYS_v1.py` с проверкой существования модели; подсчёт строк shapes переведён на `db.shapes_count` (SQL COUNT).
2. **Хардкод закрытой точки `tlt`.** ~~В `funcs_vis_count_noseller_time.py` строка `if cam_name == 'tlt'` и срез даты `'231223'`.~~ **Решено 2026-08-16:** захардкоженные строки удалены полностью.
3. **Личные данные в коде.** ~~E-mail и номер карты в кнопках «Пожелания/Благодарность» GUI-модулей (00, 01, 04, 05, 08, 10).~~ **Решено 2026-08-16:** вынесены в `utils/contacts.py` (`CONTACT_EMAIL`, `CONTACT_CARD`); 6 GUI-модулей импортируют константы. Перед публикацией заменить значения в одном файле на плейсхолдеры. `test_telegram_bot_API.py` с реальным токеном **уже удалён** Кэпом.
4. **`06_MissingPhotoFinder`** ~~использует собственный формат запроса (`_request.txt`)~~ **Решено 2026-08-16:** переведён на общий `request_app_description` (двухэтапный запуск + описание).
5. **`07_SysViscountEval`** ~~использует собственный формат параметров (`_current_params.txt`)~~ **Решено 2026-08-16:** файл переименован в `_request_app_description.txt`, добавлено описание (`#`-строки); динамический список камер сохранён.
6. **Дублирование кода.** ~~`get_coords_from_text`, `detection_zone_intersection`, `dt_slice_shape_df`, `load_camconfig`/`save_camconfig` продублированы в 04/05/07/08.~~ **Решено 2026-08-16:** все локальные копии удалены, импорты из `utils.funcs_CV` / `utils.funcs_initializer_camconfig_getcamframe`. Попутно устранено расхождение `dt_slice_shape_df` в 04 (`<= dt_end_full` без `iloc` → каноническое `< dt_end_full` с `iloc[:, 0:-1]`).
7. **`eval()`** ~~для `work_hours` в `11_FTPDataAlert`~~ **Решено 2026-08-16:** заменён на `ast.literal_eval`.
8. **pandas в exe.** ~~Загрузчики и лёгкие модули тянут pandas в сборку.~~ **Решено 2026-08-16:** `pandas` в `utils/db.py` сделан ленивым (импорт только внутри DataFrame-функций); лёгкие модули (02/03/06/09/11/01) больше не тянут pandas. `00` тянет `bs4` (BeautifulSoup) — отдельная лёгкая зависимость, добавлена в requirements.
9. **Хранение на CSV** — ~~вся БД (`db/`) это набор CSV~~ **Решено 2026-08-16:** слой доступа `utils/db.py`, скрипт `migrate_csv_to_sqlite.py`; все модули переключены на `db.*`; ручной подсчёт `1_real_viscount.xlsx` перенесён в таблицу `real_viscount`. CSV/Excel остаются холодным резервом. Не перенесён только `visitor_forecast` (см. п.12, отдельный модуль).
10. **bin/** — бинарники и старые комплекты (не для публикации, уже в `.gitignore`).
11. **`requirements.txt`** ~~в UTF-16LE~~ **Решено 2026-08-16:** перекодирован в UTF-8. Противоречие с `Настройка_среды.txt` (torch vs tensorflow) — привести к единому актуальному виду.
12. **`visitor_forecast.csv`** — генерируется отдельным модулем (запускался вручную), будет добавлен в систему в конце. Схема SQLite для него — позже.
13. **Комментарии в коде** ~~смешаны русский/английский~~ **Решено 2026-08-16:** язык унифицирован — все русские комментарии переведены на английский.
14. **Определение имени приложения Windows-специфично.** ~~GUI-модули (00, 01) используют `QCoreApplication.arguments()[0].split('\\')[-1]`, текстовые (02, 03, 06, 07, 09, 11) — `os.path.basename(sys.executable)`.~~ **Решено 2026-08-16:** введён `get_app_name()` = `os.path.splitext(os.path.basename(sys.argv[0]))[0]` в `utils/funcs_TxtUI_request_app_description.py`, внедрён во все модули (00–11); работает и под `.py`, и под exe.
15. **CV_SYS зависит от exe.** ~~`CV_SYS_v1.py` запускает `hiFTPCleaner.exe`/`CVloadAntifreeze.exe` через subprocess из `cams_media/`.~~ **Решено 2026-08-16:** введён `_launch_helper()` с приоритетом `.exe` → `.py` (через `sys.executable`) → пропуск с записью в журнал; `start_hiFTPCleaner_CVloadAntifreeze()` переведён на него. Ядро запускабельно и в песочнице, и в продакшене.
16. **Выбор языка интерфейса в загрузчиках.** ~~В 00/01 остался выбор русский/английский интерфейс.~~ **Решено 2026-08-16:** механизм выбора удалён — остался единственный русский. В `01` убраны все `if self.language == 'eng'` (19 блоков) и `self.language`; суффикс фото-папки зафиксирован `_photos`. Логика `file_type in ['_images', '_photos']` оставлена (обратная совместимость со старыми папками).

---

## 12. Технические особенности для Hermes-агента

### 12.1. Среда исполнения
- **Агентская среда:** `.venv-linux` — `/root/workspace/CV_Monitoring_Retail_Outlets_System/.venv-linux/bin/python`
- **Среда PyCharm (Кэпа):** `.venv` — **НЕ ТРОГАТЬ**.

### 12.2. Запуск
```bash
cd /root/workspace/CV_Monitoring_Retail_Outlets_System && .venv-linux/bin/python client/<script>.py
```

### 12.3. Журнал изменений
- 2026-08-16 — Составлена полная спецификация системы (изучены все модули, utils, сборка, руководство пользователя и `Описание_системы.docx`). Зафиксированы цели и технический долг.
- 2026-08-16 — Проанализирован реальный срез базы в `temp/db/`; зафиксированы типы данных для SQLite, требование «shapes_locs отдельно на камеру», scope публикации (только ui/, utils/, корневые .py), цель №6 (унифицированный текстовый интерфейс).
- 2026-08-16 — Спроектирована SQLite-схема (раздел 5). Приняты решения: `tlt` удалить полностью; `visitor_forecast` добавим в конце; комментарии очистить (цель №7).
- 2026-08-16 — Развёрнута песочница `tests/` (реальные FTP/камера-доступы, модель yolov10x.pt, файловая структура через симлинки). Создаётся `.venv-linux` (torch cu126 + ultralytics) под GPU RTX 3060. Выявлены сквозные проблемы: app_name (Windows-разделитель), зависимость CV_SYS от exe.
- 2026-08-16 — Сквозной рефакторинг: `get_app_name()` внедрён во все модули (убраны `split('\\')`/`sys.executable`). Проверено: алгоритмы посетителей/отсутствия под pandas 3.0.5 дают результаты, совпадающие с боевой базой (chm1 за 2024-08-31: 8 посетителей, 119 мин отсутствия).
- 2026-08-16 — Рефакторинг CV_SYS: зависимость от exe вынесена в `_launch_helper()` (exe → py → skip). Проверено компиляцией и негативным/позитивным запуском спутников.
- 2026-08-16 — Устранено дублирование кода в 04/07/08 (вынесено в utils). Проверено: py_compile, отсутствие локальных def, импорт и работа функций.
- 2026-08-16 — Удалён хардкод `tlt`; `eval()` в 11 заменён на `ast.literal_eval`. Проверено (visitors_counting sum=8 после удаления).
- 2026-08-16 — Унифицирован текстовый интерфейс: 06 переведён на `request_app_description`, 07 — единое имя файла + описание. Проверено (двухэтапный запуск, roundtrip параметров).
- 2026-08-16 — Личные данные (e-mail, карта) вынесены в `utils/contacts.py`; 6 GUI-модулей переведены на импорт констант. Проверено (py_compile, отсутствие хардкода в GUI).
- 2026-08-16 — Зачистка кода: `requirements.txt` перекодирован в UTF-8; все русские комментарии переведены на английский. Проверено (py_compile 19 файлов, отсутствие кириллических комментариев).
- 2026-08-16 — Создан слой доступа `utils/db.py` (SQLite). Проверено round-trip на фикстуре: camconfig (5 камер), shapes (3000 строк), visitors (392 дня), noSeller (392), evstat (50) — точное совпадение.
- 2026-08-16 — Скрипт миграции `migrate_csv_to_sqlite.py`. Проверен на полной фикстуре (chm1 268k + chm2 20k shapes, visitors/noSeller 392 дня, evstat 50) — 3.8с, точное совпадение; CSV остаётся холодным резервом.
- 2026-08-16 — Ядро алгоритмов переключено на `db.*` (`funcs_initializer` → обёртки над db; `funcs_vis_count_noseller_time` → `db.read_*/write_*`; явный `import pandas` в funcs_CV/05). Проверено на SQLite: find_new_shapes (471 shapes), visitors=8, noSeller=119 — совпадает с боевой базой.
- 2026-08-16 — Переключены на `db.*` модули `funcs_CV` (shape_db_info через SQL COUNT/MIN/MAX, shapes) и GUI 04/05/07/08 (shapes/visitors/evstat). Проверено: py_compile 9 файлов, round-trip visitors/evstat, build_shape_db_info (chm1=268656, chm2=20362). Архивный экспорт 08 остаётся CSV (экспортная папка).
- 2026-08-16 — `1_real_viscount.xlsx` перенесён в таблицу `real_viscount` (long). Миграция конвертирует активные листы (tlt/gld/chm/nvk, пропуская `*_arc`); `read_real_viscount`/`write_real_viscount` в db. Проверено round-trip (chm, 25 дней). Заметки `*` (напр. «2 islands») при переходе не сохраняются.
- 2026-08-16 — П.1: путь к модели зафиксирован (`MODEL_REL_PATH`), добавлена проверка существования; подсчёт строк shapes в CV_SYS переведён на `db.shapes_count`. Убран выбор языка в 01 (п.16, единственный русский).
- 2026-08-16 — П.8: pandas в `db.py` ленивый; лёгкие модули (02/03/06/09/11/01) без pandas. requirements.txt дополнен (beautifulsoup4, httpx, httpcore). Проверено: import лёгких модулей без pandas; тяжёлый DataFrame-путь работает.
