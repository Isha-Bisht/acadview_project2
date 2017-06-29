import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
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

def get_post_id(insta_username): #fucntion declared to get the ID of the recent post of a user by usernam
    user_id=get_user_id(insta_username)
    if user_id==None:
        print "user doesn't exist"
        exit()
        request_url=(base_url+ 'users/%s/media/recent/?access_token=%s')%(user_id, app_access_token)
        print "get request url:%s" %(request_url)
        user_media=requests.get(request_url).json()
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                return user_media['data'][0]['id']
            else:
                print 'There is no recent post of the user!'
                exit()
        else:
            print 'Status code other than 200 received!'
            exit()

def like_a_post(insta_username):  #function defined to like the recent post of a user
    media_id=get_post_id(insta_username)
    request_url=(base_url+'media/%s/likes')%(media_id)
    payload={"access_token":app_access_token}
    print "POST request url %s:"%(request_url)
    post_a_like=requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

def post_a_comment(insta_username):  #function defined to make a comment on the recent post of the user
    media_id=get_post_id(insta_username)
    comment_text=raw_input("your comment:")
    payload={"access token":app_access_token, "text":comment_text}
    request_url=(base_url+'media/%s/comments')%(media_id)
    print "POST request url%s" %(request_url)
    make_comment=requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

def delete_negative_comment(insta_username):  #function defined to make delete negative comments from the recent post
    media_id=get_post_id(insta_username)
    request_url=(base_url+'media/%s/comments/?access_token=%s')%(media_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code']==200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id=comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, app_access_token)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


def start_bot():  #to choose the action from the given menu
    while True:
        print "\n"
        print "hello people... welcome to insta bot"
        print "here we have a menu for u people"
        print "a.> get our own details here \n"  #choice1 in the menu
        print "b.> get details of other user by username \n"   #choice2 in the menu
        print "c.> get your own recent post" #choice3 in the menu
        print "d.> get the recent post of the user by entering their name" #choice4 in the menuc
        print "e.> Get a list of people who have liked the recent post of a user\n"
        print "f.> like the recent post of a user\n" #choice5 in the menu
        print "g.> Get a list of comments on the recent post of a user\n"
        print "h.> Make a comment on the recent post of a user\n"  #choice6 in the menu
        print "i.> Delete negative comments from the recent post of a user\n" #choice7 in the menu
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
       #choice=="e":
            #insta_username=raw_input("enter the name of the user")
            #get_like_list(insta_username)
        elif choice=="f":
            insta_username=raw_input("enter the name of the user")
            like_a_post(insta_username)
        #elif choice=="g":
            #nsta_username=raw_input("enter the name of the user")
            #get_comment_list(insta_username)
        elif choice=="h":
            insta_username = raw_input("enter the name of the user")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice=="j":
            print "wrong choices"
        else:
            print "sorry wrong choices"

start_bot()

























































