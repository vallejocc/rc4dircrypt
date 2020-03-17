import os
import sys
import md5

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
        if not e.startswith(".git"):
            if os.path.isdir(startdir+"/"+e):
                recurcurrentdir(callback, startdir+"/"+e)
            else:
                callback(startdir+"/"+e)


def encryptfile(dstpath):
    if "rc4thisdir.py" in dstpath: return
    if dstpath.startswith(".git"): return
    print "Encrypt:", dstpath
    f=open(dstpath,"rb")
    s=f.read()
    f.close()
    if s[0:12]=="ENC666ENC666":
        print "Already encrypted:", dstpath
        return
    k=md5.new(sys.argv[1]+s).digest()
    k+=rc4crypt(sys.argv[1],k)
    s=rc4crypt(s, k)
    keyenc=rc4crypt(k, sys.argv[1])
    f=open(dstpath,"wb")
    f.write("ENC666ENC666"+keyenc+"ENC666ENC666"+s)
    f.close()


recurcurrentdir(encryptfile)