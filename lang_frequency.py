import os
import re
from collections import Counter
from optparse import OptionParser

import time #delete

def load_data(filepath, reg_exp_rus=False):
    '''
    Функция загрузки данных из файла
    Аргументы: filepath - путь к файлу
               reg_exp_rus - какой тип регулярного выражения использовать.
                    0 - Все найденные слова
                    1 - Только русские слова
    Возвращает список всех найденных слов в файле
    '''
    if not os.path.isfile(filepath):
        return None 
    
    if reg_exp_rus:
        reg_exp = re.compile(r'[А-Яа-я]+')
    else:
        reg_exp = re.compile(r'\w+')

    return process_file_by_lines(filepath, reg_exp)

    # PASSSS


def process_file_by_lines(filepath, reg_exp):
    data = []
    for line in open(filepath, encoding='utf-8'):
        data.extend(reg_exp.findall(line.lower().rstrip('\r\n')))
        # data.extend(re.findall(r'\w+', line.lower().rstrip('\r\n')))
    return data

def process_file_by_chunks(filepath, reg_exp):
    buffer_for_string = ''
    data = []
    for chunk in read_file_by_chunk(filepath):
        print(chunk)
        chunk = buffer_for_string + chunk
        print('*', chunk)
        found_words = re.findall(reg_exp, chunk.lower())
        data.extend(found_words[:-1])
        buffer_for_string = found_words[-1]
        print(found_words[:-1])
        print(buffer_for_string)
        print('----------')
        input()

def read_file_by_chunk(filepath, chunk_size=128):
    with open(filepath, encoding='utf-8') as file_handler:
        while True:
            chunk = file_handler.read(chunk_size)
            if not chunk:
                break
            yield chunk             





def get_most_frequent_words(text, amount_to_show=10):
    words_counter = Counter(text)
    data = words_counter.most_common(amount_to_show)
    del words_counter
    return data

def pretty_print(data):
    digits_size = str(len(str(len(data))))
    string_to_show = '{:0' + digits_size + '}' + '| {}| {}'
    max_word_size = max([len(word[0]) for word in data])
    for num, word in enumerate(data):
        print(string_to_show.format(num+1, word[0].ljust(max_word_size+1), word[1]))



if __name__ == '__main__':
    usage = 'Usage: %prog -p path_to_text_file [-r] [-a amount_to_show]'
    parser = OptionParser(usage=usage)

    parser.add_option('-p', '--path', action='store', type='string', help='Путь до текстового файла')
    parser.add_option('-r', '--rus', action='store_true', default=False, help='Искать только русские слова')
    parser.add_option('-a', '--amount_to_show', action='store', type='int', help='Количество отображаемых слов в топе')
    
    options, arguments = parser.parse_args()

    if options.path:
        path = options.path
    else:
        print('Необходимо указать путь до файла')
        exit(-1)

    #todo: remove
    # process_file_by_chunks(path, reg_exp=r'\w+')

    if options.amount_to_show:
        amount = options.amount_to_show
    else:
        amount = 10

    start_time = time.time()

    words_in_text = load_data(path, options.rus)
    print(u'Файл прочитан')

    print('{}'.format(time.time() - start_time))

    if words_in_text is None:
        print('Джонни, у нас проблема с файлом. Так дело не пойдёт')
        exit(-1)

    counted_data = get_most_frequent_words(words_in_text, amount) 

    print('{}'.format(time.time() - start_time))

    pretty_print(counted_data)
