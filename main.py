from flask import Flask, render_template, request
import csv
import smtplib
import re

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the uploaded CSV file
        csv_file = request.files["csv_file"]

        # Validate the CSV file
        if not csv_file.filename.endswith(".csv"):
            return "Invalid CSV file!"

        # Read the CSV file and segment the email addresses into valid and invalid email addresses
        valid_email_addresses = []
        invalid_email_addresses = []

        csv_file.stream.seek(0)  # Move the cursor to the beginning of the file
        reader = csv.reader([line.decode('utf-8') for line in csv_file])

        for row in reader:
            email_address = row[0]
            if is_valid_email_address(email_address):
                valid_email_addresses.append(email_address)
            else:
                invalid_email_addresses.append(email_address)

        # Send the mass email
        send_mass_email(valid_email_addresses, request.form["subject"], request.form["body"])

        # Display the successful result
        return render_template('result.html', valid_email_addresses=valid_email_addresses,
                               invalid_email_addresses=invalid_email_addresses)

    return render_template('index.html')


def is_valid_email_address(email_address):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    match = re.search(regex, email_address)
    if match:
        return True
    else:
        return False


def send_mass_email(valid_email_addresses, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "ashikcsbtech@gmail.com"  # Replace with your Gmail address
    smtp_password = "lyikjkipgfnttchw"  # Replace with your Gmail password or app password if using 2-step verification

    smtp_client = smtplib.SMTP(smtp_server, smtp_port)
    smtp_client.starttls()
    smtp_client.login(smtp_username, smtp_password)

    for email_address in valid_email_addresses:
        message = f"Subject: {subject}\n\n{body}"
        smtp_client.sendmail(smtp_username, email_address, message)

    smtp_client.quit()


if __name__ == "__main__":
    app.run(debug=True)

    # smtp_password = "lyikjkipgfnttchw"  # Replace with your Gmail password or app password if using 2-step verification
