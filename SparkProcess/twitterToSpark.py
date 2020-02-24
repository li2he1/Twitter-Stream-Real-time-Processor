import socket
import sys
import requests
import requests_oauthlib
import json

ACCESS_TOKEN = "917093178137808896-SHPreegaWxr2QzIdpfnpZ4KmfozS6ui"
ACCESS_SECRET = "gWdYWNhOsK2LtWscDUDzcEIVFohXhF4JL5E4G3WoMjJCJ"
CONSUMER_KEY = "s2iEQ0cpAYL9T999RxNzOqDSW"
CONSUMER_SECRET = "fZicERZUgdjvhMkHzKoIBFODBz7L0gwJVvLnkXhVlH2DGEYtTW"
twitter_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)


def streamTweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    # query_data = [('language', 'en'), ('locations', '-122,-37,-122,38'),('track','#')]
    stream_param = [('language', 'en'), ('locations', '-90,-20,100,50'), ('track', '#')]
    stream_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in stream_param])
    resp = requests.get(stream_url, auth=twitter_auth, stream=True)
    print(stream_url, resp)
    return resp


def twitter_to_spark(resp, tcp_conn):
    for line in resp.iter_lines():
        try:
            all_tweet = json.loads(line)
            tweet_pure_text = all_tweet['text'] + '\n'      # pyspark can't accept stream, add '\n'

            print("Tweet pure text is : " + tweet_pure_text)
            print ("------------------------------------------")
            tcp_conn.send(tweet_pure_text.encode('utf-8', errors='ignore'))
        except:
            e = sys.exc_info()[0]
            print("Error is: %s" % e)


 
conn = None
TCP_IP = "localhost"
TCP_PORT = 9090
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)
print("Twitter end server is waiting for TCP connection...")
conn, addr = sock.accept()
print("Spark process connected. streaming tweets to Spark process.")
resp = streamTweets()
twitter_to_spark(resp,conn)
