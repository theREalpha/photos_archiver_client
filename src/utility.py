import os
import requests
from multiprocessing.pool import ThreadPool

from src.objects import MediaItem
from src.logger import logger, modDEBUG
from config import PATH, THREADING

def dup_name(name: str)->str:
    '''
    Generates a new name for a file by appending an incremental number if the file already exists.

    Args:
        name (str): The original name of the file.

    Returns:
        str: A new name with an incremental number appended to it if necessary to avoid filename conflicts.
    '''
    if not os.path.isfile(name):
        return name
    i=1
    ext=name.rfind('.')
    newName=name[:ext]+"_"+str(i)+name[ext:]
    while os.path.isfile(newName):
        i+=1
        newName= name[:-4]+"_"+str(i)+name[-4:]
    return newName

def media_down(media: MediaItem)->int:
    '''
    Downloads the media content specified by checking for naming conflicts and preparing download url.

    Args:
        media (MediaItem): The MediaItem object representing the media to be downloaded.

    Returns:
        statusCode (int): returns the statusCode of request if Failed, else 0
    '''
    mediaURL= media.baseUrl
    path= dup_name(PATH+media.filename)
    mediaURL = media.downloadURL
    try:
        response = requests.get(mediaURL, stream=True)
    except Exception as e:
        logger.error(f"Unknown error while processing request for id {media.id}. Exception:\n{e}")
        return -1
    logger.log(modDEBUG,f"Downloading Media Item: {media.filename}, size: {int(response.headers.get('Content-Length',0))/(1024):.3f} KB")
    if not response.ok:
        logger.error(f"failed download for media {media.filename}\nid: {media.id} ")
        logger.error(f"with response {response}")
        return response.status_code
    handle= open(str(path), 'wb')
    for block in response.iter_content(1024):
        if not block:
            handle.close()
            break
        handle.write(block)
    return 0

def downloader(items: list, threading: bool=THREADING, threadCount: int= os.cpu_count()+4, batching: bool=False) -> dict:
    '''
    Downloads media items from the provided list through media_down.

    Args:
        items (list): A list of media items to be downloaded.
        threading (bool, optional): Set to True to use multi-threading, False to use a single thread. Default: True.
        threadCount (int, optional): The number of threads to use when multi-threading is enabled. Default: No. of CPU cores + 4.
        batching (bool, optional): ToDo: add download through batching. Default is False.

    Returns:
        dict: A dictionary containing the following key-value pairs:
              - 'count' (int): The number of media items successfully downloaded.
              - 'failed' (List[MediaItem]): A list of media items which failed.
    '''

    os.makedirs(PATH, exist_ok=True)
    failed=[]
    if not threading:
        for media in items:
            if media_down(media):
                failed.append(media)

    else:
        with ThreadPool(threadCount) as pool:
            logger.log(modDEBUG,f"No.of threads running: {threadCount-4}")
            statusCodes=pool.map(media_down, items)

            for idx,code in enumerate(statusCodes):
                if code:
                    failed.append((items[idx],code))

    total,fail=len(items),len(failed)
    logger.info(f"""
            Total:  \t{total}
            Success:\t{total-fail}
            Failed: \t{fail}""")

    return {'count':total-fail,
            'failed': failed}