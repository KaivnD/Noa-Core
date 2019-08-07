from abc import ABC, abstractmethod

class Tasker (ABC):
    @abstractmethod
    def input (self):
        pass
    
    @abstractmethod
    def process (self):
        pass

    @abstractmethod
    def output (self):
        pass

class ApiTasker (Tasker):
    def input(self):
        print('input')

    def process(self):
        print('process')

    def output(self):
        print('output')

class RunnerTasker (Tasker):
    def input(self):
        print('input')

    def process(self):
        print('process')

    def output(self):
        print('output')