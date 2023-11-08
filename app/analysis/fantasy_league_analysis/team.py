class Team(object):
    def __init__(self) -> None:
        """Team metadata"""

        self.name = ""
        self.id = 0
        self.scores = []
        self.average_score = 0
        self.score_std_dev = 0
        self.matchups = []
        self.wins = 0
        self.opponents = []
        self.opponent_average_scores = []
        self.opponent_std_devs = []
        self.win_likelihoods = []
        self.win_total_probs = []
        self.future_win_total_probs = []
