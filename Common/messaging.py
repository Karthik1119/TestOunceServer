import requests
from django.conf import settings
from django.core.mail import send_mail
from pyfcm import FCMNotification
import json

"""
        CONTENT:
            Sms:
                sendMessage(phone,message)
                sendOtp(mobile)
                verifyOtp(mobile,otp,sensitve=False)
                retryOtp(mobile,is_voice=False)
            
            Email:
                send(subject,body,to=[],from_email=None)
            
            PushNotification:
                sendUser(user,title,message)
                sendTopic(topic,title,message)
                
"""


class Sms:
    SMS_KEY = settings.SMS_KEY

    def sendMessage(self,phone, message):
        otpurl = "http://api.msg91.com/api/sendhttp.php"
        params = {'message': message, 'authkey':self.SMS_KEY, 'mobiles': phone, 'sender': 'GoldLn'
            , 'country': '91', 'route': 4}
        result = requests.get(url=otpurl, params=params)
        print(str(result.content))
        return True


    def sendOtp(self,mobile):
        params = {'message': "<#> Your GoldLane otp is ##OTP## \n Y4xdqc8y+9U", 'authkey': self.SMS_KEY,
                  'mobile': "+91" + mobile, 'sender': 'GoldLN'}
        result = requests.post(url="http://control.msg91.com/api/sendotp.php", params=params)
        print(result)
        print(str(result.content))
        return result


    def verifyOtp(self,mobile, otp, sensitive=False):
        """
            sensitive means that one otp can be used only once for verification
        """
        if (mobile is not None and otp is not None):
            params = {'mobile': "+91" + mobile, 'otp': otp, 'authkey': self.SMS_KEY}
            result = requests.post(url="https://control.msg91.com/api/verifyRequestOTP.php", params=params)
            result = json.loads(result.content)

            if result['type'] == 'success':
                print("success recieved")
                return True
            else:
                if (result['message'] == 'already_verified' and sensitive):
                    print("already verified recieved")
                    return False
                elif result['message'] == 'already_verified' and not sensitive:
                    return True
                return False
        else:
            return False


    def retryOtp(self,mobile, is_voice=False):
        if is_voice:
            type = "voice"
        else:
            type = "text"
        params = {'mobile': "+91" + mobile, "authkey": self.SMS_KEY, 'retrytype': type}
        result = requests.post(url="http://control.msg91.com/api/retryotp.php", params=params)
        result = json.loads(result.content)
        return result

class Email:
    def send(self,subject,body,from_email=None,to=None):
        #configure this for email purpose and return
        return
        send_mail(subject=subject,message=body,from_emai="",recipient_list=[])

class PushNotification:
    __push_service = None
    __firebase_key = "<Enter your firebase key over here>"
    __click_action = "FLUTTER_NOTIFICATION_CLICK"


    def __init__(self):
        self.__push_service = FCMNotification(api_key=self.__firebase_key)



    def __formatted_message(self, resp):
        if resp['success'] == 1:
            return (True, resp)
        return (False, resp)

    def sendUser(self, user, title, message, on_click=None, icon=None, badge=None, color=None,data={}):
        """
        :return:(status:bool , response: json)
        """
        notification_ids = [token.notification_id for token in
                            user.auth_tokens.all().exclude(notification_id=None)]

        if len(notification_ids) != 0:
            if on_click is None:
                resp = self.__push_service.notify_multiple_devices(
                    registration_ids=notification_ids,
                    message_body=message,
                    message_title=title,
                    message_icon=icon,
                    badge=badge,
                    color=color,
                )
            else:
                data['type'] = on_click
                resp = self.__push_service.notify_multiple_devices(
                    registration_ids=notification_ids,
                    message_body=message,
                    message_title=title,
                    message_icon=icon,
                    click_action=self.__click_action,
                    data_message=data,
                    color=color,
                    badge=badge
                )

            return self.__formatted_message(resp)
        else:
            return self.sendTopic(topic=user.username, title=title, message=message, on_click=on_click, icon=icon,
                                  badge=badge, color=color)

    def sendTopic(self, topic, title, message, icon=None, badge=None, color=None, on_click=None):
        if on_click is None:
            resp = self.__push_service.notify_topic_subscribers(
                topic_name=topic,
                message_body=message,
                message_title=title,
                message_icon=icon,
                badge=badge,
                color=color,
            )
            return self.__formatted_message(resp)
        else:
            resp = self.__push_service.notify_topic_subscribers(
                topic_name=topic,
                message_body=message,
                message_title=title,
                message_icon=icon,
                click_action=self.__click_action,
                data_message={'type': on_click},
                color=color,
                badge=badge
            )
            return self.__formatted_message(resp)

