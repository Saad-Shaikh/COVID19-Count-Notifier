#!/usr/bin/env python3
import credentials as cred
import details as det
import utils
import smtplib
import schedule
import time

def send_via_email():
    """
    Send an email to every person in the email list
    """

    count_list = utils.get_count_list(det.states_and_cities, det.state_url, det.district_url)

    for entry in det.email_list:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(cred.login_email, cred.login_pass)
        message = utils.form_message_for_email(count_list, entry.get('states'), entry.get('cities'))
        s.sendmail(cred.login_email, entry.get('email'), "Subject: Daily COVID19 Count\n\n" + message)
        print("Email sent to " + entry.get('email'))
        s.quit()
    print()


# if you want to schedule mails at a specific time, use this and comment the if block below
# schedule.every().day.at("04:30").do(send_via_email)
# while(1):
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == '__main__':
    send_via_email()
