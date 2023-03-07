from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_gambits():
    plays = {}
    opening = ''
    f = open("raw_gambits.txt", "r", encoding='utf8')
    for line in f:
        if line.startswith('    '):
            line = line.strip('\n').strip(' ')
            gambit_name, _, steps = line.split(chr(8211))

            gambit_name = gambit_name.strip(' ')
            steps = steps.strip(' ')

            if opening not in plays:
                plays[opening] = {}
            plays[opening][gambit_name] = steps
        elif line != '\n':
            opening = line.strip('\n')
    return plays


@app.get("/{moves_taken}")
async def throw_gambit(moves_taken):
    gambits = get_gambits()
    possible_next_move = {}
    for opening, gambit_with_steps in gambits.items():
        for name, steps in gambit_with_steps.items():
            if steps.startswith(moves_taken):
                next_moves = steps.replace(moves_taken, '').strip(' ')
                if opening not in possible_next_move:
                    possible_next_move[opening] = {}
                possible_next_move[opening][name] = next_moves
    return {'response': 'No gambits :('} if not possible_next_move else possible_next_move
