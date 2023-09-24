import re
def read_file(file_name):
	tmp = ''
	data = []
	# mo file
	with open(file_name, 'r') as file:
		lines = file.readlines()
	filtered_lines = [line for line in lines if not line.strip().startswith("//") and not line.strip().startswith("#")]
	# string = str(filtered_lines)
	# print(lines)
		# is_inmodule = False
		#  duyet qua tung dong
		# for line in lines :
		# 	#  lay nhung dong nam trong module
		# 		if 'module' in line or is_inmodule  :
		# 				line = line.lstrip()
		# 				tmp += line
		# 				is_inmodule = True
		# 		elif 'endmodule' in line:
		# 			is_inmodule = False
		# #  Phan tach bang dau cham phay 
		# data = tmp.split(';')
	return filtered_lines

def extract_module(file_name):
	module = []

	content_ = read_file(file_name)

	for ind in content_:
		if (ind.find("endmodule") == -1) :
			if "module" in ind:
				tmp = ind.split("module")[1].split(" (")[0]
				module.append(tmp)
				print(tmp)
	return module
	# print()
def create_TMR_design(file_TMR,option):
	print("anh hen")

def extract_in_out_ff(instance_ff):
	tmp = instance_ff.split(".")
	inp = ""
	out = ""
	for indx in tmp:
		if "D(" in indx:
			inp = indx.split("(")[1].split(")")[0]
		if "Q(" in indx:
			out = indx.split("(")[1].split(")")[0]
	return inp, out

def create_signal (name_conponent):
	tmp = [name_conponent + '_1',name_conponent + '_2',name_conponent + '_3']
	Inout = "wire " + tmp[0] +", "+ tmp[1]+", "+tmp[2]+";"
	return Inout
def create_3instances(input, output):
	print("ahhhh")

def add_voter(file_main, file_netlist, file_voter):
	content_netlist = read_file(file_netlist)
	content_voter = read_file(file_voter)
	# with open (file_voter,"r") as file1:
	# 	content = file1.read()
	# comment_pattern = r"^\s*//.*$"
	# cleaned_content = re.sub(comment_pattern, "", content, flags=re.MULTILINE)
	with  open(file_main, "w") as file2:
		file2.writelines(content_netlist)
		file2.writelines(content_voter)
	with open (file_main,'r') as file:
		content = read_file(file_main)
	return content

def insert_FGTMR(file_main, file_voter):
	print("anh hien")

def insert_CGTMR():
	print("CGTMR")

def insert_FGDTMR():
	print("FGDTMR")
# Tach lay cac dau vao dau ra 
def extract_port_ff(file_netlist):
	input_q =[]
	output_q = []
	fliflop = []
	wire = []

	lines_data = read_file(file_netlist)



	for indx in lines_data:
		if 'input' in indx:
			in_put = re.split(r",|;|\s", indx)
			in_put = indx.split("input ")[1].split(";")[0].split(", ")
			input_q.append(in_put)
		if 'output' in indx:
			out_put = indx.split("output ")[1].split(";")[0].split(", ")
			output_q.append(out_put)
		if 'dti_12g_ff' in indx:
			ff = indx.split("\n")[0].split("; ")
			fliflop.append(ff)
		if "wire" in indx:
			w = indx.split("wire ")[1].split(";")[0].split(", ")
			wire.append(w)
	return input_q,output_q,fliflop,wire

def extract_intance(data):
	data_1 = []
	for indx in data:
		if 'assign' in indx:
			tmp = indx.split("assign ")
			data_1.append(tmp[1])

		if 'dti' in indx:
			in_put = []
			output = ''
			name =''
			if "," in indx:
				words = indx.split(",")
				for j in range(len(words)-1):
					if words[j+1][0] != " ":
						words[j+1] = " " + words[j+1]
					tmp = ",".join(words)
			tmp = indx.split(" ")
			# tach	ten	, input, output cua cac instance	
			for i in tmp:
				if 'dti' in i:
					name = i.split("_")[3].split("x8")[0]
					name = re.split("\d+", name)[0]
					if name == "inv":
						name = "~"
					elif name == "and":
						name = "&"
					elif name == "or":
						name = "|"
					elif name == "xor":
						name = "^"
				if '.' in i:
					if 'Z' in i:
						output = i.split('(')[1].split(')')[0]
					else:
						temp = i.split('(')[1].split(')')[0]
						in_put.append(temp) 
			data_1.append(extract_boolean(in_put, output,name))
	return data_1
	
def extract_boolean(in_put, out_put, name):
	boolean = ""
	size_in = len(in_put)
	if size_in >1:
		for indx in range(size_in):
			boolean += str(in_put[indx]) 
			if indx < size_in-1:
				boolean += " "+ str(name)+" "
			else:
				break
		out_put = out_put + " = " +"(" + boolean + ")"
	else:
		boolean = name + "(" + in_put[0] +")"
		out_put = out_put +" = " + boolean
	return out_put


# Tach cac bieu thuc dau ra phu thuoc dau vao
def extract (data_q, output):
	final_data = []
	for tmp in data_q:
		for out in output:
			if out in tmp:
				temp = tmp.split(" = ")
				left = temp[1]
				string = tmp
				count = 0
				while(count < len(data)):
					count = count +1
					for i in data_q:
						i = i.split(" = ")
						if i[0] in left:
							string = string.replace(i[0],i[1])
							left = string.split(" = ")[1]
				final_data.append(string)
	return final_data

if __name__ == '__main__':
	file_name ='test.v'
	file_voter = 'dti_voter_netlist.v'
	file_main = 'main.v'
	file_name1 = "rt_qos_controller_netlist.v"

	# add_voter(file_name,file_voter)
	# file_name ='addr_conv_l2p_252_netlist.v'
	# file_name ='addr_conv_l2p_64_netlist.v'
	# data = read_file(file_name)
	# with open(file_main, 'w') as file:
 #    	file.write(data)
	# data=add_voter(file_main,file_name,file_voter)
	# print(data)
	data1= extract_port_ff(file_name)
	# print(data1[2][0])
	# for i in data1[2][0]:
	# 	tmp = extract_in_out_ff(i)
	# 	print(tmp)
	# 	print(create_signal(tmp[0]))
	# 	print(create_signal(tmp[1]))
	extract_module(file_name1)

	# main = read_file(file_main)
	# in_out_ff=extract_in_out_ff(data)
	# print(in_out_ff[2][0])
	# for i in data:
	# 	print(i)
	# print(data)
	# data_queu = extract_intance(data)
	# in_out = extract_in_out(data)
	# final = extract(data_queu ,in_out[1])
	# for i in final:
	# 	print(i)




