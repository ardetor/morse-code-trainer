import morse
import random
import colorama

colorama.init()

def params_out_of_bounds():
    print(colorama.Back.RED + "Please enter parameters within the specified limits." + colorama.Style.RESET_ALL + "\n\n\n")

def select_level():
    print(colorama.Back.GREEN + "Welcome to Morse Trainer. Enter '%' to exit." + colorama.Style.RESET_ALL + "\n")
    difficulty = input("Select difficulty level:\n\t1: aoeuidhtns\n\t2: aoeuidhtnspyfgcrl\n\t3: Whole alphabet\n\t4: Alphabet with punctuation\n\nYour choice: ")
    print("\n\n")
    if difficulty == "%":
        print("Goodbye.")
        exit()
    trainer_setup(difficulty)


def trainer_setup(difficulty):
    training_sets = {
        "1" : "aoeuidhtns",
        "2" : "aoeuidhtnspyfgcrl",
        "3" : "aoeuidhtnspyfgcrlqjkxbmwvz",
        "4" : "aoeuidhtnspyfgcrlqjkxbmwvz..,,"
    }
    try:
        now_training = training_sets[difficulty]
    except KeyError:
        params_out_of_bounds()
        return 0
    training_list = []
    for char in now_training:
        training_list.append(char)
    
    train(training_list)


def train(training_list):
    random.seed()
    train_type = input("Select training type:\n\t1: Morse to alphabet translation\n\t2: Alphabet to Morse translation\n\t3: Morse (audio) to alphabet translation\n\n Your choice: ")
    print("\n\n")
    if train_type == "%":
        print(colorama.Back.GREEN + "Quitting..." + colorama.Style.RESET_ALL + "\n\n")
        return 0
    
    if train_type == "1":
        while True:
            letter_to_test = random.choice(training_list)
            if test_to_alpha(letter_to_test) == 0:
                return 0;
    elif train_type == "2":
        while True:
            letter_to_test = random.choice(training_list)
            if test_to_morse(letter_to_test) == 0:
                return 0;
    elif train_type == "3":
        try:
            dot_length = float(input("Set dot length in seconds: (Default is 0.07)\n\nYour choice: "))
        except ValueError:
            dot_length = 0.07
        while True:
            letter_to_test = random.choice(training_list)
            if test_sound_to_alpha(letter_to_test, dot_length) == 0:
                return 0;
    else:
        params_out_of_bounds()
        return 0
        
    
    
def test_to_alpha(alpha):
    answer = alpha
    question = morse.char_to_morse(alpha)
    return test_generic(question, answer)

def test_to_morse(alpha):
    question = alpha
    answer = morse.char_to_morse(alpha)
    return test_generic(question, answer)

def test_sound_to_alpha(alpha, dot_length):
    answer = alpha
    question = morse.morse_to_sound(morse.char_to_morse(alpha), dot_length)
    return test_generic(question, answer)    

def test_generic(question, answer):
    user_answer = input("Translate: " + question + "\n")
    if user_answer == "%":
        print(colorama.Back.GREEN + "Exiting trainer..." + colorama.Style.RESET_ALL + "\n\n")
        return 0
    elif user_answer == answer:
        print("Correct!\n\n")
        return 1
    elif user_answer == "":
        print("The answer is: '", answer, "'\n\n")
        return 1
    else:
        print("Wrong. The answer is: '", answer, "'\n\n")
        return 1

while True:
    select_level()
    
