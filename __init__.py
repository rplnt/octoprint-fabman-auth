from __future__ import absolute_import
import requests

from octoprint.settings import settings
from octoprint.users import FilebasedUserManager, User


__version__ = '1.0.0'
__author__ = 'Matej Buday <m.buday@o0.sk>'
__url__ = 'https://github.com/rplnt/octoprint-fabman-auth'


class FabmanUser(User):
    '''
    User class storing Fabman extras.
    '''
    def __init__(self, username):
        User.__init__(self, username, None, True, [])
        self.fabman_user_id = None
        self.fabman_cookie = None

    def set_fabman_data(self, user_id, cookie):
        self.fabman_user_id = user_id
        self.fabman_cookie = cookie

    def get_fabman_id(self):
        return self.fabman_user_id

    def get_fabman_auth_cookie(self):
        return self.fabman_cookie

    def add_role(self, role):
        self._roles.append(role)


class FabmanUserManager(FilebasedUserManager):
    '''
    UserManager class that can authenticate Octoprint users using Fabman.

    Allows for using local users alongside it.
    '''
    ACCEPT_HEADER = {'Accept': 'application/json'}
    FABMAN_API_URL = 'https://fabman.io/api/v1'
    API_LOGIN_PATH = '/user/login'
    API_RESOURCES_PATH = '/members/{id}/trained-resources'
    OK_CODES = [200]

    def __init__(self):
        FilebasedUserManager.__init__(self)

        self.url = (settings().get(['accessControl', 'fabman', 'url']) or self.FABMAN_API_URL).rstrip('/')
        self.fabman_enabled = settings().getBoolean(['accessControl', 'fabman', 'enabled']) or False
        self.local_enabled = settings().getBoolean(['accessControl', 'fabman', 'allowLocalUsers']) or False
        self.restrict_access = settings().getBoolean(['accessControl', 'fabman', 'restrictAccess']) or False
        self.resource_set = set(settings().get(['accessControl', 'fabman', 'resourceIds']) or [])

        # { username: (id, cookie) }
        self.fabman_users = {}

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
            # using only id from the first member, whatever that means
            try:
                user_id = data['members'][0]['id']
            except (KeyError, TypeError, IndexError):
                user_id = None

            self.fabman_users[mail] = (user_id, r.cookies)
            self._logger.info('Authenticated Fabman user "{}"'.format(mail))
            return True

        self._logger.info('Fabman user "{}" NOT authenticated'.format(mail))
        return False

    def _fabman_get_resources(self, user_id, auth_cookie):
        '''Return set of resources given user is "trained on" on Fabman'''
        r = requests.get((self.url + self.API_RESOURCES_PATH).format(id=user_id), headers=self.ACCEPT_HEADER, cookies=auth_cookie)

        if r.status_code not in self.OK_CODES:
            self._logger.error('Could not load user ({}) resources with error code {}'.format(user_id, r.status_code))
            return set()

        try:
            resource_ids = r.json()
        except ValueError:
            self._logger.error('Failed to parse Fabman response with resources for user id'.format(user_id))
            return set()

        self._logger.info('Loaded available resources for user id "{}"'.format(user_id))
        return set(resource_ids)

    def _fabman_has_permission(self, user):
        user_id = user.get_fabman_id()
        auth_cookie = user.get_fabman_auth_cookie()
        if not user_id or not auth_cookie:
            return False
        return bool(self.resource_set & self._fabman_get_resources(user_id, auth_cookie))

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

        if not self.fabman_enabled:
            return None

        return FabmanUser(userid)

    def checkPassword(self, username, password):
        if self.local_enabled:
            user = super(FabmanUserManager, self).findUser(username)
            if user is not None and not isinstance(user, FabmanUser):
                return FilebasedUserManager.checkPassword(self, username, password)

        if not self.fabman_enabled:
            return False

        return self._fabman_auth(username, password)

    def login_user(self, user):
        if isinstance(user, FabmanUser):
            username = user.get_name()

            # store cookie and id we got during auth inside user class
            if username in self.fabman_users:
                user.set_fabman_data(*self.fabman_users[username])

            # check if we have permission to use resources controlled by this OctoPrint instance
            if not self.restrict_access or self._fabman_has_permission(user):
                self._logger.info('Elevating user {} to role "user"'.format(username))
                user.add_role('user')

        return super(FabmanUserManager, self).login_user(user)

    # more functions like these... should be harmless to just let them fail
    def changeUserPassword(self, username, password):
        if username not in self._users.keys():
            self._logger.error('Trying to change password of Fabman user')
            return

        return super(FabmanUserManager, self).changeUserPassword(username, password)
