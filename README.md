# YTD
YouTube Video Downloader For Linux. [FULL GUI SUPPORT] Download YouTube video for free, easily.

For Linux,
step 1: Open terminal and paste this:
```bash
sudo apt update && sudo apt upgrade -y
```
step 2: after update, paste this full code [Important]
```bash
sudo apt install python3 python3-pip -y
pip3 install yt-dlp
sudo apt install python3-tk -y
sudo apt install ffmpeg -y
sudo apt install xdg-utils -y
sudo apt install python3-psutil -y
```
step 3: after install all requirements, download the YTD.py and copy to documents folder.
```bash
cd ~/Documents
wget https://github.com/manir-devs/YTD/raw/main/YTD.py
wget https://github.com/manir-devs/YTD/raw/main/icon.png
chmod +x ~/Documents/YTD.py

```
step 4: Create desktop entry by typing this command..
```bash
nano ~/.local/share/applications/ytd.desktop
```
Then paste this full code, replace <YOUR USERNAME> with your username
```bash
[Desktop Entry]
Name=YT Downloader Linux Edition 😎
Exec=python3 /home/<YOUR USERNAME>/Documents/YTD.py
Icon=/home/<YOUR USERNAME>/Documents/icon.png
Type=Application
Terminal=false
Categories=Utility;
```
then, paste this code to copy desktop icon to desktop
```bash
cp ~/.local/share/applications/ytd.desktop ~/Desktop/
chmod +x ~/Desktop/ytd.desktop
gio set ~/Desktop/ytd.desktop metadata::trusted true
```
Done! enjoy
