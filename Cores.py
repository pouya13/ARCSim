""""
Random Instruction Generator (ARCSim)

Written by Pouya Narimani (pouyanarimani.kh@gmail.com).

(c) Copyright SCL, All Rights Reserved. NO WARRANTY.

"""


class Cores(object):
	def __init__(self):
		super(Cores, self).__init__()
		
		self.cores = ['atmega8']

		self.fetch_instructions_set = (# one cycle instructions
	                                 'add', 'adc', 'sub', 'subi', 'sbc', 'sbci', 'and', 'andi', 'or', 'ori', 'eor',
	                                 'com', 'neg', 'sbr', 'cbr', 'inc', 'dec', 'tst', 'clr', 'ser', 'cp',
	                                 'cpc', 'cpi', 'mov', 'movw', 'ldi',
	                                 # 'in', 'out',
	                                 'lsl', 'lsr', 'rol', 'ror',
	                                 'asr', 'swap', 'bset', 'bclr', 'bst', 'bld',
	                                 'sec', 'clc',
	                                 'sen', 'cln',
	                                 'sez', 'clz',
	                                 'sev', 'clv',
	                                 'ses', 'cls',
	                                 'set', 'clt',
	                                 'seh', 'clh'
	                                 # 'sei', 'cli'
	                                 )

		self.instructions_set = (# one cycle instructions = 50
                                 'add', 'adc', 'sub', 'subi', 'sbc', 'sbci', 'and', 'andi', 'or', 'ori', 'eor',
                                 'com', 'neg', 'sbr', 'cbr', 'inc', 'dec', 'tst', 'clr', 'ser', 'cp',
                                 'cpc', 'cpi', 'mov', 'movw', 'ldi',
                                 # 
                                 # 'in', 'out',
                                 'lsl', 'lsr', 'rol', 'ror',
                                 'asr', 'swap', 'bset', 'bclr', 'bst', 'bld',
                                 'sec', 'clc',
                                 'sen', 'cln',
                                 'sez', 'clz',
                                 'sev', 'clv',
                                 'ses', 'cls',
                                 'set', 'clt',
                                 'seh', 'clh',
                                 # 
                                 # 'sei', 'cli',
                                 # ############################
                                 # two cycle instructions = 53
                                 'sbiw' , 'adiw', 
                                 'mul', 'muls', 'mulsu', 'fmul', 'fmuls', 'fmulsu',
                                 'rjmp', # 'ijmp'
                                 'brbs', 'brbc', 'breq', 'brne', 'brcs', 'brcc', 'brsh', 'brlo', 'brmi', 'brpl',
                                 'brge', 'brlt', 'brhs', 'brhc', 'brts', 'brtc', 'brvs', 'brvc', 'brie', 'brid',
                                 'ld_x', 'ld_x+', 'ld_-x', 'ld_y', 'ld_y+', 'ld_-y', 'ldd_y','ld_z', 'ld_z+',
                                 'ld_-z', 'ldd_z', 'lds', 'st_x', 'st_x+', 'st_-x', 'st_y', 'st_y+',
                                 'st_-y', 'std_y', 'st_z', 'st_z+', 'st_-z', 'std_z', 'sts',
                                 # 
                                 # 'sbi', 'cbi',
                                 # 'push', 'pop',
                                 # ############################
                                 # three cycle instructions = 8
                                 'cpse', 'sbrc', 'sbrs', 'sbic', 'sbis', 'lpm', 'lpm_z', 'lpm_z+')
                                 # 
                                 # 'nop', 'sleep', 'wdr',
                                 # 'rcall', 'icall',
                                 # 'ret', 'reti',
                                 # 'spm'

	def get_cores(self):
		return self.cores

	def get_len(self):
		return len(self.cores)

	def get_instruction_sets(self):
		return (self.instructions_set, self.fetch_instructions_set)
