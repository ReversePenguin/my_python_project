#_*_ coding:utf-8 _*_

def MyXreadlines(file_name):
    seek = 0
    while True :
        with open(file_name) as f :
            f.seek(seek)
            data = f.readline()
            if data:
                yield data
                seek = f.tell()
            else:
                return


content = MyXreadlines("file1")
print content
for line in content:
    print line,




