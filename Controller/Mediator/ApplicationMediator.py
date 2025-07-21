from abc import ABCMeta, abstractmethod
import logging


class IApplicationMediator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def notify(self, message):
        pass

    @staticmethod
    @abstractmethod
    def receive(self, observer):
        pass


class IComponent:
    def __init__(self, mediator, name):
        self.mediator = mediator
        self.name = name

    def notify(self, message):
        logging.info(f"{self.name} got message: {message}")
        self.mediator.notify(self, message)

    def receive(self, message):
        logging.info(f"{self.name} received message: {message}")


class Mediator(IApplicationMediator):
    def __init__(self):
        self.components = []

    def register(self, component):
        self.components.append(component)

    def notify(self, sender, message):
        for component in self.components:
            if component is not sender:
                component.receive(message)
