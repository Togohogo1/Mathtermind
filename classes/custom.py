from classes.classic import Classic
from random import sample


class Custom(Classic):
    def __init__(self, ctx, settings):
        super().__init__(ctx)

        # Changeable variables
        self.ranges = []
        self.tmp_sets = {"rl": None, "gsl": None, "mg": None, "ca": None}

        # Unchangeable variables
        self.game_id = 3
        self.settings = settings

        # Embeds
        self.game_over_msg.title = f"{ctx.author}'s Custom Game"
        self.board.title = f"{ctx.author}'s Custom Game"

    def create_answer(self, settings):
        answer = []

        # Splitting by times repeated
        for part in settings.split(","):
            rest, _, repeat = part.partition(":")
            range_rng = []

            if not repeat:
                repeat = "1"

            # Splitting by ranges
            for subpart in rest.split("|"):
                start, _, end = subpart.partition("-")

                if not end:
                    end = start

                start, end = sorted((int(start), int(end)))

                # Answer's numbers go out of the range limit
                if start < 1 or end > self.tmp_sets["rl"]:
                    raise ValueError

                # Adding numbers from range to temp array, then picking a random sample from it
                range_rng += range(start, end+1)
                self.ranges.append((start, end))

            answer += sample(range_rng, int(repeat))

        return sorted(answer)

    def is_classic(self):
        return self.settings is None

    def parse_settings(self):
        for indiv in self.settings.split():
            key, val = indiv.split("=")

            if key in {"rl", "range_limit"}:
                self.tmp_sets["rl"] = int(val)
            elif key in {"gsl", "guess_size_limit"}:
                self.tmp_sets["gsl"] = int(val)
            elif key in {"mg", "max_guesses"}:
                self.tmp_sets["mg"] = int(val)
            elif key in {"ca", "custom_answer"}:
                self.tmp_sets["ca"] = val
            else:
                raise ValueError

    def sets_in_range(self):
        return 1 <= self.tmp_sets["rl"] <= 50 and 1 <= self.tmp_sets["gsl"] <= 50 and 1 <= self.tmp_sets["mg"] <= 50

    def rep_possible(self):
        return self.tmp_sets["gsl"] > self.tmp_sets["rl"]

    def set_custom_ans(self):
        if self.tmp_sets["ca"] is None:
            self.answer = self.create_answer(f"1-{self.tmp_sets['rl']}:3")
            self.tmp_sets["ca"] = f"1-{self.tmp_sets['rl']}:3"  # Setting for debugging purposes
        else:
            self.answer = self.create_answer(self.tmp_sets["ca"])

    def range_intersect(self):
        self.ranges.sort()

        if len(self.ranges) > 1:
            for i in range(len(self.ranges)-1):
                # Intersection exists
                if self.ranges[i][1] >= self.ranges[i+1][0]:
                    return True

        return False

    def valid_settings(self):
        """Checks if passed settings are valid or not by making use of the previous helper methods."""

        # No settings passed = classic mode
        if self.is_classic():
            return True

        try:
            self.parse_settings()
        except ValueError:
            self.log_msg.description = "Your settings cannot be parsed properly"
            return False

        # Overriding missing temp settings with default values
        for key, val in self.tmp_sets.items():
            if val is None:
                self.tmp_sets[key] = self.sets_dict[key]

        if not self.sets_in_range():
            self.log_msg.description = "Some of your settings are not within their range limits"
            return False

        # Isn't possible to guess more than the range of numbers without repeats
        if self.rep_possible():
            self.log_msg.description = "Your guess size limit cannot exceed your range limit"
            return False

        try:
            self.set_custom_ans()
        except ValueError:
            self.log_msg.description = "Check your custom answer settings for range and syntax issues"
            return False

        if self.range_intersect():
            self.log_msg.description = "Your custom answer ranges cannot intersect"
            return False

        # Applying custom settings
        for key, val in self.tmp_sets.items():
            self.sets_dict[key] = self.tmp_sets[key]

        return True
