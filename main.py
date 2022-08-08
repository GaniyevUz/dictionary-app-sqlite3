import os
from model import Dictionary  # type: ignore
from utils.db import create_connection, read_all, update, delete, create, \
    execute, read_one, update_used  # type: ignore
from rich.console import Console
from rich.table import Table
from rich import print
from rich.theme import Theme
from translations import *  # type: ignore

theme = Theme({"success": 'green', "error": 'bold red', "info": 'bold blue', "warning": 'bold yellow'})
console = Console(theme=theme)

if __name__ == '__main__':
    os.system('cls')
    console.print(MENU, style="green")
    conn = create_connection('database.db')
    cur = conn.cursor()
    if conn:
        while True:
            menu = input("$ ~# ")
            while not menu.isdigit():
                console.print('use only numbers', style="error")
                menu = input("$ ~# ")
            menu = int(menu)
            if menu == 1:
                source, target = execute(conn, "select `source`, `target` from language")
                s, t = language[source], lang[target]
                word_input = input(f"{source}->{target} ~#  ").lower()
                word = read_one(conn, {s: word_input})
                if word:
                    update_used(conn, word[0])
                    print('result:', end=' ')
                    console.print(word[t].capitalize(), style='success')
                else:
                    console.print('word not found:', word_input, style='error')
                    like = execute(conn, f"select {s} from dictionary where {s} like '%{word_input}%' limit 10", False,
                                   True)
                    if like and len(word_input) >= 2:
                        console.print('did you mean these words ?', style='success')
                        for word in like:
                            console.print(word[0], end=' ', style='info')
                        print()
            elif menu == 2:
                new_words = []
                for i in langs:
                    new = input(f'{i}: ')
                    new_words.append(new.lower())
                uzbek, russian, english = new_words
                is_exist = execute(conn,
                                   f"SELECT * FROM dictionary WHERE uzbek='{uzbek}' or russian='{russian}' "
                                   f"or english='{english}'")
                if is_exist:
                    console.print('word already exists in dictionary', style='error')
                else:
                    create(conn, new_words)
                    console.print("word has been added successfully", style='success')
            elif menu == 3:
                indexes = read_all(conn, 'id')
                print(*list(*zip(*indexes)))
                print("enter the desired word index from the list above")
                index = int(input("update$ ~#  "))
                new_words = []
                for i in langs:
                    new = input(f'{i}: ')
                    new_words.append(new.lower())
                uzbek, russian, english = new_words
                new_words = Dictionary(id=index, uzbek=uzbek, russian=russian, english=english)
                update(conn, new_words)
                console.print("word has been updated successfully", style="success")
            elif menu == 4:
                indexes = read_all(conn, 'id')
                print(*list(*zip(*indexes)))
                print("enter the desired word index from the list above")
                index = int(input("delete$ ~#  "))
                print(delete(conn, index))
                console.print("word has been deleted successfully", style="success")
            elif menu == 5:
                words = read_all(conn)
                table1 = Table(title="List of words", padding=(0, 2))
                table1.add_column("#", style="magenta")
                table1.add_column("Uzbek", style="cyan")
                table1.add_column("Russian", style="purple")
                table1.add_column("English", style="yellow")
                num = 1
                for word in words:
                    table1.add_row(str(num), word[1], word[2], word[3])
                    num += 1
                    # print(f'{word[-2]} is used in {word[-1]} times')
                console.print(table1)
            elif menu == 6:
                console.print("uz: Uzbek, ru: Russian, en: English", style='warning')
                console.print('Please enter source & target language like uz->en', style='info')
                input_lang = input('lang ~# ')
                if input_lang.__contains__('->'):
                    source, target = input_lang.split('->')
                else:
                    console.print('use -> and ', end=' ')
                    source, target = None, None
                while True:
                    if source in ['uz', 'ru', 'en'] and target in ['uz', 'ru', 'en']:
                        break
                    else:
                        console.print('incorrect source or target language', style='error')
                        input_lang = input('lang ~# ')
                        if input_lang.__contains__('->'):
                            source, target = input_lang.split('->')
                execute(conn, f"update language set source='{source}', "
                              f"target='{target}' where id=1", True)
                console.print('language has been updated successfully', style='success')
            elif menu == 7:
                words = execute(conn, f"select * from dictionary order by used desc limit 10", False, True)
                table = Table(title="Most searched words", padding=(0, 2))
                table.add_column("#", style="cyan")
                table.add_column("word", style="magenta")
                table.add_column("used", style="yellow")
                num = 1
                for word in words:
                    if word[-1] > 0:
                        table.add_row(str(num), word[-2], str(word[-1]) + ' times')
                        num += 1
                        # print(f'{word[-2]} is used in {word[-1]} times')
                console.print(table)
            elif menu == 8:
                print("program finished!!!")
                break
            else:
                os.system('cls')
                console.print(MENU, style="green")
