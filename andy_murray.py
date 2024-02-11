import requests
import networkx as nx
import matplotlib.pyplot as plt

# Initialize your API credentials
headers = {
    "X-RapidAPI-Key": "c96095ab6fmsh8aef27ede081c79p16bc1djsn06537ad6130c",
    "X-RapidAPI-Host": "twitter-api45.p.rapidapi.com"
}


def fetch_following(screen_name, target_count=120):
    url = "https://twitter-api45.p.rapidapi.com/following.php"
    all_following = []
    querystring = {"screenname": screen_name}
    next_cursor = None  
    
    while len(all_following) < target_count:
        if next_cursor is not None:  
            querystring['cursor'] = next_cursor
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            all_following.extend([user['screen_name'] for user in data.get('following', []) if 'screen_name' in user])
            
           
            next_cursor = data.get('next_cursor')  
            if not next_cursor:  
                break
        else:
            print(f"Failed to fetch data for {screen_name}: {response.status_code}")
            break  
    
    return all_following[:target_count]


G = nx.DiGraph()

#Fetch Murray's following and add them to the graph
murray_following = fetch_following("andy_murray")
G.add_node("andy_murray")
print(murray_following)

for user in murray_following:
    if user:  
        G.add_node(user)
        G.add_edge("andy_murray", user)

#For each of Murray's followings, fetch their followings and add edges if they follow each other
for user in murray_following:
    if user:  
        user_following = fetch_following(user)
        for followed_user in user_following:
            if followed_user and followed_user in murray_following:
                G.add_edge(user, followed_user)


nx.write_gexf(G, "andy_murray_network_graph.gexf")
plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_size=200, node_color="lightblue", font_size=10, font_weight="bold")
plt.show()
