import streamlit as st
from PIL import Image
import pytesseract
from io import BytesIO
import zipfile

# Set up Tesseract path (replace with your Tesseract path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image):
    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(image)
    return text

def create_zip_file(text_latex, text_html):
    # Create a zip file containing LaTeX and HTML files
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr("text_latex.txt", text_latex)
        zip_file.writestr("text_html.html", text_html)
    return zip_buffer

def main():
    st.title("Image Text Analyzer")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze and Download"):
            # Extract text from the image
            text = extract_text(image)

            # Display the extracted text
            st.subheader("Extracted Text:")
            st.write(text)

            # Convert text to LaTeX and HTML
            text_latex = f"\\documentclass{{article}}\n\\begin{{document}}\n{text}\n\\end{{document}}"
            text_html = f"<html><body><p>{text}</p></body></html>"

            # Create a zip file
            zip_buffer = create_zip_file(text_latex, text_html)

            # Download the zip file
            st.download_button(
                label="Download Text",
                data=zip_buffer.getvalue(),
                file_name="extracted_text.zip",
                key="download_button",
            )

if __name__ == "__main__":
    main()
