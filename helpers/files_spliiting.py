import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import asyncio
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import math

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

    try:
        total_file_size = os.path.getsize(download_directory)
        
        parts = math.ceil(total_file_size/splitting_size)
        #need this to be implemented to remove recursive file split calls
        #remove saftey margin
        #parts += 1
        logger.info(f"Parts {parts}")

        minimum_duration = (total_duration / parts) 
        
        #casting to int cuz float Time Stamp can cause errors
        minimum_duration = int(minimum_duration)
        logger.info(f"Min dur :- {minimum_duration} total {total_duration}")

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

        return splitted_files_directory
    except Exception as e:
        logger.info(e)
        pass

      
async def cult_small_video(download_directory, out_put_file_name, start_time, end_time):
    file_genertor_command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        download_directory,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        "-c",
        "copy",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=aio.subprocess.PIPE,
        stderr=aio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return out_put_file_name
