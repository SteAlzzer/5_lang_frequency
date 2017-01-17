import math
import os
import re
from collections import Counter
from optparse import OptionParser


def load_data(filepath):
    '''
    Функция загрузки данных из файла
    '''
    if not os.path.isfile(filepath):
        return None
    with open(filepath, encoding='utf-8') as file_handle:
        return file_handle.read()


def process_data(data_from_file):
    '''
    Функция обрабатывает текст и формирует список слов
    '''
    list_of_words = re.findall(r'\w+', data_from_file.lower())
    return list_of_words


def get_most_frequent_words(words, amount_to_show=10):
    '''
    Функция возвращает самые частовстречаемые слова в списке
    '''
    words_counter = Counter(words)
    most_common_words = words_counter.most_common(amount_to_show)

    return most_common_words


def pretty_print(most_common_words):
    '''
    Выводим слова в виде таблички
    '''
    amount_of_words = len(most_common_words)
    amount_of_digits_in_number = int(math.log10(amount_of_words)) + 1
    string_template_for_show = '{:0' + str(amount_of_digits_in_number) + '}' + '| {}| {}'
    max_word_length = max([len(word[0]) for word in most_common_words])
    for num, word in enumerate(most_common_words):
        print(string_template_for_show.format(num+1, word[0].ljust(max_word_length+1), word[1]))


def main(options):
    if options.path:
        path = options.path
    else:
        print(u'Необходимо указать путь до файла')
        exit(-1)

    data_from_file = load_data(path)
    print(u'Файл прочитан')

    if data_from_file is None:
        print(u'Джонни, у нас проблема с файлом. Так дело не пойдёт')
        exit(-1)

    words_in_text = process_data(data_from_file)

    most_common_words = get_most_frequent_words(words_in_text, options.amount_to_show)
    pretty_print(most_common_words)


if __name__ == '__main__':
    usage = 'Usage: %prog -p path_to_text_file [-a amount_to_show]'
    parser = OptionParser(usage=usage)

    parser.add_option('-p', '--path', action='store', type='string', help='Путь до текстового файла')
    parser.add_option('-a', '--amount_to_show', action='store', type='int', default=10, help='Количество отображаемых слов в топе')

    options, arguments = parser.parse_args()

    main(options)
