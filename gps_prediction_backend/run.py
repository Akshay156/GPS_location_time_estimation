import os
import logging
from app.api import app

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Logging is set up.")

def main():
    """Main entry point to run the Flask application."""
    # Set up logging
    setup_logging()
    
    # Get host and port from environment variables or use defaults
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')  # Allows access from any IP
    port = int(os.getenv('FLASK_RUN_PORT', 5000))  # Default Flask port

    # Start the Flask application
    logging.info(f"Starting server at http://{host}:{port}")
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()
