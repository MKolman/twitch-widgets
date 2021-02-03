import re
import requests
from time import sleep
from datetime import datetime
import json

class State(object):
  URL = 'https://www.codingame.com/services/Leaderboards/getClashLeaderboard'
  FILTER = [1, {'keyword': '', 'active': False, 'column': '', 'filter': ''}, None, True, 'global', None]
  ME = 'MKoding'

  @classmethod
  def fetch(cls):
    response = requests.post(cls.URL, json=cls.FILTER).json()
    data = []
    for u in response['users']:
      data.append({
        'userId': u['codingamer'].get('userId'),
        'pseudo': u.get('pseudo'),
        'rank': u['rank'],
        'score': u['score'],
      })
    return cls(data, datetime.now())

  @classmethod
  def load(cls, data):
    """ Load state from a jsonified dict """
    return cls(data['data'], datetime.fromisoformat(data['timestamp']))

  def __init__(self, data, timestamp):
    self.data = data
    self.timestamp = timestamp
    self.lookup = {}
    for i, u in enumerate(data):
      self.lookup[u['userId']] = i
      if u['pseudo']:
        self.lookup[u['pseudo']] = i

  def my_rank(self):
    idx = self.lookup[State.ME]
    return self.data[idx]['rank']

  def my_score(self):
    idx = self.lookup[State.ME]
    return self.data[idx]['rank']

  def dump(self):
    """ Save state into a dict to be jsonified """
    return {
      'timestamp': self.timestamp.isoformat(),
      'data': self.data,
    }

def load_history():
  states = []
  with open('history.json') as f:
    states = list(map(State.load, json.load(f)))
  return states

def save_history(states):
  data = list(map(State.dump, states))
  with open('history.json', 'w') as f:
    json.dump(data, f)

def update_index(state):
  rank = state.my_rank()
  with open('index.html') as f:
    txt = f.read()
  txt = re.sub("<body>.*</body>", f"<body>#{rank}</body>", txt)
  with open('index.html', 'w') as f:
    f.write(txt)

history = load_history()
while True:
  history.append(State.fetch())
  print(history[-1].my_rank())
  save_history(history)
  if len(history) == 1 or history[-1].my_rank() != history[-2].my_rank():
    update_index(history[-1])
  sleep(30)
