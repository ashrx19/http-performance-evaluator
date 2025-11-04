# HTTP Performance Evaluator Web

This project is a web-based application that benchmarks the performance of HTTP/1.1 and HTTP/2 protocols. It provides an interactive dashboard for users to input URLs and visualize performance metrics in real-time.

## Features

- Benchmarking of HTTP/1.1 and HTTP/2 protocols.
- User-friendly web interface built with Flask.
- Live dashboard displaying performance metrics and charts.
- Continuous tracking of performance metrics.
- Alert system for performance thresholds.

## Project Structure

```
http-performance-evaluator-web
├── src
│   ├── benchmark.py        # Contains benchmarking logic for HTTP protocols.
│   ├── app.py              # Main entry point for the Flask application.
│   ├── config.py           # Configuration settings for the application.
│   ├── tasks.py            # Manages background tasks for continuous tracking.
│   ├── templates           # HTML templates for the web interface.
│   │   ├── index.html      # Landing page with user input forms.
│   │   └── dashboard.html   # Live dashboard for performance metrics.
│   └── static              # Static files for CSS and JavaScript.
│       ├── css
│       │   └── styles.css   # Styles for the web application.
│       └── js
│           ├── dashboard.js  # JavaScript for dashboard interactivity.
│           └── chart-config.js # Configuration for Chart.js.
├── tests                   # Unit tests for benchmarking functions.
│   └── test_benchmark.py   # Tests to ensure benchmarking works correctly.
├── requirements.txt        # Lists dependencies for the project.
├── .env                    # Environment variables for configuration.
├── Procfile                # Commands to run the application on Heroku.
└── README.md               # Documentation for the project.
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/http-performance-evaluator-web.git
   cd http-performance-evaluator-web
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables in the `.env` file as needed.

## Usage

1. Start the Flask application:
   ```
   python src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000` to access the application.

3. Input the URL you want to benchmark and start the tests. The dashboard will display the results in real-time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.