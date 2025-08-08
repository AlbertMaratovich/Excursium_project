from dotenv import load_dotenv
import os

base_url = "https://excursium.com/"
login_url = "https://excursium.com/Client/Login"
account_url = "https://excursium.com/Account/Startup"
all_excursion_url = "https://excursium.com/ekskursii-dlya-shkolnikov/list"
feedback_url = "https://excursium.com/About/Contact#from-feedback"

load_dotenv()

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
