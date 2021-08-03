import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os

from fsplit.filesplit import Filesplit

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

def split_files(download_directory, splitting_size, splitted_files_directory):
    try:
        fs = Filesplit()
        fs.split(
            file=download_directory,
            split_size=splitting_size,
            output_dir=splitted_files_directory,
        )
    except:
        pass
