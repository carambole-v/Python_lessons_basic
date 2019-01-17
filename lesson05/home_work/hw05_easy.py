# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.
import os

i = 1
while i < 10:
    try:
        os.mkdir(f"dir_{i}")
        print(f"Создана директория dir_{i}")
    except Exception as e:
        print(f"При создании директории dir_{i} произошла ошибка: {e}")
    finally:
        i += 1

i = 1
while i < 10:
    try:
        os.rmdir(f"dir_{i}")
        print(f"Удалена директория dir_{i}")
    except Exception as e:
        print(f"При удалении директории dir_{i} произошла ошибка: {e}")
    finally:
        i += 1

# Задача-2:
# Напишите скрипт, отображающий папки текущей директории.
import os

for item in os.scandir():
    if item.is_dir():
        print(item.name)

# Задача-3:
# Напишите скрипт, создающий копию файла, из которого запущен данный скрипт.
import sys

source_fn = sys.argv[0]
dest_fn = sys.argv[0]+".cpy"

print(f"Copy {source_fn} to {dest_fn}")
try:
    source = open(source_fn, "r", encoding="UTF-8")
    content = source.readlines()
except Exception as e:
    print(f"Возникла ошибка при чтении из файла {source_fn}: {e}")
finally:
    source.close()

try:
    dest = open(dest_fn, "w", encoding="UTF-8")
    dest.writelines(content)
except Exception as e:
    print(f"Возникла ошибка при записи в файл {dest_fn}: {e}")
finally:
    dest.close()
