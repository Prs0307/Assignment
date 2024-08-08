import os
import pandas as pd
from flask import Flask, request, render_template, redirect, flash
from werkzeug.utils import secure_filename
import random
import uuid   


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = "BAD_DEVELOPER"
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            filename = secure_filename(str(uuid.uuid4()) + '.xlsx')   
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            try:
                df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                column_data1 = df['Software Developer'].dropna().tolist()
                column_data2 = df['Data Analyst'].dropna().tolist()
                column_data3 = df['Buisiness Analyst'].dropna().tolist()

        
                num_teams = min(len(column_data1) // 3, len(column_data2), len(column_data3))
                teams = []
                for i in range(num_teams):
                    while len(column_data1) >= 3 and len(column_data2) > 0 and len(column_data3) > 0:
                        if len(column_data1) < 3 or len(column_data2) < 1 or len(column_data3) < 1:
                            print("Insufficient members to form a team")
                            break
                        selected_developers = random.sample(column_data1, 3)
                        selected_data_analyst = random.sample(column_data2, 1)
                        selected_business_analyst = random.sample(column_data3, 1)
                        team = selected_developers + selected_data_analyst + selected_business_analyst
                        teams.append(team)

                        column_data1 = [d for d in column_data1 if d not in selected_developers]
                        column_data2 = [d for d in column_data2 if d not in selected_data_analyst]
                        column_data3 = [d for d in column_data3 if d not in selected_business_analyst]

                return render_template('index.html', teams=teams, found="Teams  :  Team members")
            except Exception as e:
                flash(f'Error reading file: {e}')
                return redirect(request.url)
        else:
            flash('Invalid file type. Only excel files allowed.')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
