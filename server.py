from flask import *
import json,time
import requests
from k2flix import *
import lightkurve as lk
import numpy as np
import matplotlib
matplotlib.use('Agg') #matplotlib as backend
import matplotlib.pyplot as plt


app = Flask(__name__)

# http://192.168.0.238:5000/mission/?star_id=261136679
@app.route('/mission/')
def get_mission_info():
    paramters = request.args.to_dict()
    search_results = lk.search_lightcurve('TIC'+str(paramters['star_id']))
    data = {'Mission':str(set(zip(search_results.mission, search_results.year)))}
    return json.dumps(data)

# http://192.168.0.238:5000/plot/lightcure/simple/?star_id=261136679&sector=4
@app.route('/plot/lightcure/simple/')
def get_lightcurve_simple_plot():
    paramters = request.args.to_dict()
    search_results = lk.search_lightcurve('TIC'+str(paramters['star_id']), sector=int(paramters['sector']))
    #preprocessing
    lc = search_results[0].download()
    lc = lc.remove_outliers(sigma=5)
    lc = lc.flatten(window_length=501, break_tolerance=50)

    plt.plot(ax=lc.plot())
    plt.savefig('simple_plot.jpg')
    return send_file('simple_plot.jpg', mimetype='image/jpeg')

# http://192.168.0.238:5000/plot/lightcure/periodogram/?star_id=261136679&sector=4
@app.route('/plot/lightcure/periodogram/')
def get_lightcurve_periodogram_plot():
    paramters = request.args.to_dict()
    search_results = lk.search_lightcurve('TIC'+str(paramters['star_id']), sector=int(paramters['sector']))
    #preprocessing
    lc = search_results[0].download()
    lc = lc.remove_outliers(sigma=5)
    lc = lc.flatten(window_length=501, break_tolerance=50)

    plt.plot(ax = lc.to_periodogram(method='bls').plot())
    plt.savefig('periodogram_plot.jpg')
    return send_file('periodogram_plot.jpg', mimetype='image/jpeg')


# http://192.168.0.238:5000/plot/flix/?star_id=261136679&sector=4
@app.route('/plot/flix/')
def get_flix_video():
    paramters = request.args.to_dict()
    search_results =  lk.search_lightcurve('TIC'+str(paramters['star_id']), sector=int(paramters['sector']))

    url = "https://mast.stsci.edu/tesscut/api/v0.1/astrocut?ra=" + str(search_results[0].ra[0]) + "&dec=" + str(search_results[0].dec[0]) + "&y=30&x=30&units=px&sector=1"
    data = requests.get(url)
    open('flix_in.fits', 'wb').write(data.content)

    tpf = TargetPixelFile('flix_in.fits')
    loc = "flix_out.mp4"
    tpf.save_movie(loc)
    return send_file('flix_out.mp4', mimetype='video/mp4')



@app.route('/', methods=['GET'])
def home_page():
    return "Welcome to Home Page"


if __name__ == '__main__':
    # app.run(host='192.168.0.238', port=5000, debug=True, threaded=False)
    # below setting and network type = 'private' rather public
    app.run(host='0.0.0.0')
