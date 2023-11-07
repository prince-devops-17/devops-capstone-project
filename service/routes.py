"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

@app.route("/accounts", methods=["GET"])
def read_all_accounts():
    """
    Lists all existing account in the service
    This endpoint will list all accounts existing within the service
    """
    try:
        app.logger.info("Request to list all Account")
        accounts = Account.all()
        return accounts, status.HTTP_200_OK
    except Exception as e:
        return make_response([], status.HTTP_200_OK)


######################################################################
# READ AN ACCOUNT
######################################################################

@app.route("/accounts/<account_id>", methods=["GET"])
def read_account(account_id):
    """
    Lists details pertaining to an existing account in the service
    This endpoint will list details pertaining to an existing account in the service
    """
    try:
        app.logger.info("Request to list Account details")
        account = Account.find(account_id)

        if not account:
            return make_response("", status.HTTP_404_NOT_FOUND)

        return account.serialize(), status.HTTP_200_OK
    except Exception as e:
        return make_response("", status.HTTP_404_NOT_FOUND)

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

@app.route("/accounts/<account_id>", methods=["PUT"])
def update_account(account_id):
    """
    Updates the details of an account in the service
    This endpoint will update the details of an account in the service
    """
    try:
        app.logger.info("Request to list Account details")
        account = Account.find(account_id)

        if(not account):
            return make_response("", status.HTTP_404_NOT_FOUND)
        
        account.deserialize(request.get_json())
        account.update()

        return make_response(account.serialize(), status.HTTP_200_OK)
    except Exception as e:
        return make_response("", status.HTTP_404_NOT_FOUND)

######################################################################
# DELETE AN ACCOUNT
######################################################################

@app.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    Updates the details of an account in the service
    This endpoint will update the details of an account in the service
    """
    try:
        app.logger.info("Request to list Account details")
        account = Account.find(account_id)
        account.delete()
        return make_response("", status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
