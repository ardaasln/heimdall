from src.api.validator import validate, field
from flask import Blueprint, request
from src.service.user import register
from src.errors.custom_error import CustomError
from src.entity.user import User

bp = Blueprint("user", __name__)


@bp.route("/register", methods=['POST'])
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
            message="ToS is not accepted.",
            status_code=400
        )

    user = User(body)
    user.registration_ip = request.access_route

    register(user)

    return "User successfully registered."



