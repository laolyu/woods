# -*- coding: GB2312 -*-
import os
import os.path
import time
import glob

# ɾ�����в���cmd�ű�
path = "E:\\monkey_test\\"
for file in glob.glob(os.path.join(path, '*.cmd')):
    os.remove(file)

os.system("cls")  # os.system("cls")������������
rt = os.popen('adb devices').readlines()  # os.popen()ִ��ϵͳ�������ִ�к�Ľ��
n = len(rt) - 2
print("��ǰ�����Ӵ����ֻ���Ϊ��" + str(n))
aw = input("�Ƿ�Ҫ��ʼ���monkey���ԣ�������(yes or no): ")

if aw == 'yes':
    print ("monkey���Լ�����ʼ....")
    count = input("��������Ҫ���е�monkey���Դ���: ")
    testmodel = input("����������Ҫ���е��β��Ի��Ƕ���������ԣ�������(1-�����β��ԣ�2-��������������): ")
    ds = list(range(n))
    for i in range(n):
        nPos = rt[i + 1].index("\t")
        ds[i] = rt[i + 1][:nPos]
        dev = ds[i]
        promodel = os.popen(
            "adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.model="').readlines()  # ��ȡ�ֻ��ͺ�
        # modelname = ('').join(promodel)  # ��listתΪ�ַ���
        modelname = promodel[0]  # ��list��ȡ����һ��ֵ
        model = modelname[17:].strip('\r\n')
        proname = os.popen(
            "adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.brand="').readlines()  # ��ȡ�ֻ�����
        roname = proname[0]
        name = roname[17:].strip('\r\n')
        packagename = os.popen(
            "adb -s " + dev + ' shell pm list packages | find "xxx"').readlines()
        package = packagename[0]
        pk = package[8:].strip('\r\n')
        if pk == 'com.zm.sport':
            filedir = os.path.exists("E:\\monkey_test\\")
            if filedir:
                print("File Exist!")
            else:
                os.mkdir("E:\\monkey_test\\")
            devicedir = os.path.exists("E:\\monkey_test\\" + name + '-' + model + '-' + dev)
            if devicedir:
                print ("File Exist!")
            else:
                os.mkdir("E:\\monkey_test\\" + name + '-' + model + '-' + dev)  # ���豸ID������־Ŀ¼�ļ���
            wl = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-logcat' + '.cmd', 'w')
            # wl.write('adb -s ' + dev + ' logcat -v time ACRA:E ANRManager:E System.err:W *:S')
            wl.write('adb -s ' + dev + ' logcat -v time *:W')
            wl.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\logcat_%random%.txt\n')
            wl.close()
            if testmodel == '1':
                wd = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-device' + '.cmd', 'w')
                wd.write(
                    'adb -s ' + dev + ' shell monkey -p com.zm.sport --monitor-native-crashes --ignore-crashes --pct-syskeys 5 --pct-touch 55 --pct-appswitch 20 --pct-anyevent 20 --throttle 200 -s %random% -v ' + count)  # ѡ���豸ִ��monkey
                wd.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\monkey_%random%.txt\n')
                wd.write('@echo ���Գɹ���ɣ���鿴��־�ļ�~')
                wd.close()
            elif testmodel == '2':
                wd = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-device' + '.cmd', 'w')
                wd.write(':loop')
                wd.write('\nset /a num+=1')
                wd.write('\nif "%num%"=="4" goto end')
                wd.write(
                    '\nadb -s ' + dev + ' shell monkey -p com.zm.sport --monitor-native-crashes --ignore-crashes --pct-syskeys 5 --pct-touch 55 --pct-appswitch 20 --pct-anyevent 20 --throttle 200 -s %random% -v ' + count)  # ѡ���豸ִ��monkey
                wd.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\monkey_%random%.txt\n')
                wd.write('@echo ���Գɹ���ɣ���鿴��־�ļ�~')
                wd.write('\nadb -s ' + dev + ' shell am force-stop ' + pk)
                wd.write('\n@ping -n 15 127.1 >nul')
                wd.write('\ngoto loop')
                wd.write('\n:end')
                wd.close()
        else:
            print ("��ȷ�ϴ����ֻ�" + name + '-' + model + "δ��װcom.zm.sport~")

    # ִ���������ɵ�cmd�ű�path='E:\\monkey_test\\'
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) == True:
            if file.find('.cmd') > 0:
                os.system('start ' + os.path.join(path, '"' + file + '"'))  # dos�������ļ�������пո������˫����
                time.sleep(1)
elif aw == 'no':
    print('������ȷ�����д����ֻ��Ƿ���ͨ��adb����������pc!')
else:
    print ("���Խ���������Ƿ�������������yes or no��")