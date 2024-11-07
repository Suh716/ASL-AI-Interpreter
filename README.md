# ASL-Interpreter

steps needed 

Create a virtual environment in your project folder:
pip install virtualenv

Create a virtual environment in your project folder:
virtualenv venv

Activate the virtual environment:
On Windows: venv\Scripts\activate
On macOS/Linux: source venv/bin/activate

Make sure ffmpeg is installed and available in your system's PATH.
On macOS, you can install it using Homebrew:
brew install ffmpeg
On Windows, you can download it from ffmpeg.org and follow the installation instructions.

install libraries:
pip install tensorflow opencv-python numpy pandas matplotlib scikit-learn install yt-dlp

get youtube cookies using cookies.txt extension on chrome

.gitigore:
# Ignore cookie files
/data/www.youtube.com_cookies
/data/www.youtube.com_cookies.txt


# Ignore virtual environment folder
venv/

# Ignore videos folder

# Ignore data and model files 
*.npy
/models/*.h5
/models/*.keras