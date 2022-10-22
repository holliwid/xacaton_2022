# xacaton_2022
## :notebook_with_decorative_cover: Описание проекта
Нейронная сеть, способная распознавать людей в СИЗ(Средство индивидуальной защиты) на заводе.
![Alt text](./Readme_sourse/image.png?raw=true "Detected man")
## Интерфейс приложения
![Alt text](./Readme_sourse/interface_1.png?raw=true "Interface_1")
![Alt text](./Readme_sourse/interface_2.png?raw=true "Interface_2")
## Heatmap и scatter
У нас строится heatmap и scatter по 4 разным категориям:

-люди

-люди без штанов

-люди без куртки

-люди без штанов и куртки
![Alt text](./Readme_sourse/heat_human.png?raw=true "Heat human")

## :scroll: Стек
```
Python3.9
SQLite3
PyQt
YoLov5m - для детекции
Deep Sort - для трекинга
```
## :floppy_disk: Установка
База данных находится в папке вмесе со всеми файлами и называется reports.db.

### Установка библиотек для питона
pip install -r requirement_1.txt

запуск приложения через запуск app.py

а дальше просто устанавливаем, что просит в консоли(или само установит)