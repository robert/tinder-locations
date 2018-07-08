import time
import pynder
import robobrowser
import pickle
import re

import logging_config

def setup(email, password):
    fb_token = _get_fb_token(email, password)
    parent_folder = logging_config.parent_folder

    try:
        # Read token
        access_token_file = open(parent_folder + email + "_access_token.txt", "r")
        access_token = access_token_file.read()
        access_token_file.close()
        session = pynder.Session(access_token)
    except Exception as e:
        # Update token
        access_token = _get_fb_token(email, password)
        access_token_file = open(parent_folder + email + "_access_token.txt", "w")
        access_token_file.write(access_token)
        access_token_file.close()
        session = pynder.Session(access_token)

    # Assert setup succeeded
    session._api.profile()

    return session

def _get_fb_token(email, password):
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
    FB_AUTH_URL = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"
    
    rb = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="html5lib")
    
    # Facebook login
    rb.open(FB_AUTH_URL)
    login_form = rb.get_form()
    login_form["pass"] = password
    login_form["email"] = email
    rb.submit_form(login_form)
    
    # Get token
    auth_form = rb.get_form()
    rb.submit_form(auth_form, submit=auth_form.submit_fields["__CONFIRM__"])
    access_token = re.search(r"access_token=([\w\d]+)", rb.response.content.decode()).groups()[0]
        
    return access_token

def _get_happn_fb_token(email, password):
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
    FB_AUTH_URL = "https://www.facebook.com/v2.9/dialog/oauth?redirect_uri=fb247294518656661%3A%2F%2Fauthorize%2F&state=%7B%22challenge%22%3A%22VS6zY12VAx3qDc%252BvSgWUbxXINPg%253D%22%2C%220_auth_logger_id%22%3A%2212F72F8D-1EBF-477B-AFE3-55C161468659%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=email%2Cuser_birthday%2Cuser_likes%2Cuser_photos%2Cuser_friends&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=247294518656661&sdk=ios&fbapp_pres=0&sdk_version=4.23.0&_rdr"
    
    rb = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="html5lib")
    
    # Facebook login
    rb.open(FB_AUTH_URL)
    login_form = rb.get_form()
    login_form["pass"] = password
    login_form["email"] = email
    rb.submit_form(login_form)
    
    # Get token
    auth_form = rb.get_form()
    rb.submit_form(auth_form, submit=auth_form.submit_fields["__CONFIRM__"])
    access_token = re.search(r"access_token=([\w\d]+)", rb.response.content.decode()).groups()[0]
        
    return access_token
