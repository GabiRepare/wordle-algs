#!/usr/bin/python3

import math
import random
import string
from constants import *
from wordle_game import Game, print_game_status

scores = []

# Starts with an arbitrary word, eliminates impossible words and randomly chose
# the next one until the answer is found.
def basic_alg(all_words=False):
    answers = MAIN_ANSWERS + all_words * OTHER_ANSWERS
    for answer in answers:
        if len(scores) % ((len(MAIN_ANSWERS)+all_words*len(OTHER_ANSWERS))//100) == 0:
            print(f"Progress: {len(scores)//((len(MAIN_ANSWERS)+all_words*len(OTHER_ANSWERS))//100)}%")
        possibilities = MAIN_ANSWERS.copy() + OTHER_ANSWERS.copy()
        editable_columns = list(range(0,len(answer)))
        game = Game(answer=answer)
        game.submit("soare")
        while not game.is_won and possibilities:
            # print(f"{answer} is still in the {len(possibilities)} possibilities? {answer in possibilities}")
            # print_game_status(game)
            last_response = game.responses[-1]
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "full"]:
                if i in editable_columns:
                    possibilities = [possibility for possibility in possibilities if possibility[i] == j["guess_char"]]
                    editable_columns.remove(i)
            partial_letters_count = {i:0 for i in string.ascii_lowercase}
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "partial"]:
                new_possibilities = []
                for possibility in possibilities:
                    if possibility[i] != j["guess_char"] and \
                        [possibility[i] for i in editable_columns].count(j["guess_char"]) > partial_letters_count[j["guess_char"]]:
                        new_possibilities.append(possibility)
                possibilities = new_possibilities
                partial_letters_count[j["guess_char"]] += 1
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "none"]:
                possibilities = [possibility for possibility in possibilities if [possibility[i] for i in editable_columns].count(j["guess_char"]) <= [partial["guess_char"] for (k, partial) in last_response.items() if partial["match"] == "partial"].count(j["guess_char"])]
            if possibilities:
                next_guess = random.choice(possibilities)
                possibilities.remove(next_guess)
                game.submit(next_guess)
        if game.is_won:
            scores.append(len(game.responses))
        else:
            print(f"Had a problem with answer \"{answer}\"")
    print(f"The average score is {sum(scores)/len(scores)} ({len(scores)} game played)")
    winning_scores = [score for score in scores if score <= 6]
    print(f"There was {len(winning_scores)} winning games ({len(winning_scores)/len(scores)*100.0}%)")
    print(f"The average score of winning games was {sum(winning_scores)/len(winning_scores)}")


def gab_alg(all_words=False):
    answers = MAIN_ANSWERS + all_words * OTHER_ANSWERS
    for answer in answers:
        if len(scores) % ((len(MAIN_ANSWERS)+all_words*len(OTHER_ANSWERS))//100) == 0:
            print(f"Progress: {len(scores)//((len(MAIN_ANSWERS)+all_words*len(OTHER_ANSWERS))//100)}%")
        # print(f"Started game with answer: {answer}")
        possibilities = MAIN_ANSWERS.copy() + OTHER_ANSWERS.copy()
        editable_columns = list(range(0,len(answer)))
        game = Game(answer=answer)
        game.submit("tares")
        while not game.is_won and possibilities:
            # print(f"{answer} is still in the {len(possibilities)} possibilities? {answer in possibilities}")
            # print_game_status(game)
            last_response = game.responses[-1]
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "full"]:
                if i in editable_columns:
                    possibilities = [possibility for possibility in possibilities if possibility[i] == j["guess_char"]]
                    editable_columns.remove(i)
            partial_letters_count = {i:0 for i in string.ascii_lowercase}
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "partial"]:
                new_possibilities = []
                for possibility in possibilities:
                    if possibility[i] != j["guess_char"] and \
                        [possibility[i] for i in editable_columns].count(j["guess_char"]) > partial_letters_count[j["guess_char"]]:
                        new_possibilities.append(possibility)
                possibilities = new_possibilities
                partial_letters_count[j["guess_char"]] += 1
            for (i, j) in [(i, j) for (i, j) in last_response.items() if j["match"] == "none"]:
                possibilities = [possibility for possibility in possibilities if [possibility[i] for i in editable_columns].count(j["guess_char"]) <= [partial["guess_char"] for (k, partial) in last_response.items() if partial["match"] == "partial"].count(j["guess_char"])]
            if possibilities:
                next_guess = find_best_candidate(possibilities)
                possibilities.remove(next_guess)
                game.submit(next_guess)
        if game.is_won:
            scores.append(len(game.responses))
        else:
            print(f"Had a problem with answer \"{answer}\"")
    print(f"The average score is {sum(scores)/len(scores)} ({len(scores)} game played)")
    winning_scores = [score for score in scores if score <= 6]
    print(f"There was {len(winning_scores)} winning games ({len(winning_scores)/len(scores)*100.0}%)")
    print(f"The average score of winning games was {sum(winning_scores)/len(winning_scores)}")


def freq_score_transform(freq):
    return -1.0 * abs(freq-0.5)+1.5

def find_best_candidate(possibilities):
    # print(f"Number of possibilities: {len(possibilities)}")
    letter_freq = {}
    for letter in string.ascii_lowercase:
        letter_freq[letter] = len([possibility for possibility in possibilities if letter in possibility])/len(possibilities)
    letter_position_freq = {}
    for letter in string.ascii_lowercase:
        letter_position_freq[letter] = {}
        for i in range(0,5):
            letter_position_freq[letter][i] = len([possibility for possibility in possibilities if letter == possibility[i]])/len(possibilities)
    scores = []
    for possibility in possibilities:
        position_freq_score  = math.prod([freq_score_transform(letter_position_freq[possibility[i]][i]) for i in range(0,len(possibility))])
        unique_letters = list(set(possibility))
        freq_score = math.prod([freq_score_transform(letter_freq[unique_letters[i]]) for i in range(0,len(unique_letters))])
        scores.append((possibility, position_freq_score*freq_score))
    sorted_scores = sorted(scores, key=lambda item: item[1], reverse=True)
    # print(sorted_scores[0:100])
    return sorted_scores[0][0]

def find_best_starting_word():
    possibilities = MAIN_ANSWERS.copy() + OTHER_ANSWERS.copy()
    print(find_best_candidate(possibilities))



gab_alg(all_words=True)
