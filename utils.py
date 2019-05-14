import cv2
def read_data(imgs_path, file_path, shape, offset=0):
    import numpy as np

    X=[]
    y=[]
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if(offset > 0):
            for l in lines[:-offset]:
                img_file, label = l.strip().split(', ')
                # invert shape is necessary, input of function is (x,y) and shape = (h,w,c)
                X.append(cv2.resize(cv2.imread(imgs_path + str(int(img_file) + offset) + '.jpg'), (shape[1], shape[0])))
                y.append(label)
        elif(offset == 0):
            for l in lines:
                img_file, label = l.strip().split(', ')
                # invert shape is necessary, input of function is (x,y) and shape = (h,w,c)
                X.append(cv2.resize(cv2.imread(imgs_path + str(int(img_file) + offset) + '.jpg'), (shape[1], shape[0])))
                y.append(label)
    X = np.array(X)
    names = get_names()
    y = np.array([names[x] for x in y])
    
    return X, y, names

def get_names():
	names = {}
	with open('names.csv', 'r') as f:
		lines = f.readlines()
		for l in lines:
			name,id = l.strip().split(',')
			names[name] = int(id)
	
	return names

def distance(P, kind):
    dic = {'stop': 3.6, 'sem':2.3}
    W =  dic[kind] # (CM)
    F = 575 
    D = (W*F)/P
    return D
