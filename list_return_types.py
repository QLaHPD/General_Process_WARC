from warcio.archiveiterator import ArchiveIterator

def print_content_types(warc_file_path):
    content_types = set()

    with open(warc_file_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                content_type = record.http_headers.get_header('Content-Type')
                if content_type:
                    content_types.add(content_type)
                    print(content_types)

    for content_type in content_types:
        print(content_type)

# Replace with your WARC file path
warc_file_path = "/home/visilionosh/Downloads/archiveteam_orkut_20160929211144/orkut_20160929211144.megawarc.warc"
print_content_types(warc_file_path)
