import restipy
import re, sys, webbrowser

# Nearly trivial Facebook REST API wrapper
def fb_get_logged_in_requestor():
    auth_url = "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token&scope=ads_management,offline_access"%FB_APP_ID
    webbrowser.open_new(auth_url)
    url_bar = raw_input("Paste the URL bar contents here: ")
    match = re.search('access_token=([^&]+)', url_bar)
    access_token = match.group(1)
    fb_format_str = "https://api.facebook.com/method/%s?access_token="+access_token+"&format=json&%s"
    return make_requestor(lambda *args: fb_format_str%args)

fb_request = fb_get_logged_in_requestor()
ads = fb_request('ads.getAccounts')

