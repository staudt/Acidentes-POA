import os
import zlib


if __name__ == '__main__':
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.csv.zlib'):
            with open(filename, 'rb') as f_read:
                with open('%s' % filename[:-len('.zlib')], 'wb') as f_write:
                    print 'Decompressing file "%s"' % (filename)
                    f_write.write(zlib.decompress(f_read.read()))
