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
        print("inside post request")
        # Check if a file is part of the request
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                df = pd.read_excel(file, engine='openpyxl')
                print("inside allowed file df")
                print(df.columns)
                required_columns = ['Software Developer', 'Data Analyst', 'Business Analyst']
                for col in required_columns:
                    if col not in list(df.columns):
                        message=f'Missing required column: {col}'
                        print(message)
                        return render_template('index.html',message="Missing required column")
                

                column_data1 = df['Software Developer'].dropna().tolist()
                column_data2 = df['Data Analyst'].dropna().tolist()
                column_data3 = df['Business Analyst'].dropna().tolist()

                num_teams = min(len(column_data1) // 3, len(column_data2), len(column_data3))
                teams = []
                
                # Generate teams
                for i in range(num_teams):
                    if len(column_data1) < 3 or len(column_data2) < 1 or len(column_data3) < 1:
                        print("Insufficient members to form a team")
                        break
                    
                    selected_developers = random.sample(column_data1, 3)
                    selected_data_analyst = random.sample(column_data2, 1)
                    selected_business_analyst = random.sample(column_data3, 1)
                    
                    team = selected_developers + selected_data_analyst + selected_business_analyst
                    teams.append(team)

                    # Remove selected members from the lists
                    column_data1 = [d for d in column_data1 if d not in selected_developers]
                    column_data2 = [d for d in column_data2 if d not in selected_data_analyst]
                    column_data3 = [d for d in column_data3 if d not in selected_business_analyst]
                # Render the template with the teams
                print(len(teams))
                print("------")
                return render_template('index.html', teams=teams, found="Teams created successfully")
            except Exception as e:
                message=f'Error reading file: {e}'
                return render_template('index.html',message="error reading file:")
        else:
            print('Invalid file format')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
