from src.api.validator import validate, field
from flask import Blueprint, request, jsonify, g
from src.service.user import forgot_password as user_forgot_password, login as user_login, register as user_register, reset_password as user_reset_password, verify as user_verify, resend_verification_email as user_resend_verification_email
from src.errors.custom_error import CustomError
from src.entity.user import User
from src.api.http import Http

bp = Blueprint("user", __name__)


@bp.route("/account/register", methods=['POST'])
def register():
    """
    Validates the request body and tries to register the user
    """

    body = validate({
        "fullname": field("string", maxlength=100),
        "email": field("email"),
        "password": field("password"),
        "tos": field("tos")
    }, request.get_json(force=True, silent=True))

    if not body["tos"]:
        raise CustomError(
            message="Servis kosullarini kabul etmeniz gerekmektedir",
            status_code=400
        )

    user = User(body)
    user.registration_ip = request.access_route

    user_register(user)

    return "User successfully registered."


@bp.route("/account/login", methods=['POST'])
def login():
    """
    Validates the request body and tries to log the user in and returns jwt
    """

    body = validate({
        "email": field("email"),
        "password": field("password")
    }, request.get_json(force=True, silent=True))

    token = user_login(
        body["email"],
        body["password"],
        request.access_route
    )

    return jsonify({"token": token})


@bp.route("/account/forgot-password", methods=['POST'])
def forgot_password():
    """
    Validates the request body and tries to send a password reset mail to the user
    """

    body = validate({
        "email": field("email")
    }, request.get_json(force=True, silent=True))

    user_forgot_password(body["email"])

    return "Password reset email sent"


@bp.route("/account/reset-password", methods=['POST'])
def reset_password():
    """
    Validates fields sent on form and updates the password of user after successful jwt authentication
    """

    body = validate({
        "password": field("password")
    }, request.get_json(force=True, silent=True))

    token = request.headers.get("AUTHORIZATION")

    Http.auth(token)

    user_reset_password(g.user["email"], body["password"])

    return "Password reset"


@bp.route("/account/verify-email", methods=['GET'])
def verify_email():
    """
    Verifies the jwt after user clicks his mail and makes user verified in database
    """
    user_verify(request.query_string.decode("utf-8").split("=")[-1])

    return "Email Verified"


@bp.route("/account/resend-verification-email", methods=['POST'])
def resend_verification_email():
    """
    Resends the verification email
    """

    body = validate({
        "email": field("password")
    }, request.get_json(force=True, silent=True))

    user_resend_verification_email(body["email"])

    return "Resent Verification Email"
