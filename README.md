# ASL-Interpreter

steps needed:

Creating the Virtual Environment: Users can recreate the environment using:
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt

if libraries are not correctly installed used:
install libraries:
pip install tensorflow opencv-python numpy pandas matplotlib scikit-learn install yt-dlp

Make sure ffmpeg is installed and available in your system's PATH.
On macOS, you can install it using Homebrew:
brew install ffmpeg
On Windows, you can download it from ffmpeg.org and follow the installation instructions.

get youtube cookies using cookies.txt extension on chrome

.gitigore:
Ignore cookie files
/data/www.youtube.com_cookies
/data/www.youtube.com_cookies.txt


Ignore virtual environment folder
venv/

Ignore videos folder
/videos/

Ignore model folder
/models/

Ignore data files
*.npy
