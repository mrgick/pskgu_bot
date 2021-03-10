#for programming; create.env file with TOKEN_VK, GROUP_ID, MONGO_URL
import os
from dotenv import load_dotenv
path_to_env_file=os.path.dirname(__file__)[0:os.path.dirname(__file__).rfind("/")]
dotenv_path = os.path.join(path_to_env_file, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)