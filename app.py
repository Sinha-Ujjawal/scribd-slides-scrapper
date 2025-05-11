import subprocess
import tempfile
import os
import logging
import sys
import streamlit as st

def render_errors():
    errors = st.session_state.get("errors")
    if not errors: return
    for err_msg in errors:
        st.error(err_msg)
    st.session_state.errors = []

def st_error(*err_msgs):
    if "errors" not in st.session_state:
        st.session_state.errors = []
    for err_msg in err_msgs:
        st.session_state.errors.append(err_msg)

def download_pptx(slideshare_url, scale):
    try:
        data = None
        with tempfile.NamedTemporaryFile(suffix=".pptx") as tmpfile:
            output_path = tmpfile.name
            script_path = './download_slides_as_pptx.sh'

            process = subprocess.Popen(
                ["sh", script_path, slideshare_url, output_path, str(scale)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env={
                    "PYTHON_EXEC": sys.executable,
                },
            )

            logs = []
            with st.expander("See Logs"):
                for line in process.stdout:
                    line = line.rstrip()
                    if not line:
                        continue
                    logs.append(line)
                    st.text(line)

            process.wait()
            if process.returncode != 0:
                st_error("Logs from cli:\n" + "\n".join(logs))
                return None, False
            with open(output_path, "rb") as f:
                data = f.read()
        return data, True
    except Exception as e:
        st_error(f"An error occurred: {e}")
        return None, False

def main():
    st.title("SlideShare to PPTX Converter")

    # Initialize session state variables
    if "processing" not in st.session_state:
        st.session_state.processing = False

    def disable_form():
        st.session_state.processing = True

    def end_processing():
        st.session_state.processing = False

    # Create a form to group the inputs and button
    with st.form(key="slideshare_form"):
        slideshare_url = st.text_input("Enter SlideShare URL:", key="slideshare_url")
        file_name = st.text_input("Enter desired file name (without extension):", "slideshare_presentation", key="file_name")
        scale = st.number_input("Enter scale for slides (e.g., 1, 1.5, 2, ...)", min_value=0.1, value=0.33, step=0.05, key="scale")

        # Submit button inside the form
        submit_button = st.form_submit_button(label="Download as PPTX", on_click=disable_form,
                                              disabled=st.session_state.get("processing", False))

    render_errors()

    # Display processing indicator
    if st.session_state.processing:
        if not slideshare_url:
            st_error("Please enter a SlideShare URL.")
            st.session_state.processing = False
            st.rerun()
            return
        if not file_name:
            st_error("Please enter a file name.")
            st.session_state.processing = False
            st.rerun()
            return
        with st.spinner("Processing..."):
            data, success = download_pptx(slideshare_url, scale)
        if success:
            st.success("PPTX generated successfully!")
            # Provide download button
            st.download_button(
                label="Download PPTX",
                data=data,
                key="download_file",
                on_click=end_processing,
                file_name=file_name + ".pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            st.session_state.processing = False
            st.rerun()
            return

if __name__ == "__main__":
    main()
