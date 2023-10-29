from enum import Enum

class GPTKeywordPrompts(Enum):
    NUTRITION = "Provide a list of keywords related to nutrition in quotation marks and seperated by commas."
    SLEEP = "List keywords associated with sleep and its benefits in quotation marks and seperated by commas."
    EXERCISE = "Mention keywords relevant to physical exercise and fitness in quotation marks and seperated by commas."

class GPTBlogPrompts(Enum):
    GENERAL = "Write a blog"