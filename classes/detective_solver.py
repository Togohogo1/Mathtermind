from classes.classic_solver import ClassicSolver


class DetectiveSolver(ClassicSolver):
    def gen_embed(self):
        """Creates an embed displaying all possible solutions of valid guesses if there are 64 or less"""

        # If guesses so far are unverified
        if len(self.rounds) <= 4 and True not in self.verified:
            self.sol_panel.title = f"Valid Solutions Unknown"
            self.sol_panel.description = f"No verified guesses exist for solutions to be determined. Guesses 5 to 8 are guaranteed to be verified and guesses 1 to 4 can be verified by using the `;id` command."
            return

        self.sol_panel.title = f"{self.valid_cnt} Valid Solution{'s'*(self.valid_cnt != 1)}"

        if self.valid_cnt > 64:
            self.sol_panel.description = f"Solutions will not be listed since there are over 64 possible valid combinations"
        else:
            self.sol_panel.description = f"||{', '.join(self.valid)}||"
