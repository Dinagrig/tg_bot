import logging
logger = logging.getLogger(__name__)


def write_to_db(userid, name, surname,  birthday):
    with open("database.txt", "a", encoding="UTF-8") as file:
        file.write(str(userid) + '\t')
        file.write(name + '\t')
        file.write(surname +'\t')
        file.write(birthday + '\n')


def find_user_by_id(userid):
    logger.info(f'{userid=} вызвал файнд бай айди')
    with open("database.txt", "r", encoding="UTF-8") as file:
        for line in file:
            user_data = line.strip().split('\t')
            if user_data[0] == str(userid):
                return user_data

if __name__ == '__main__':
    write_to_db(123456, 'name', 'surname', '01.01.2000')
    print(find_user_by_id(123456))
