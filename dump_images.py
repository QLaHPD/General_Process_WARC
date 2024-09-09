from warcio.archiveiterator import ArchiveIterator
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import os

output_dir = '/media/ramdisk/test_output'
os.makedirs(output_dir, exist_ok=True)

def is_image(content_type):
    return content_type in ['image/jpeg', 'image/png']

mimetypes = {}

with open("/home/visilionosh/Downloads/archiveteam_orkut_20160929211144/archiveteam_orkut_20160929211144.cdx", "r") as cdx:
    for line in cdx:
        parts = line.split(" ")
        mime_type = parts[3]
        if mime_type in mimetypes:
            mimetypes[mime_type] += 1
        else:
            mimetypes[mime_type] = 1
    del mimetypes['b']

total_image_count = mimetypes['image/png'] + mimetypes['image/jpeg'] + mimetypes['image/gif']
print(f"Total number of images: {total_image_count}")
print(mimetypes)

print(f"Total number of images: {mimetypes['image/png'] + mimetypes['image/jpeg'] + mimetypes['image/gif']}")

with open("/home/visilionosh/Downloads/archiveteam_orkut_20160929211144/orkut_20160929211144.megawarc.warc", "rb") as stream:
    with tqdm(total=total_image_count, desc="Saving images") as pbar:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                content_type = record.http_headers.get_header('Content-Type')
                if is_image(content_type):
                    image_data = record.content_stream().read()
                    image = Image.open(BytesIO(image_data))
                    uri = record.rec_headers.get_header('WARC-Target-URI')
                    image_name = os.path.join(output_dir, os.path.basename(uri))
                    image.save(fp=image_name, format='png')
                    pbar.update(1)
