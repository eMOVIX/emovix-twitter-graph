__author__ = 'Jordi Vilaplana'

import json
import logging
import time
import csv
import tweepy

logging.basicConfig(
    filename='emovix_twitter_graph.log',
    level=logging.WARNING,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%d-%m-%y %H:%M')

# Configuration parameters
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""
client = None

NODES_FILENAME = "nodes.json"
LINKS_FILENAME = "links.json"


def addUserNode(user):
    pass

def loadConfig():
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
        global access_token; access_token = config['access_token']
        global access_token_secret; access_token_secret = config['access_token_secret']
        global consumer_key; consumer_key = config['consumer_key']
        global consumer_secret; consumer_secret = config['consumer_secret']

if __name__ == '__main__':
    logging.debug('emovix_twitter_graph.py starting ...')

    loadConfig()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    with open(NODES_FILENAME, mode='w') as nodes_json:
        json.dump([], nodes_json)

    with open(LINKS_FILENAME, mode='w') as links_json:
        json.dump([], links_json)

    with open('usernames.csv', 'r') as csvfile:
        csv_usernames = csv.reader(csvfile.read().splitlines())
        usernames = []
        nodes = []
        links = []

        # Used to track down already existing nodes to avoid duplicates
        node_list = []

        for username in csv_usernames:
            usernames.append(username)

        # We first add to our node list the original Twitter users
        for username in usernames:
            user_node = {'id': username[0], 'group': 1}
            nodes.append(user_node)
            node_list.append(username[0])

        # Then, for each user we are going to work out additional nodes (followers and friends) and links
        for username in usernames:
            screen_name = username[0]
            logging.debug('Checking username ' + str(screen_name) + ' ...')

            try:
                # Let's work with the followers first
                followers_ids = []
                for tweepy_user in tweepy.Cursor(api.followers, screen_name=screen_name).items():
                    followers_ids.append(tweepy_user.screen_name)
                    #print followers_ids
                    #time.sleep(60)

                for follower_id in followers_ids:
                    # We check if this node already exists
                    if not follower_id in node_list:
                        # We add it to the json list
                        follower_node = {'id': follower_id, 'group': 2}
                        node_list.append(follower_id)
                        # And to the node list
                        nodes.append(follower_node)

                    # We also add the connection between the user and the follower
                    link_node = {'source': follower_id, 'target': screen_name}
                    links.append(link_node)

                # Now let's go to the friends (users followed by username)
                friends_ids = []
                for tweepy_user in tweepy.Cursor(api.friends, screen_name=screen_name).items():
                    friends_ids.append(tweepy_user.screen_name)
                    #print friends_ids
                    #time.sleep(60)

                for friend_id in friends_ids:
                    # We check if this node already exists
                    if not friend_id in node_list:
                        # We add it to the json list
                        friend_node = {'id': friend_id, 'group': 2}
                        node_list.append(friend_id)
                        # And to the node list
                        nodes.append(friend_node)

                    # We also add the connection between the user and the follower
                    link_node = {'source': screen_name, 'target': friend_id}
                    links.append(link_node)


            except tweepy.TweepError:
                logging.debug("Oops, Tweepy error! Sleeping for 15 minutes ...")
                time.sleep(60 * 15)
                continue

            except StopIteration:
                break

        with open(NODES_FILENAME, mode='w') as nodes_json:
            json.dump(nodes, nodes_json)

        with open(LINKS_FILENAME, mode='w') as links_json:
            json.dump(links, links_json)
