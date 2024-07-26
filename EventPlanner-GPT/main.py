from flask import Flask, request, jsonify, send_from_directory,render_template
import openai
import os

app = Flask(__name__)
TlUgDqXb9BE2ZdITAbJBT3BlbkFJKNCrwL0CYiKAg1cyKY2a'



@app.route('/')
def index():
    return send_from_directory('templates','index.html')



@app.route("/plan-event",methods=['POST'])
def plan_event():
    data=request.get_json()
    description=data.get('description')
    try:
        res=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"You are a helpful event planner."},
                {"role":"user","content":f"Plan an event based on following query : {description}"}
            ],
            max_tokens=200
        )
        plan=res.choices[0].message['content'].strip()
        return jsonify({'plan':plan})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
