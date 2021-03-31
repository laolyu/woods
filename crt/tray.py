# $language = "python"
# $interface = "1.0"
import random
import string


def project():
    # global proj
    project_0 = crt.Dialog.Prompt(
        "xiaoyu-1,kuaizip-2,kantu-3,heinote-4,finder-5,browser-6//pdf-10,wx-11,haotu-12,bz01-13//lszip-20,jcwallpaper-21,xinnote-22,qingjiepdf-23",
        "project",
        "11",
        False)
    proj = int(project_0)

    if proj == 1:
        qid = 'xiaoyu'
    elif proj == 2:
        qid = 'kuaizip'
    elif proj == 3:
        qid = 'kantu'
    elif proj == 4:
        qid = 'heinote'
    elif proj == 5:
        qid = 'finder'
    elif proj == 6:
        qid = 'browser'
    elif proj == 10:
        qid = 'whirlwindpdf'
    elif proj == 11:
        qid = 'smartlook'
    elif proj == 12:
        qid = 'haotu'
    elif proj == 13:
        qid = 'calfwallpaper'
    elif proj == 14:
        qid = 'sesame'
    elif proj == 15:
        qid = 'jkkantu'
    elif proj == 20:
        qid = 'lszip'
    elif proj == 21:
        qid = 'jcwallpaper'
    elif proj == 22:
        qid = 'xinnote'
    elif proj == 23:
        qid = 'qingjiepdf'
    else:
        qid = ''
        crt.Dialog.MessageBox('qid-num error')
    return proj, qid


def enve():
    env_0 = crt.Dialog.Prompt(
        "测试-0,线上-1",
        "env",
        "0",
        False)
    env_int = int(env_0)
    return env_int


def exe_host():
    path = r'Desktop' + '\\'
    exe_list = ['TrayTip.exe ', 'TrayTip-mx.exe ', 'xftrayflash.exe ', 'wxhardware.exe ', 'ktelfin.exe ']
    url_host = ["http://test-ssp.7654.com", "http://ssp.7654.com", 'http://test-ssp.7654.com/ys', 'http://domain.thorzip.muxin.fun/ys',
                "http://page-backend.nanjingchenxi.com", "http://smartlook-s.shheshou.com", "http://ggs.wallpaper.shqingzao.com"]
    if proj in range(1, 7):
        exe = path + exe_list[0]
        if env == 0:
            host = url_host[0]
        else:
            host = url_host[1]
    elif proj in range(20, 24):
        exe = path + exe_list[1]
        if env == 0:
            host = url_host[2]
        else:
            host = url_host[3]
    elif proj == 10:
        exe = path + exe_list[2]
        if env == 0:
            host = url_host[0]
        else:
            host = url_host[4]
    elif proj == 11:
        exe = path + exe_list[3]
        if env == 0:
            host = url_host[0]
        else:
            host = url_host[5]
    elif proj == 12 or proj == 13:
        exe = path + exe_list[4]
        if env == 0:
            host = url_host[0]
        else:
            host = url_host[6]
    else:
        exe = 'err'
        host = 'err'
        crt.Dialog.MessageBox('exe error')
    return exe, host

    # for i in range(len(exe)):
    #     crt.Screen.Send("taskkill /f /t /im " + exe_list[i] + "\r")
    # crt.Screen.WaitForString("进程")


def argue():
    # crt.Dialog.MessageBox(proj)
    previewurl = 'http://test.gamma-minipage.news.7654.com/shanbiao/kt_s/1/'  # 当-previewurl不为空,走新闻样式
    trayiconurl = 'http://down1.7654.com/n/tui/tips/2/trayicon.ico'  # 当-previewurl不为空,走新闻样式
    traytext = "360环境弹出新闻"  # 当-previewurl不为空,走新闻样式
    mutex = random.choice(string.ascii_letters)  # 包含所有字母(大写或小写)的字符串

    if project == "finder":
        qid_ssp = "sousuo"
    elif project == "kuaizip":
        qid_ssp = "kuaiya"
    else:
        qid_ssp = project

    if proj in range(1, 7):
        adurl = '-adurl="%s/ssp/list?qid=%s&ad=%s_shanbiao_1"' % (host, project, qid_ssp)

        # arg = exe + '-closebuttonjsonurl=http://down1.7654browser.shzhanmeng.com/tui/close.json -killprocess=1 -usewebmode=1 -trayopentype=1 -showneglect=1 ' \
        #             '-mutex=%s -project=%s -adurl=%s -previewurl=%s -trayiconurl=%s-traytext=%s' % (mutex, project, adurl, previewurl, trayiconurl, traytext)
    else:
        if proj in range(20, 24):  # -adurl=http://domain.thorzip.muxin.fun/ys -qid=lszip -ad=lszip_shanbiao_1 -trayopentype=1
            adurl = '-adurl=%s -qid=%s -ad=%s_shanbiao_1' % (host, project, project)
            # adurl = 'http://domain.thorzip.muxin.fun/ys?qid=%s&ad=%s_shanbiao_1' % (project, qid_ssp)
        elif proj == 10:  # -adurl=http://page-backend.nanjingchenxi.com/pdf -ad=tuopan_pdf -qid=whirlwindpdf
            adurl = '-adurl=%s/pdf -qid=%s -ad=tuopan_pdf' % (host, project)
        elif proj == 11:
            adurl = '-adurl=%s/smartlook -qid=%s -ad=smartlook_shanbiao_1' % (host, project)
        elif proj == 12:
            adurl = '-adurl=%s/bz -qid=%s -ad=haotutuopan' % (host, project)
        elif proj == 13:
            adurl = '-adurl=%s/bz -qid=%s -ad=bztuopan' % (host, project)
        else:
            adurl = 'error'
            crt.Dialog.MessageBox('adurl error')

    arg = '%s -taskid=tray-py -killprocess=1 -usewebmode=1 -localcity="青夏" -mutex=%s -project=%s %s -reportjsonurl=http://down1.7654browser.shzhanmeng.com/tui/tnews/haotu.data -reportprefix=traytip-1-dsp-zm -hibernate=0 ' % (
        exe, mutex, project, adurl)

    arg_skin = '%s -taskid=tray.py -usewebmode=0 -killprocess=1 -skinurl=http://down1.7654browser.shzhanmeng.com/tui/test/traytip.zip -traytext=一刀7777亿 ' \
               '-landingpage=https://s.click.taobao.com/CVzZJvu -trayiconurl=http://down1.7654browser.shzhanmeng.com/tui/test/ad.ico ' \
               '-closeimagesize=14x14_w -showtraypopupskin=1 -trayopentype=2 -showneglect=0 -mutex=%s -project=%s' % (exe, mutex, project)

    arg_news = '%s -taskid=tray.py -closebuttonjsonurl=http://down1.7654browser.shzhanmeng.com/tui/close.json -killprocess=1 -usewebmode=1 -trayopentype=1 -showneglect=1 ' \
               '-landingpage=https://s.click.taobao.com/CVzZJvu -mutex=%s -project=%s %s -previewurl=%s -trayiconurl=%s -traytext=%s' % (
                   exe, mutex, project, adurl, previewurl, trayiconurl, traytext)

    close = "-closebuttonjsonurl=http://down1.7654browser.shzhanmeng.com/test/close.json "
    close_fei = "-closebuttonjsonurl=http://down1.7654browser.shzhanmeng.com/test/close_fei.json "
    if proj in range(10, 15):
        arg += close_fei
    else:
        arg += close

    arg += '-trayopentype=0 '  # 无预览图弹出“忽略+查看详情+退出闪标"菜单,
    # arg += '-trayopentype=1 ' #不写或=1 左右键都打开落地页
    # arg += '-trayopentype=2 '  # =2时（有预览图时，按=1方式处理;无预览图无忽略点击右键菜单中的 "查看详情", 则打开落地页，同时上报.view-click,点退出)
    # arg += '-trayopentype=3 '  # =3时(有预览图时，按=1方式处理;无预览图弹出“忽略”菜单，点击“忽略”后左右键都打开落地页;无忽略点击右键菜单中的 "查看详情", 则打开落地页，同时上报.view-click)

    # arg += '-showneglect=0 '  # 无预览图=1弹出“忽略”菜单，点击“忽略”后左右键都打开落地页(只有在没有预览图且FLG_trayopentype != 3的情况下才起作用)

    '''
    -showtraypopupskin  usewebmode=0时是否显示托盘的预览窗口
    -trayopentype   控制闪标左右按键行为(=1时，左右键都打开落地页， =2时（有预览图时，按=1方式处理;无预览图弹出“忽略”菜单，点击“忽略”后左右键都打开落地页;无忽略点击右键菜单中的 "查看详情", 则打开落地页，同时上报.view-click)
    -showneglect 无预览图=1弹出“忽略”菜单，点击“忽略”后左右键都打开落地页(只有在没有预览图且FLG_trayopentype != 3的情况下才起作用)

    '''

    return arg
    # return arg_skin
    # return arg_news


def main():
    cmd = argue()
    crt.Screen.Send(cmd + "\r")


env = enve()
proj, project = project()
exe, host = exe_host()
main()
