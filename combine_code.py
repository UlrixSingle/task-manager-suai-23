# Сборка всех листингов кода для представления в документе
import os

def read_file( path):
    tmp = ''
    with open( path, 'r') as inputfile:
        for line in inputfile.readlines():
            tmp += line
    return tmp

def read_entry( entry):
    return read_file( read_file(entry.path))

with open('combine_code_result.txt', 'w') as f:
    f.write('\tГенерация базы данных\n')
    f.write('\tСодержание файла generate.sql\n')
    f.write( read_file( './db/generate.sql'))
    f.write( '\n')
    
    f.write('\tОсновные программы приложения\n')
    with os.scandir('./app') as dir_entries:
        for entry in dir_entries:
            if entry.is_file():
                f.write('\tСодержание файла ' + entry.name + '\n')
                f.write( read_file( entry))
                f.write( '\n')
                
    f.write('\tСодержание файла myproject.py\n')
    f.write( read_file('./myproject.py'))
    f.write( '\n')
    
    f.write('\tШаблоны страниц приложения\n')
    with os.scandir('./app/templates') as dir_entries:
        for entry in dir_entries:
            if entry.is_file():
                f.write('\tСодержание файла ' + entry.name + '\n')
                f.write( read_file( entry))
                f.write( '\n')
