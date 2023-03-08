from fastapi import FastAPI
import json

app = FastAPI()

f = open('formatted_gambits.json')
gambits = json.load(f)
f.close()

@app.get("/")
def get_gambits():
    return gambits


@app.get("/{color}/{moves_taken}")
async def throw_gambit(color, moves_taken):
    gambits = gambits[color]
    possible_next_move = {}
    for opening, gambit_with_steps in gambits.items():
        for name, steps in gambit_with_steps.items():
            if steps.startswith(moves_taken):
                next_moves = steps.replace(moves_taken, '').strip(' ')
                if opening not in possible_next_move:
                    possible_next_move[opening] = {}
                possible_next_move[opening][name] = next_moves
    return {'response': 'No gambits :('} if not possible_next_move else possible_next_move
