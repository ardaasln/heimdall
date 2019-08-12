import boto3
from botocore.exceptions import ClientError
from pyquery import PyQuery as pq
from flask import current_app


def send_verification_email(destination: str, token: str):
    """
    Sends verification email to the given destination with token attached to it
    """

    f = open("assets/email-verification.html", "rt", encoding="utf-8")

    doc = pq(f.read())

    doc("#verification-link").attr("href", "http://localhost:3000/verify/{}".format(token))

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

    # def send_forgot_password_email(self, destination: str, token: str, name: str, roles: list):
    #     """
    #     Sends forgot password email to the given destination with token attached to it
    #     """
    #     try:
    #         f = open(api.MSROOT + "/assets/forgot-password.html", "rt", encoding="utf-8")
    #     except FileNotFoundError:
    #         raise MicrozException(
    #             "Email template does not exist",
    #             status=500,
    #             code=CODE_FILE_DOES_NOT_EXIST
    #         )
    #
    #     doc = pq(f.read())
    #     if Roles.ROLE_CUSTOMER in roles:
    #         doc("#reset-link").attr("href", "{}/password-reset/{}".format(self.app_endpoint, token))
    #     else:
    #         doc("#reset-link").attr("href", "{}/password-reset/{}".format(self.partner_endpoint, token))
    #     doc("#user-name").text(name)
    #
    #     self.logger.debug("Attempting to send an forgot-password email to: {}".format(destination))
    #
    #     self.email_wrapper.send_email(self.settings, destination, "Forgot Password", doc.html())
    #
    #     self.logger.debug("Forgot password mail sent to {}".format(destination))
    #
    #     f.close()
