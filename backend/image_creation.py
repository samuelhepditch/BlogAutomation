from PIL import Image, ImageDraw, ImageFont


def text_wrap(text, font, max_width):
    lines = []
    # If the text width is smaller than the image width, then no need to wrap
    if font.getbbox(text)[2] <= max_width:
        lines.append(text)
    else:
        # Split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # While there are words left to be checked
        while i < len(words):
            line = ''
            # Build a line while the line is shorter than the image width
            while i < len(words) and font.getbbox(line + words[i])[2] <= max_width:
                line += words[i] + " "
                i += 1
            if not line:
                # If text never fits the line, force break the line
                line = words[i]
                i += 1
            # Remove trailing space
            line = line.rstrip()
            lines.append(line)
    return lines


def create_image(title):
    # Load the image
    image = Image.open('base_image.png')
    draw = ImageDraw.Draw(image)

    # Define the base font size
    base_font_size = 40

    # Load fonts with the new sizes
    title_font_size = 6 * base_font_size  # Three times bigger for the title
    url_font_size = 1.25 * base_font_size  # Twice as big for the URL

    title_font = ImageFont.truetype('Roboto-Black.ttf', title_font_size)
    url_font = ImageFont.truetype('Roboto-Black.ttf', url_font_size)

    # Calculate the bounding box of the text
    url_box = url_font.getbbox("wellnesswonderspot.com")
    # The width and height are the differences between the right and left (for width)
    # and the bottom and top (for height) of the bounding box
    url_w, url_h = url_box[2] - url_box[0], url_box[3] - url_box[1]

    # Desired color for the text
    text_color = (255, 255, 255)

    # Wrap the title text
    title_lines = text_wrap(title, title_font, image.width)

    # Calculate the height of the title block
    sum(title_font.getbbox(line)[3] for line in title_lines)

    # Initial position of the title block, padded from top by 1/6th of image height
    y_position = image.height // 6
    for line in title_lines:
        # Get the width and height of the line of text
        line_width, line_height = title_font.getbbox(line)[2:]
        # Calculate the x position
        x_position = (image.width - line_width) // 2
        # Draw the line on the image
        draw.text((x_position, y_position), line, font=title_font, fill=text_color)
        # Update the y_position to move down to the next line
        y_position += line_height

    # Position for the URL text
    url_position = (image.width - url_w - 20, image.height - url_h - 20)

    # Draw URL text onto the image
    draw.text(url_position, "wellnesswonderspot.com", font=url_font, fill=text_color)

    # Save the edited image
    image.save(f"{title}.png")

