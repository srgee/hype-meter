from abc import ABC, abstractmethod

class BaseProvider(ABC):
    '''
    Mandatory interface for all data sources for Hypemeter.
    '''
    
    @abstractmethod
    def fetch_score(self, keyword: str) -> int:
        '''
        It should return an integer value between 0 and 100.
        '''
        pass

    @abstractmethod
    def fetch_history(self, keyword: str) -> dict:
        '''
        It should return a dictionary with time series data.
        '''
        pass