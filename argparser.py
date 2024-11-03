
"""Module to parse the command line arguments."""

import argparse

class Arguments:
    """Class to parse the command line arguments."""
    def __init__(self):
        self.is_seed_set = False
        self.seed = 0
        self.is_log_set = False
        self.log_path = None
        self.pieces_folder = None

    def parse_arguments(self):
        """Parse the command line arguments."""
        parser = argparse.ArgumentParser(description='Launch Termtris')
        parser.add_argument("--seed", type=int, help="Seed for the random generator")
        parser.add_argument("--log", type=str , help="Path to the log file")
        parser.add_argument("--piece", "-p", type=str , help="Path to the pieces file")

        args = parser.parse_args()
        if args.seed:
            self.seed = args.seed
            self.is_seed_set = True

        if args.log:
            self.log_path = args.log
            self.is_log_set = True

        if args.piece:
            self.pieces_folder = args.piece
