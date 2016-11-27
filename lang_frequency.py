import os
import re
from collections import Counter
from optparse import OptionParser

def load_data(filepath):
    '''
    Функция загрузки данных из файла
    Аргументы: filepath - путь к файлу
    Возвращает список всех найденных слов в файле
    '''
    if not os.path.isfile(filepath):
        return None 
    with open(filepath, encoding='utf-8') as file_handler:
        text = file_handler.read()
        data = re.findall(r'\w+', text.lower()) 
        return data


def get_most_frequent_words(text, amount_to_show=10):
    words_counter = Counter(text)
    digits_size = str(len(str(amount_to_show)))
    string_to_show = '{:0' + digits_size + '}' + '| {}\t| {}'
    for num, word in enumerate(words_counter.most_common(amount_to_show)):
        print(string_to_show.format(num+1, word[0], word[1]))



if __name__ == '__main__':
    usage = 'Usage: %prog -p path_to_text_file [-a amount_to_show]'
    parser = OptionParser(usage=usage)

    parser.add_option('-p', '--path', action='store', type='string', help='Путь до текстового файла')
    parser.add_option('-a', '--amount_to_show', action='store', type='int', help='Количество отображаемых слов в топе')
    
    options, arguments = parser.parse_args()

    if options.path:
        path = options.path
    else:
        print('Необходимо указать путь до файла')
        exit(-1)

    if options.amount_to_show:
        amount = option.amount_to_show
    else:
        amount = 10

    words_in_text = load_data(path)

    if words_in_text is None:
        print('Джонни, у нас проблема с файлом. Так дело не пойдёт')
        exit(-1)

    get_most_frequent_words(words_in_text, amount)    
