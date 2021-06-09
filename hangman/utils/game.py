import random
from typing import List


class Hangman:
    """"
    Class Hangman represents one game of Hangman wherein players
    try to guess for a mystery word within a given number of turns (5).
    Every turn the players have to guess a letter.
    """

    def __init__(self) -> None:
        """"
        Constructs a hangman game environment with all the necesarry attributes.
        A random word is picked out of a fixed list of possible words.
        List are created for keeping track of rightly and wrongly guessed letters.
        It declares variables to keep track of lives of a player, amount of turns
        taken and amount of wrongly chosen letters.
        """

        self.possible_words: List[str] = self.fill_list_possible_words()
        self.word_to_find: List[str] = self.fill_list_word_to_find()
        self.lives: int = 5
        self.correctly_guessed_numbers: List[str] = self.initialize_correctly_guessed_letters(self.word_to_find)
        self.wrongly_guessed_letters: List[str] = []
        self.turn_count: int = 0
        self.error_count: int = 0


    def start_game(self) -> None:
        """"
        Initializes the game by starting a while loop with two conditions.
        The loop continues as long as these conditions remain unchanged:
        one: the word is not guessed
        two: the player has at least 1 life

        If the word is guessed, end the program with a 'well played'-message
        If there are no more lives left, end the program with a 'game over'-message

        Otherwise play another round. Or if it is the start of the game, play the first round
        """

        word_guessed: bool = False
        lives_left: bool = True

        while not word_guessed and lives_left:
            # check if word is guessed
            if '_' not in self.correctly_guessed_numbers:
                word_guessed = True
                self.well_played()
            # check if lives left
            elif self.lives == 0:
                lives_left = False
                self.game_over()
            # else play another round
            else:
                # for the first play
                if self.turn_count > 0:
                    self.print_turn()
                # for the second and following plays
                else:
                    print("\nWELCOME TO ## HANGMAN ##"
                          "\nFIND OUR MYSTERY WORD BEFORE YOU RUN OUT OF LIVES"
                          "\nYOU HAVE FIVE"
                          "\nGOOD LUCK!"
                          "\n")

                    self.print_mystery_word_letters_found()
                self.play()


    def play(self) -> None:
        """
        Asks the player to guess an alphabet letter. If player provides something else,
        this function will continue to ask for another, correct letter before advancing.
        Then it checkes if this letter is in the mystery word.
        If so, it replaces the '_' in the rightly guessed letters list.
        If not, it is added to the wrongly guessed letters list (if it is not already there).
        In this case, a life is lost and an error is counted.
        Count a turn at the end.
        """

        # ask for user input
        guessed_letter: str = input("Choose a letter: ")
        guessed_letter: str = guessed_letter.strip().upper()

        # check formal correctness of string-input:
        letter_format_correct: bool = self.check_letter_format(guessed_letter)
        while not letter_format_correct:
            guessed_letter: str = input("Choose a letter: ").strip().upper()
            letter_format_correct: bool = self.check_letter_format(guessed_letter)

        # check if input letter is in word_to_find
        if guessed_letter in self.word_to_find:
            self.replace_letter_in_correctly_guessed_letters(guessed_letter)
        else:
            self.error_count += 1
            self.lives -= 1
            if guessed_letter not in self.wrongly_guessed_letters:
                self.wrongly_guessed_letters.append(guessed_letter)

        # increment turn_count
        self.turn_count += 1


    def print_turn(self) -> None:
        """"
        Prints the status of the game after every turn, for as long as the game is not finished.
        Included in the information: which turn, mystery word with already found letters, wrongly
        guessed letters, lives left, errors made
        """

        print("\n"
              "TURN", self.turn_count,
              "\n======")

        self.print_mystery_word_letters_found()

        print("These letters you already used: ", end=' ')
        for letter in self.wrongly_guessed_letters:
            print(letter, end=' ')
        print("\n")

        if self.lives == 1:
            life_or_lives: str = 'life'
        else:
            life_or_lives = 'lives'
        print("You have", self.lives, life_or_lives, "left")

        if self.error_count == 1:
            error_or_errors: str = 'error'
        else:
            error_or_errors = 'errors'
        print("You have made", self.error_count, error_or_errors)
        print("\n")


    def print_mystery_word_letters_found(self) -> None:
        """"
        Prints the mystery word.
        '_' for letters that have not been found yet.
        The letter itself for found letters.
        """

        print("MYSTERY WORD: ", end=' ')
        for letter in self.correctly_guessed_numbers:
            print(letter, end=' ')
        print("\n")


    def well_played(self) -> None:
        """
        Prints as message when game ends in a win for the player.
        It provides information about amount of turns, the mystery word, the lives left
        """
        mystery_word: str = ''
        for letter in self.word_to_find:
            mystery_word += letter

        if self.lives == 1:
            life_or_lives = 'life'
        else:
            life_or_lives = 'lives'
        print("\nWell played!"
              "\nIt took you", self.turn_count, "turns to solve the puzzle and find the mystery word:", mystery_word,
              "\nYou had", self.lives, life_or_lives ,"left"
              "\n")


    def game_over(self) -> None:
        """"
        Prints info when game ends in a loss for the player.
        Provides the amount of turns and lift the mask of the mystery word itself.
        """

        mystery_word: str = ''
        for letter in self.word_to_find:
            mystery_word += letter

        print("\nAuwch. You do not have any lives left."
              "\nYou had", self.turn_count, "turns and you still were not capable of finding the mystery word ;)"
              "\nThe mystery word was", mystery_word,
              "\n***********"
              "\n*GAME OVER*"
              "\n***********"
              "\n")


    def check_letter_format(self, letter: str) -> bool:
        """
        Checks the formal correctness of a given letter. It should be one letter from
        a to z (or A to Z). Prints a detailed error message for two types of mistakes:
        not a single character or not an letter from a to z
        :param letter: letter: the letter that is provided as input by the player
        :return: a boolean value indicating True for correctness of the format, False is not
        """

        if len(letter) != 1:
            print("ERROR: please insert only one character")
            return False
        elif letter < 'A' or letter > 'Z':
            print("ERROR: please insert a letter from the alphabet only: ")
            return False
        return True


    def replace_letter_in_correctly_guessed_letters(self, letter: str) -> None:
        """
        Replaces a correctly guessed letter in the corresponding list
        :param letter: the letter that the player has lastly provided and is part of the mystery word
        """

        for index, character in enumerate(self.word_to_find):
            if character == letter:
                self.correctly_guessed_numbers[index] = letter


    def fill_list_possible_words(self) -> List[str]:
        """
        Fills the attribute-list with possible mystery words
        :return: a list with candidate-mystery words
        """

        return ['becode',
                'learning',
                'mathematics',
                'sessions',
                'arduino',
                'python',
                'hangman']


    def fill_list_word_to_find(self) -> List[str]:
        """
        Picks a random word from the candidate-mystery words and
        transforms it into a list a single characters
        :return: a list of string characters that each represent a letter from the mystery word
        """

        random_word_to_find: str = self.pick_random_word()

        # create an empty list to fill up with the separate characters of a word. Then fill it up
        word_to_find_in_letters: List[str] = []
        for character in random_word_to_find:
            char: str = character.upper()
            word_to_find_in_letters.append(char)

        return word_to_find_in_letters


    def pick_random_word(self) -> str:
        """
        Picks a random word from the candidate-mystery words
        :return: a randomly chosen mystery word
        """

        count_possible_words: int = len(self.possible_words)
        random_number: int = random.randint(0, count_possible_words - 1)
        random_word: str = self.possible_words[random_number]
        return random_word


    def initialize_correctly_guessed_letters(self, word_to_find: List[str]) -> List[str]:
        """
        Creates a list of '_' for every letter of the mystery word
        :param word_to_find: list of every character in the mystery word
        :return: list with the same amount of strings '_'
        """

        count_letters_to_find = len(word_to_find)
        empty_correctly_guessed_numbers = ['_'] * count_letters_to_find

        return empty_correctly_guessed_numbers
