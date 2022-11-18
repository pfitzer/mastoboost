import os
import platform
import sys
from getpass import getpass

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mastodon import Mastodon
from options import options

CLIENT_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_clientcred.secret'))
USER_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_usercred.secret'))
CONFIG = os.path.join(os.path.dirname(__file__), '..', 'config.yml')


def register_app():
    uri = input('Mastodon URL: ')
    login = input('login: ')
    if platform.system() in ['linux', 'linux2', 'darwin']:
        pw = getpass(prompt='Password: ')
    else:
        pw = input('Password: ')
    Mastodon.create_app(
        'MastoBoost',
        api_base_url=uri,
        to_file=CLIENT_CRED
    )
    mastodon = Mastodon(
        client_id=CLIENT_CRED,
        api_base_url=uri
    )

    mastodon.log_in(
        login,
        pw,
        to_file=USER_CRED,
    )


if options.register or not os.path.exists(USER_CRED) or not os.path.exists(CLIENT_CRED):
    register_app()
    sys.exit(0)


class MastoBoost(object):

    def __init__(self):
        self.mastodon = Mastodon(access_token=USER_CRED)
        self.settings = self.__load_config()
        boost = False
        last = {'id': self.settings['last_id']} if 'last_id' in self.settings else None
        toots = self.mastodon.timeline(timeline='public', since_id=last)
        if toots:
            last_id = toots[0]['id']
            self.__update_config(last_id)
        for toot in toots:
            for tag in toot['tags']:
                if tag['name'] in self.settings['hashtags']:
                    boost = True
            if boost:
                print(toot['id'])
                # self.mastodon.status_reblog(toot['id'])

    def __load_config(self):
        try:
            f = open(CONFIG)
        except FileNotFoundError:
            raise Exception(f'{CONFIG} not found')
        return yaml.load(f, Loader=Loader)

    def __update_config(self, last_id: int):
        self.settings['last_id'] = last_id
        yaml.dump(self.settings, open(CONFIG, 'w'), Dumper=Dumper)


if __name__ == '__main__':
    mb = MastoBoost()
