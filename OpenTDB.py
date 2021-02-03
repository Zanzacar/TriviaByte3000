import string
import requests
import random
import html
from datetime import datetime, timedelta


class OpenTDB:
    """
        Class to interface with https://opentdb.com/
    """

    def __init__(self):
        self.token = None
        self.token_expires = datetime.now() - timedelta(hours=6)
        self.question = {}
        self.answers = {}
        self.question_bank = []
        self.__update_questions()
        self.next_question()

    def __token_expired(self):
        if (datetime.now() - self.token_expires).total_seconds() > 0:
            return True
        return False

    def __update_token(self):
        self.token = requests.get('https://opentdb.com/api_token.php?command=request').json()['token']
        self.token_expires = datetime.now() + timedelta(hours=6)

    def __update_questions(self):
        if self.__token_expired():
            self.__update_token()
        self.question_bank = requests.get('https://opentdb.com/api.php?amount=10&token='+self.token).json()['results']

    def get_category(self):
        return html.unescape(self.question['category'])

    def get_difficulty(self):
        return html.unescape(self.question['difficulty'])

    def get_question(self):
        return html.unescape(self.question['question'])

    def get_correct_answer(self):
        return html.unescape(self.question['correct_answer'])

    def get_all_answers(self):
        answers = self.question['incorrect_answers']
        answers.append(self.question['correct_answer'])
        random.shuffle(answers)
        self.answers = {}
        self.answers = dict(zip(list(string.ascii_uppercase), answers))
        return self.answers

    def next_question(self):
        if len(self.question_bank) > 0:
            self.question = self.question_bank.pop()
        else:
            self.__update_questions()
            self.question = self.question_bank.pop()

    def check_answer(self, answer):
        if answer in self.answers:
            if self.question['correct_answer'] == self.answers[answer]:
                return 'Correct Answer'
            else:
                return 'Incorrect Answer'
        else:
            return 'Invalid Input'

