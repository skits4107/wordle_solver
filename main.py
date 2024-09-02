
import random
from colorama import Fore

def get_word_from_user(words):
    while True:
        word = input("enter wordle word to solve for: ")
        if word not in words:
            print("not a valid word")
            exit(-1)
        return word

def get_correctness(guess, word_to_solve):
    correctness = {}
    remaining_letters = list(word_to_solve)

    for i in range(len(guess)):
        if guess[i] == remaining_letters[i]:
            # mark letter as used
            remaining_letters[i] = None
            # 1 for correct letter and spot
            correctness[i] = 1

        elif guess[i] in remaining_letters:
            # mark letter as used
            remaining_letters[remaining_letters.index(guess[i])] = None
            #0 for crrect letter in wrong spot
            correctness[i] = 0 

        else:
             # -1 for wrong letter completely
            correctness[i] = -1

    return correctness

def get_possible_words(words, guess, correctness):  
    possible_words = []

    for word in words:
        is_valid = True
        used_positions = set()  # Track positions of letters we've accounted for

        # First pass: Check green letters and mark their positions as used
        for i, (g, c) in enumerate(zip(guess, word)):
            if correctness[i] == 1:
                if g != c:
                    is_valid = False
                    break
                used_positions.add(i)

        if not is_valid:
            continue

        # Second pass: Check yellow and gray letters
        for i, g in enumerate(guess):
            if correctness[i] == 0:  # Yellow letter
                #ensure letter is not in same posiiton
                if g == word[i]:
                    is_valid = False
                    break
                # Find a position where this yellow letter appears in the word in a position not already accounted for
                for j, c in enumerate(word):
                    if c == g and j not in used_positions:
                        used_positions.add(j)
                        break
                else:  # If we didn't break, it means we couldn't find a valid position
                    is_valid = False
                    break
            elif correctness[i] == -1:  # Gray letter
                if g in word and word.index(g) not in used_positions:
                    is_valid = False
                    break

        if is_valid:
            possible_words.append(word)

    return possible_words

def print_guess(guess, correctness):
    for i, c in enumerate(guess):
        color = Fore.WHITE
        if correctness[i] == 1:
            color = Fore.GREEN
        elif correctness[i] == 0:
            color = Fore.YELLOW
        print(color + c, end="")

    print(Fore.WHITE+"\n", end="")

def solve_wordle(words, word_to_solve):
    valid_words = words

    amount_of_guesses = 6

   # guesses = []

    for i in range(amount_of_guesses):
        guess = random.choice(valid_words)
        #guesses.append(guess)

        correctness = get_correctness(guess, word_to_solve)

        print_guess(guess, correctness)

        if guess == word_to_solve:
            return True

        valid_words = get_possible_words(valid_words, guess, correctness)

        if not valid_words:
            print("how did you do this")
            exit(-1)
    print("ran out of guesses!")
    return False

def main():
    with open("wordle_words.txt", 'r') as file:
        file_content = file.read()
    words = file_content.strip().split('\n')

    word = get_word_from_user(words)

    solved = solve_wordle(words, word)

if __name__ == "__main__":
    main()