#!/usr/bin/env python
#-*-encoding:utf-8-*-

import os
import sys
import md5
import os.path
import shutil
import re
import zipfile

Old_version=raw_input("Please Enter old version:" )
New_version=raw_input("Please Enter new version:")

Old_filesMd5={}
New_filesMd5={}
diff_filesMd5={}


Old_versionDir="app_v"+Old_version
New_versionDir="app_v"+New_version

# Old_versionDir="app_v1.0.0"
# New_versionDir="app_v1.0.1"

print("old version dir:"+Old_versionDir)
print("new version dir:"+New_versionDir)




def walk_dir(mapset_md5,dir,fileinfo,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            path = os.path.join(root,name)
            md5v = sumfile(path)
            newpath = path.replace(dir,'')
            fileinfo.write(newpath + ':' + md5v + '\n')
            mapset_md5[newpath]=md5v
            

def sumfile(fpath):
    m = md5.new()
    fobj = open(fpath)
    while True:
        d = fobj.read(8096)
        if not d:
            break
        m.update(d)
    return m.hexdigest()

#获取脚本文件的当前路径
def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

#打印结果
print "cur dir:"+cur_file_dir()


def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

def main():
    cur_dir = cur_file_dir()

    fileinfo1 = open(cur_dir+'\\'+Old_versionDir+'.txt','w')
    walk_dir(Old_filesMd5,cur_dir+'\\'+Old_versionDir,fileinfo1)

    fileinfo2= open(cur_dir+'\\'+New_versionDir+'.txt','w')
    walk_dir(New_filesMd5,cur_dir+'\\'+New_versionDir,fileinfo2)



    fileinfo1.close()
    fileinfo2.close()
    os.remove(cur_dir+'\\'+Old_versionDir+'.txt')
    os.remove(cur_dir+'\\'+New_versionDir+'.txt')



	############################################################
	##获取差异文件  
    for key in New_filesMd5:
    	if Old_filesMd5.has_key(key):
    		if New_filesMd5[key]!=Old_filesMd5[key]:
    			diff_filesMd5[key]=New_filesMd5[key]
    			#print("update file:"+key)
    	else:
    		#print("add file:"+key)
    		diff_filesMd5[key]=New_filesMd5[key]
    		
    print("update files:")
    for key2 in diff_filesMd5:
    	print(key2+":"+diff_filesMd5[key2])	


   ############################################################
   ##创建 更新包目录
    appdir=cur_dir+"\\app"
    
    if os.path.exists(appdir):
    	print("rm dir:"+appdir)
    	shutil.rmtree(appdir)
    	

	print("create dir:"+appdir)
    os.makedirs(appdir)

	############################################################
	##提取  差异文件到更新包

    for key3 in diff_filesMd5:
    	print(key3+":"+diff_filesMd5[key3])	
    	sourceFilePath=cur_dir+'\\'+New_versionDir+key3
    	targetFilePath=appdir+key3
    	targetDir=targetFilePath[0:targetFilePath.rindex("\\")]
    	if not os.path.exists(targetDir):
    		print("\ncreate sub dir:"+targetDir)
    		os.makedirs(targetDir)
    	print("copy from:"+sourceFilePath)
    	print("to: "+targetFilePath)
    	#shutil.copyfile(sourceFilePath, targetDir)
    	open(targetFilePath, "wb").write(open(sourceFilePath, "rb").read())
        
	############################################################
	##压缩 更新包到zip  计算zip的md5
	#print("\ncreate zip file")
	#zipfile=cur_dir+"\\app.zip"
	#zip_dir(appdir,zipfile)

	#md5v = sumfile(zipfile)
	#print("zip md5:"+md5v)

	#appversion=cur_dir+"\\version_v"+Old_version+"_"+New_version+".txt"
	#appversionfile=open(appversion,"w")
	#appversionfile.write("Old_version:"+Old_version+"\n")
	#appversionfile.write("New_version:"+New_version+"\n\n")
	#appversionfile.write("ZIP md5:"+md5v+"\n\n")
    #for key2 in diff_filesMd5:
     #   appversionfile.write(key2+":"+diff_filesMd5[key2]+"\n") 




    ############################################################
if __name__ == '__main__':
   main()



