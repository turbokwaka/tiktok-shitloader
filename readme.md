![тупоя](https://coolgifs.neocities.org/gifs/68.gif)
# Bullshido Backend Borker

---
Це бекенд-воркер для сайту, який який отримує завдання на генерацію відео,  
створює TTS-аудіо, накладає його на відео та додає субтитри.

---

## Залежності

Основні бібліотеки, що використовуються в проєкті:

- [kokoro-tts](https://pypi.org/project/kokoro-tts/) — синтез мовлення (TTS)
- [whisper-timestamped](https://pypi.org/project/whisper-timestamped/) — розпізнавання мовлення та таймкоди
- [moviepy](https://pypi.org/project/moviepy/) — обробка відео
- [Pillow](https://pypi.org/project/Pillow/) — робота з зображеннями

---

## Запуск локально

1. Клонуй репозиторій:
```bash
   git clone https://github.com/yourname/media-worker.git
   cd media-worker
```

2. Встанови залежності:
```bash
pip install . && pip install .[dev]
```

3. Запусти воркер:

   ```bash
   python main.py
   ```

При першому запуску автоматично завантажуються необхідні моделі у `bin/`.

---

## Тести
```bash
pytest -s tests/smoke_test.py
```
