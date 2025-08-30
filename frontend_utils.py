import streamlit as st
import io
import contextlib

def run_button(func, key, success_message, error_message, func_arg = None):
    if st.button("Run", width="stretch", key=key):
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                if func_arg is not None:
                    func(func_arg)
                else:
                    func()
            st.success(success_message)
        except Exception as e:
            st.error(f"{error_message}: {e}")
        if buf.getvalue().strip() != "":
            st.code(buf.getvalue(), language="text")


def week_number_input(key):
    return st.number_input(
        "Enter Week/Module number to retrieve (e.g. 2.1)",  
        key=key,
        min_value=0.0, 
        step=0.1,
        format="%0.1f"
    )
