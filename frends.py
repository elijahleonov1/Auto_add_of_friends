import vk
from time import sleep


session = vk.AuthSession(access_token='access_token')
api = vk.API(session)


def add_friends():
    """
    Добавление вохможных друзей, предлагаемых вконтактом.
    """
    fiends = api.friends.getSuggestions(filter='mutual, contacts, mutual_contacts', count=500,
                                        offset=0, fields='', name_case='')
    num = 0
    for user in fiends:
        try:
            sleep(5)
            api.friends.add(user_id=user['uid'], text='', follow='0')
            num += 1
            print('{} Заявка отправлена : {} {}'.format(num, user['first_name'], user['last_name']))
            if 51 is num:
                break
        except vk.exceptions.VkAPIError:
            print('error {} {}'.format(user['first_name'], user['last_name']))

    return 'Скрипт завершил работу.'


def add_followings(*, offset=0, count=1000):
    """
    Добавление подписчиков в друзья, пропускает удаленный или
    заблокированные страницы оставляя их в подписках
    """

    id_followers = api.users.getFollowers(offset=offset, count=count)
    numbers = 0

    for id_folofer in id_followers['items']:

        try:
            user = api.users.get(user_id=id_folofer)
            first_name = user[0]['first_name']
            last_name = user[0]['last_name']
            deactivated = user[0]['deactivated']
        except UnboundLocalError:
            print('Ошибка users.get')

        try:
            sleep(2)
            api.friends.add(user_id=id_folofer, text='', follow='0')
            print('Добавлен - {} {}'.format(first_name, last_name))
            print('https://vk.com/id{}'.format(id_folofer))
        except vk.exceptions.VkAPIError:
            numbers += 1
            print('error - {}'.format(numbers))
            print('{} {} - Статус {}'.format(first_name, last_name, deactivated))

    return 'Скрипт завершил работу.'


if __name__ == '__main__':
    add_friends()
    add_followings()
