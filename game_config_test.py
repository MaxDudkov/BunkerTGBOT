from game_config import GameConfig


def shuffle_test():
    config = GameConfig().config
    assert(config is not None)
    game = GameConfig().shuffle_game_by_persons_count(3)
    assert(game.disaster_name is not None)

shuffle_test()