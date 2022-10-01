from flask import *
import json,time

import lightkurve as lk
import numpy as np
import matplotlib
matplotlib.use('Agg') #matplotlib as backend
import matplotlib.pyplot as plt


app = Flask(__name__)



@app.route('/data/plot')
def get_lightcurve_plot():

    search_results = lk.search_lightcurve('Pi Mensae', mission='TESS', author='SPOC')
    lc = search_results[0].download()
    plt.scatter(lc.time.value, lc.flux.value)
    plt.xlabel("Time")
    plt.ylabel("Flux Value")
    plt.savefig('plot.jpg')
    plt.close("all")
<<<<<<< HEAD

=======
    
>>>>>>> 7459de0194f42c32603e7dd9b04ba8c8fbf5ecd9
    return send_file('plot.jpg', mimetype='image/jpeg')



@app.route('/data/<star_id>')
def get_data(star_id):
    # Eg. star_id = "KIC 8462852"
    pixelfile = lk.search_targetpixelfile("KIC "+str(star_id), quarter=16).download()
    lc = pixelfile.to_lightcurve(aperture_mask='all')
    data = {'Time Seires':list(lc.time.value)[:10]}
    return json.dumps(data)



@app.route('/', methods=['GET'])
def home_page():
    return "Welcome to Home Page"


if __name__ == '__main__':
<<<<<<< HEAD
    app.run()
=======
    app.run(port = 7777)
>>>>>>> 7459de0194f42c32603e7dd9b04ba8c8fbf5ecd9
