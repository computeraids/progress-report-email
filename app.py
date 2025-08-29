import streamlit as st
from frontend_utils import run_button, week_number_input
import funcs

st.title("Progress Report Emailer")
tool_tab, config_tab = st.tabs(["Tools", "Config"])

with tool_tab:
    st.header("API Scraper")
    st.write("This will scrape the assignments from Canvas using the API and save them to the userdata folder.")
    run_button(funcs.api_scrape, 
            key="api_scrape", 
            success_message="Scrape completed", 
            error_message="Scrape failed")

    st.header("Canvas API")
    st.write("This will scrape the assignments from Canvas using the API and save them to the userdata folder.")
    week_for_api = week_number_input("api_week_input")
    run_button(funcs.canvas_api, 
            key="canvas_api", 
            success_message="Scrape completed", 
            error_message="Scrape failed", 
            func_arg=week_for_api)

    st.header("Validation")
    st.write("This will check the consistency of the data in the userdata folder.")
    run_button(
        funcs.check, 
        key="check", 
        success_message="Check finished. See output below", 
        error_message="Check failed"
    )

    st.header("Make Emails")
    st.write("This will make the emails for the assignments.")
    week_for_emails = week_number_input("email_week_input")
    run_button(funcs.make_emails, 
            key="make_emails", 
            success_message="Emails made", 
            error_message="Emails failed", 
            func_arg=week_for_emails
        )


with config_tab:
    st.header("Setup User Config")
    st.write("Creates local user configuration files")
    config_files = st.multiselect('Choose files to create', options=["assignments","modules","api", "config"])

    run_button(
        funcs.setup_data,
        key='run_setup_data',
        success_message="Successfully created user config",
        error_message="Error during user config creation",
        func_arg=config_files
    )