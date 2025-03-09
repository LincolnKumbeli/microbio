# MicroBio App

A Flask-based web application for microbiological media recommendations and growth characteristics.

## Features

- Select microorganisms and growth media
- Get media recommendations based on organism selection
- View growth characteristics and results
- Get suggestions for confirmatory tests

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd microbio_app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python run.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
microbio_app/
│── app/
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── routes/              # Route handlers
│   ├── models/              # Data models
│   ├── utils/               # Utility functions
│   └── static_data/         # JSON data store
│── tests/                   # Unit tests
└── requirements.txt         # Dependencies
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 