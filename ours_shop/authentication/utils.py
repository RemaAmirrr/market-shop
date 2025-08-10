
# import ghasedakpack
from django.contrib import messages
from django.shortcuts import redirect
GHASEDAK_API_KEY = "" # this code gasedaksite will give you when you rigester in gasedak site

def send_sms( to, body):
            sms = ghasedakpack.Ghasedak(GHASEDAK_API_KEY)
            good_line_number_for_sending_otp = '30005088'
            template_name_in_ghasedak_me_site = "markt_shop"
            answer = sms.verification({'receptor' : to, 'linenumber' : good_line_number_for_sending_otp, 'type' : '1', 'template': template_name_in_ghasedak_me_site,'param1' : body})
            if answer:
                return answer
            else:
               pass
            return redirect("phone_verification")  
    