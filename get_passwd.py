import os
import struct
import re


g_passwd_filepath = 'passwd.txt'
g_error_passwd_filepath = 'error_passwd.txt'

g_f = open(g_passwd_filepath, 'a')
g_e = open(g_error_passwd_filepath, 'a')

#g_user_pos = 0x3d24c0
#g_pass_pos = 0x3d24e0
g_max_len = 0x20


def search_admin_account_pos(_filepath):
    _L = []
    re_compile = re.compile(b"\x00\x61\x64\x6D\x69\x6E\x00")
    # file_size = os.path.getsize(_filepath)
    with open(_filepath, 'rb') as f:
        s = f.read()
        for match_obj in re_compile.finditer(s):
            offset = match_obj.start()
            _L.append(offset)
    return _L


def get_password(_filepath, _pos_list):
    bin = open(_filepath, 'rb')
    file_size = os.path.getsize(_filepath)
    for _pos in _pos_list:
        bin.seek(_pos)
        _user = bin.read(g_max_len)
        _user = _user.replace('\x00', '')
        if(_user != 'admin'):
            print 'error_pos:' + _filepath + ':' + hex(_pos) + _user
            g_e.write(str(file_size) + ':' + _filepath)
            g_e.write('\n')
            continue
        bin.seek(_pos + 0x20)
        _pass = bin.read(g_max_len)
        _pass = _pass.replace('\x00', '')
        _pass = _pass.replace('\xFF', '')
        g_f.write(_filepath + ':' + _user + ':' + _pass)
        #g_f.write(_user + ':' + _pass)
        g_f.write('\n')
    return


def get_info(_filepath):
    _list_post = search_admin_account_pos(_filepath)
    get_password(_filepath, _list_post)
    return


def get_con_filename(_file_dir, _ext):
    L = []
    for root, dirs, files in os.walk(_file_dir):
        for file in files:
            if os.path.splitext(file)[1] == _ext:
                L.append(os.path.join(root, file))
    return L


def main():

    _list_plantext = get_con_filename('./', '.plantext')
    i = 0
    t_count = len(_list_plantext)
    for _l in _list_plantext:
        i = i + 1
        _l = _l.replace('./', '')
        get_info(_l)
        print '[' + str(i) + '/' + str(t_count) + ']'
        # break

    g_f.close()
    g_e.close()
    print 'Done'

if __name__ == '__main__':
    main()
