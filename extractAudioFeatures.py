from flask import Flask, request, jsonify
import librosa
import numpy as np
import tempfile
import os

app = Flask(__name__)

def extract_audio_features(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Extract audio features
	chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = np.mean(librosa.feature.rms(y=y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y))

    return {
	    'chroma_stft': chroma_stft,
        'rms': rms,
        'spectral_centroid': spectral_centroid,
        'spectral_bandwidth': spectral_bandwidth,
        'rolloff': rolloff,
        'zero_crossing_rate': zero_crossing_rate
    }
	
def extract_mean(file):
    y, sr = librosa.load(file)
    # Extract audio features
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = np.mean(librosa.feature.rms(y=y))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y))
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    
    # Print or use the extracted features
    data1=str(np.mean(chroma_stft))+","+str(rms)+","+str(spectral_centroid)+","+str(spectral_bandwidth)+","+str(rolloff)+","+str(zero_crossing_rate)
    length = len(mfccs)
      
    # Iterating the index
    # same as 'for i in range(len(list))'
    data2=""
    for i in range(length):
       data2=","+data2+str(np.mean(mfccs[i]))
    dataAll="["+data1+data2+"]"
    #print(dataAll)
    return {
	    'data': dataAll
	}

@app.route('/extract_audio_features', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded file to a temporary location
        _, temp_audio_file = tempfile.mkstemp(suffix='.wav')
        file.save(temp_audio_file)

        # Extract audio features
        audio_features = extract_mean(temp_audio_file)

        # Delete the temporary audio file
        os.remove(temp_audio_file)

        return jsonify(audio_features)

if __name__ == '__main__':
    app.run(debug=True)
