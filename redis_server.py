import redis



import json
import redis

class FilterRedis:

    # Redis Configuration
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    # Tweet Configuration
    redis_key = 'ankit5'
    num_tweets = 20

    def __init__(self):
        self.db  = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
        self.trim_count = 0

    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # Periodically trim the list so it doesn't grow too large.
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0

    def fetch_all(self, limit=15):
        print("Hello fetch all")
        tweets = []
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item.decode('utf-8'))
            tweets.append(tweet_obj)
        print("My tweets : ", tweets)
        return tweets[:10]