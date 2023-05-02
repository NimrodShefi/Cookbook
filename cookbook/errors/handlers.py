from flask import Blueprint, render_template, current_app
from sqlalchemy.exc import OperationalError, IntegrityError, PendingRollbackError
from cookbook import db

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
    current_app.logger.info("404")
    current_app.logger.info(error)
    return render_template("errors/error.html", 
                           error=True,
                           error_type="Oops. Page Not Found", 
                           error_msg="That page does not exist. Please try a different location"), 404

@errors.app_errorhandler(403)
def error_403(error):
    current_app.logger.info("403")
    current_app.logger.info(error)
    return render_template("errors/error.html", 
                           error=True,
                           error_type="You don't have permission to do that", 
                           error_msg="Please check your account and try again"), 403

@errors.app_errorhandler(500)
def error_500(error):
    current_app.logger.info("500")
    current_app.logger.info(error)
    return render_template("errors/error.html", 
                           error=True,
                           error_type="Something went wrong (500)", 
                           error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500

@errors.app_errorhandler(AttributeError)
def error_AttributeError(error):
    current_app.logger.info("AttributeError")
    current_app.logger.info(error)
    return render_template("errors/error.html",
                           error=True,
                           error_type="Something went wrong",
                           error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500

@errors.app_errorhandler(OperationalError)
def error_OperationalError(error):
    current_app.logger.info("OperationalError")
    current_app.logger.info(error)
    db.session.rollback()
    return render_template("errors/error.html", 
                            error=True,
                            error_type="Something went wrong",
                            error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500

@errors.app_errorhandler(IntegrityError)
def error_IntegrityError(error):
    current_app.logger.info("IntegrityError")
    current_app.logger.info(error)
    db.session.rollback()
    return render_template("errors/error.html",
                    error=True,
                    error_type="Something went wrong",
                    error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500

@errors.app_errorhandler(PendingRollbackError)
def error_PendingRollbackError(error):
    current_app.logger.info("PendingRollbackError")
    current_app.logger.info(error)
    db.session.rollback()
    return render_template("errors/error.html",
                    error=True,
                    error_type="Something went wrong",
                    error_msg="We're experiencing some trouble on our end. Please try again in the near future"), 500
