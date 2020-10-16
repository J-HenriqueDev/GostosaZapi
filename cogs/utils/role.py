import json

with open("utils/cargos-membros.json", encoding="utf-8") as cargos:
    cargos = json.load(cargos)

with open("reactionrole.json", encoding="utf-8") as react:
    reactions = json.load(react)

with open("utils/emojis.json", encoding="utf-8") as emj:
    emojis = json.load(emj)
