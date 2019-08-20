from src.api.validator import validate, field
from flask import Blueprint, request, jsonify, g
from src.service.user import forgot_password as user_forgot_password, login as user_login, register as user_register, reset_password as user_reset_password, verify as user_verify, resend_verification_email as user_resend_verification_email, update_user as user_update_user
from src.errors.custom_error import CustomError
from src.entity.user import User
from src.api.http import Http
from src.repo.user import list_users as repo_list_users

bp = Blueprint("user", __name__)


@bp.route("/account/", methods=['GET'])
def health_check():
    return "ok"


@bp.route("/account/register", methods=['POST'])
def register():
    """
    Validates the request body and tries to register the user
    """

    body = validate({
        "username": field("string", maxlength=180, required=True, empty=False, nullable=False),
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
        "email": field("email")
    }, request.get_json(force=True, silent=True))

    user_resend_verification_email(body["email"])

    return "Resent Verification Email"


@bp.route("/account/users", methods=['GET'])
def list_users():
    """
    Returns users according to given filters
    """
    token = request.headers.get("AUTHORIZATION")
    Http.auth(token, ["ROLE_ADMIN"])

    params = {
        "page": request.args.get("page", default=1, type=int),
        "size": request.args.get("size", default=100, type=int),
        "name": request.args.get("name", type=str),
        "order_by": request.args.get("order_by", default="id", type=str),
        "order_dir": request.args.get("order_dir", default="DESC", type=str),
    }

    users, total_row_count = repo_list_users(params)

    return jsonify({
        "data": users,
        "page": {
            "current": params["page"],
            "total": total_row_count,
            "size": params["size"]
        }
    })


@bp.route("/account/user/<user_id>", methods=['PUT'])
def update_user(user_id: int):
    token = request.headers.get("AUTHORIZATION")
    Http.auth(token, ["ROLE_ADMIN"])

    body = validate({
        "enabled": field("integer", required=False, nullable=False, empty=False),
        "email_verified": field("integer", required=False, nullable=False, empty=False),
        "roles": field("list", required=False, nullable=False, empty=False)
    }, request.get_json(force=True, silent=True))

    user_update_user(body, user_id)

    return "ok"
