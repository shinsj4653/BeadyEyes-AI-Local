import io
import os
from PIL import Image, ImageDraw

# Set environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gdsc-sc-team4-pointer-0d2a3b269fad.json"

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('cafe.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
    

# Performs text detection on the image file
response = client.text_detection(image=image)
texts = response.text_annotations

img = Image.open(file_name)
draw = ImageDraw.Draw(img)


print('Texts:')
for text in texts:
    print(text.description)
    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])
    print('bounds: {}'.format(','.join(vertices)))
    # draw.text(((text.bounding_poly.vertices)[0].x, (text.bounding_poly.vertices)[0].y), text.description, fill='red')
    draw.polygon([
        (text.bounding_poly.vertices)[0].x, (text.bounding_poly.vertices)[0].y,
        (text.bounding_poly.vertices)[1].x, (text.bounding_poly.vertices)[1].y,
        (text.bounding_poly.vertices)[2].x, (text.bounding_poly.vertices)[2].y,
        (text.bounding_poly.vertices)[3].x, (text.bounding_poly.vertices)[3].y], None, 'red')

img.save('annotated_cafe.jpg')
img.show()