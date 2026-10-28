# Multimodal Construction Intelligence Platform

A generative AI-assisted construction management application developed as a college capstone project.

## Live Demo

https://multimodal-construction-intelligence-byharsh.streamlit.app/

## Project Overview

The platform provides a single interface for construction safety reporting, preliminary crack assessment, construction cost estimation, property valuation, and site guidance.

It is built with Python and Streamlit, with optional integration with the Google Gemini API.

## Features

### 1. Site Safety & PPE
- Construction-site image upload.
- Safety report generation workflow.
- PPE inspection checklist and recommended corrective actions.

### 2. Preliminary Crack Assessment
- Upload images of possible cracks.
- Generate a preliminary assessment report.
- Provide documentation recommendations and professional follow-up guidance.

### 3. Construction Planning & Valuation
- Estimate construction costs using built-up area and rate per square foot.
- Calculate contingency and additional costs.
- Calculate an illustrative total property value.
- Download budget data as JSON.

### 4. Construction Site Assistant
- Construction planning and coordination guidance.
- General construction documentation recommendations.
- User-provided weather context for site guidance.

## Technology Stack

- **Language:** Python
- **Web framework:** Streamlit
- **AI integration:** Google Gemini API (optional)
- **Image processing:** Pillow
- **Data format:** JSON
- **Development environment:** GitHub Codespaces
- **Deployment:** Streamlit Community Cloud
- **Version control:** Git and GitHub

## Architecture

1. The user interacts with the Streamlit web interface.
2. Images and project inputs are collected through the relevant module.
3. Planning and valuation calculations are performed in Python.
4. If a Gemini API key is configured and API access is available, prompts and optional images can be sent to Gemini.
5. Without an API key, the application uses clearly labelled offline demonstration responses.
6. Reports and budget data can be downloaded by the user.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/techie-ayushyadav/multimodal-construction-intelligence.git
cd multimodal-construction-intelligence
```

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

## AI Configuration

Gemini API access is optional. Leave the API key field empty to use offline demonstration mode.

If API access is configured, provide the key through the application's password field. Never commit API keys, passwords, or other secrets to the repository.

## Limitations

- Offline demonstration reports do not perform actual image analysis.
- AI-generated image observations may be incomplete or incorrect.
- Crack assessment is not a structural engineering diagnosis.
- Safety reports do not replace professional site inspections.
- Property estimates are illustrative calculations, not certified valuations or live market estimates.
- The application does not retrieve live weather data.

## Future Enhancements

- Real image analysis with an eligible multimodal AI service.
- Weather API integration.
- Construction project scheduling and progress tracking.
- Historical report storage and comparison.
- Improved validation and automated testing.
- More detailed project cost breakdowns.

## Academic Project Notice

This application is a college capstone prototype developed for educational and demonstration purposes. It is not intended to replace qualified construction, engineering, valuation, or safety professionals.
