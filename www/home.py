from flask import Flask, render_template
from scipy.io import wavfile
import imageio
# This line imports most packages you'll need. You may need to import others (eg random and cmath)
import numpy as np, scipy as sp, matplotlib.pyplot as plt, matplotlib, sklearn, librosa, cmath, math, crepe

app=Flask(__name__) 

###
# Python Functions
###
def plot_audio(x, sr, figsize=(16,4)):
    """
    A simple audio plotting function
    
    Parameters
    ----------
    x: np.ndarray
        Audio signal to plot
    sr: int
        Sample rate
    figsize: tuple
        A duple representing the figure size (xdim,ydim)
    """
    length = float(x.shape[0]) / sr
    t = np.linspace(0,length,x.shape[0])
    plt.figure(figsize=figsize)
    plt.plot(t, x)
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.show()

##
# Default/Home Page
##
@app.route('/')
@app.route('/home')
def home(): 
    return render_template('home.html')

##
# Other Pages
##
lib_audio,sr = librosa.load('./audiofiles/gtr-jazz.wav',sr=44100)
plt.plot(lib_audio)
plt.savefig('./figures/testfig1.png')
figure = imageio.imread('./figures/testfig1.png')
# figure = plot_audio(lib_audio,sr)

sr, crepe_audio = wavfile.read('./audiofiles/gtr-jazz.wav')
# time, frequency, confidence, activation = crepe.predict(crepe_audio, sr, viterbi=True)
@app.route('/test')
def test(): 
    return render_template('test.html', audio=lib_audio, figure=figure)

# @app.route('/sound/audio/gtr-jazz.wav')
# def download_file(filename):
#     return send_from_directory('./audio/', filename)

###
# Flask Settings
# don't need to set ENV variables
###
if __name__ =='__main__':
    app.run(debug=False)
app.run(port=5000)