# Afrotales
Microsoft generative AI hackathon
# Afro-tales Capture

Afro-tales Capture is a web application designed to promote African literature using generative AI. The project leverages advanced AI technologies to generate illustrative images and provide educational analysis based on excerpts from African literary works.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Afro-tales Capture aims to foster a deeper connection to African cultural heritage among youths and children by transforming literary excerpts into engaging visual content. Users can upload images of African novels or screenshots, which the application processes to generate illustrative images representing the described events or characters.

## Features

- Upload images or screenshots of African literature.
- Extract text using Azure Read OCR.
- Generate descriptive images using OpenAI's DALL-E.
- Provide educational analysis using OpenAI's ChatCompletions.
- Enhance engagement with African literary works.

## Tech Stack

The project utilizes the following technologies:

- **Backend**: Django
- **AI Services**: OpenAI API (ChatCompletions, DALL-E)
- **Cloud Services**: Microsoft Azure
  - **Hosting**: Azure App Service
  - **File Storage**: Azure Blob Storage
  - **OCR**: Azure Cognitive Services (Read OCR)

## Setup

To set up the project locally, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/afro-tales-capture.git
   cd afro-tales-capture
2. **Create and activate a virtual environment**
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
3. **Install Dependencies**
   pip install -r requirements.txt
4. **Set up environment variables**
   Create a .env file in the project root directory and add the necessary environment variables:
   AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
   AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
   AZURE_OCR_ENDPOINT=your_azure_ocr_endpoint
   AZURE_OCR_KEY=your_azure_ocr_key
   OPENAI_API_KEY=your_openai_api_key
5. **Run the Migrations**
   python manage.py migrate
6. **Start the development server**
   python manage.py runserver

## Usage
1. Upload an Image: Users can upload images of African novels or screenshots.
2. Text Extraction: The app uses Azure Read OCR to extract text from the uploaded image.
3. AI Processing: The extracted text is processed using OpenAI's ChatCompletions and DALL-E to generate descriptive and illustrative outputs.
4. View Results: The generated images and educational analysis are displayed to the user.

## Contributing
We welcome contributions to enhance Afro-tales Capture. To contribute:
1. Fork the repository.
2. Create a new feature branch (git checkout -b feature/your-feature-name).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a pull request.
Please ensure your code adheres to the project's coding standards and includes relevant tests.


