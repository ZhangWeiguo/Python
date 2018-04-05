from svd import SVD as SVD1
from svd_advance import SVD as SVD2
from svd_direct import SVD as SVD
import json,random,numpy
from conf import conf

def train():
    filename = "action_train.log"
    init_step = 0.5
    n_samples = 2e7
    n_epoches = 2
    n_dimsion = conf["n_dimsion"]
    alpha_user = 0.01
    alpha_item = 0.01
    decay_rate = 0.5
    step_decay = (decay_rate, n_samples*n_epoches)
    Model = SVD(n_dimsion,init_step=init_step,step_decay=step_decay,alpha1=alpha_user,alpha2=alpha_item)
    #Model.restore('user_vector', 'video_vector')
    Model.train_file(filename, N = n_epoches)
    Model.save('user_vector','video_vector')


if __name__ == "__main__":
    train()
