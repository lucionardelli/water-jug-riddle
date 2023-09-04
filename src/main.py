import sys

from ui.jug_riddle_ui import water_jug_riddle_ui
from web.solver_endpoint import run_flask_app

if __name__ == "__main__":
    import threading

    # Create a thread for the Flask app so the GUI can be spawn while the flask server is running
    flask_thread = threading.Thread(target=run_flask_app)
    # Start the thread
    flask_thread.start()

    # Run the GUI
    water_jug_riddle_ui()

    # Wait for the Flask thread to finish (if needed)
    flask_thread.join()

    sys.exit(0)
