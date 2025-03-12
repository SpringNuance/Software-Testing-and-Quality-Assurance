import os

class Scoreboard:
    def __init__(self, filename="scoreboard.txt"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            return []

        scores = []
        with open(self.filename, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) != 3:
                    continue  # Skip invalid lines
                name, score_str, difficulty = parts
                if not score_str.isdigit():
                    continue  # Skip lines where score is not a valid integer
                score = int(score_str)
                scores.append((name, score, difficulty))
        
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def save_scores(self):
        with open(self.filename, "w") as file:
            for name, score, difficulty in self.scores[:10]:
                file.write(f"{name}:{score}:{difficulty}\n")

    def add_score(self, name, score, difficulty):
        if score is None or score <= 0:
          raise ValueError("Score must be a positive number.")
        self.scores.append((name, score, difficulty))
        self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)
        self.save_scores()
        
    def display_scores(self):
        sorted_scores = sorted(self.scores, key=lambda x: x[1], reverse=True)
        print("\nTop 10 High Scores:")
        for i, (name, score, difficulty) in enumerate(sorted_scores[:10], start=1):
            print(f"{i}. {name}: {score} ({difficulty})")

    def get_scores(self):
        self.scores = self.load_scores()
        return self.scores[:10]

# Test the Scoreboard class
if __name__ == "__main__":
    scoreboard = Scoreboard()
    scoreboard.add_score("Alice", 450, "easy")
    scoreboard.add_score("Bob", 300, "hard")
    scoreboard.add_score("Charlie", 600, "easy")
    print(scoreboard.get_scores())
