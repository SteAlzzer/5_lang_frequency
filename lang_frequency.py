import os
import re
from collections import Counter
from optparse import OptionParser


def load_data(filepath, reg_exp_rus=False, process_big_file=False):
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

    if process_big_file:
        print(u'Читаем файл по чанкам')
        return process_file_by_chunks(filepath, reg_exp)
    else:
        return process_file_by_lines(filepath, reg_exp)


def process_file_by_lines(filepath, reg_exp):
    data = []
    for line in open(filepath, encoding='utf-8'):
        data.extend(reg_exp.findall(line.lower()))
    return data


def process_file_by_chunks(filepath, reg_exp):
    buffer_for_string = ''
    data = {}
    for chunk in read_file_by_chunk(filepath):
        chunk = buffer_for_string + chunk
        found_words = reg_exp.findall(chunk.lower())
        if not found_words:
            continue
        data = process_data(found_words[:-1], data)
        pos_for_buffer = chunk.rfind(found_words[-1])
        buffer_for_string = chunk[pos_for_buffer:]

    if buffer_for_string:
        found_words = reg_exp.findall(buffer_for_string.lower())
        data = process_data(found_words, data)

    return data


def read_file_by_chunk(filepath, chunk_size=2048):
    with open(filepath, encoding='utf-8') as file_handler:
        while True:
            chunk = file_handler.read(chunk_size)
            if not chunk:
                break
            yield chunk             


def process_data(input_words, data_list):
    for word in input_words:
        if word in data_list:
            data_list[word] += 1
        else:
            data_list[word] = 1
    return data_list


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
    usage = 'Usage: %prog -p path_to_text_file [-r] [-b] [-a amount_to_show]'
    parser = OptionParser(usage=usage)

    parser.add_option('-p', '--path', action='store', type='string', help='Путь до текстового файла')
    parser.add_option('-r', '--rus', action='store_true', default=False, help='Искать только русские слова')
    parser.add_option('-b', '--big', action='store_true', default=False, help='Чтение огромнейшего файла')
    parser.add_option('-a', '--amount_to_show', action='store', type='int', help='Количество отображаемых слов в топе')
    
    options, arguments = parser.parse_args()

    if options.path:
        path = options.path
    else:
        print('Необходимо указать путь до файла')
        exit(-1)

    if options.amount_to_show:
        amount = options.amount_to_show
    else:
        amount = 10


    words_in_text = load_data(path, options.rus, options.big)
    print(u'Файл прочитан')

    if words_in_text is None:
        print('Джонни, у нас проблема с файлом. Так дело не пойдёт')
        exit(-1)

    counted_data = get_most_frequent_words(words_in_text, amount) 
    pretty_print(counted_data)
