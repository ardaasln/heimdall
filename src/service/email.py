import boto3
from botocore.exceptions import ClientError
from pyquery import PyQuery as pq
from flask import current_app

# TODO do not repeat boto3 client send_email


def send_verification_email(destination: str, token: str):
    """
    Sends verification email to the given destination with token attached to it
    """

    f = open("assets/email-verification.html", "rt", encoding="utf-8")

    doc = pq(f.read())

    base_url = current_app.config["BASE_URL"]

    doc("#verification-link").attr("href", "{}/verify/{}".format(base_url, token))

    current_app.logger.debug("Attempting to send an verification email to: {}".format(destination))

    client = boto3.client('ses', region_name='eu-west-1')

    try:
        client.send_email(
            Destination={
                'ToAddresses': [
                    destination,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': doc.html(),
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': doc.html(),
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': 'Email Verification',
                },
            },
            Source='support@sporplatz.com'
        )
    except ClientError as e:
        current_app.logger.error("Exception while sending verification email: {}".format(e))
    else:
        current_app.logger.debug("Verification mail sent to {}".format(destination))

    f.close()


def send_forgot_password_email(destination: str, token: str, name: str):
    """
    Sends forgot password email to the given destination with token attached to it
    """
    f = open("assets/forgot-password.html", "rt", encoding="utf-8")

    doc = pq(f.read())

    base_url = current_app.config["BASE_URL"]

    doc("#reset-link").attr("href", "{}/password-reset/{}".format(base_url, token))

    doc("#user-name").text(name)

    current_app.logger.debug("Attempting to send an forgot-password email to: {}".format(destination))

    client = boto3.client('ses', region_name='eu-west-1')

    try:
        client.send_email(
            Destination={
                'ToAddresses': [
                    destination,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': doc.html(),
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': doc.html(),
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': 'Forgot Password',
                },
            },
            Source='support@sporplatz.com'
        )
    except ClientError as e:
        current_app.logger.error("Exception while sending verification email: {}".format(e))
    else:
        current_app.logger.debug("Forgot password mail sent to {}".format(destination))

    f.close()
