# -*-encoding:utf-8 -*-
# created by wegozng in 20180430
import os,numpy,json,time

def get_train_data(train_files, batch_size, users_vdict, items_vdict):
    for i in train_files:
        f = open(i,'r')
        all_str = f.read().split("\n")
        start = 0
        end = start + batch_size
        fin = len(all_str)
        while True:
            user_ids    = []
            item_ids    = []
            other_vec   = []
            goal_vec    = []
            if start >= fin:
                break
            else:
                if end >= fin:
                    end = fin
                for j in range(start,end):
                    line = all_str[j]
                    user_id,item_id,goal = parse_line(line)
                    if len(user_id) == 24 and len(item_id) == 11:
                        user_ids.append(users_vdict[user_id])
                        item_ids.append(items_vdict[item_id])
                        goal_vec.append(goal)
                        other_vec.append([])
                start = end
                end = start + batch_size
                yield user_ids,item_ids,other_vec,goal_vec
        f.close()

def rm(train_files):
    for i in train_files:
        os.remove(i)


def parse_line(line):
    line = line.split("`")
    user_id     = ""
    video_id    = ""
    goal        = [0]
    for i in line:
        if "u_id=" in i:
            s = i.replace("u_id=","")
            user_id = s
        elif "v_id=" in i:
            s = i.replace("v_id=","")
            video_id = s
        elif "play_pv=" in i:
            s = int(i.replace("play_pv=",""))
            if s >= 1:
                goal = [1]
    return user_id,video_id,goal


def random_str(num):
    s = range(97,123)
    L = [chr(numpy.random.choice(s)) for i in range(num)]
    S = "".join(L)
    return S

def shuffle(train_files):
    N = len(train_files)
    if N >= 1:
        parent_path,file_name = os.path.split(train_files[0])
    shuffle_files = []
    while True:
        if len(shuffle_files) == N:
            break
        else:
            S = random_str(24)
            if not S in shuffle_files:
                shuffle_files.append(os.path.join(parent_path,S))
    fws = [open(i,'w') for i in shuffle_files]
    for i in train_files:
        fr = open(i,'r')
        s = fr.read().split("\n")
        numpy.random.shuffle(s)
        s= [line + "\n" for line in s]
        n = int(len(s)/len(shuffle_files))
        k = 0
        for j in range(N):
            fws[j].writelines(s[k:k+n])
            k = k + n
        fr.close()
    [fw.close() for fw in fws]
    return shuffle_files