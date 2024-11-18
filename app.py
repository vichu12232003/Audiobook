import streamlit as st
import torch
from transformers import VitsModel, AutoTokenizer
import scipy.io.wavfile
import numpy as np
import tempfile
import os

# Dictionary of supported languages with their codes
SUPPORTED_LANGUAGES = {
    "English": "eng",
    "Tamil": "tam",
    "Hindi": "hin",
    "Spanish": "spa",
    "French": "fra",
    "German": "deu",
    "Malayalam": "mal"
    
    # Add more languages as needed
}

def load_model_and_tokenizer(lang_code):
    """Load the MMS TTS model and tokenizer for a specific language."""
    model_name = f"facebook/mms-tts-{lang_code}"
    try:
        model = VitsModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model for language code {lang_code}: {str(e)}")
        return None, None

def chunk_text(text, max_length=200):
    """Split text into chunks based on punctuation and max length."""
    sentences = text.replace('\n', ' ').split('.')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip() + "."
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += " " + sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_audio_for_chunk(chunk, model, tokenizer):
    """Generate audio for a single text chunk."""
    inputs = tokenizer(chunk, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    return output.numpy().flatten()

def combine_audio_chunks(audio_chunks, sample_rate):
    """Combine multiple audio chunks into a single audio file."""
    combined = np.concatenate(audio_chunks)
    return combined

def main():
    st.title("MMS Audiobook Generator")
    
    # Language selection
    selected_language = st.selectbox(
        "Select Language",
        options=list(SUPPORTED_LANGUAGES.keys())
    )
    
    # Text input
    text_input = st.text_area(
        "Enter your text",
        height=200,
        help="Enter the text you want to convert to audio"
    )
    
    if st.button("Generate Audiobook"):
        if not text_input:
            st.warning("Please enter some text.")
            return
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Load model and tokenizer
        status_text.text("Loading model...")
        lang_code = SUPPORTED_LANGUAGES[selected_language]
        model, tokenizer = load_model_and_tokenizer(lang_code)
        
        if model is None or tokenizer is None:
            return
        
        # Process text in chunks
        status_text.text("Processing text...")
        chunks = chunk_text(text_input)
        audio_chunks = []
        
        for i, chunk in enumerate(chunks):
            status_text.text(f"Generating audio for chunk {i+1}/{len(chunks)}")
            progress_bar.progress((i + 1) / len(chunks))
            
            try:
                audio_chunk = generate_audio_for_chunk(chunk, model, tokenizer)
                audio_chunks.append(audio_chunk)
            except Exception as e:
                st.error(f"Error processing chunk {i+1}: {str(e)}")
                return
        
        # Combine chunks
        status_text.text("Combining audio chunks...")
        combined_audio = combine_audio_chunks(audio_chunks, model.config.sampling_rate)
        
        # Save and provide download
        status_text.text("Preparing download...")
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            scipy.io.wavfile.write(
                temp_file.name,
                rate=model.config.sampling_rate,
                data=combined_audio
            )
            
            # Create download button
            with open(temp_file.name, 'rb') as f:
                st.download_button(
                    label="Download Audiobook",
                    data=f,
                    file_name="audiobook.wav",
                    mime="audio/wav"
                )
            
            # Play audio preview
            st.audio(temp_file.name, format="audio/wav")

        # Clean up temp file after rendering
        status_text.text("Cleaning up temporary files...")
        os.unlink(temp_file.name)

        status_text.text("Done!")
        progress_bar.progress(100)

if __name__ == "__main__":
    main()
