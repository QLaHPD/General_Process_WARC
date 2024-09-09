from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup
import re


def print_matching_community_content(warc_file_path, target_description_texts):
    """
    Prints the content of responses from a WARC file where:
      - The response status code is 200.
      - The content type is not an image or CSS.
      - The community description div contains any of the target texts.
    """

    for record in ArchiveIterator(open(warc_file_path, "rb")):
        if record.rec_type == 'response':
            mime_type = record.http_headers.get_header('Content-Type')
            status_code = record.http_headers.get_statuscode()

            if status_code == '200' and (mime_type not in ['image/jpeg', 'image/png', 'image/gif', 'text/css']):
                uri = record.rec_headers.get_header('WARC-Target-URI')
                content = record.content_stream().read().decode('utf-8', errors='ignore')

                soup = BeautifulSoup(content, 'html.parser')

                community_description_div = soup.find('div', class_='communityProfileSection communityProfileHeader')

                if community_description_div:
                    description_text = community_description_div.text
                    for target_text in target_description_texts:
                        if re.search(target_text, description_text, re.IGNORECASE):
                            print(f"URI: {uri}")
                            print(content)
                            print("\n" + "-" * 80 + "\n")
                            break # Move to next record after a match


# Example usage:
warc_file_path = "/home/visilionosh/Downloads/archiveteam_orkut_20160929211144/orkut_20160929211144.megawarc.warc.gz"
target_description_texts = [r"(^|\b)Fake News(\b|$)", r"(^|\b)Noticia Falsa(\b|$)", r"(^|\b)é mentira(\b|$)", r"(^|\b)e mentira(\b|$)"]
print_matching_community_content(warc_file_path, target_description_texts)
