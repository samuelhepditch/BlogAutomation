class BlogPost:
    title: str
    content: str
    status: str
    category: str
    category_id: int
    featured_image_id: str

    def __init__(self, title, content, featured_image_id, category_id):
        self.title = title
        self.content = content
        self.status = "publish"
        self.featured_image_id = featured_image_id
        self.category_id = category_id