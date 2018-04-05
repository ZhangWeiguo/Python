import os,numpy,shelve,pandas,random,shutil
from sklearn import neural_network as nn
from sklearn import ensemble,linear_model
from sklearn.cross_validation import train_test_split
from PIL import Image,ImageFilter

man_file = 'E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\man\\'
woman_file = 'E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\woman\\'
# man_file = 'E:\\zhangweiguo\\Python\\data\\woman-man-recog-master\\snapshot\\man-snapshot\\'
# woman_file = 'E:\\zhangweiguo\\Python\\data\\woman-man-recog-master\\snapshot\\woman-snapshot\\'
Sex_file = 'Sex_outer.dat'
shape = (128, 128)

def image2array(filename,shape):
    img = Image.open(filename)
    img = img.convert('L')
    img = img.resize(shape)
    # img = img.filter(ImageFilter.EDGE_ENHANCE)
    data = numpy.array(img)
    w,h = shape
    data = data.reshape(( w*h,))
    return data

def save_data():
    woman_images = os.listdir(woman_file)
    man_images = os.listdir(man_file)
    Data = []
    Target = []
    for image in man_images:
        try:
            image_path = os.path.join(man_file,image)
            print (image_path)
            data = image2array(image_path,shape)
            Target.append(0)
            Data.append(data)
        except:
            pass
    for image in woman_images:
        image_path = os.path.join(woman_file,image)
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

def split_image_by_tag():
    All_video = pandas.read_csv('E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\video_tag.csv', header=0)
    Videos = list(All_video['id'])
    Tags = list(All_video['tag'])
    Images_jpg_exist = os.listdir("E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\all_jpg")
    Video_tag = {}
    for i,j in zip(Videos, Tags):
        Video_tag[i+".jpg"] = j
    for i in Images_jpg_exist:
        if "man" in Video_tag[i]:
            shutil.copyfile("E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\all_jpg\\"+  i,
                            "E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\man\\"+i)
        elif "girl" in Video_tag[i]:
            shutil.copyfile("E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\all_jpg\\"+  i,
                            "E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\woman\\"+i)
if __name__ == '__main__':
    # split_image_by_tag()
    save_data()