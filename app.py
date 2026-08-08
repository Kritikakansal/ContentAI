import os

from dotenv import load_dotenv
from google import genai
import streamlit as st


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ContentAI",
    page_icon="✨",
    layout="centered"
)


# ==========================================
# CUSTOM UI
# ==========================================

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

h1 {
    font-size: 3rem !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-weight: 600;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 0.7rem 1rem;
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCTION TO DISPLAY OUTPUT
# ==========================================

def display_output(content, download_name):

    st.divider()

    st.subheader("✨ Your Generated Content")

    with st.container(border=True):

        # Generated content
        # Streamlit provides a native copy button here
        st.code(
            content,
            language=None,
            wrap_lines=True
        )

        st.divider()

        # Statistics
        character_count = len(content)
        word_count = len(content.split())

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Characters",
                character_count
            )

        with col2:
            st.metric(
                "Words",
                word_count
            )

        # Download
        st.download_button(
            label="⬇️ Download Content",
            data=content,
            file_name=download_name,
            mime="text/plain"
        )


# ==========================================
# HEADER
# ==========================================

st.title("✨ ContentAI")

st.markdown(
    "### Create better content, faster."
)

st.write(
    "Generate or improve platform-ready content tailored "
    "to your audience, tone and style."
)

st.divider()


# ==========================================
# MODE SELECTION
# ==========================================

mode = st.radio(
    "What would you like to do?",
    [
        "Create New Content",
        "Improve Existing Content"
    ],
    horizontal=True
)


# =========================================================
# CREATE NEW CONTENT
# =========================================================

if mode == "Create New Content":

    # Content type
    content_type = st.selectbox(
        "What do you want to create?",
        [
            "LinkedIn Post",
            "Instagram Caption",
            "Professional Email",
            "Blog Outline"
        ]
    )

    # Topic
    topic = st.text_area(
        "What is your topic?",
        placeholder="Example: AI tools for college students"
    )

    # Audience
    audience = st.text_input(
        "Target audience",
        placeholder="Example: College students"
    )

    # Tone and length
    col1, col2 = st.columns(2)

    with col1:
        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Casual",
                "Friendly",
                "Persuasive"
            ]
        )

    with col2:
        length = st.selectbox(
            "Length",
            [
                "Short",
                "Medium",
                "Long"
            ]
        )

    # Language and emoji
    col3, col4 = st.columns(2)

    with col3:
        language = st.selectbox(
            "Language",
            [
                "English",
                "Hindi",
                "Hinglish"
            ]
        )

    with col4:
        emoji_style = st.selectbox(
            "Emoji style",
            [
                "None",
                "Minimal",
                "Moderate"
            ]
        )


    # ==========================================
    # GENERATE CONTENT
    # ==========================================

    if st.button("✨ Generate Content"):

        if not topic.strip():

            st.warning("Please enter a topic first.")

        else:

            prompt = f"""
You are an expert digital content writer.

Create high-quality content based on the user's requirements.

CONTENT TYPE:
{content_type}

TOPIC:
{topic}

TARGET AUDIENCE:
{audience}

TONE:
{tone}

LENGTH:
{length}

LANGUAGE:
{language}

EMOJI STYLE:
{emoji_style}


PLATFORM-SPECIFIC REQUIREMENTS:

If the content type is LinkedIn Post:

- Start with a strong and relevant hook.
- Use short, readable paragraphs.
- Provide useful insights or takeaways.
- Keep the writing professional but human.
- Avoid sounding robotic or overly promotional.
- End with an appropriate call to action.
- Use emojis only according to the selected emoji style.


If the content type is Instagram Caption:

- Start with an engaging opening.
- Keep the writing concise and conversational.
- Make it suitable for Instagram users.
- Use emojis according to the selected emoji style.
- End with a suitable call to action.
- Add relevant hashtags.


If the content type is Professional Email:

- Include a clear subject line.
- Use an appropriate greeting.
- Clearly explain the purpose of the email.
- Keep the message professional and concise.
- Include a clear call to action when appropriate.
- End with a professional closing.


If the content type is Blog Outline:

- Create a clear and engaging title.
- Organize the content using logical headings.
- Include useful subheadings.
- Add the key points that should be discussed under each section.
- Keep the structure easy to follow.


GENERAL REQUIREMENTS:

- Follow the selected tone.
- Follow the selected length.
- Follow the selected language.
- Follow the selected emoji style.
- Make the content useful and specific to the topic.
- Avoid unnecessary repetition.
- Do not invent personal experiences.
- Do not make unsupported claims.
- Do not explain how the content was generated.
- Return only the requested content.
"""

            # Gemini
            with st.spinner("Creating your content..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )

                    generated_content = response.text

                except Exception as e:

                    st.error(
                        "Something went wrong while generating the content."
                    )

                    st.exception(e)
                    st.stop()

            display_output(
                generated_content,
                "generated_content.txt"
            )


# =========================================================
# IMPROVE EXISTING CONTENT
# =========================================================

else:

    st.subheader("Improve Your Content")

    st.write(
        "Paste your existing content and let AI rewrite it "
        "to make it clearer, stronger and more effective."
    )

    # Existing content
    existing_content = st.text_area(
        "Paste your content here",
        height=220,
        placeholder="Paste the content you want to improve..."
    )

    # Improvement type
    improvement = st.selectbox(
        "What would you like to improve?",
        [
            "Make it more professional",
            "Make it more engaging",
            "Make it more concise",
            "Improve grammar and clarity",
            "Make it suitable for LinkedIn",
            "Make it suitable for Instagram",
            "Make it suitable for an email"
        ]
    )

    # Tone
    improve_tone = st.selectbox(
        "Preferred tone",
        [
            "Professional",
            "Casual",
            "Friendly",
            "Persuasive"
        ]
    )


    # ==========================================
    # IMPROVE CONTENT
    # ==========================================

    if st.button("✨ Improve Content"):

        if not existing_content.strip():

            st.warning("Please paste some content first.")

        else:

            improve_prompt = f"""
You are an expert content editor.

Improve the following content.

ORIGINAL CONTENT:
{existing_content}

IMPROVEMENT GOAL:
{improvement}

PREFERRED TONE:
{improve_tone}


REQUIREMENTS:

- Preserve the original meaning.
- Improve clarity and readability.
- Remove unnecessary repetition.
- Correct grammar and awkward wording.
- Make the content natural and human.
- Do not add information that was not present in the original content.
- Follow the selected improvement goal.
- Return only the improved content.
"""

            # Gemini
            with st.spinner("Improving your content..."):

                try:

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=improve_prompt
                    )

                    improved_content = response.text

                except Exception as e:

                    st.error(
                        "Something went wrong while improving the content."
                    )

                    st.exception(e)
                    st.stop()

            display_output(
                improved_content,
                "improved_content.txt"
            )