from Bot.Strategies.RandomStrategy import RandomStrategy
from Bot.Strategies.NaiveStrategy import NaiveStrategy

def create(strategyType, game):
    """Factory method for planners."""
    switcher = {
        "random": RandomStrategy(game),
        "naive": NaiveStrategy(game)
    }

    strategy = switcher.get(strategyType.lower())

    return Planner(strategy)

class Planner:
    def __init__(self, strategy):
        self._strategy = strategy

    def makeMove(self):
        return self._strategy.choose()