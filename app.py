from langchain_openai import ChatOpenAI
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from prod_review_schema import ProdReview

load_dotenv()

model = ChatOpenAI()
# create model with predefined schema output
structured_model = model.with_structured_output(ProdReview)

# create ui components
st.header('Product Review - AI Analysis')
# type review here
custom_css = """
<style>
.stTextArea [data-baseweb=base-input] {
    background-color: #f0f2f6; /* Light gray background */
    border: 2px solid #4CAF50; /* Green border */
    border-radius: 5px;
    font-family: 'Arial', sans-serif;
    font-size:12
    color: #333;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-size: cover;
}
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

#initialize session state for text input
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
# Display the text area, linked to session state
review = st.text_area(label='Enter product review',
                      max_chars=12000,
                      height='content',
                      placeholder='Start typing..',
                      key="input_text", value=st.session_state.input_text)

if st.button('Click to analyze'):
    if review:
        # invoke model for structured result
        result = structured_model.invoke(review)
        # convert result into tabular format
        df = pd.DataFrame(result,columns=["Query","AI analysis"])
        
        # apply styling to highlight sentiment
        def highlight_sentiment(value):
            if value == 'POSITIVE':
                return 'background-color:lightgreen'
            elif value == 'NEGATIVE':
                return 'background-color:lightcoral'
            elif value == 'NEUTRAL':
                return 'background-color:lightyellow'
        
        # apply style
        df = df.style.map(highlight_sentiment,subset=['AI analysis'])
        
        # display table     
        st.dataframe(df,
                     hide_index=True,
                     column_config={'Query':st.column_config.TextColumn(width='small'),
                                    'AI analysis':st.column_config.TextColumn(width="large")
                     }
                     )
    else:
        st.write("Type a review to start analysis")

# Callback function to clear the text area
def clear_text_area():
    st.session_state.input_text = ""
# clear text area on button click
st.button('Clear',on_click=clear_text_area)



