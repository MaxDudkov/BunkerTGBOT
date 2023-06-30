import random
import yaml


class PlayerInfo(object):
    def __init__(self, biology, profession, health, phobia, baggage, hobby, add_info, bonus):
        self.biology = biology
        self.profession = profession
        self.health = health
        self.phobia = phobia
        self.baggage = baggage
        self.hobby = hobby
        self.add_info = add_info
        self.bonus = bonus

    def get_all_info_message(self):  # TODO: write 'toString()'
        return ""


class GameInfo(object):
    def __init__(self, disaster_name, disaster_info, bunker_cards, players):
        self.disaster_name = disaster_name
        self.disaster_info = disaster_info
        self.bunker_cards = bunker_cards
        self.players = players


class GameConfig(object):
    def __init__(self):
        self.config = yaml.safe_load(open('feature_set.yml'))

    def shuffle_game_by_persons_count(self, count):
        disaster = random.choice(self.config["disasters"])
        bunker_cards = random.sample(self.config["bunker_cards"], self.get_count_of_bunker_cards_by_players_count(count))
        players = self.get_random_players_info_by_count(count)

        return GameInfo(
            disaster["name"],
            disaster["description"],
            bunker_cards,
            players)

    def get_random_players_info_by_count(self, count):
        health_list = random.sample(self.config["health"], count)  # full cringe but mne len'
        biology_list = random.sample(self.config["biology"], count)
        professions_list = random.sample(self.config["professions"], count)
        phobias_list = random.sample(self.config["phobias"], count)
        hobbies_list = random.sample(self.config["hobbies"], count)
        baggage_list = random.sample(self.config["baggage"], count)
        add_info_list = random.sample(self.config["add_info"], count)
        bonus_list = random.sample(self.config["bonus"], count)

        players = []
        for i in range(count):
            players.append(PlayerInfo(
                biology_list[i],
                professions_list[i],
                health_list[i],
                phobias_list[i],
                baggage_list[i],
                hobbies_list[i],
                add_info_list[i],
                bonus_list[i]))

        return players


    def get_count_of_bunker_cards_by_players_count(self, players_count):
        return 2
