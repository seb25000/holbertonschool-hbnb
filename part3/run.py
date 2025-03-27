from app import create_app
from config import DevelopmentConfig  # or ProductionConfig, etc.

app = create_app(DevelopmentConfig)


if __name__ == '__main__':
    app.run()
