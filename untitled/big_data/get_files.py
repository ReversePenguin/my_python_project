#_*_ coding:utf-8 _*_

import os
from read_origin_data import *

def merge_files(final_file):
    '''
    合并不同文件夹下面的所有文件
    :param final_file:
    :return:
    '''
    origin_path = u'D:/study/实验室/项目/大数据/MY/3_weeks/09'
    paths = []
    filenames = []
    for i in range(5,26):
        s = ""
        if i < 10:
            s = '0' + str(i)
        else:
            s = str(i)
        real_path = origin_path + s
        filelist = os.listdir(real_path)
        paths.append(real_path)
        filenames.append(filelist)
    print paths
    print filenames
    final = file(final_file,'w')
    for i in range(len(filenames)):
        filepath = paths[i] +'/'+ filenames[i][0]
        final.write(file(filepath).read())


if __name__ =="__main__":
    '''
    #merge_files('data_source_3weeks')
    cleaned_null = clean_null("data_source_3weeks")
    print '空值的数量',cleaned_null['null_count']
    #json.dump(cleaned_null['result_data'],open('data_source_3weeks_nonull_list','w'))
    result = get_perons_outing(cleaned_null['result_data'])
    print '整合前：',result['origin_length']
    print '整合后（即为用户数）：',result['final_length']
    json.dump(result, open('data_source_3weeks_nonull_dict', 'w'))
    '''
    f = json.load(file('data_source_3weeks_nonull_dict'))
    counts = f['persons_count']
    #print sorted(counts)
    #print counts.count(1)
    '''
    no_repetition =  list(set(counts))
    data_count = {}
    for i in no_repetition:
        data_count[str(i)] = counts.count(i)
    for i in no_repetition:
        print i,"：",data_count[str(i)]
    '''
    print counts.index(359)

