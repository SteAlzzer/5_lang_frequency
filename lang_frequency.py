import os
import re
from collections import Counter
from optparse import OptionParser
import prettytable


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
    table = prettytable.PrettyTable(['#', 'Слово', 'Кол-во'])
    table.align['#'] = 'r'
    table.align['Слово'] = 'r'
    for num, word in enumerate(most_common_words):
        table.add_row([num+1, word[0], word[1]])
    print(table)


def main(options):
    if options.path:
        path = options.path
    else:
        print('Необходимо указать путь до файла')
        exit(-1)

    data_from_file = load_data(path)

    if data_from_file is None:
        print('Джонни, у нас проблема с файлом. Так дело не пойдёт')
        exit(-1)

    print('Файл прочитан')

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
