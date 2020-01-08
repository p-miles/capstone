from flask import Flask, request
from matplotlib.figure import Figure
from io import BytesIO

import hypothesis_testing

app = Flask(__name__)

# Form page to submit text
@app.route('/')
def submission_page():
    # in this form, method = 'POST' means that data entered into
    # the 'user_input' variable will be sent to the /word_counter routing
    # block when the 'Enter text' submit button is pressed
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
    loc = str(request.form['location']) #gets the value entered in the input type="text", name="user_input"
    date = str(request.form['date'])
    
    fig = Figure()

    hypothesis_testing.gen_plot(fig,loc,date)
    
    image = BytesIO()
    fig.savefig(image)  #the plot is saved

    return image.getvalue(), 200, {'Content-Type': 'image/png'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
