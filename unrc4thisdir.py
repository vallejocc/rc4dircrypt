import os
import sys

print "Key:", sys.argv[1]

def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    return ''.join(out)


def recurcurrentdir(callback, startdir=None):
    if startdir==None: startdir=os.getcwd()
    for e in os.listdir(startdir):
        if os.path.isdir(startdir+"/"+e):
            recurcurrentdir(callback, startdir+"/"+e)
        else:
            callback(startdir+"/"+e)


def decryptfile(dstpath):
    if "rc4thisdir.py" in dstpath: return
    print "Decrypt:", dstpath
    f=open(dstpath,"rb")
    s=f.read()
    f.close()
    if len(s)<12 or s[0:12]!="ENC666ENC666":
        print "Non encrypted file:", dstpath
        return
    s=rc4crypt(s[12:], sys.argv[1])
    f=open(dstpath,"wb")
    f.write(s)
    f.close()


recurcurrentdir(decryptfile)