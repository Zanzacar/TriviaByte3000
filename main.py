

from OpenTDB import OpenTDB

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    trivia = OpenTDB()
    while True:
        print(f'{trivia.get_category()} - {trivia.get_difficulty()}')
        print(trivia.get_question())
        for a in trivia.get_all_answers():
            print(f'{a}: {trivia.answers[a]}')
        answer = input('Enter Selection: ')
        print(trivia.check_answer(answer))
        print('#'*140)
        trivia.next_question()
