from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()



api_key = os.getenv("OPEN_AI_TOKEN")

print(api_key)



