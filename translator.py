import requests
import sys
from bs4 import BeautifulSoup

args = sys.argv
languages = {0: 'all', 1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese',
             8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}


def create_request(word, direction):
    return requests.get(f'https://context.reverso.net/translation/{direction.lower()}/{word.lower()}',
                        headers={'User-Agent': 'Mozilla/5.0'})


def web_scraping(data):
    soup = BeautifulSoup(data.content, 'html.parser')
    soup.prettify()
    translated_word = soup.find_all('a', {'class': ['translation', 'translation.rtl']})
    usage_examples_1 = soup.find_all('div', {'class': 'src ltr'})
    usage_examples_2 = soup.find_all('div', {'class': ['trg ltr', 'trg rtl arabic', 'trg rtl']})
    return translated_word, usage_examples_1, usage_examples_2


def extract_words(translations, num_of_words):
    trans_words = []
    for i, word in enumerate(translations[:num_of_words + 1]):
        if i == 0:
            pass
        else:
            trans_words.append(word.text.strip())
    return trans_words


def extract_examples(ex_first_lang, ex_second_lang, num_of_examples):
    usage_ex_1 = []
    for use in ex_first_lang[:num_of_examples]:
        usage_ex_1.append(use.text.strip())
    usage_ex_2 = []
    for use in ex_second_lang[:num_of_examples]:
        usage_ex_2.append(use.text.strip())
    usages = []
    for i, j in zip(usage_ex_1, usage_ex_2):
        usages.append(i)
        usages.append(j)
    return usages


def take_input():
    first_language = languages[int(input('Type the number of your language:'))]
    second_language = languages[int(input("Type the number of a language you want to translate to "
                                          "or '0' to translate to all languages:"))]
    word = input('Type the word you want to translate:')
    return first_language, second_language, word


def translate(first_language, second_language, word, num_of_translations=5):
    direction = f'{first_language}-{second_language}'
    r = create_request(word, direction)
    translations, examples_first_language, examples_second_language = web_scraping(r)
    words = extract_words(translations, num_of_translations)
    examples = extract_examples(examples_first_language, examples_second_language, num_of_translations)
    return words, examples


def main():
    if len(args) == 4:
        first_language = args[1]
        second_language = args[2]
        word = args[3]
    else:
        print("Hello, you're welcome to the translator. Translator supports:")
        for i, language in languages.items():
            if i == 0:
                pass
            else:
                print(f'{i}. {language}')
        first_language, second_language, word = take_input()
    if second_language == 'all':
        file = open(f'{word}.txt', 'w', encoding='utf-8')
        for language in languages.values():
            word_translation, usage_example = translate(first_language, language, word, num_of_translations=1)
            if word_translation:
                file.write(f'\n{language.capitalize()} Translations:' + '\n' + word_translation[0] + '\n\n')
                file.write(f'{language.capitalize()} Example:' + '\n' + '\n'.join(usage_example) + '\n\n')
        file.close()
        file = open(f'{word}.txt', 'r', encoding='utf-8')
        print(file.read())
        file.close()
    else:
        file = open(f'{word}.txt', 'w', encoding='utf-8')
        word_translations, usage_examples = translate(first_language, second_language, word)
        if word_translations:
            file.write(f'\n{second_language.capitalize()} Translations:' + '\n' + '\n'.join(word_translations) + '\n\n')
            file.write(f'{second_language.capitalize()} Example:' + '\n' + '\n'.join(usage_examples) + '\n\n')
        file.close()
        file = open(f'{word}.txt', 'r', encoding='utf-8')
        print(file.read())
        file.close()


if __name__ == "__main__":
    main()
