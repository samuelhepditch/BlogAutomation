from enum import Enum


class GPTKeywordPrompts(Enum):
    NUTRITION = "Provide a list of keywords related to nutrition in quotation marks and seperated by commas."
    SLEEP = "List keywords associated with sleep and its benefits in quotation marks and seperated by commas."
    EXERCISE = "Mention keywords relevant to physical exercise and fitness in quotation marks and seperated by commas."


class GPTBlogPrompts:
    def get_intro_prompt_with_keywords(title, keywords):
        return (
            f"Write a 100 word introduction for a blog article titled '{title}'. "
            "Keep it simple & informative. Use an active voice. Write at the level of a twelfth-grader. "
            f"Include these keywords: {', '.join(keywords)}. Output as HTML. Do not include quotes in your output. Do not include the title."
        )

    def get_intro_prompt_no_keywords(title):
        return (
            f"Write a 100 word introduction for a blog article titled '{title}'. "
            "Keep it simple & informative. Use an active voice. Write at the level of a twelfth-grader. "
            "Output as HTML. Do not include quotes in your output. Do not include the title."
        )

    def get_outline_prompt_with_keywords(title, keywords):
        return (
            f"Create a detailed outline for the blog post titled '{title}' with a maximum of 8 topics "
            f"using these keywords: {', '.join(keywords)}. "
            "Separate each section. Do not give the title. Do not mention introduction. "
        )

    def get_outline_prompt_no_keywords(title):
        return (
            f"Create a detailed outline for the blog post titled '{title}' with a maximum of 8 topics. "
            "Separate each section. Do not give the title. Do not mention introduction. "
        )

    def get_content_prompt(section):
        return (
            "Expand upon the outline below, writing 250 words for an article. "
            "No need for an intro or conclusion. "
            "Keep it interesting & informative. Organize the content by the subtopic, including "
            "headings for each subtopic. Write 2 paragraphs for each subtopic."
            "Use an active voice. Write at the level of a 9th grader. Use lists where appropriate. "
            "Output as HTML. Do not use <h1>. Do not include quotes in your output. "
            f"This is the outline:\n{section}"
        )

    def get_category_prompt(title, categories):
        return (
            "I will give you a list of categories for a health blog. "
            f"Based on this post's title: '{title}', what category would you put this post into? "
            f"Here are the categories: {', '.join(categories)}. Just give the category name."
        )
