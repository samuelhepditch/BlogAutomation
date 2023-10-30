from enum import Enum

class GPTKeywordPrompts(Enum):
    NUTRITION = "Provide a list of keywords related to nutrition in quotation marks and seperated by commas."
    SLEEP = "List keywords associated with sleep and its benefits in quotation marks and seperated by commas."
    EXERCISE = "Mention keywords relevant to physical exercise and fitness in quotation marks and seperated by commas."

class GPTBlogPrompts(Enum):
    ROLE = "I want you to act as an internet health blogger"
    BLOG = "You are a well-loved author of a popular blog that writes about women’s health and wellness. Please write an interesting click worthy article about {0}. Include these keywords: {1}. Keep the title simple yet click worthy."