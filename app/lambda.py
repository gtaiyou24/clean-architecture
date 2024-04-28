from mangum import Mangum

from app import app

handler = Mangum(app, lifespan="on", api_gateway_base_path="/")
