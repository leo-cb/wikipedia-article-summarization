import streamlit as st
from summarize_t5 import TextSummarization
from summarize_wikipedia import get_wikipedia_text
from urllib.parse import urlparse

# set page title
st.set_page_config(page_title="Wikipedia Summarizer")

@st.cache_resource
def load_summarizer():
    return TextSummarization()

# initialize text summarizer
summarizer = load_summarizer()

# create form
with st.form(key='summarize_form'):
    url = st.text_input('Enter the URL of the Wikipedia page')
    limit = st.number_input('Enter the character limit', value=1000, min_value=500)
    submit_button = st.form_submit_button(label='Summarize')

# when the form is submitted
if submit_button:
    # validate if url is from wikipedia.org
    parsed_url = urlparse(url)
    if 'wikipedia.org' not in parsed_url.netloc:
        st.write('Please enter a valid Wikipedia URL.')
    else:
        # get text from wikipedia
        text = get_wikipedia_text(url)
        
        # apply character limit
        if limit is not None:
            text = text[:limit]

        # generate summary
        summary = summarizer.summarize_text_t5(text)

        # display summary
        st.write(summary)