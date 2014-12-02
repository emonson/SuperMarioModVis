import struct

nes = open('1985-Super Mario Bros. (Japan, USA).nes', 'rb').read()
ips = open('Super Mario Bros - Peach and Daisy and The Royal Games (SMB1 Hack).ips', 'rb').read()

idx = 5

while True:

    ob = ips[idx:idx+3]
    
    if ob == 'EOF':
        print 'EOF'
        break
        
    offset = struct.unpack('>I', '\0' + ob)[0]
    idx += 3
    
    ob = ips[idx:idx+2]
    size = struct.unpack('>H', ob)[0]
    idx += 2
    
    # Run Line Encoding (repeated bytes)
    if size == 0:
        print "RLE"
        ob = ips[idx:idx+2]
        repeats = struct.unpack('>H', ob)[0]
        idx += 2
        
        ob = ips[idx:idx+1]
        repbyte = struct.unpack('>H', '\0' + ob)[0]
        idx += 1
       
        print "{:04x} : {:04x}".format(offset, offset+repeats-1), '  (', offset, offset+repeats-1, ')'
        print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+repeats])
        print '+', ' '.join("{:02x}".format(repbyte) for ii in range(repeats))
        print
    
    # Normal patch
    else:
        patch = ips[idx:idx+size]
        print "{:04x} : {:04x}".format(offset, offset+size-1), '  (', offset, offset+size-1, ')'
        print '-', ' '.join("{:02x}".format(ord(dd)) for dd in nes[offset:offset+size])
        print '+', ' '.join("{:02x}".format(ord(dd)) for dd in patch)
        print
        idx += size
    
