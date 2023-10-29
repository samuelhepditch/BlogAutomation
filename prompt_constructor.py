from enum import Enum

class GPTKeywordPrompts(Enum):
    NUTRITION = "Provide a list of keywords related to nutrition."
    SLEEP = "List keywords associated with sleep and its benefits."
    EXERCISE = "Mention keywords relevant to physical exercise and fitness."

class GPTBlogPrompts(Enum):
    GENERAL = "Write a blog"