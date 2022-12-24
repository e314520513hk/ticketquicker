from twocaptcha import TwoCaptcha
import os
import sys
solver = TwoCaptcha(os.getenv("ANSON_APIKEY_2CAPTCHA"))
try:
    print("trying")
    result = solver.normal('captcha.png')
except Exception as e:
    sys.exit(e)

sys.exit('solved: ' + str(result))
