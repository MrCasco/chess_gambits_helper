import openai
from dotenv import load_dotenv
import os
import json

load_dotenv()

openai.api_key = os.getenv('API_KEY')

def ask_if_black_or_white():
    f = open("gambits.txt", "r", encoding='utf8')
    colors = {}
    requests = {}
    for line in f:
        if line.startswith('    '):
            line = line.strip('\n').strip(' ')
            gambit_name, _, steps = line.split(chr(8211))

            completion = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-0301",
              messages=[{"role": "user", "content": "Use 1 word to tell me if the gambit"+gambit_name+" is for black or white"}]
            )
            colors[gambit_name] = completion['choices'][0]['message']['content'].strip('\n')
            requests[gambit_name] = completion
    f.close()

    json_object = json.dumps(colors, indent=2)

    # Writing to sample.json
    with open("gambits_with_colors.json", "a") as outfile:
        outfile.write(json_object)
    return colors



def add_color():
    f = open('gambits_with_colors.json')
    gambits_with_colors = json.load(f)
    f.close()

    plays = {'black':{}, 'white':{}, 'neither':{}}
    opening = ''
    f = open("raw_gambits.txt", "r", encoding='utf8')
    for line in f:
        if line.startswith('    '):
            line = line.strip('\n').strip(' ')
            gambit_name, _, steps = line.split(chr(8211))

            gambit_name = gambit_name.strip(' ')
            steps = steps.strip(' ')

            color = gambits_with_colors[gambit_name].lower().strip('.')
            if color == 'both':
                color = 'neither'
            elif color not in plays:
                print(gambit_name)
                continue
            if opening not in plays[color]:
                plays[color][opening] = {}
            plays[color][opening][gambit_name] = steps
        elif line != '\n':
            opening = line.strip('\n')

    f.close()

    with open("formatted_gambits.json", "a") as outfile:
        json.dump(plays, outfile)

add_color()


# ask_if_black_or_white()
