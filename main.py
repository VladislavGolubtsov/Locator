import sqlite3
from dadata import Dadata


# Функция для поиска координат по адресу
def search(api_key, secret_key, language):
    dadata = Dadata(api_key, secret_key)
    line = input('Введите адрес: ')

    try:
        version = dadata.suggest(name="address", query=line, language=language)
    except Exception as e:
        print(f"\n\nError fetching suggestions: {e}")
        return

    for id_version, key in enumerate(version, start=1):
        print(f"{id_version}. {key['value']}")
    print('0. Вернуться назад')

    version_pick = "none"

    while True:
        pick = input("\nВыберите один из предложенных вариантов"
                     "\nВведите значение и нажмите Enter: ")
        # Проверка введенного значения
        if pick.isdigit() and 0 <= int(pick) <= len(version):
            if int(pick) == 0:
                break
            else:
                version_pick = version[int(pick) - 1]['value']
            print(version_pick)
            break
        else:
            print("Пожалуйста, введите корректное значение.")

    # Получение координат по выбранному адресу
    result = dadata.clean("address", version_pick)
    print(f"Координаты:\n"
          f"\tширота: {result['geo_lat']}\n"
          f"\tдолгота: {result['geo_lon']}")


# Функция для настройки параметров
def settings():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,            
            api_key TEXT,
            secret_key TEXT,
            language TEXT
        )
    ''')

    cursor.execute('SELECT * FROM settings')
    row = cursor.fetchone()

    if row is None:
        print(f'Параметры не заданы!'
              f'\nApi-ключ и Секретный ключ можно получить после регистрации на сайте:'
              f'\n https://dadata.ru/profile/#info\n')
        api = input('Введите значение API-ключа: ')
        key = input('Введите значение Секретного ключа: ')
        while True:
            language = input('Язык, на котором будет возвращаться ответ (en/ru): ')
            if language == 'ru' or language == 'en':
                break
            else:
                print('Пожалуйста, введите корректное значение.')
        cursor.execute('INSERT INTO settings (api_key, secret_key, language) VALUES (?, ?, ?)', (api, key, language))
        conn.commit()

    cursor.execute('SELECT * FROM settings')
    value = cursor.fetchall()
    print(f'\n Api-ключ и Секретный ключ можно получить после регистрации на сайте:'
          f'\n https://dadata.ru/profile/#info\n')
    print(f'\n1. API-ключ: {value[0][1]}')
    print(f'2. Секретный ключ: {value[0][2]}')
    print(f'3. Язык: {value[0][3]}')

    while True:
        mas = [1, 2, 3, 4]

        value = input(f'\n\nВведите 1-3, если хотите изменить один из параметров.\n'
                      f'Введите 4, если хотите вернуться назад.\n'
                      f'Ввод: ')

        if value.isdigit() and int(value) in mas:
            if int(value) == 4:
                conn.commit()
                break
            elif int(value) == 1:
                api = input('Введите значение API-ключа: ')
                cursor.execute('UPDATE settings SET api_key=? WHERE id=?', (api, 1))
            elif int(value) == 2:
                key = input('Введите значение Секретного ключа: ')
                cursor.execute('UPDATE settings SET secret_key=? WHERE id=?', (key, 1))
            else:
                while True:
                    language = input('Язык, на котором будет возвращаться ответ (en/ru): ')
                    if language == 'ru' or language == 'en':
                        break
                    else:
                        print('Пожалуйста, введите корректное значение.\n\n')
                cursor.execute('UPDATE settings SET language=? WHERE id=?', (language, 1))
            conn.commit()
        else:
            print('Пожалуйста, введите корректное значение.')
    conn.commit()
    conn.close()


# Основная функция
def main():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS settings (
               id INTEGER PRIMARY KEY,            
               api_key TEXT,
               secret_key TEXT,
               language TEXT
           )
       ''')
    conn.commit()

    while True:
        while True:
            conn.commit()
            cursor.execute('SELECT * FROM settings')
            row = cursor.fetchone()
            print(f"\n\nLocator\n\n",
                  f"1. Ввести адрес\n",
                  f"2. Настройки\n",
                  f"3. Выход")
            pick = input(f"\nВыберите один из предложенных вариантов"
                        f"\nВведите значение и нажмите Enter: ")
            if pick == "1":
                if row is None:
                    print('\n\nПараметры не заданы!\nПерейдите в настройки')
                else:
                    cursor.execute('SELECT * FROM settings')
                    value = cursor.fetchall()
                    api_key = value[0][1]
                    secret_key = value[0][2]
                    language = value[0][3]
                    search(api_key, secret_key, language)
            elif pick == "2":
                settings()
            elif pick == "3":
                i = -1
                print("Программа завершена.")
                break
            else:
                print('Пожалуйста, введите корректное значение.\n\n')
        if i == -1:
            break


# Запуск основной функции при выполнении скрипта
if __name__ == '__main__':
    main()
