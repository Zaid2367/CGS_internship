<<<<<<< HEAD
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
=======
import os

data = "data"
output = "output"
figures = os.path.join(output, "figures")

gradesf = os.path.join(data, "grades.csv")
attendancef = os.path.join(data, "attendance.csv")
demof = os.path.join(data, "demographics.csv")
>>>>>>> 6d2fa163a856b789b0147b16b4fd1a3adad24610
