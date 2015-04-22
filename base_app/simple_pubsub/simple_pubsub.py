__author__ = 'Michael Redmond'

from collections import defaultdict


class SimplePubSub(object):
    def __init__(self):
        self._topics = defaultdict(set)

    def subscribe(self, func, message):

        self._topics[message].add(func)

    def unsub(self, func, message):
        self._topics[message].remove(func)

    def unsub_all(self, func):
        for message in self._topics:
            if func in self._topics[message]:
                self._topics[message].remove(func)

    def publish(self, message, *args, **kwargs):
        topics = self._all_topics(message)

        for topic in topics:
            for func in self._topics[topic]:
                func(*args, **kwargs)

    def publish_with_results(self, message, *args, **kwargs):
        topics = self._all_topics(message)

        result = []

        for topic in topics:
            result.append([func(*args, **kwargs) for func in self._topics[topic]])

        return result

    def _all_topics(self, message):
        split_topic = message.split('.')

        topics = []

        topic = ''

        for piece in split_topic:
            if topic == '':
                topic = piece
            else:
                topic += '.%s' % piece

            topics.append(topic)

        return reversed(topics)