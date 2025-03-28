# In your main application entry point (e.g., run.py or app.py)
from app import create_app
from config import DevelopmentConfig, ProductionConfig

# Create the app with the desired configuration
# app = create_app(ProductionConfig)
app = create_app(DevelopmentConfig)  # Use DevelopmentConfig for development

if __name__ == "__main__":
    app.run(debug=True) # You can add this here for a basic run
