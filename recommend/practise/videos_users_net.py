import networkx,numpy
from matplotlib import pyplot
from conf import score_dict
from matplotlib import pyplot

def draw_map():
    f = file("action_train.log", 'r')
    all_data = f.read().split("\n")
    order = range(len(all_data))
    f.close()
    data = []

    for i in order:
        s = all_data[i]
        L = s.split(",")
        if len(L) == 3:
            user_id = L[0]
            item_id = L[1]
            action = L[2]
            if len(user_id) >= 10 and len(item_id) >= 10:
                if score_dict[action] >= 1:
                    data.append([user_id,item_id,score_dict[action]])
    

    users = {}
    items = {}
    items_inv = {}
    users_items = {}
    items_users = {}
    items_similarity = None

    k_i = 0
    k_u = 0
    for user,item,weight in data:
        if user not in users:
            users[user] = k_u
            users_items[k_u] = set()
            k_u += 1
        if item not in items:
            items[item] = k_i
            items_users[k_i] = set()
            k_i += 1
        users_items[users[user]].add(items[item])
        items_users[items[item]].add(users[user])



    N = len(items)
    n = 10000
    items_similarity = numpy.zeros((n,n))
    
    for i in range(n):
        for j in range(n):
            item1 = i
            item2 = j
            if item1 >= item2:
                if item1 == item2:
                    items_similarity[item1,item2] = len(items_users[item1])
                continue
            commen_users = items_users[item1].intersection(items_users[item2])
            nn = len(commen_users)
            print item1,item2,nn
            items_similarity[item1,item2] = nn
            items_similarity[item2,item1] = nn
    x = range(n)
    y = range(n)
    X,Y = numpy.meshgrid(x,y)
    print X.shape,Y.shape,items_similarity.shape
    pyplot.contour(X,Y,items_similarity)
    pyplot.show()

draw_map()
    

def draw_net():
    edges = {}
    f = file("action_train.log", 'r')
    all_data = f.read().split("\n")
    f.close()

    for i in range(1000):
        s = all_data[i]
        L = s.split(",")
        if len(L) == 3:
            user_id = L[0]
            video_id = L[1]
            action = L[2].replace("\n", "")
            if len(user_id) >= 10 and len(video_id) >= 10:
                if (user_id,video_id) in edges:
                    if edges[(user_id,video_id)] < score_dict[action]:
                        edges[(user_id, video_id)] = score_dict[action]
                else:
                    edges[(user_id, video_id)] = score_dict[action]




    edges_tuple = []
    users_set = set()
    videos_set = set()
    users = {}
    videos = {}
    for i in edges.keys():
        if edges[i] >= 1:
            edges_tuple.append((i[0], i[1], edges[i] * 10))
            users_set.add(i[0])
            videos_set.add(i[1])
            if i[0] in users:
                users[i[0]] += 1
            else:
                users[i[0]] = 1
            if i[1] in videos:
                videos[i[1]] += 1
            else:
                videos[i[1]] = 1
        else:
            del edges[i]
    '''
    for i in users.keys():
        if users[i] >= 5:
            pass
        else:
            del users[i]
            users_set.remove(i)

    for i in videos.keys():
        if videos[i] >= 5:
            pass
        else:
            del videos[i]
            videos_set.remove(i)

    edges_tuple = []
    for i in edges.keys():
        if i[0] in users and i[1] in videos:
            edges_tuple.append((i[0],i[1],edges[i]*10))
        else:
            del edges[i]


    '''

    print len(videos_set),len(users_set),len(edges_tuple)
    print users,videos


    G = networkx.Graph()
    G.add_nodes_from(users_set)
    G.add_nodes_from(videos_set)
    G.add_weighted_edges_from(edges_tuple)
    pos = networkx.spring_layout(G)


    networkx.draw_networkx_nodes(G,pos=pos,
                        nodelist=videos_set,
                        node_color="red",
                        alpha=0.4,
                        node_size=1)

    networkx.draw_networkx_nodes(G,pos=pos,
                        nodelist=users_set,
                        node_color="blue",
                        alpha = 0.5,
                        node_size=3)

    networkx.draw_networkx_edges(G,pos=pos,
                                edgelist=edges.keys(),
                                width=edges.values()*10,
                                alpha=0.2)

    pyplot.show()



