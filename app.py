import streamlit as st
from gtts import gTTS
import io
import anthropic

api_key = st.secrets['anthropic_api_key']

# Initialize Anthropics client
client = anthropic.Anthropic(api_key=api_key)

# Function to generate a response using LLM
def generate_dream_theory(dream_text):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=600,
        temperature=0,
        system="""You are an expert in dream analysis and cultural references,
                    Your task is to provide a detailed analysis and cultural theory based on the user's dream description. 

                1. Start with a brief summary of the dream's main elements.
                2. Analyze the dream's specific elements and their possible meanings.
                3. Include relevant cultural or psychological theories related to the dream.
                4. Ensure your response is clear, empathetic, and sensitive to personal or emotional content.
                5. Make the output concise and to the point that are points to be discussed will include in it.
                6. Summarize the key points and offer a concise conclusion.
                """,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": dream_text
                    }
                ]
            }
        ]
    )
    ans = message.content[0].text
    return ans 

# Function to handle text-to-speech using gTTS
def text_to_speech(text):
    tts = gTTS(text, lang='en')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp

# Main app
def main():
    # Custom CSS for background and styling
    st.markdown("""
    <style>
    body {
        background-color: #f0f8ff; /* Alice blue background for a soft look */
        color: #333333; /* Dark grey text for readability */
    }
    .stApp {
        background-color: #f0f8ff; /* Consistent Alice blue for the main app container */
    }
    .stSidebar .stText {
        color: #ffffff; /* White text color in the sidebar for the "About This App" section */
    }
    .stTextInput textarea {
        background-color: #ffffff; /* White background for the text area */
        border: 2px solid #1e90ff; /* Dodger blue border for high visibility */
        color: #1e90ff; /* Dodger blue text color inside the text area */
        box-shadow: 0 0 10px rgba(30, 144, 255, 0.5); /* Glowing blue shadow to enhance visibility */
    }
    .stTextInput textarea:focus {
        border: 2px solid #4169e1; /* Royal blue border when focused */
        box-shadow: 0 0 15px rgba(65, 105, 225, 0.8); /* Stronger blue shadow when focused */
    }
    .stButton>button {
        background-color: #1e90ff; /* Dodger blue button background color */
        color: white; /* Button text color */
        border-radius: 12px; /* Rounded corners for buttons */
        padding: 10px 20px; /* Add some padding to the buttons */
        font-size: 16px; /* Increase font size */
    }
    .stButton>button:hover {
        background-color: #4169e1; /* Royal blue button background color on hover */
    }
    h1, h2, h3 {
        color: #1e90ff; /* Dodger blue color for headers */
    }
    .stAudio {
        text-align: right; /* Align audio player to the right */
    }
    /* Specific style for output text */
    .stMarkdown p, .stMarkdown span {
        color: #000000 !important; /* Ensure all output text is black */
    }
    </style>
    """, unsafe_allow_html=True)


    # Sidebar with app description
    st.sidebar.header("About This App")
    st.sidebar.write(
        """
        **Dream Chronicles** is an application that analyzes your dreams and provides insights based on dream analysis and cultural theories.

        **How to Use:**
        1. Describe your dream in the text area.
        2. Click 'Generate' to get an analysis and hear it in audio format.
        """
    )
    
    # Main content
    st.title("Dream Chronicles🌀")

    # Input text area for dream description
    dream_input = st.text_area("Tell Me About Your Dream:", height=150)

    if st.button('Generate'):
        if dream_input:
            # Get theory and cultural reference from LLM
            theory_response = generate_dream_theory(dream_input)
            st.write("Dream Analysis:", theory_response)
            
            # Option to hear the dream analysis
            audio_fp = text_to_speech(theory_response)
            st.audio(audio_fp, format='audio/mp3')

if __name__ == "__main__":
    main()
