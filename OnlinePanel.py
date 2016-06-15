import requests


class OnlinePanel:
    def __init__(self, url, number, username, password):
        self.url = url
        self.number = number
        self.username = username
        self.password = password

    def send(self, to, text):
        url = 'http://{}/post/sendsms.ashx?from={}&to={}&text={}&password={}&username={}' \
            .format(self.url, self.number, to, text, self.password, self.username)
        return requests.get(url)
