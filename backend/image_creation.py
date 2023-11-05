import logging
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import re

__location__ = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger()


def create_image_name(title):
    # Replace any non-alphanumeric character with an underscore
    s = re.sub(r"\W+", "_", title)
    # Remove any trailing underscores that might have been added
    s = s.strip("_")
    # Convert the string to lowercase
    s = s.lower()

    s += ".jpg"

    return s


def create_image(title):
    # Generate featured image based on title
    # Try, and if failure, no problem. We will do it manually. We don't want to throw out the whole post because of a missing image.
    try:
        # Load the image

        image = Image.open(os.path.join(__location__, "images", "base_image.jpg"))
        draw = ImageDraw.Draw(image)

        # Define the base font size
        base_font_size = 40

        # Load fonts with the new sizes
        title_font_size = 6 * base_font_size  # Three times bigger for the title
        url_font_size = 1.25 * base_font_size  # Twice as big for the URL

        title_font = ImageFont.truetype(
            os.path.join(__location__, "fonts", "Roboto-Black.ttf"), title_font_size
        )
        url_font = ImageFont.truetype(
            os.path.join(__location__, "fonts", "Roboto-Black.ttf"), url_font_size
        )

        # Calculate the bounding box of the text
        url_box = url_font.getbbox("wellnesswonderspot.com")
        # The width and height are the differences between the right and left (for width)
        # and the bottom and top (for height) of the bounding box
        url_w, url_h = url_box[2] - url_box[0], url_box[3] - url_box[1]

        # Desired color for the text
        text_color = (255, 255, 255)

        # Wrap the title text
        title_lines = textwrap.wrap(title, width=image.width // (title_font_size // 2))

        # Calculate the total height of the title block
        title_block_height = 0
        for line in title_lines:
            _, _, _, line_height = title_font.getbbox(line)
            title_block_height += line_height  # Adjust line height incrementally

        # Calculate the initial y position to vertically center the title block
        y_position = (image.height - title_block_height) // 2

        for line in title_lines:
            # Get the width and height of the line of text
            line_width, line_height = (
                title_font.getbbox(line)[2],
                title_font.getbbox(line)[3],
            )
            # Calculate the x position
            x_position = (image.width - line_width) // 2
            # Draw the line on the image
            draw.text((x_position, y_position), line, font=title_font, fill=text_color)
            # Update the y_position to move down to the next line
            y_position += line_height

        # Position for the URL text
        url_position = (image.width - url_w - 20, image.height - url_h - 20)

        # Draw URL text onto the image
        draw.text(
            url_position, "wellnesswonderspot.com", font=url_font, fill=text_color
        )

        image_name = create_image_name(title)

        # Save the edited image
        image.save(os.path.join(__location__, "images", image_name))

        return image_name
    except Exception as e:
        logger.error(f"Failed to crate image for {title}")
        return None
