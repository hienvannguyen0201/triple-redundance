import re
import sys
import argparse
def read_file(file_name):
	tmp = ''
	data = []
	# mo file
	with open(file_name, 'r') as file:
		lines = file.readlines()
	filtered_lines = [line for line in lines if not line.strip().startswith("//") and not line.strip().startswith("#")]
	return filtered_lines

def write_to_file(file_path, content, option):
    with open(file_path, option) as file:
        file.write(content)
    file.close()
def extract_module(file_name):
	module = []

	content_ = read_file(file_name)

	for ind in content_:
		if (ind.find("endmodule") == -1) :
			if "module" in ind:
				tmp = ind.split("module")[1].split(" (")[0]
				module.append(tmp)
	return module

def get_top (list_module):
	print("top")

def create_TMR_design(file_TMR,option):
	print("anh hen")

def extract_in_out_ff(instance_ff):
	tmp = instance_ff.split(".")
	inp = ""
	out = ""
	# print(instance_ff)
	name = instance_ff.strip().split(" ")[1]
	# print(name)
	for indx in tmp:
		if "D(" in indx:
			inp = indx.split("(")[1].split(")")[0].strip()
		if "Q(" in indx:
			out = indx.split("(")[1].split(")")[0].strip()
	return inp, out, name

def get_inout(instance):
	tmp = instance.strip().split(".")
	inp = []
	out = ""
	name = tmp[0].split(" ")[1]
	for indx in tmp:
		# print(indx)
		if"Z(" in indx or "Q(" in indx:
			# print(indx)
			out = indx.replace("\n","").split("(")[1].split(")")[0].strip()
		elif "(" in indx:
			inp_tmp = indx.replace("\n","").split("(")[1].split(")")[0]
			inp.append(inp_tmp)
	inp=[element for element in inp if element.strip() != ""]
	return inp,out,name

def create_signal (name_conponent):
	tmp = [name_conponent + '_1',name_conponent + '_2',name_conponent + '_3']
	Inout = "wire " + tmp[0] +", "+ tmp[1]+", "+tmp[2]+";"
	return Inout
def create_3instances(input, output):
	print("ahhhh")

def add_voter(file_main, file_netlist, file_voter):
	content_netlist = read_file(file_netlist)
	content_voter = read_file(file_voter)
	with  open(file_main, "w") as file2:
		file2.writelines(content_netlist)
		file2.writelines(content_voter)
	with open (file_main,'r') as file:
		content = read_file(file_main)
	return content
def insert_voter(name_voter,ind, inp,output):
	instance = name_voter+" "+name_voter+"_"+str(ind)+"( .in_0("+inp+"_0"+"), "+".in_1("+inp+"_1"+"), "+".in_2("+inp+"_2), "+".out("+output+"))"
	return instance
def check_value_in_list(lst, value):
    if value in lst:
        return True
    else:
        return False
def insert_FGTMR(origin_design, output_file, top_module):
	modules = extract_module(origin_design)

	final_content = ""
	for module in modules :
		# print(module)
		content = get_port(origin_design, "module"+module)
		# print(content)
		port_ff = extract_port_ff(content)[2]

		# content = content.split(";")
		content_0 = content.split("\n\n")[0]
		content_0 = content_0 + "\n"

		content_1 = content.split("\n\n")[1]
		# for ind in port_ff
		k =0
		tmp_content = content_1.split(";")
		for ind in port_ff:
			# print(ind)
			# print("anhhhh")
			tmp1=extract_in_out_ff(ind)
			# print(tmp1[1])
			# tmp1[1] = tmp1[1].strip()
			# print(tmp1[1])
			

			ins_ffs = ""

			for i in range(3):
				# if len(instance[1]):
				tmp = ind.replace(tmp1[1], tmp1[1]+"_"+str(i))+";"
				# print(tmp1[2])
				tmp = tmp.replace(tmp1[2], tmp1[2]+"_"+str(i))
				ins_ffs = ins_ffs+tmp
			voter = insert_voter("dti_voter",k, tmp1[1], tmp1[1])
			k = k+1
			ins_ffs = ins_ffs+"\n  "+voter
			# print(ins_ffs)
			
			for i in range(len(tmp_content)):
				if tmp1[1] in tmp_content[i]:
					# print(tmp1[1])
					tmp_content[i] = ins_ffs
					# print(tmp_content[i])
					break

			wire_tmp = "  wire "+ tmp1[1]+"_0"+", "+tmp1[1]+"_1"+", "+tmp1[1]+"_2"+"; \n"
			content_0 = content_0 +wire_tmp

		content_1 = ";".join([str(element) for element in tmp_content])
		final_content = final_content + content_0+content_1 +"\n"
	# print(final_content)
	write_to_file(output_file,final_content,'w')

def insert_CGTMR(origin_design, output_file, top_module):
	print("CGTMR")
	string = get_port(origin_design, "module rt_qos_controller")
	# print(string)
	port_top = (extract_port_ff(string))
	contents = read_file(origin_design)
	new_contents = [line.replace(top_module, "rt_tmp") for line in contents]
	# print(content)
	with open(output_file, 'w') as file:
		lines = file.writelines(new_contents)
	file.close()

	# khai bao tin hieu ouput cua cac instance 
	wire_signal = []
	wire_tmp_1=""
	# print(port_top[1])
	for indx in range(len(port_top[1])):
		for key,value in port_top[1][indx].items():
			if value > 1:
				wire_tmp = "wire "+"["+str(value-1)+":0] " +key+"_1"+", "+key+"_2"+", "+key+"_3"+";"
				
			else :
				wire_tmp = "wire "+ key+"_1"+", "+key+"_2"+", "+key+"_3"+"; "
			wire_signal.append(wire_tmp)
		# print(wire_signal)

    # copy file top module
	# string = get_port(origin_design, "module rt_qos_controller")
	# print(string)
	split_text = string.split("\n\n")[0]
	content = split_text+"\n"

	for indx in wire_signal:
		content = content + "  " + indx +"\n"
	# print(content)


    # create instances
	instances = []
	voters = []
	# tmp=""
	for k in range(3):
		tmp = ""
		for i in range(len(port_top[0])):
			for inp, value in port_top[0][i].items():
				# if inp == "clk" or inp == "reset_n":
				tmp_ip = "."+inp+"("+inp+")"+", "
				# print(inp)
				# else:
					# tmp_ip = "."+inp+"("+inp+"_"+str(k)+")"+", "
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
		content = content + "  " + ind +"\n"
	# content = content +"endmodule"
	# print(content)

	# insert voter at output
	ind =0
	for i in range(len(port_top[1])):
		for out, value in port_top[1][i].items(): 
			if value > 1:
				for k in range(value):
					tmp_name = out+"["+str(k)+"]"
					tmp=insert_voter("dti_voter",ind, tmp_name,out)
					ind=ind+1
					voters.append(tmp)
					# print(tmp)
					content = content +"  "+tmp+";\n"
			else:
				tmp=insert_voter("dti_voter",ind,out,out)
				ind=ind+1
				content = content +"  "+tmp+";\n"
				voters.append(tmp)
				# print(tmp)
	content = content + "endmodule"
	# print (content)
	write_to_file(output_file,content,'a')

def insert_FGDTMR(origin_design, output_file, top_module):
	print("FGDTMR")
	modules = extract_module(origin_design)
	print (modules)
	final_content = ""
	for module in modules :
		# print(module)
		if module.strip() != top_module:
			content = get_port(origin_design, "module"+module)
			# print(content)
			port_ff = extract_port_ff(content)[2]
			instance_cell = extract_port_ff(content)[4]
			content_0 = content.split("\n\n")[0]
			tmp_content0 = content.split(";")

			content_1 = content.split("\n\n")[1]

			inp 	= extract_port_ff(content)[0]
			out 	= extract_port_ff(content)[1]
			wire 	= extract_port_ff(content)[3]
			assig 	= extract_port_ff(content)[6]

			assigns = []
			if len(assig) >0:
				for ind in assig:
					tmp = ind.replace(" ","").split("=")
					tmp_left = tmp[0]
					tmp_right = tmp[1]

					for i in range(3):
						k = "  assign "+tmp_left+"_"+str(i)+" = "+tmp_right+"_"+str(i)+";\n"
						assigns.append(k)


			print("anhhhh")
			# print(assig)
			wire_signal = [] 
			for indx in range(len(out)):
				for key,value in out[indx].items():
					if value > 1:
						wire_tmp = "  wire "+"["+str(value-1)+":0] " +key+"_1"+", "+key+"_2"+", "+key+"_3"+";\n"
					
					else :
						wire_tmp = "  wire "+ key+"_1"+", "+key+"_2"+", "+key+"_3"+";\n"
					wire_signal.append(wire_tmp)
			for indx in range(len(wire)):
				for key,value in wire[indx].items():
					if value > 1:
						wire_tmp = "  wire "+"["+str(value-1)+":0] " +key+"_1"+", "+key+"_2"+", "+key+"_3"+";\n"
					
					else :
						wire_tmp = "  wire "+ key+"_1"+", "+key+"_2"+", "+key+"_3"+";\n"
					wire_signal.append(wire_tmp)
			for ind in tmp_content0[:]:
				if "wire" in ind:
					tmp_content0.remove(ind)
				elif "assign" in ind:
					tmp_content0.remove(ind)


			# tmp_content0 = tmp_content0 + wire_signal
			result = ";".join(tmp_content0)
			content_0 = result.split("\n\n")[0]+"\n"
			# print(result)
			for indx in wire_signal:
				content_0 = content_0 + indx 
			
			# print(inp)
			# print(out)
			# print(wire)

			# Split content_1 by ";"

			new_content_1 = content_1.split(";")
			# print(new_content_1)
			temp = ""
			inp_list = extract_port_ff(content_0)[5]
			# print(inp_list)
			index = 0
			voters = []
			for ind in new_content_1[:-1]:
				# print(ind)
				if "dti_12g_ff" in ind:
					# indx = indx.replace("\n","")
					instance = get_inout(ind)
					out_ff_tmp = "  wire "+instance[1] + "_tmp_0, " +instance[1] + "_tmp_1, " +instance[1] + "_tmp_2;\n" 
					content_0 = content_0 + out_ff_tmp
					# print(instance[0])
					for i in range(3):
						# print("anh hien")
						# print(instance[1])
						tmp = ind.replace(instance[2],instance[2]+"_"+str(i+1))
						if len(instance[1]):
							tmp = tmp.replace("("+instance[1],"("+instance[1]+"_tmp_"+str(i))
					
						# print(tmp)
						for j in range(len(instance[0])):
							# print(instance[0][j])
							if check_value_in_list(inp_list,instance[0][j]) == False:
								tmp = tmp.replace(instance[0][j],instance[0][j]+"_"+str(i))
								# print(tmp)
						temp = temp + tmp +";\n"
					# insert voter
					for ind in range(3):
						tmp = insert_voter("dti_voter",index,instance[1]+"_tmp_",instance[1]+"_"+str(ind))+";\n"
						index = index+1
						voters.append(tmp)
				else:
					instance = get_inout(ind)
					# print(instance[0])
					for i in range(3):
						# print("anh hien")
						# print(instance[1])
						tmp = ind.replace(instance[2],instance[2]+"_"+str(i+1))
						if len(instance[1]):
							tmp = tmp.replace("("+instance[1],"("+instance[1]+"_"+str(i+1))
						# print(tmp)
						for j in range(len(instance[0])):
							# print(instance[0][j])
							if check_value_in_list(inp_list,instance[0][j]) == False:
								tmp = tmp.replace(instance[0][j],instance[0][j]+"_"+str(i+1))
								# print(tmp)
						temp = temp + tmp +";\n"
			for indx in assigns:
				content_0 = content_0 + indx
			for indx in voters:
				temp = temp + "  "+indx
		# print(content_0)
		# print(temp)
			final_content = final_content+ content_0 + temp +"endmodule"
		else:
			content = get_port(origin_design, "module"+module)

			final_content = content
		print(final_content)
		
def check_value_in_array(value, array):
    for element in array:
        if element == value:
            return True
    return False

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
	instance 	= []
	inp_nosize  = []
	assign 		= []

	# lines_data = read_file(file_netlist)
	lines_data = module.split(";")
	# print(lines_data[0])
	for indx in lines_data:
		if 'input' in indx:
			# in_put = re.split(r",|;|\s", indx)
			in_put = indx.split("input ")[1].split(";")[0]
			dict1=get_size_port(in_put)
			input_q.append(dict1)
			inp_nosize=inp_nosize+list(dict1.keys())
		elif 'output' in indx:
			out_put = indx.split("output ")[1].split(";")[0]
			dict1=get_size_port(out_put)
			output_q.append(dict1)
		elif 'dti_12g_ff' in indx:
			ff = indx.split(";")[0]
			# print(ff)
			fliflop.append(ff)
		elif 'dti' in indx:
			ins = indx.split(";")[0]
			instance.append(ins)
		elif "wire" in indx:
			w = indx.split("wire ")[1].strip().split(";")[0]
			dict1=get_size_port(w)
			wire.append(dict1)
		elif"assign" in indx:
			assi = indx.split("assign")[1].split(";")[0].strip()
			assign.append(assi)
	return input_q,output_q,fliflop,wire,instance,inp_nosize,assign
	
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
	
	if ":" in signal_name:
		size = signal_name.split("] ")[0].split("[")[1].split(":")[0].strip()
		value = int(size) +1
		tmp_name = signal_name.split("] ")[1]
		tmp_name = tmp_name.replace(" ", "").split(",")
	else:
		value = 1
		tmp_name = signal_name.replace(" ", "").replace("\n","").split(",")
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
	return final_datas
# if _name_ == '__main__':

file_voter = 'dti_voter_netlist.v'
file_netlist = "rt_qos_controller_netlist.v"
name = file_netlist.split(".")[0]
file_out_lv1 = name+'_CGTMR_inserted.v'
file_out_lv2 = name+'_FGTMR_inserted.v'
file_out_lv3 = name+'_FGDTMR_inserted.v'

file_rpt_lv1 = name+'_CGTMR_list.rpt'
file_rpt_lv2 = name+'_FGTMR_list.rpt'
file_rpt_lv3 = name+'_FGDTMR_list.rpt'

# insert_CGTMR(file_netlist,file_out_lv1,"rt_qos_controller")
insert_FGDTMR(file_netlist,file_out_lv3,"rt_qos_controller")
# insert_FGTMR(file_netlist,file_out_lv2,"rt_qos_controller")

def main():

	parser = argparse.ArgumentParser(description='Generate TMR.')

	# Thêm các tùy chọn

	parser.add_argument('-fi', help='File netlist in')

	parser.add_argument('-fo', help='File netlist out')

	parser.add_argument('-fv', help='File netlist voter')
   
	parser.add_argument('-lv', help='Level: \n\t 1 == CGTMR \n\t 2 == FGTMR \n\t 3 == FGDTMR')

    # Phân tích các đối số dòng lệnh
	args = parser.parse_args()

    # Truy cập vào các tùy chọn
	if args.fi and args.fo and args.fv and args.lv:
		print('Tùy chọn 1 được kích hoạt:')
		print(sys.argv)
		if args.lv == "1":
			insert_CGTMR(file_name1,port,file_out_lv1,"rt_qos_controller")
		elif args.lv == "2":
			insert_FGTMR(file_name1,file_out_lv2,"rt_qos_controller")
		elif args.lv == "3":
			insert_FGDTMR(file_name1,file_out_lv3,"rt_qos_controller")
		else :
			print("Level failed")


	elif not args.fi:
		print(' File netlist in not find')
	elif not args.fi:
		print(' File netlist out not find')
	elif not args.fi:
		print(' File netlist voter not find')	
	elif not args.fi:
		print(' Level not find')

# main()
