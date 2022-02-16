#!/usr/bin/python3

import random
from sty import fg, bg, rs
from constants import *

class Game:
    def __init__(self, answer=None):
        self.answer = answer if answer is not None else random.choice(MAIN_ANSWERS)
        self.is_won = False
        self.responses = []

    def submit(self, guess: str):
        if len(guess) != 5:
            raise ValueError("The provided guess wasn't 5 characters long")
        if guess.lower() not in [*MAIN_ANSWERS, *OTHER_ANSWERS]:
            raise ValueError("The provided guess isn't a valid word")
        response = {}
        char_map = {key: value for (key, value) in enumerate(guess.lower())}
        answer_map = {key: value for (key, value) in enumerate(self.answer)}
        #Check for full matches
        for (key,char) in list(char_map.items()):
            if char == answer_map[key]:
                response[key] = {"guess_char": char, "match": "full"}
                char_map.pop(key)
                answer_map.pop(key)
        self.is_won = not char_map
        #Check for patrial matches
        for (key,char) in list(char_map.items()):
            match_key = self.find_in_dict(answer_map, char)
            if match_key != None:
                response[key] = {"guess_char": char, "match": "partial"}
                char_map.pop(key)
                answer_map.pop(match_key)
        #Check for mismatches
        for (key,char) in list(char_map.items()):
            response[key] = {"guess_char": char, "match": "none"}
        self.responses.append(response)

    def find_in_dict(self, dict: dict, value):
        for (key,item) in dict.items():
            if item == value:
                return key
        return None

def print_game_status(game, with_answer=False):
    print("-----------------")
    if game.is_won:
        print("The game is won!")
    if game.is_won or with_answer:
        print(f"Answer: {game.answer}")
    print(f"Number of tries: {len(game.responses)}")
    print("")
    for (key, response) in enumerate(game.responses):
        colorized_reponse = ""
        for (i, j) in sorted(response.items()):
            if j["match"] == "full":
                colorized_reponse += bg.green + j["guess_char"] + bg.rs
            elif j["match"] == "partial":
                colorized_reponse += bg.yellow + j["guess_char"] + bg.rs
            elif j["match"] == "none":
                colorized_reponse += bg.blue + j["guess_char"] + bg.rs
        print(f"{key+1}: {colorized_reponse}")
    print("-----------------")

if __name__ == "__main__":
    game = Game("naval")
    while not game.is_won:
        print("\nPlease enter your guess (5 letters word):")
        guess = input()
        try:
            game.submit(guess)
            print_game_status(game, with_answer=True)
        except ValueError as err:
            print(err.args[0])
