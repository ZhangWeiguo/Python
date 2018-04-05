import os,numpy,shelve,pandas,random,shutil
from sklearn import neural_network as nn
from sklearn import ensemble,linear_model
from sklearn.cross_validation import train_test_split
from PIL import Image,ImageFilter

others_file = 'E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\others\\'
face_file = 'E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\self'

Sex_file = 'Self.dat'
shape = (128, 128)

def image2array(filename,shape):
    img = Image.open(filename)
    img = img.convert('L')
    img = img.resize(shape)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    data = numpy.array(img)
    w,h = shape
    data = data.reshape(( w*h,))
    return data

def save_data():
    face_images = os.listdir(face_file)
    others_images = os.listdir(others_file)
    Data = []
    Target = []
    for image in others_images:
        try:
            image_path = os.path.join(others_file,image)
            print (image_path)
            data = image2array(image_path,shape)
            Target.append(0)
            Data.append(data)
        except:
            pass
    for image in face_images:
        image_path = os.path.join(face_file,image)
        print (image_path)
        data = image2array(image_path,shape)
        Target.append(1)
        Data.append(data)
    Data = numpy.array(Data)
    Target = numpy.array(Target)
    L = random.sample(range(len(Data)),len(Data))
    Data = Data[L,:]
    Target = Target[L]
    Sex_data = shelve.open(Sex_file)
    Sex_data['Data'] = numpy.array(Data)
    Sex_data['Target'] = numpy.array(Target)
    Sex_data.close()

if __name__ == '__main__':
    save_data()