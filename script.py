import re
def read_file(file_name):
	tmp = ''
	data = []
	# mo file
	with open(file_name, 'r') as file:
		lines = file.readlines()
	filtered_lines = [line for line in lines if not line.strip().startswith("//") and not line.strip().startswith("#")]
	return filtered_lines

def extract_module(file_name):
	module = []

	content_ = read_file(file_name)

	for ind in content_:
		if (ind.find("endmodule") == -1) :
			if "module" in ind:
				tmp = ind.split("module")[1].split(" (")[0]
				module.append(tmp)
				# print(tmp)
	return module
	# print()

def get_top (list_module):
	print("top")

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
def insert_voter(name_voter, inp,output):
	instance = name_voter+" "+name_voter+"_"+str(i)+"( .in_0("+inp+"_0"+"), "+".in_1("+inp+"_1"+"), "+".in_2("+inp+"_2)"+".out("+output+");"
	return instance

def insert_FGTMR(origin_design, port_top, output_file, top_module):
	modules = extract_module(origin_design)
	for module in modules :
		content = get_port(origin_design, "module "+module)
		port_ff = extract_port_ff(content)[2]

		content = content.split(";")
		content_0 = content.split("\n\n")[0]

		content_1 = content.split("\n\n")[1]
		# for ind in port_ff
		for ind in port_ff:
			print(ind)
			tmp=extract_in_out_ff(ind)
			# print(tmp[1])
			content_0 = content_0 + "\n"

			for i in range(3):

				content_1 = content_1.replace(tmp[1],tmp[1]+"_0")
				print(tmp[0])
			# insert voter
			tmp1 = insert_voter("dti_voter","tmp[0]","aa")
			# content_1=content_1.replace("\t"+tmp1,"endmodule")+"\nendmodule"
		print (content_1)
	content = read_file

	print("anh hien")

def insert_CGTMR(origin_design, port_top, output_file, top_module):
	print("CGTMR")
	contents = read_file(origin_design)
	new_contents = [line.replace(top_module, "rt_tmp") for line in contents]
	# print(content)
	with open(output_file, 'w') as file:
		lines = file.writelines(new_contents)

	# khai bao tin hieu ouput cua cac instance 
	wire_signal = []
	wire_tmp_1=""
	for indx in range(len(port_top[1])):
		for key,value in port_top[1][indx].items():
			if value > 1:
				wire_tmp = "wire "+"["+str(value-1)+":0] " +key+"_1"+", "+key+"_2"+", "+key+"_3"+";"
				
			else :
				wire_tmp = "wire "+ key+"_1"+", "+key+"_2"+", "+key+"_3"+"; "
			wire_signal.append(wire_tmp)
		# print(wire_signal)

    # copy file top module
	string = get_port(origin_design, "module rt_qos_controller")
	# print(string)
	split_text = string.split("\n\n")[0]
	content = split_text+"\n"

	for indx in wire_signal:
		content = content + "\t" + indx +"\n"


    # create instances
	instances = []
	voters = []
	tmp=""
	for k in range(3):
		for i in range(len(port_top[0])):
			for inp, value in port_top[0][i].items():
				if inp == "clk" or inp == "reset_n":
					tmp_ip = "."+inp+"("+inp+")"+", "
				# print(inp)
				else:
					tmp_ip = "."+inp+"("+inp+"_"+str(k)+")"+", "
				tmp = tmp+tmp_ip
		for i in range(len(port_top[1])):
			for out, value in port_top[1][i].items():
				tmp_out = "."+out+"("+out+"_"+str(k)+")"+", "
				tmp = tmp + tmp_out
			tmp = tmp[:-2]
			instance = "rt_tmp" + " " + "instance_"+str(k)+ " (" +tmp+");" 
		instances.append(instance)
	# print(instances[1])
	for ind in instances:
		content = content + "\t" + ind +"\n"
	content = content +"endmodule"
	print(content)

	# insert voter at output
	ind =0
	for i in range(len(port_top[1])):
		for out, value in port_top[1][i].items(): 
			if value > 1:
				for k in range(value):
					tmp_name = out+"["+str(k)+"]"
					tmp=insert_voter("dti_voter",tmp_name,out)
					ind=ind+1
					voters.append(tmp)
			else:
				tmp=insert_voter("dti_voter",out,out)
				ind=ind+1
				voters.append(tmp)
	print (voters)


def insert_FGDTMR(origin_design, output_file, top_module):
	print("FGDTMR")
	modules = extract_module(origin_design)
	for module in modules :
		# print(module)
		content = get_port(origin_design, "module"+module)
		# print(content)
		port_ff = extract_port_ff(content)[2]
		content_0 = content.split("\n\n")[0]

		content_1 = content.split("\n\n")[1]
		for ind in port_ff:
			print(ind)
			tmp=extract_in_out_ff(ind)
			# print(tmp[1])
			content_0 = content_0 + "\n" 

			content_1 = content_1.replace(tmp[1],tmp[1]+"_0")
			print(tmp[0])
			# insert voter
			tmp1 = insert_voter("dti_voter","tmp[0]","aa")
			# content_1=content_1.replace("\t"+tmp1,"endmodule")+"\nendmodule"
		print (content_1)




# Tach lay cac dau vao dau ra 
def get_port(file_path, module_name):
	with open(file_path, 'r') as file:
		content = file.read()
		module_start_index = content.rfind(module_name)
		if module_start_index != -1:
      		    # Tìm vị trí bắt đầu của module
      		    module_start = module_start_index 
      		    # Tìm vị trí kết thúc của module gần nhất
      		    module_end_index = content.find('endmodule', module_start)
      		    if module_end_index != -1:
      		        module_end = module_end_index + len('endmodule')
      		        # Lấy nội dung module
      		        module_content = content[module_start:module_end]
      		        return module_content
def extract_port_ff(module):
	input_q 	= []
	output_q 	= []
	fliflop 	= []
	wire 		= []

	# lines_data = read_file(file_netlist)
	lines_data = module.split(";")
	# print(lines_data[0])
	for indx in lines_data:
		if 'input' in indx:
			# in_put = re.split(r",|;|\s", indx)
			in_put = indx.split("input ")[1].split(";")[0]
			dict1=get_size_port(in_put)
			input_q.append(dict1)
		if 'output' in indx:
			out_put = indx.split("output ")[1].split(";")[0]
			dict1=get_size_port(out_put)
			output_q.append(dict1)
		if 'dti_12g_ff' in indx:
			ff = indx.split(";")[0]
			# print(ff)
			fliflop.append(ff)
		if "wire" in indx:
			w = indx.split("wire ")[1].split(";")[0]
			dict1=get_size_port(w)
			wire.append(dict1)
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

def get_size_port(signal_name):
	value = 1
	dict1 = {}
	
	if "]" in signal_name:
		size = signal_name.split("] ")[0].split("[")[1].split(":")[0]
		value = int(size) +1
		tmp_name = signal_name.split("] ")[1]
		tmp_name = tmp_name.replace(" ", "").split(",")
	else:
		value = 1
		tmp_name = signal_name.replace(" ", "").split(",")
	for indx in tmp_name:
		dict1[indx] = value

	return dict1

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

print("anh hien")
# if _name_ == '__main__':

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
	# data1= extract_port_ff(file_name)
	# print(data1[2][0])
	# for i in data1[2][0]:
	# 	tmp = extract_in_out_ff(i)
	# 	print(tmp)
	# 	print(create_signal(tmp[0]))
	# 	print(create_signal(tmp[1]))
	# extract_module(file_name1)

string = get_port(file_name1, "module rt_dyn_pri_fsm")
# print(string)
# print(string)
split_text = string.split("\n\n")[1]
# print(split_text)
# port = (extract_port_ff(string))
# print(extract_port_ff(string)[2])

# insert_CGTMR(file_name1,port,file_main,"rt_qos_controller")
insert_FGDTMR(file_name1,file_main,"rt_qos_controller")