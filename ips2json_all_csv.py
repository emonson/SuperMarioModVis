import struct
import pandas as pd
import os

out_file = 'patches_all.csv'

nes = open('1985-Super Mario Bros. (Japan, USA).nes', 'rb').read()
print "Original ROM length = ", len(nes)

mods_list = []

with open('patch_names.txt', 'r') as patch_names:
    for patch_idx, patch_path in enumerate(patch_names):
        
        print patch_path
        ips = open(patch_path.strip(), 'rb').read()
        idx = 5

        while True:
    
            mod = {}
            mod['mod_file'] = os.path.split(patch_path)[1]
            
            ob = ips[idx:idx+3]
    
            if ob == 'EOF':
#                 print 'EOF'
                break
        
            offset = struct.unpack('>I', '\0' + ob)[0]
            mod['start'] = offset
            idx += 3
    
            ob = ips[idx:idx+2]
            size = struct.unpack('>H', ob)[0]
            idx += 2
    
            # Run Line Encoding (repeated bytes)
            if size == 0:
#                 print "RLE"
                mod['type'] = 'RLE'
        
                ob = ips[idx:idx+2]
                repeats = struct.unpack('>H', ob)[0]
                mod['bytes'] = repeats
                idx += 2
        
                ob = ips[idx:idx+1]
                repbyte = struct.unpack('>H', '\0' + ob)[0]
                idx += 1
        
                # mod['orig'] = ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+repeats])
                # mod['new'] = ' '.join("{:02x}".format(repbyte) for ii in range(repeats))
       
#                 print "{:04x} : {:04x}".format(offset, offset+repeats-1), '  (', offset, offset+repeats-1, ')'
#                 print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+repeats])
#                 print '+', ' '.join("{:02x}".format(repbyte) for ii in range(repeats))
#                 print
    
            # Normal patch
            else:
                patch = ips[idx:idx+size]

                mod['type'] = 'record'
                mod['bytes'] = size
                # mod['orig'] = ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+size])
                # mod['new'] = ' '.join("{:02x}".format(ord(dd)) for dd in patch)
        
#                 print "{:04x} : {:04x}".format(offset, offset+size-1), '  (', offset, offset+size-1, ')'
#                 print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+size])
#                 print '+', ' '.join("{:02x}".format(ord(dd)) for dd in patch)
#                 print
                idx += size
    
            mods_list.append(mod)

df = pd.DataFrame(mods_list)
df.to_csv(out_file, sep=',', encoding='utf-8')
