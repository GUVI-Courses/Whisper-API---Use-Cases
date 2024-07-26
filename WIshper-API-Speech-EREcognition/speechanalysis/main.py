from flask import Flask,render_template,request,jsonify
from pydub import AudioSegment
import openai
import librosa
import numpy as np
from scipy.io.wavfile import write
from transformers import pipeline
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import os
from collections import Counter


nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)



# Initialize sentiment analysis pipeline
sentiment_pipeline=pipeline('sentiment-analysis')

# load stop words
stop_words=list(set(stopwords.words('english')))

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    return render_template('index.html')



# frequent phrases extraction
def extract_patterns(text):
    words=nltk.word_tokenize(text.lower())
    bigrams=list(nltk.bigrams(words))
    bigrams_freq=Counter(bigrams)
    common_bigrams=bigrams_freq.most_common(5)
    return [f"{pair[0]} {pair[1]}" for pair in common_bigrams]


# function to extract trends (frequent keywordss)
def extract_trends(text):
    words=nltk.word_tokenize(text.lower())
    word_freq=Counter(words)
    common_words=word_freq.most_common(10)
    return [word[0] for word in common_words]



# function to call whisper API
def transcribe_audio(file_path):
    openai.api_key=api_key
    audio_file=open(file_path,'rb')
    transcript=openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcript.text



def process_audio(file_path):
    # load audio
    y,sr=librosa.load(file_path,sr=None)

#   perform noise reduction (example using simple noise reduction)
    y_denoised=librosa.effects.remix(y,intervals=librosa.effects.split(y,top_db=20))

    #perform speaker diarization 
    segments=[(0, len(y_denoised))]
    return y_denoised,sr,segments

# function for sentiment analysis
def analayse_sentiment(text):
    return sentiment_pipeline(text)


# function to extract the keywords
def extract_keywords(text):
    vectorizer=CountVectorizer(stop_words=stop_words,max_features=10)
    X=vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()



@app.route("/upload",methods=['POST'])
def upload_audio():
    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    print(audio_file)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
    audio_file.save(file_path)

    # process audio
    y, sr,segments=process_audio(file_path)

    # save processed audio for whisper api
    processed_file_path=f"./uploads/processed_{audio_file.filename}"
    write(processed_file_path,sr,y.astype(np.float32))

    # tarnscribe audio
    transcript=transcribe_audio(processed_file_path)
    print("transcript",transcript)

    # analyze sentiment
    sentiment=analayse_sentiment(transcript)
    print("sentiment",sentiment)

    # extract the keywords
    keywords=extract_keywords(transcript)
    print("keywords",keywords)

    patterns=extract_patterns(transcript)
    trends=extract_trends(transcript)

    behavior_analysis={
        "patterns":patterns,
        "trends":trends
    }
    print("behavior analysis")
    print(behavior_analysis)

    response_data={
        "transcript":transcript,
        "sentiment":sentiment[0],# extracting the first result from the list
        "keywords":keywords.tolist(), # convertiong the numpy arary to list
        "behavior_analysis":behavior_analysis
    }
    return jsonify(response_data)


if __name__=='__main__':
    app.run(debug=True)
