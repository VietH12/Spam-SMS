from flask import Flask, request, render_template
import pandas as pd
from joblib import load
import re
import subprocess

app = Flask(__name__)

# Load the pre-trained SVM model and vectorizer
model = load('path_to_my_model/spam_classifier_model_svc.pkl')
vectorizer = load('path_to_my_model/vectorizer.pkl')  # Assuming the vectorizer was saved separately

def preprocess_text(text):
    return vectorizer.transform([text])

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    phone_number = ''  # Default empty phone number
    if request.method == 'POST':
        phone_number = request.form['phone_number'].strip()
        if not re.match(r'^\d+$', phone_number):
            error_message = f"<strong>Error: </strong> '{phone_number}' does not exist. Please enter a numeric phone number."
            results.append((error_message, "", 0))
        else:
            try:
                # Attempt to run the get.py file before reading the CSV file
                subprocess.run(["python", "get.py", phone_number], check=True)

                phone_number = int(phone_number)

                # Load the messages from CSV file where 'cell_number' column matches the input
                df = pd.read_csv('sms_data.csv')

                # Ensure the 'cell_number' column is treated as a string for matching
                df['cell_number'] = df['cell_number'].astype(str)
                phone_number = str(phone_number)

                filtered_df = df[df['cell_number'] == phone_number]
                messages = filtered_df['message'].tolist()

                if not messages:
                    results.append((f"No messages found for phone number: {phone_number}", "", 0))
                else:
                    for message in messages:
                        processed_message = preprocess_text(message)
                        processed_message_dense = processed_message.toarray()
                        prediction = model.predict(processed_message_dense)[0]
                        prediction_label = 'Spam' if prediction == 1 else 'Not Spam'
                        results.append((message, prediction_label, prediction))

            except FileNotFoundError:
                results.append(("<strong>Error: </strong> File not found. Please check the file path.", "", 0))
            except subprocess.CalledProcessError:
                results.append((f"<strong>Error: </strong> Phone number <strong>{phone_number}</strong> does not exist or could not be processed.", "", ""))
            except Exception as e:
                results.append((f"<strong>Error: </strong> {str(e)}", "", 0))

    return render_template('index.html', results=results, phone_number=phone_number)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
