import configparser

config = configparser.ConfigParser()
config.read('config/permissions.ini')


def check_permission(status, command):
    """
    Проверка наличия прав у пользователя.
    status - группа пользователя
    command - команда для проверки
    """
    if status in config.sections():
        perms = config[status]["command_list"].split(' ')
        if command in perms:
            return True
        else:
            return False
    else:
        return False
