d2b = lambda x : '%08d' % int(bin(x)[2:])
b2d = lambda x : int(x, 2)
flip_bits = lambda x : ''.join('1' if i == '0' else '0' for i in x)
	
def cidr2mask(cidr):
	host_bits = 32-cidr
	return bin( int(32*'1',2) ^ int(host_bits*'1',2) )[2:] # XOR
	
def b_full2dec_dotted(x):
	x_arr = [x[i:i+8] for i in range(0, len(x), 8)]
	return '.'.join([str(b2d(x_arr[i])) for i in range(0, len(x_arr))])
	
def to_dec_dotted(x):
	if type(x) is int and not type(x) is str:
		x = bin(x)[2:]
	x_arr = [x[i:i+8] for i in range(0, len(x), 8)]
	return '.'.join([str(b2d(x_arr[i])) for i in range(0, len(x_arr))])
	
def dec_dotted2bin_full(x):
	x_arr =	[d2b(int(i)) for i in x.split('.') ]
	return ''.join(x_arr)

input = '172.0.0.17/28'

(ip, cidr) = input.split('/')

cidr = int(cidr)

if not (1 <= cidr <= 32):
	print('Invalid CIDR used (1-32)')
	exit(1)

count_a = config = {}

config['network'] =  config['gateway'] = config['broadcast'] = ip
count_a['usable'] = count_a['all'] = 2**(32-cidr)

address_bin		= 	dec_dotted2bin_full(ip)
subnetmask_bin 	=	cidr2mask(cidr)

if count_a['all'] > 4:
	network_address = int(address_bin,2) & int(subnetmask_bin,2) # AND
	last_address = int(address_bin,2) | int( flip_bits( subnetmask_bin ) ,2) #OR
	i = 0
	usable_addresses = []
	for ip in range( network_address , last_address + 1 ) :
		if i == 0:
			config['network'] = ip
		elif i == 1:
			config['gateway'] = ip
		elif ip == last_address:
			config['broadcast'] = ip
		else:
			usable_addresses.append(ip)
		i+=1
		
count_a['usable'] = len(usable_addresses)

print [ (name, '->', to_dec_dotted(value)) for name, value in config.items() ]
print [ to_dec_dotted(ip) for ip in usable_addresses ]
print [ (n, '->',c) for n,c in count_a.items() ]
