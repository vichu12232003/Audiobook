# Audiobook

﻿This project is an Audiobook Generator designed to convert text into audio using advanced AI models. It leverages MMS TTS (Massively Multilingual Speech Text-to-Speech) models from Facebook, available on Hugging Face, to produce high-quality, natural-sounding audio in multiple languages.

Purpose of the Project
The project aims to make content for  people who prefer listening over reading. It’s especially useful for those with visual impairments, busy lifestyles, or anyone looking for a convenient way to consume text-based content.

Key Features
    1. Support for Multiple Languages:
The app supports a wide range of languages, including English, Hindi, Spanish, French, Tamil, Bengali, and more, making it suitable for a global audience.
    2. Time Efficiency:
Generates audio quickly, even for lengthy text inputs, saving time compared to manual recording.
    3. Natural Sounding Audio:
For most languages, the generated audio closely resembles natural human speech, enhancing the listening experience.

How It Works
    1. Language Selection:
The user selects the language of their choice from a dropdown menu.
    2. Text Input:
Users provide the text they wish to convert into audio.
    3. Model Loading:
Based on the selected language, the app loads the appropriate pre-trained MMS TTS model and tokenizer.
    4. Text Chunking:
To handle large text inputs, the text is divided into smaller chunks using punctuation and a predefined length limit.
    5. Audio Generation:
Each text chunk is processed by the AI model, which generates audio for it.
    6. Audio Combining:
The individual audio chunks are combined into a single, seamless audio file.
    7. Download and Playback:
The final audio file is made available for download as a WAV file, and users can also preview the generated audio within the app.

Why It’s Useful
    1. Accessibility:
Makes content accessible to people with disabilities, such as visual impairments or reading difficulties.
    2. Global Reach:
With support for multiple languages, it’s versatile and caters to a worldwide audience.
    3. Time Efficiency:
Converts text to audio faster than traditional recording methods, saving time and effort.
    4. Flexibility:
Can be adapted for various use cases, including educational audiobooks, podcasts, or voiceovers for multimedia projects.
