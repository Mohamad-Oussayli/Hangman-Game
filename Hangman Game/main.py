import data
from thinker import Thinker

def play_game(word_length: int, tries: int = 6) -> None:
    thinker = Thinker(nb_of_letters=word_length)

    while  tries > 0:
        guessed_letter = thinker.guess()

        if not right_guess(guessed_letter):
            tries -= 1
            print("Incorrect guess. Attempts remaining:", tries)
            thinker.think(guessed_letter , [])
            continue

        while True:
            try:
                positions = get_positions(guessed_letter=guessed_letter)
                response = thinker.think(letter=guessed_letter, positions=positions)
                print("Current word state: ", response)
                break
            except ValueError:
                    print("Invalid position(s). Please enter new position(s).")
        
        if is_word_guessed(response):
            print("Congratulations! I guessed the word.")
            data.learn_word(word=response)
            return

    handle_game_end(word_length=word_length)  


def is_word_guessed(state: str) -> bool:
    return '_' not in state


def right_guess(guessed_letter: str) -> bool:
    response = input(f"Is '{guessed_letter}' in the word? (y/n): ").strip().lower()
    if response not in ["y","n"]:
        print("Invalid input. Please enter 'y' or 'n'.")
        return right_guess(guessed_letter)
    return response == "y"


def get_positions(guessed_letter) -> list[int]:
    positions_str = input(f"Enter the position(s) of '{guessed_letter}' in the word (space-separated): ")
    positions = [int(pos.strip()) - 1 if pos.strip().isdigit() else str(pos.strip()) for pos in positions_str.split()]
    return positions


def handle_game_end(word_length) -> None:
    print("Game over! All attempts have been exhausted.")
    while True:
        new_word = input("Please enter the word you were thinking of: ")
        if len(new_word) == word_length:
            data.learn_word(new_word)
            break
        else:
            print(f"The word must have exactly {word_length} letters.")


def get_word_length() -> int:
    word_length = input("Enter the size of the word(between 4 and 15): ")
    if not ( word_length.isdigit() and (3 < int(word_length) <= 15) ):
        return get_word_length()
    return int(word_length)


if __name__ == "__main__":
    word_length = get_word_length()
    play_game(word_length=word_length)
