from __future__ import absolute_import
import requests

from octoprint.settings import settings
from octoprint.users import FilebasedUserManager, User


__version__ = '1.0.0'
__author__ = 'Matej Buday <m.buday@o0.sk>'
__url__ = 'https://github.com/rplnt/octoprint-fabman-auth'


class FabmanUser(User):
    '''Clone of User class used for type checking.'''
    def __init__(self, username):
        User.__init__(self, username, None, True, ['user'])


class FabmanUserManager(FilebasedUserManager):
    '''
    UserManager class that can authenticate Octoprint users using Fabman.

    Allows for using local users alongside it.
    '''
    ACCEPT_HEADER = {'Accept': 'application/json'}
    FABMAN_API_URL = 'https://fabman.io/api/v1'
    API_LOGIN_PATH = '/user/login'
    OK_CODES = [200]

    def __init__(self):
        FilebasedUserManager.__init__(self)

        self.url = (settings().get(['accessControl', 'fabman', 'url']) or self.FABMAN_API_URL).rstrip('/')
        self.enabled = settings().getBoolean(['accessControl', 'fabman', 'enabled']) or False
        self.local_enabled = settings().getBoolean(['accessControl', 'fabman', 'allowLocalUsers']) or False

        self._cookies = {}

    def _fabman_auth(self, mail, password):
        '''Call Fabman API to log in.'''
        login_data = {'emailAddress': mail, 'password': password}
        r = requests.post(self.url + self.API_LOGIN_PATH, json=login_data, headers=self.ACCEPT_HEADER)

        if r.status_code not in self.OK_CODES:
            # TODO better logging - response can contain reason for failure
            self._logger.error('Failed login to Fabman for user "{}" with code {}'.format(mail, r.status_code))
            return False

        try:
            data = r.json()
        except ValueError:
            self._logger.error('Failed to parse Fabman response for login attempt of user "{}"'.format(mail))
            return False

        # only auth active users
        if data['state'] == 'active':
            # _cookies[mail] = r.cookies
            self._logger.info('Authenticated user Fabman user {}'.format(mail))
            return True

        return False

    def findUser(self, userid, apikey=None, session=None):
        '''
        Search for existing users - called before each login attempt.

        We don't have a way to check existence of user on Fabman (other than failed login)
        so we always act like we found our user.
        '''
        if self.local_enabled:
            user = super(FabmanUserManager, self).findUser(userid, apikey=apikey, session=session)

            if user is not None:
                return user

        if not self.enabled:
            return None

        return FabmanUser(userid)

    def checkPassword(self, username, password):
        if self.local_enabled:
            user = super(FabmanUserManager, self).findUser(username)
            if user is not None and not isinstance(user, FabmanUser):
                return FilebasedUserManager.checkPassword(self, username, password)

        if not self.enabled:
            return False

        # call fabman API to login
        return self._fabman_auth(username, password)

    def login_user(self, user):
        if isinstance(user, FabmanUser):
            # add any saved data to our user class for use in other places
            pass

        return super(FabmanUserManager, self).login_user(user)

    # more functions like these... should be harmless to just let them fail
    def changeUserPassword(self, username, password):
        if username not in self._users.keys():
            self._logger.error('Trying to change password of Fabman user')
            return

        return super(FabmanUserManager, self).changeUserPassword(username, password)
