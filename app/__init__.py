from config import DevelopmentConfig
from app.app_factory import create_app

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
