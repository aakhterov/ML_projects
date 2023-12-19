from abc import ABC, abstractmethod
from typing import List, Dict


class NewsCollector(ABC):
    '''
    TODO
    '''

    @abstractmethod
    def collect(self) -> List[Dict]:
        '''
        TODO
        :return:
        '''
        raise NotImplemented(f"Implement collect in {self.__class__.__name__}")


class Saver(ABC):
    '''
    TODO
    '''

    @abstractmethod
    def save(self, *args, **kwargs):
        '''
        TODO
        :return:
        '''
        raise NotImplemented(f"Implement save in {self.__class__.__name__}")