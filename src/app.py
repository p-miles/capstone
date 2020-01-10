import flask
import matplotlib
from io import BytesIO

from climate_or_weather import WeatherRecord

matplotlib.rcParams.update({'font.size': 18})

app = flask.Flask(__name__)

# Form page to submit text
@app.route('/')
def submission_page():
    # in this form, method = 'POST' means that data entered into
    # the 'location' and 'date' variables will be sent to the /plot.png routing
    # block when the submit button is pressed
    return '''
        <form action="/plot.png" method='POST' >
            <center>
            <h1> Climate Change or Just Weather? </h1>
            <br> Location <br>
            <input type="text" name="location" size="25" />
            <br> Date <br>
            <input type="date" name="date">
            <br> <br>
            <input type="submit">
            </center>
        </form>
        '''


@app.route('/plot.png', methods=['GET', 'POST'])
def get_graph():
    # retrieve input data from submission page
    loc = str(flask.request.form['location'])
    date = str(flask.request.form['date'])

    # must create figure using Figure(), not subplots() or app will crash
    fig = matplotlib.figure.Figure(figsize=(12, 8))

    # create object that encapsulates all the data
    # needed for analysis and plotting methods
    weather_record = WeatherRecord(loc, date)
    weather_record.gen_plot(fig)

    image = BytesIO()
    fig.savefig(image)  # the plot is saved

    return image.getvalue(), 200, {'Content-Type': 'image/png'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
