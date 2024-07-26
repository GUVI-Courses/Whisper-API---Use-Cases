from flask import Flask,request,jsonify,send_from_directory
import openai
import os

app=Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('templates','index.html')



@app.route('/generate',methods=['POST'])
def generate_image():
    data=request.get_json()
    description=data.get('description')
    try:
        response=openai.Image.create(
             model="dall-e-3",
            prompt=description,
            n=1,
            quality="standard",
            size="1024x1024"
        )
        image_url=response['data'][0]['url']
        return jsonify({'imageUrl':image_url})
    except :
        return jsonify({'error':"something went wrong"})



if __name__=='__main__':
    app.run(debug=True)
