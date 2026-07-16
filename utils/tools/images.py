import base64


def image_to_base64(image_path: str) -> str:
    """Convert an image file to base64 for embedding in HTML."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()