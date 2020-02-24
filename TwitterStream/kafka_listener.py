
from tweepy import OAuthHandler, Stream, StreamListener
from kafka import SimpleProducer, KafkaClient

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="s2iEQ0cpAYL9T999RxNzOqDSW"
consumer_secret="fZicERZUgdjvhMkHzKoIBFODBz7L0gwJVvLnkXhVlH2DGEYtTW"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="917093178137808896-SHPreegaWxr2QzIdpfnpZ4KmfozS6ui"
access_token_secret="gWdYWNhOsK2LtWscDUDzcEIVFohXhF4JL5E4G3WoMjJCJ"

class KafkaListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print("process started")
        producer.send_messages("twitter-stream", data.encode("utf-8"))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    kafka_client = KafkaClient("localhost:9092")
    producer = SimpleProducer(kafka_client)

    l = KafkaListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['#'])



