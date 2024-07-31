from flask import Flask, render_template, request, send_file
from flask.helpers import redirect
import os

app = Flask(__name__, template_folder='templets', static_folder='statics')


@app.route('/')
@app.route('/home')
def index():
  return render_template('index.html')


@app.route('/uploads', methods=['POST'])
def upload():
  # Get the uploaded file
  file = request.files['file']
  file.save(f'/uploads/{file.filename}')
  return redirect('/')


if __name__ == '__main__':
  app.run(debug=True)
