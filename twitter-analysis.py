import requests
import networkx as nx
import matplotlib.pyplot as plt

followed_names = []

nxt_ptr = 2

def call_api(nxt_cursor = -1):
    
    url = "https://twitter-api45.p.rapidapi.com/following.php"
    querystring = {"screenname": "JohnCena", "cursor": nxt_cursor}

    headers = {
        "X-RapidAPI-Key": "c96095ab6fmsh8aef27ede081c79p16bc1djsn06537ad6130c",
        "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    next_cursor = response.json().get("next_cursor")

    if response.status_code == 200:
        data = response.json()
        following = data.get('following', [])  # Safely get the 'following' list if it exists
        for user in following:
            username = user.get('screen_name')
            followed_names.append(username)   # Extract screen name
               

    return next_cursor, followed_names




while nxt_ptr:
    nxt_cursor, followed_names = call_api()
    nxt_ptr-=1


# print(followed_names)
G = nx.Graph()

G.add_node("JohnCena")

for screen_name in followed_names:
    G.add_node(screen_name)
    G.add_edge("JohnCena", screen_name)

print(len(followed_names))

plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
plt.show()
