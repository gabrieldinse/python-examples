# Author: gabri
# File: download_imagens
# Date: 16/09/2019
# Made with PyCharm

# Standard Library

# Third party modules
from google_images_download import google_images_download

# Local application imports


def main():
    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": "automovel", "limit": 500,
                 "print_urls": True, 'format': 'jpg'}

    paths = response.download(
        arguments)
    print(paths)


if __name__ == "__main__":
    main()
