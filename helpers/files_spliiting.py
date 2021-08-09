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

async def split__video_files(download_directory, splitting_size, splitted_files_directory, fname):
    metadata = extractMetadata(createParser(download_directory))
    if metadata.has("duration"):
        total_duration = metadata.get('duration').seconds

    metadata = metadata.exportDictionary()
    try:
        mime = metadata.get("Common").get("MIME type")
    except:
        mime = metadata.get("Metadata").get("MIME type")
    
    

    ftype = mime.split("/")[0]
    ftype = ftype.lower().strip()

    split_dir = os.path.join(os.path.dirname(path),str(time()))

    if not os.path.isdir(split_dir):
        os.makedirs(split_dir)
    
    if ftype == "video" and not force_docs:
        total_file_size = os.path.getsize(download_directory)
        
        parts = math.ceil(total_file_size/splitting_size)
        #need this to be implemented to remove recursive file split calls
        #remove saftey margin
        #parts += 1
        torlog.info(f"Parts {parts}")

        minimum_duration = (total_duration / parts) 
        
        #casting to int cuz float Time Stamp can cause errors
        minimum_duration = int(minimum_duration)
        logger..info(f"Min dur :- {minimum_duration} total {total_duration}")

        # END: proprietary
        start_time = 0
        end_time = minimum_duration


        base_name = fname
        input_extension = base_name.split(".")[-1]
        
        i = 0
        flag = False
        
        while end_time <= total_duration:

            #file name generate
            parted_file_name = "{}_PART_{}.{}".format(str(base_name),str(i).zfill(5),str(input_extension))

            output_file = os.path.join(splitted_files_directory, parted_file_name)
            
            opfile = await cult_small_video(
                download_directory,
                output_file,
                str(start_time),
                str(end_time)
            )
            torlog.info(f"Output file {opfile}")
            torlog.info(f"Start time {start_time}, End time {end_time}, Itr {i}")

            #adding offset of 3 seconds to ensure smooth playback 
            start_time = end_time - 3
            end_time = end_time + minimum_duration
            i = i + 1

            if (end_time > total_duration) and not flag:
                 end_time = total_duration
                 flag = True
            elif i+1 == parts:
                end_time = total_duration
                flag = True
            elif flag:
                break

    return split_dir
