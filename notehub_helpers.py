from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime


import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import random
import string

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



# transform the string
def transformString(s):
    if s is None:
        return "No description provided"
    if len(s) > 120:
        return s[:120] + "..."
    
    return s

# generate the svg
def generateSvg(language, username="admin"):
    

  ref = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
 
  linkt = language + username + ref 

  # make an API call and store the responses
  url = f"https://api.github.com/search/repositories?q=topic:blockchain&sort=stars"
  r = requests.get(url)

  # check if response was successful
  print("Status code: ",r.status_code)

  # Store API response as a dictionary
  response_dict = r.json()


  # how many python reps there is in github
  total_repos = response_dict['total_count']
  print("total number of repositories : ", total_repos)

  # a dict of repos we have data about
  repos_dict = response_dict['items']


  # store names and stars for retrieved repos
  names, plot_dicts = [], []

  for repo_dict in repos_dict:
      names.append(repo_dict['name'])
      plot_dicts.append({'value':repo_dict['stargazers_count'], 
                        'label':transformString(repo_dict['description']),
                        'xlink':{'href':repo_dict['html_url'], 'target':'_blank'}})
      
      
      
  # Make visualization
  my_config = pygal.Config()
  my_config.x_label_rotation = 45
  my_config.show_legend = False
  my_config.title_font_size = 24
  my_config.label_font_size = 24
  my_config.major_label_font_size = 18
  my_config.truncate_label = 15
  my_config.show_y_guides = False
  my_config.width = 1200
  my_config.height = 800
  my_style = LS('#1e1e1e', base_style=LCS)


  chart = pygal.Bar(my_config, style=my_style)
  chart.title = f'Most-Starred {language.upper()} Projects on GitHub'
  chart.x_labels = names
  chart.add('', plot_dicts)
  chart.render_to_file(f'./static/images/{linkt}.svg')
  return chart.render_data_uri(), repos_dict




def get_current_date_str():
    # Get the current date and time
    now = datetime.now()
    # Format the date as YYYY-MM-DD
    date_str = now.strftime('%Y-%m-%d')
    return date_str


