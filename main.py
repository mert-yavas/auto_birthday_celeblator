import random
import smtplib
import datetime as dt
import pandas

MY_EMAIL = "YOUR MAIL"
PASSWORD = "YOUR PASSWORD"

now = dt.datetime.now()
current_month = now.month
current_day = now.day

# Select a random letter template from the available choices
letters = f"letter_templates/letter_{random.randint(1, 3)}.txt"

birthday_data = pandas.read_csv("birthdays.csv")
birthdays = birthday_data.to_dict(orient="records")


def send_mail(name, email):
    # Use a chosen letter template
    chosen_letter = letters

    # Read the content of the selected letter template
    with open(chosen_letter, "r") as letter_file:
        original_content = letter_file.read()

    # Modify the letter content by replacing the placeholder with the name
    modified_content = original_content.replace("[NAME]", name)

    # Use a temporary file to avoid modifying the original template
    with open(chosen_letter + "_temp", "w") as file:
        file.write(modified_content)

    # Establish an SMTP connection and send the modified letter
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=email,
        msg=f"Subject: Happy Birthday\n\n{modified_content}"
    )
    connection.close()

    # Restore the original content of the template
    with open(chosen_letter, "w") as file:
        file.write(original_content)


for birthday in birthdays:
    birthday_month = birthday['month']
    birthday_day = birthday['day']
    birthday_name = birthday['name']
    birthday_mail = birthday['email']

    # Check if it's the birthday of someone in the dataset
    if birthday_month == current_month and birthday_day == current_day:
        send_mail(birthday_name, birthday_mail)
