import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import streamlit as st
from io import BytesIO
import zipfile

def download_images(url, folder_path='downloaded_images'):
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        # Create a BytesIO object to store images in memory
        zip_data = BytesIO()
        with zipfile.ZipFile(zip_data, 'w') as zip_file:
            for img_tag in img_tags:
                img_url = img_tag.get('src')
                img_url = urljoin(url, img_url)
                img_name = os.path.basename(urlparse(img_url).path)
                img_data = requests.get(img_url).content
                img_path = os.path.join(folder_path, img_name)

                # Save the image to the ZIP file
                zip_file.writestr(img_name, img_data)

        # Seek to the beginning of the BytesIO object
        zip_data.seek(0)

        # Provide the ZIP file for the user to download
        st.write(f'Downloading ZIP file...')
        st.download_button(
            label='Download Images',
            data=zip_data,
            file_name='downloaded_images.zip',
            key='download_button'
        )
    else:
        st.error(f'Error: Unable to fetch content from {url}')

# Streamlit app
st.title("Website Image Downloader")
website_url = st.text_input("Enter the website URL:")
if st.button("Download Images"):
    st.info("Downloading images...")
    download_images(website_url)
