import vk
from time import sleep


class Frends:
    """
    Добавление вохможных друзей, предлагаемых вконтактом.
    """
    def __init__(self, *, accessToken):
        self.session = vk.AuthSession(access_token=accessToken)
        self.api = vk.API(self.session)
        self.addFrend = {}
        
    def addFriends(self):
        countAddUsers = 0
        countError = 0
        fiends = self.api.friends.getSuggestions(filter='mutual, contacts, mutual_contacts', count=500, offset=0, fields='', name_case='')
        for user in fiends:
            try:
                sleep(5)
                self.api.friends.add(user_id=user['uid'], text='', follow='0')
                countAddUsers += 1
                self.addFrend[countAddUsers] = '{} {}'.format(user['first_name'], user['last_name'])
                print('{} Заявка отправлена : {} {}'.format(countAddUsers, user['first_name'], user['last_name']))
            except vk.exceptions.VkAPIError:
                countError += 1
                print('{2} error {0} {1}'.format(user['first_name'], user['last_name'], countError))
            if 100 is countError or 51 is countAddUsers:
                break
        print('Список добавленных друзей\n', self.addFrend)
        return 'Скрипт завершил работу.'

    def addFollowings(self, offset=0, count=1000):
        idFollowers = self.api.users.getFollowers(offset=offset, count=count)
        countError = 0
        for idFollower in idFollowers['items']:
            try:
                user = self.api.users.get(userId=idFollower)
                firstName = user[0]['first_name']
                lastName = user[0]['last_name']
                deactivated = '-'
            except UnboundLocalError:
                print('Ошибка users.get')
            try:
                sleep(2)
                self.api.friends.add(userId=idFollower, text='', follow='0')
                print('Добавлен - {} {}'.format(firstName, lastName))
                print('https://vk.com/id{}'.format(idFollower))
            except vk.exceptions.VkAPIError:
                countError += 1
                print('Error - {}'.format(countError))
                print('{} {} - Статус {}'.format(firstName, lastName, deactivated))
        return 'Скрипт завершил работу.'

if __name__ == '__main__':
    print('Получит токен по ссылке :')
    print('https://oauth.vk.com/authorize?client_id=6076877&display=page&redirect_uri=&scope=likes+notifications+post+wall+friends+status&response_type=token&v=&state=')
    accessToken = input('Введите полученный токен : ')
    Frends(accessToken=accessToken).addFriends()