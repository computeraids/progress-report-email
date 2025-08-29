import streamlit as st
import funcs

st.title("Progress Report Emailer")


tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

with tab1:
    # Example: add two numbers
    a = st.number_input("Enter first number", value=0)
    b = st.number_input("Enter second number", value=0)

    if st.button("Add Numbers"):
        result = a+b
        st.success(f"Result: {result}")

# Example: greet someone
name = st.text_input("Enter your name")
if st.button("Say Hello"):
    greeting = f'Hello {name}!'
    st.write(greeting)