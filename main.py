import csv
import random
from pathlib import Path
import sys  # import necessary crates

def load_database(filepath):  #database loading prog
    cards = []
    try:
        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cards.append({
                    "type": row["type"].strip().lower(),
                    "prompt": row["prompt"].strip(),
                    "answer": row["answer"].strip(),
                    "notes": row.get("notes", "").strip()  # load csv file into categories
                })
        print(filepath)
        return cards
    except FileNotFoundError:
        print(f"Could not find '{filepath}'.")  # basic failsafe
        sys.exit(1)

def grade_user(correct,total,missed_cards):
    if correct == total:
        print(f"\nSession Complete! Score: {correct}/{total} (\033[32m100.0%\033[0m)")
        print(f"\nCongrats, you nailed it!")
        return
    elif 0.85 <= correct/total < 1:
        print(f"\nSession Complete! Score: {correct}/{total} (\033[32m{(correct / total * 100):.1f}%\033[0m)")  # score
    elif 0.50 <= correct/total < 0.85:
        print(f"\nSession Complete! Score: {correct}/{total} (\033[33m{(correct / total * 100):.1f}%\033[0m)")
    else:
        print(f"\nSession Complete! Score: {correct}/{total} (\033[31m{(correct / total * 100) if total else 0:.1f}%\033[0m)")

    try_again = input(f"\nYou missed {total - correct} cards! Would you like to try them again? (y/N) ")

    if try_again.lower() == "y":
        selected_type = "missed"
        run_quiz(missed_cards, selected_type)
    else:
        return

def scramble_hints(answer): # scramble words for hints for sentences
    words = answer.split()

    if len(words) > 1:
        shuffled = words.copy()
        while shuffled == words:
            random.shuffle(shuffled)
        words = shuffled
    else:
        random.shuffle(words)

    return " ".join(words).lower()

def run_quiz(cards, selected_type):
    if not cards:
        print("No cards found for this choice")  # check if cards of type selected are available
        return

    random.shuffle(cards)
    correct = 0
    total = len(cards)  # setup var
    hints_flag = False
    missed_cards = []

    if selected_type == "sentence":
        hints = input(f"\nStarting sentence session with {total} cards. Would you like hints? (y/N) : \n")  # warns user how many cards to do

        if hints.lower() == 'y':
            hints_flag = True

    print(f"\nStarting session with {total} cards. Type 'q' to exit early.\n")  # warns user how many cards to do

    for i, card in enumerate(cards, 1):  # actual game loop
        try:
            print(f"[{i}/{total}] [{card['type'].upper()}] {card['prompt'].split('-', 1)[1]}")  # for new conjugation endings feature/inline prompt hints
            answer_prompt = card['prompt'].split('-', 1)[0]
            user_input = input(f"Your Answer: {answer_prompt}").strip()  # get answer
        except IndexError:
            print(f"[{i}/{total}] [{card['type'].upper()}] {card['prompt']}")  # fallback for if no inline prompt in csv
            if hints_flag:
                print(f"Hint: {scramble_hints(card['answer'])}") # prints hint if sentence mode
            user_input = input(f"Your Answer: ").strip()  # get answer

        if user_input.lower() == 'q':
            total = i - 1
            break  # quit function

        if user_input.lower() == card["answer"].lower():
            print("\033[32mCorrect!\033[0m")
            correct += 1  #dopamine hit. score system
        else:
            print(f"\033[31mIncorrect.\033[0m Answer: {card['answer']}")  # correction
            missed_cards.append({
                "type": card["type"].strip().lower(),
                "prompt": card["prompt"].strip(),
                "answer": card["answer"].strip(),
                "notes": card.get("notes", "").strip()  # load csv file into categories
            })

        if card["notes"]:
            print(f"  Note: {card['notes']}")
        print("-" * 35)  # next line reset

    grade_user(correct, total, missed_cards)

def choose_database():
    folder_prefix = Path("databases")
    database_input = input("Input file name of database: ").strip()

    if database_input == "":  # blank choice -> default database
        database_choice = str(folder_prefix / "default.csv")
    else:
        user_path = Path(database_input)
        database_choice = str(folder_prefix / f"{user_path.stem}.csv") # clean up database import for the user

    return database_choice

def choose_type(card_types, all_cards):
    selected_type = "all" # default selected type

    print("=== Language Flashcard Trainer ===")  # in principle can be any language
    print("1. All Cards")
    for idx, ctype in enumerate(card_types, 2):
        print(f"{idx}. Only {ctype.capitalize()}")  #print set options

    choice = input("\nSelect mode (number): ").strip()  # lets user pick what set to do

    if choice == "1":
        selected_cards = all_cards  # sets cards to all cards
    elif choice.isdigit() and 2 <= int(choice) <= len(card_types) + 1:
        selected_type = card_types[int(choice) - 2]
        selected_cards = [c for c in all_cards if c["type"] == selected_type]  # sets card to whatever user chose
    else:
        print("Invalid selection. Loading all cards.")
        selected_cards = all_cards  # failsafe for idiot users

    return selected_cards, selected_type

def main():
    database_choice = choose_database()
    all_cards = load_database(database_choice)  # let user pick database
    card_types = sorted(list(set(c["type"] for c in all_cards)))  # sets up user choice for which card set to do

    selected_cards, selected_type = choose_type(card_types, all_cards)

    run_quiz(selected_cards, selected_type)  #run quiz normally

if __name__ == "__main__":
    main()
