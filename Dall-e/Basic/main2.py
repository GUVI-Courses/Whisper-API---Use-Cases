import openai


with open("bird.png","rb") as image_file:
    response=openai.Image.create_variation(
    image=image_file,
    n=1,
    model="dall-e-2",
    size="1024x1024"
)
    
image_url=response['data'][0]['url']
print(image_url)
