from io import BytesIO
from PIL import Image
import openai


# read the image
image=Image.open("image.jpg")
width,height=1024,1024
image=image.resize((width,height))

# convert the image to BytesIO object
byte_stream=BytesIO()
image.save(byte_stream,format='PNG')
bytearray=byte_stream.getvalue()

# integrate dalle-2
response=openai.Image.create_variation(
    image=bytearray,
    n=3,
    model="dall-e-2",
    size="1024x1024"
)
print(response)
