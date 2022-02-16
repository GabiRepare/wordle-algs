This is just a small project to explore ways to improve an average score in the popular game Wordle. Was done during a night, hacketon style, so it's a bit of a mess.

`constants.py` contains the two wordlists used in the source code of the NewYorkTime Wordle game at the time of this project.

Running `wordle_game` gives you a working CLI version of Wordle

Running `wordle_alg` currently runs my latest algorithm on the whole 12k word list.

I've made 2 algorithms, one basic (`basic_alg`) and one with an extra kick.

## basic_alg

Starts with an arbitrary word, eliminates impossible words and randomly chose the next one until the answer is found. Nothing crazy. The arbitrary starting word currently is "soare" (recommended by a random website)

**Output of basic_alg on the Wordle word list**
```
The average score is 4.840190558683413 (2309 game played)
There was 2018 winning games (87.39714161974881%)
The average score of winning games was 4.444995044598612
```

**Output of the basic_alg on the accepted words list**
```
The average score is 5.095311655209701 (12947 game played)
There was 10726 winning games (82.84544682165753%)
The average score of winning games was 4.507644974827522
```

## gab_alg

This is the same as `basic_alg`, but instead of using an arbitrary starting word and randomly chosing followup words, a scoring function is used on each possible word to find the one with the highest score. The scoring fonction looks like this.

```
word_score = letter_frequency_score X in_position_frequency_score
```
Where
```
letter_frequency_score = t(f_1)*t(f_2)*t(f_3)...
```
t() is a function that transforms a frequency into a score, more on that further
`f_1`, `f_2`, `f_3`, ... are the the respective frequencies for each unique letter in the word (number of word containing the given letter divided by the dictionnary size, 12947)

```
in_position_frequency_score = t(p_1)*t(p_2)*t(p_3)...
```
`p_1`, `p_2`, `p_3`, ...are the letter frequency at a given postion. For exemple, in the word "toast", `p_1` would be the frequency of words with a letter `t` at the beggining.

**The function t()**
The best frequency that garanty the maximum amount of word elimination is 50%. Anything higher and we won't learn much about the secret word. So t() has to peak at 0.5 and have its lows at 0 and 1.
It also needs to return numbers bigger than 1 because other wise, words with less than 5 unique letters gets better scores.

So I came up with this simple absolute value function
```
t(x) = -1 * abs(x - 0.5) + 1.5
```

I didn't really tune or optimize this scoring function since the sun was already rising and that the result was already a big improvement.

**Output of the gab_alg on the Wordle word list**
```
The average score is 4.130359462970983 (2309 game played)
There was 2245 winning games (97.22823733217844%)
The average score of winning games was 4.028953229398664
```

**Output of the gab_alg on the accepted words list**
```
The average score is 4.7106665636827065 (12947 game played)
There was 11525 winning games (89.01676063953039%)
The average score of winning games was 4.293015184381779
```
