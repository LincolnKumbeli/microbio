# MicroBio App

A Flask-based web application for microbiological media information and organism identification. This application helps microbiologists and laboratory professionals access information about different culture media, organism growth characteristics, and confirmatory tests.

## Features

- **Media Information:**
  - Detailed information about various culture media (Blood Agar, MacConkey, EMB, etc.)
  - Media composition and characteristics
  - Common uses and applications
  - Example images of growth patterns

- **Organism Information:**
  - Growth characteristics on different media
  - Confirmatory test results and interpretations
  - Visual references of colony morphology

- **Interactive Interface:**
  - Search by media type
  - Search by organism
  - Automatic display of media information on selection
  - Image carousel for visual references

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd Bugs\ App
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask
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
├── app/
│   ├── static/
│   │   └── images/
│   │       ├── organisms/    # Organism-specific images
│   │       └── plates/       # Media plate images
│   ├── templates/           # HTML templates
│   └── routes/
│       └── main.py         # Main route handlers
└── run.py                  # Application entry point
```

## Media Types Included

- Blood Agar
- MacConkey Agar
- EMB (Eosin Methylene Blue) Agar
- Chocolate Agar
- Mueller Hinton Agar
- Mannitol Salt Agar

## Organisms Included

- Escherichia coli
- Staphylococcus aureus
- Pseudomonas aeruginosa
- Klebsiella pneumoniae
- Streptococcus pneumoniae
- Neisseria gonorrhoeae
- Clostridioides difficile
- Haemophilus influenzae
- And more...

## Contributing

If you'd like to contribute to this project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License. 