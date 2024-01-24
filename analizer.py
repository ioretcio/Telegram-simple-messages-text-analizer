import json
import sys
import shutil
from datetime import datetime



def plot(x, y, rows=None, columns=None):
    def_col, def_row = get_terminal_size()
    rows = rows if rows else def_row
    columns = columns if columns else def_col
    rows -= 4
    x_scaled = scale(x, columns)
    y_scaled = scale(y, rows)
    canvas = [[" " for _ in range(columns)] for _ in range(rows)]
    
    
    for magic in range (0, 100):
        for ix, iy in zip(x_scaled, y_scaled):
            yyy = min(max(0, rows - iy - 1+magic), rows-1)
            canvas[yyy ][ix] = "▬"
  
    for row in ["".join(row) for row in canvas]:
        print(row)

def scale(x, length):
    s = (
        float(length - 1) / (max(x) - min(x))
        if x and max(x) - min(x) != 0
        else length
    )
    return [int((i - min(x)) * s) for i in x]

def get_terminal_size():
    return shutil.get_terminal_size()


if len(sys.argv)<2:
    print("You need to export chat history from telegram (json format without media) and pass its pass as argument.")
else: 
    json_path = sys.argv[1]

    words = {}
    autors_messages = {}
    autors_characters = {}
    autors_lenght = {}
    autor_calories = {}
    time_segments = {}
    
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        message_count = len(data['messages'])
        time_diff = (datetime.strptime(data['messages'][-1]['date'], "%Y-%m-%dT%H:%M:%S") - datetime.strptime(data['messages'][0]['date'], "%Y-%m-%dT%H:%M:%S")).total_seconds()
        time_interval = time_diff / 50
        for message in data['messages']:
            if message['type'] == "service":
                continue
            
            if not message['from'] in autors_messages.keys():
                autors_messages[message['from']] = 1
            else:
                autors_messages[message['from']] += 1
            
            if not message['from'] in autors_characters.keys():
                autors_characters[message['from']] = len(message['text'])
            else:
                autors_characters[message['from']] += len(message['text'])
            
            if isinstance(message['text'], str):
                message_words = message['text'].split()
                for mword in message_words:
                    if not mword in words.keys():
                        words[mword] = 1
                    else:
                        words[mword] += 1

            message_date = message['date']
            message_segment = int((datetime.strptime(message_date, "%Y-%m-%dT%H:%M:%S") - datetime.strptime(data['messages'][0]['date'], "%Y-%m-%dT%H:%M:%S")).total_seconds() / time_interval)
            if message_segment in time_segments.keys():
                time_segments[message_segment] += 1
            else:
                time_segments[message_segment] = 1
        words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
        
        
        for key in autors_messages.keys():
            autors_lenght[key] = autors_characters[key]/autors_messages[key]
        
        for key in autors_messages.keys():
            autor_calories[key] = (autors_characters[key]/240)/1000
        
        print(f"50 most popular words: ")
        for key in list(words.keys())[:50]:
            print(f"{words[key]}:{key}", end=' ')
        print()
        print()
        print(f"Unique wods count: ", len(words))
        print(f"Autor comparision: (messages) ", dict(sorted(autors_messages.items(), key=lambda item: item[1], reverse=True)) )
        print(f"Autor comparision: (characters) ",dict(sorted(autors_characters.items(), key=lambda item: item[1], reverse=True)) )
        print(f"Autor comparision: (avarage message length) ",dict(sorted(autors_lenght.items(), key=lambda item: item[1], reverse=True)) )
        print(f"Autor calories: (Kcal) ",dict(sorted(autor_calories.items(), key=lambda item: item[1], reverse=True)) )
        print()
        print("Communication frequency:")
        print()
        x = range(0, 50, 1)
        y = list(time_segments.values())
        plot(x, y)