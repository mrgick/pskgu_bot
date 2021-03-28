from parser_module import parser
from utils.log import logger
import io
import json
import time
import asyncio
import os

def main():
    t0 = time.time()
    logger.info("Start parser")
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(parser.run_parser())
    event_loop.close()    
    logger.info("Parser has been finished. %f seconds elapsed." % (time.time() - t0))
    
    #from parser_module.db import data_base_dict
    if not os.path.exists("logs"):
        os.mkdir("logs")
    with io.open("logs/page.txt", "w") as f:
        f.write(json.dumps(parser.data_base_dict, indent=2, ensure_ascii=False))
    #print(len(parser.data_base_dict))

if __name__=="__main__":
    main()
