import streamlit as st

def load_css():

    st.markdown(
        """
        <style>

        /* Main App */

        .main{
            padding-top:1rem;
        }

        /* Title */

        h1{
            color:#0E6FFF;
            font-weight:700;
        }

        /* Metric Cards */

        div[data-testid="metric-container"]{
            background-color:#FFFFFF;
            border-radius:15px;
            padding:15px;
            border:1px solid #E6E6E6;
            box-shadow:0px 2px 8px rgba(0,0,0,0.08);
        }

        /* Buttons */

        .stButton>button{
            border-radius:10px;
            width:100%;
            height:3em;
            font-weight:bold;
        }

        /* Download Button */

        .stDownloadButton>button{
            border-radius:10px;
            width:100%;
        }

        
        </style>
        """,
        unsafe_allow_html=True
    )