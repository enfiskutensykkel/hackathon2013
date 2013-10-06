# -*- coding: utf-8 -*-


class PeekableGenerator(object):
    def __init__(self, generator):
        self.debug = generator
        self.__generator = generator
        self.__element = None
        self.__isset = False
        self.__more = False
        try:
            self.__element = generator.next()
            self.__more = True
            self.__isset = True
        except StopIteration:
            pass

    def hasMore(self):
        return self.__more or self.__isset

    def peek(self):
        if not self.hasMore():
            assert "Shouldn't happen"
            raise StopIteration

        return self.__element

    def next(self):
        if not self.hasMore():
            assert "Shouldn't happen"
            raise StopIteration

        self.__more == self.__isset
        element = self.__element
        self.__isset = False

        try:
            self.__element = self.__generator.next()
            self.__isset = True
        except StopIteration:
            self.__isset = False

        return element