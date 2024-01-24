import json
import sys

if len(sys.argv)<2:
    print("You need to export chat history from telegram (json format without media) and pass its pass as argument.")
else: 
    json_path = sys.argv[1]

    words = {}
    autors_messages = {}
    autors_characters = {}
    autors_lenght = {}
    
    
    
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        message_count = len(data['messages'])
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
                        words[mword]+=1
        words = dict(sorted(words.items(), key=lambda item: item[1], reverse=True))
        
        
        for key in autors_messages.keys():
            autors_lenght[key] = autors_characters[key]/autors_messages[key]
        
        
        print(f"50 most popular words: ")
        for key in list(words.keys())[:50]:
            print(f"{words[key]}:{key}", end=' ')
        print()
        print()
        print(f"Unique wods count: ", len(words))
        print(f"Autor comparision: (messages) ", dict(sorted(autors_messages.items(), key=lambda item: item[1], reverse=True)) )
        print(f"Autor comparision: (characters) ",dict(sorted(autors_characters.items(), key=lambda item: item[1], reverse=True)) )
        print(f"Autor comparision: (avarage message length) ",dict(sorted(autors_lenght.items(), key=lambda item: item[1], reverse=True)) )