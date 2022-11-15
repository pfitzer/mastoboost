from mastodon import StreamListener


class Listener(StreamListener):

    def on_status_update(self, update):
        print(update)
