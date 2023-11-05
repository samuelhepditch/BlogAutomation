import datetime
import logging
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logger = logging.getLogger()


class BlogPost:
    title: str
    content: str
    status: str
    category: str
    category_id: int
    featured_image_id: int

    def __init__(
        self, title, content, featured_image_id=None, category_id=None, status="draft"
    ):
        self.title = title
        self.content = content
        self.status = status
        self.featured_image_id = featured_image_id
        self.category_id = category_id

    # Saves the blog posts as text in case of upload failure
    def save(self):
        try:
            # Create a filename that is a sanitized version of the blog post title
            # Replace spaces with underscores and remove any characters that are not allowed in filenames
            sanitized_title = "".join(
                char if char.isalnum() else "_" for char in self.title
            )
            filename = f"{sanitized_title}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

            # Construct the full path
            filepath = os.path.join(__location__, "faileduploads", filename)

            # Save the attributes to the file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(f"Title: {self.title}\n")
                file.write(f"Content: {self.content}\n")
                file.write(f"Status: {self.status}\n")
                file.write(f"Category: {self.category}\n")
                file.write(f"Category ID: {self.category_id}\n")
                file.write(f"Featured Image ID: {self.featured_image_id}\n")

            logger.info(f"Blog Post Saved Successfully to: {filepath}")

        except Exception as e:
            logger.error(f"Failed to save failed uploaded blog post. Error: {e}")

        return
