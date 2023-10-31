class BlogPost:
    title: str
    content: str
    status: str
    category: str

    def __init__(self, title, content, category):
        self.title = title
        self.content = content
        self.status = "publish"
        self.category = category