import struct
import json

out_file = 'patch.json'
nes = open('1985-Super Mario Bros. (Japan, USA).nes', 'rb').read()
print "Original ROM length = ", len(nes)

ips = open('Super Mario Bros - Peach and Daisy and The Royal Games (SMB1 Hack).ips', 'rb').read()


mods_list = []

idx = 5

while True:
    
    mod = {}
    ob = ips[idx:idx+3]
    
    if ob == 'EOF':
        print 'EOF'
        break
        
    offset = struct.unpack('>I', '\0' + ob)[0]
    mod['start'] = offset
    idx += 3
    
    ob = ips[idx:idx+2]
    size = struct.unpack('>H', ob)[0]
    idx += 2
    
    # Run Line Encoding (repeated bytes)
    if size == 0:
        print "RLE"
        # mod['type'] = 'RLE'
        
        ob = ips[idx:idx+2]
        repeats = struct.unpack('>H', ob)[0]
        mod['bytes'] = repeats
        idx += 2
        
        ob = ips[idx:idx+1]
        repbyte = struct.unpack('>H', '\0' + ob)[0]
        idx += 1
        
        # mod['orig'] = ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+repeats])
        # mod['new'] = ' '.join("{:02x}".format(repbyte) for ii in range(repeats))
       
        print "{:04x} : {:04x}".format(offset, offset+repeats-1), '  (', offset, offset+repeats-1, ')'
        print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+repeats])
        print '+', ' '.join("{:02x}".format(repbyte) for ii in range(repeats))
        print
    
    # Normal patch
    else:
        patch = ips[idx:idx+size]

        # mod['type'] = 'record'
        mod['bytes'] = size
        # mod['orig'] = ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+size])
        # mod['new'] = ' '.join("{:02x}".format(ord(dd)) for dd in patch)
        
        print "{:04x} : {:04x}".format(offset, offset+size-1), '  (', offset, offset+size-1, ')'
        print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+size])
        print '+', ' '.join("{:02x}".format(ord(dd)) for dd in patch)
        print
        idx += size
    
    mods_list.append(mod)

with open(out_file, 'w') as f:
    json.dump(mods_list, f)

