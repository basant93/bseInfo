import redis
import json
import redis

class FilterRedis:

    # Redis Configuration
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    # Configuration
    redis_key = 'sensex'
    num_records = 20
    max_no_of_records = 200

    def __init__(self):
        self.db  = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
        self.trim_count = 0

    def push(self, data):
        """
        Push the data to self.redis_key. Also trim it to max_no_of_records, so that data
        does not become huge.
        """
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # Periodically trim the list so it doesn't grow too large.
        if self.trim_count > self.max_no_of_records:
            self.db.ltrim(self.redis_key, 0, self.num_records)
            self.trim_count = 0

    def fetch_all(self, limit=15):
        """"
        Fetch all the records based on limit provided by user. Default to 15.
        """
        records = []
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            record_obj = json.loads(item.decode('utf-8'))
            records.append(record_obj)
        
        return records
    

    def search_result(self, search_text, limit=15):
        """
        Search the redis table based on the search text entered by the user. 
        If no search text is provided, it return the first 10 records.
        To sort on basis of any column, uncomment the sorted return.
        """
        records = []
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            if(search_text !=None):
                record_obj = json.loads(item.decode('utf-8'))
                if search_text in record_obj['SC_NAME']:
                    records.append(record_obj)

            else:
                record_obj = json.loads(item.decode('utf-8'))
                records.append(record_obj)

        #return sorted(records, key = lambda x : x['HIGH']) [:10]
        return records[:10]