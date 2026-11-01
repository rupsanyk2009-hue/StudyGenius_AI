STUDYGENIUS AI — QUICK START (WINDOWS)

1. Install Python from https://www.python.org/downloads/
   During installation, tick "Add python.exe to PATH".
2. Open Command Prompt in this folder.
3. Run:
   py -m pip install -r requirements.txt
4. Start the app:
   py -m streamlit run app.py
5. It opens in your laptop browser.

TO SHOW IT ON YOUR IPAD PRO:
1. Connect the Dell laptop and iPad to the same trusted Wi-Fi.
2. In Command Prompt, stop the app with Ctrl+C.
3. Run:
   py -m streamlit run app.py --server.address 0.0.0.0
4. Run ipconfig in a second Command Prompt and find the IPv4 Address
   under the Wi-Fi adapter (often starts with 192.168).
5. On iPad Safari, open:
   http://YOUR-IPV4-ADDRESS:8501
   Replace YOUR-IPV4-ADDRESS with the number you found.
6. If Windows asks, allow Python on Private networks only.
   Do not turn off Windows Firewall or expose the app to public networks.

IMPORTANT:
This is a functional educational prototype. Notes generation and Study Assistant
use simple programmed logic, and the quiz uses built-in questions. It is not
connected to a generative AI model yet. Be transparent about this in your
exhibition presentation.
