import csv

class Keyword:
    def __init__(self, keyword, volume, keyword_difficulty, cpc, competitive_density, number_of_results, intent, serp_features, trend):
        self.keyword = keyword
        self.volume = int(volume)
        self.keyword_difficulty = int(keyword_difficulty)
        self.cpc = float(cpc)
        self.competitive_density = float(competitive_density)
        self.number_of_results = int(number_of_results)
        self.intent = intent
        self.serp_features = serp_features.split(', ')  # Assuming multiple features are comma-separated
        self.trend = list(map(float, trend.split(',')))  # Assuming trend values are comma-separated

    def __str__(self):
        return f"Keyword({self.keyword}, Volume: {self.volume}, Difficulty: {self.keyword_difficulty}, ...)"  # You can expand this for other attributes

class KeywordsList:
    def __init__(self, csv_path):
        self.keywords = []

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                keyword = Keyword(row['Keyword'], row['Volume'], row['Keyword Difficulty'], row['CPC (CAD)'], row['Competitive Density'], row['Number of Results'], row['Intent'], row['SERP Features'], row['Trend'])
                self.keywords.append(keyword)

    def __iter__(self):
        return iter(self.keywords)

    def __len__(self):
        return len(self.keywords)

    def __getitem__(self, index):
        return self.keywords[index]

    def filter_keywords(self, keyword_difficulty, query_number, cost_per_click):
        self.keywords = [keyword for keyword in self.keywords if 
                         keyword.cpc > cost_per_click and 
                         keyword.number_of_results > query_number and 
                         keyword.keyword_difficulty < keyword_difficulty]
