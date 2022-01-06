import requests
import sys

from enum import Enum
from bs4 import BeautifulSoup


args = sys.argv


class Languages(Enum):
    All = 'all'
    Arabic = 'arabic'
    German = 'german'
    English = 'english'
    Spanish = 'spanish'
    French = 'french'
    Hebrew = 'hebrew'
    Japanese = 'japanese'
    Dutch = 'dutch'
    Polish = 'polish'
    Portuguese = 'portuguese'
    Romanian = 'romanian'
    Russian = 'russian'
    Turkish = 'turkish'


class Translator:
    URL = f'https://context.reverso.net/translation/'

    def __init__(self, number_language, type_language, word_translate):
        self.number_language = number_language
        self.type_language = type_language
        self.word_translate = word_translate

    def connect(self, translate_conn, wrd):
        headers = {'User-Agent': 'Mozilla/5.0'}
        page = requests.get(f'{self.URL}{translate_conn}{wrd}', headers=headers)

        return page

    def translate(self, org_lang, lang_target, num):
        translate_direction = f"{org_lang}-{lang_target}/".lower()
        conn = self.connect(translate_direction, self.word_translate)

        try:
            if conn.status_code == 200:
                soup = BeautifulSoup(conn.content, 'html.parser')

                translations = [x.text.strip() for x in soup.select('#translations-content > .translation')]
                examples = [x.text.strip() for x in soup.select('#examples-content > .example >  .ltr')]

                translate = f'{lang_target} Translations:'
                example = f'{lang_target} Examples:'
                result = translations[:num]
                example_res = '\n'.join(f'{x}\n{y}\n' for x, y in zip(examples[:num * 2:2], examples[1:num * 2:2]))

                with open(f'{self.word_translate}.txt', 'a', encoding='utf-8') as f:
                    print(translate, file=f)
                    print(*result, '\n', file=f)
                    print(example, file=f)
                    print(example_res, file=f)
            else:
                print(f'Sorry, unable to find {self.word_translate}')
                exit()
        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection')

    def info_print(self):
        self.start()

        with open(f'{self.word_translate}.txt', 'r', encoding='utf-8') as f:
            print(f.read())

    def start(self):
        if self.type_language == 'All':
            for target in Languages:
                if target.name == 'All' or target.name == self.number_language:
                    continue
                self.translate(self.number_language, target.name, 1)
        else:
            self.translate(self.number_language, self.type_language, 1)


if __name__ in '__main__':
    if len(args) > 4:
        print('The script should be called with two arguments, the first and the second number to be multiplied')
    else:
        first_num = str(args[1])
        second_num = str(args[2])
        last_num = str(args[3])

        try:
            if Languages(second_num):
                translator_res = Translator(
                    number_language=first_num.title(),
                    type_language=second_num.title(),
                    word_translate=last_num
                )
                translator_res.info_print()
        except (KeyError, ValueError):
            print(f'Sorry, the program doesn\'t support {second_num}')
            exit()
