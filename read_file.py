def get_vecs(filename):   
    with open(filename,'r') as file:
        data=file.readlines()
    word_vec={}
    for i in data:
        i=i.strip().split(' ')
        word= i[0]
        vecs=i[1:]
        vecs=[float(i) for i in vecs]
        word_vec[word] = vecs
    return word_vec
        