import requests, urllib
app_access_token='2240894747.9e9344f.7155f8b5801d4279828eabb4def04a60' #app access token
base_url='https://api.instagram.com/v1/' #base url

def get_own_post(): #function defined to see ur own post
    request_url=(base_url+'users/self/media/recent/?access_token=%s')%(app_access_token)
    print "GET request url: %s" %(request_url)
    own_media=requests.get(request_url).json()

    if own_media['meta']['code']==200:
        if len(own_media['data']):
            image_name=own_media['data'][0]['id']+'.jpeg'
            image_url=own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "your image has been downloaded"
        else:
            print "post doesn't exist"
    else:
        print "code other than 200 recieved"
def get_user_id(insta_username):  #function defined to take the user id
    request_url=(base_url+'users/search?q=%s&access_token=%s')%(insta_username, app_access_token)
    print 'GET request url:%s' %(request_url)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code']==200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print "status code other than 200 recieved"
        exit()

def get_user_post(insta_username): #function defined to get the recent post of the user
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "user doesn't exist"
        exit()
    request_url=(base_url+'users/%s/media/recent/?access_token=%s')%(user_id, app_access_token)
    print  'GET request url %s'%(request_url)
    user_media=requests.get(request_url).json()

    if user_media['meta']['code']==200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print "post doesn't exist"
    else:
        print "code other than 200 recieved"


def self_info():  #self_info() function definition
    request_url=(base_url+ 'users/self/?access_token=%s') %(app_access_token)
    print 'GET request url:%s' %(request_url)
    user_info=requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print 'username: %s' %(user_info['data']['username'])
            print 'no. of followers:%d'%(user_info['data']['counts']['followed_by'])
            print 'no. of people u are following %d' %(user_info['data']['counts']['follows'])
            print 'no. of posts %d' %(user_info['data']['counts']['media'])
        else:
            print "user doesn't exist"
    else:
        print "status code other than 200 recieved"




def get_user_info(insta_username): #function defined to get the user details
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "user doesn't exist"
        exit()
    request_url=(base_url+'users/%s?access_token=%s')%(user_id, app_access_token)
    print 'GET request url:%s'%(request_url)
    user_info=requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "there is no data is present for this user"
    else:
        print "status code other than 200 is received"

def start_bot():  #to choose the action from the given menu
    while True:
        print "\n"
        print "hello people... welcome to insta bot"
        print "here we have a menu for u people"
        print "a.> get our own details here \n"  #choice1 in the menu
        print "b.> get details of other user by username \n"   #choice2 in the menu
        print "c.> get your own recent post" #choice3 in the menu
        print "d.> get the recent post of the user by entering their name" #choice4 in the menuc
        print "j.Exit"
        choice=raw_input("enter your choice:")
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username=raw_input("enter the username:")
            get_user_info(insta_username)
        elif choice=="c":
            get_own_post()
        elif choice=="d":
            insta_username=raw_input("enter the username:")
            get_user_post(insta_username)
        elif choice=="j":
            print "wrong choices"
        else:
            print "sorry wrong choices"

start_bot()

























































