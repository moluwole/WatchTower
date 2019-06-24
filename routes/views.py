# import python packages here
import os

# import 3rd party or framework level packages here
from vibora.responses import JsonResponse
from vibora.blueprints import Blueprint
from vibora import Vibora

# Import project level packages here
from core.config import app_config
from controllers.test_controller import TestController

api = Blueprint()


@api.route('/')
async def index():
    test = TestController()
    message = test.return_message()
    return JsonResponse({'name': message})


def create_server(app: Vibora):
    # Add the blueprints here.
    app.add_blueprint(api)
    return app
