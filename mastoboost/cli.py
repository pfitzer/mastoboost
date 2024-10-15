import os

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mastodon import Mastodon, StreamListener

CLIENT_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_clientcred.secret'))
USER_CRED = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'ftm_usercred.secret'))
CONFIG = os.path.join(os.path.dirname(__file__), '..', 'config.yml')


def register_app():
    """
    register the app on a Mastodon instance
    :return:
    """
    Mastodon.create_app(
        'MastoBoost',
        api_base_url=os.getenv('INSTANCE'),
        to_file=CLIENT_CRED
    )
    mastodon = Mastodon(
        client_id=CLIENT_CRED,
        api_base_url=os.getenv('INSTANCE')
    )

    mastodon.log_in(
        os.getenv('USERNAME'),
        os.getenv('PASSWORD'),
        to_file=USER_CRED,
    )


def run_app():
    mastodon = Mastodon(
        version_check_mode="none",
        access_token='ftm_usercred.secret',
        api_base_url=f'{os.getenv("INSTANCE")}'
    )

    listener = Listener(mastodon=mastodon)
    mastodon.stream_public(listener)


class Listener(StreamListener):

    def __init__(self, mastodon: Mastodon):
        with open(CONFIG, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=Loader)
        self.mastodon = mastodon

    def on_update(self, status):
        if status["visibility"] in ("public", "unlisted"):
            content = status["content"]
            print(f"processing {status['id']}")
            for hashtag in self.config["hashtags"]:
                if f"#{hashtag}" in content:
                    print(f"Boosting status {status['id']}")
                    self.mastodon.status_reblog(status["id"], visibility='public')
                    break


if not os.path.exists(USER_CRED) or not os.path.exists(CLIENT_CRED):
    register_app()

run_app()
