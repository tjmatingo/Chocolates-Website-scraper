import redis
from redis import from_url

# Create a redis client
redisClient = redis.from_url('redis://default:Cl3UQPYBrkiE2DNf1TC8eqbGBm6ABPuv@redis-10209.c8.us-east-1-2.ec2.cloud.redislabs.com:10209')

# Push URLs to Redis Queue
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/1/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/2/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/3/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/4/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/5/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/6/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/7/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/8/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/9/")
redisClient.lpush('quotes_queue:start_urls', "https://quotes.toscrape.com/page/10/")
