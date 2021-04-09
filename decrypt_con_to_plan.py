import struct
import os
import datetime
import random
import uuid

'''
class XORDecode {

    public static void main(String[] args) throws IOException{
        
        File file = new File("decryptedoutput");
        byte[] fileContents = Files.readAllBytes(file.toPath());
        byte[] xorOutput = new byte[fileContents.length];

        byte[] key = {(byte)0x73, (byte)0x8B, (byte)0x55, (byte)0x44};

        for(int i = 0; i < fileContents.length; i++) {
            xorOutput[i] = (byte)((int)fileContents[i] ^ (int)key[i % key.length]);
        }

        FileOutputStream stream = new FileOutputStream("plaintextOutput");
        stream.write(xorOutput);


    }
}
'''
g_key = [0x73, 0x8B, 0x55, 0x44]


def de_decryptedoutput(_defilepath, _outplaintext_path):
    plaintextOutput_file = open(_outplaintext_path, 'ab')
    file_size = os.path.getsize(_defilepath)
    with open(_defilepath, 'rb') as f:
        data = f.read(1)
        i = 0
        while data != '':
            num, = struct.unpack('B', data)
            _key = g_key[i % len(g_key)]
            _xor_code = num ^ _key
            plaintextOutput_file.write(struct.pack('B', _xor_code))
            data = f.read(1)
            i += 1
    plaintextOutput_file.close()
    # print 'Done'


def aes_decode(_in_file_str, _out_file_str):
    cmd = 'openssl enc -d -in %s -out %s -aes-128-ecb -K 279977f62f6cfd2d91cd75b889ce0c9a -nosalt -md md5' % (
        _in_file_str, _out_file_str)
    os.system(cmd)
    # print 'openssl:' + _out_file + ' Done'


def del_file(_file_path):
    cmd = 'rm -rf %s' % (_file_path)
    os.system(cmd)
    # print 'delfile OK'


def decrypt_byfilename(_confilepath, _planfilepath):

    unique_filename = str(uuid.uuid4())
    aes_decode(_confilepath, unique_filename)
    de_decryptedoutput(unique_filename, _planfilepath)
    del_file(unique_filename)


def get_con_filename(_file_dir):
    L = []
    for root, dirs, files in os.walk(_file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.con':
                L.append(os.path.join(root, file))
    return L


def main():
    #aes_decode('configurationFile', 'decryptedoutput1')
    #de_decryptedoutput('decryptedoutput1', 'plaintextOutput1')
    # del_file('decryptedoutput1')
    # print gen_uni_filename()
    #decrypt_byfilename('218.73.151.187_84.con', '218.73.151.187_84.plantext')
    _list_dir = get_con_filename('./')

    i = 0
    t_count = len(_list_dir)

    for _l in _list_dir:
        i = i + 1
        _l = _l.replace('./', '')
        _url_list = _l.split('.con')
        _plantext_filename = _url_list[0] + '.plantext'
        decrypt_byfilename(_l, _plantext_filename)
        print '[' + str(i) + '/' + str(t_count) + ']'

    print 'Done'


if __name__ == '__main__':
    main()
