import os
import zlib


if __name__ == '__main__':
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.csv'):
            with open(filename, 'rb') as f_read:
                with open('%s.zlib' % filename, 'wb') as f_write:
                    print 'Compressing file "%s" to "%s.zlib"' % (filename, filename)
                    f_write.write(zlib.compress(f_read.read()))
