from flask import Blueprint, render_template, redirect
from sqlalchemy import exc

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
        return render_template("errors/error.html", 
                            error_type="Oops. Page Not Found (404)", 
                            error_msg="That page does not exists. Please try a different location"), 404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template("errors/error.html", 
                            error_type="You don't have persmission to do that (403)", 
                            error_msg="Please check your account and try again"), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template("errors/error.html", 
                            error_type="Something went wrong (500)", 
                            error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500

@errors.app_errorhandler(exc.OperationalError)
def error_exc_OperationalError(error):
    return redirect("/")
