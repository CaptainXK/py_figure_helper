import numpy as np
import matplotlib.pyplot as plt
import data_file_cal as dfc
import sys, getopt
import re # regex
import traceback
import json
import os

'global var'
class Config_Var:
    xlabel='x'
    ylabel='y'
    nb_file = 0
    nb_data = 0
    files_list = []
    datas_list = []
    names_list = []
    title = ''
    target_file = "out.png"
    type = 'bar'
    dir = ''

    def __init__(self):
        self.xlabel='x'
        self.ylabel='y'
        self.nb_file = 0
        self.nb_data = 0
        self.files_list = []
        self.datas_list = []
        self.names_list = []
        self.title = ''
        self.target_file = "out.png"
        self.type = 'bar'
        self.dir = ''

'parse regex in cmd to get data file\'s name and path'
class Reg_Helper:
    @staticmethod #static funtion
    def do_search(string):
        #match pattern like [file_path,legend_name]
        resOBJ = re.search(r'\[(.+),(.+)\]', 
                            string)
        
        if resOBJ:
            return list(resOBJ.groups())
        else:
            return []

'command line helper class'
class Cmd_Helper:  

    def __error_out(self):
        print("Option Error")
        print("Please use -h to get usage")

    def __usage__(self):
        print("Usage:")
        print("\t--data_files:\t source data file and name, file will be used as data source file path, name will be used as figure label, form is look as [file, name]:[file1,name1]")
        print("\t--out:\t target figure file")
        print("\t--xlabel=, --ylabel=, --title=\t:content of xlabel, ylabel and title")
        print("\t--type : bar, plot")
        print("\t--json : json file cantaining figure setup")
        print("\tExample\t:\n\t\tpython create_fig.py --data_files [data1,met1]:[data2,met2] --out out.png --xlabel=rounds --ylabel=\"value(ms)\" --title=\"name empty\" --type=plot")
        print("\tExample\t:\n\t\tpython create_fig.py --json=insert.json")
        return

    def parse_json(self, json_path, cfg):
        data_dict={}

        with open(json_path, 'r') as f_in:
            data_dict = json.load(f_in)
            # data_dict = json.dumps(raw_json_data)
            # data_dict = json.loads(str(raw_json_data))

        # print("Json dict:")
        # print(data_dict)

        for key in data_dict.keys():
            if key == "data_files":
                files_list = data_dict[key].split(',')
                for file in files_list:
                    cfg.files_list.append(file.replace(' ',''))
                    data_list_temp = []

            elif key == "data_names":
                names_list = data_dict[key].split(',')
                for name in names_list:
                    cfg.names_list.append(name.replace(' ',''))

            elif key == 'out':
                cfg.target_file = data_dict[key]

            elif key == 'xlabel':
                cfg.xlabel = data_dict[key]

            elif key == 'ylabel':
                cfg.ylabel = data_dict[key]

            elif key == 'title':
                cfg.title = data_dict[key]
            
            elif key == 'type':
                cfg.type = data_dict[key]

            elif key == 'dir':
                cfg.dir = data_dict[key]
            
            else:
                self.__err_out()
                sys.exit(0)

    def __parse_cmd__(self, argv, cfg):
        try:
            opts, args = getopt.getopt(argv, "h", ["data_files=","out=","xlabel=", "ylabel=", "title=", "type=", "dir=","json="])
        except getopt.GetoptError as err:
            print("Error:"+str(err))
            self.__usage__()
            sys.exit(2)

        'return and notification for none option'
        if(len(opts) == 0):
            self.__error_out()
            return

        for opt, arg in opts:
            if opt == '--json':
                print("Read figure setup from json file {}".format(arg))
                self.parse_json(arg, cfg)
            
            elif opt == '--data_files':
                'form : (file, label)'
                print(arg)
                for data_tuple in arg.split(":"):
                    # print("parse:"+data_tuple)
                    res = Reg_Helper.do_search(data_tuple)
                    # print("res:%s,%s"%(res[0], res[1]))
                    if(len(res) != 0):
                        cfg.files_list.append(res[0])
                        cfg.names_list.append(res[1])
                        data_list_temp = []

            elif opt == '--out':
                cfg.target_file = arg

            elif opt == '--xlabel':
                cfg.xlabel = arg

            elif opt == '--ylabel':
                cfg.ylabel = arg

            elif opt == '--title':
                cfg.title = arg
            
            elif opt == '--type':
                cfg.type = arg

            elif opt == 'dir':
                cfg.dir = arg

            elif opt == '-h':
                self.__usage__()
                exit(0)

            else:
                self.__error_out()
                sys.exit(0)
        
        # read datas from files list
        for file in cfg.files_list:
            data_list_temp = []
            with open("{}/{}".format(cfg.dir, file), 'r') as fp_in:
                for item in fp_in.readlines():
                    data_list_temp.append(float(item.replace('\n','')))
                
                cfg.datas_list.append(data_list_temp)
        cfg.nb_data = len(cfg.datas_list[0])

        # perpare dirs
        if os.path.isdir(cfg.dir) is not True:
            os.mkdir(cfg.dir)
        if os.path.isdir("figures") is not True:
            os.mkdir("figures")

'main api class'
class __main__():

    def __init__(self, cmd=''):
        cfg = Config_Var()
        parser = Cmd_Helper()

        # print("argv:" + str(sys.argv[0:]))
        if cmd == '':
            print("Configure by cmd")
            parser.__parse_cmd__(sys.argv[1:], cfg)
        else:
            print("Configure by list:" + str(cmd) )
            parser.__parse_cmd__(cmd, cfg)

        # print(cfg.datas_list)

        print("%d datas in each data file"%(cfg.nb_data))
        for file_name, name in zip(cfg.files_list, cfg.names_list):
            print("file '%s' is labeled as '%s'"%(file_name, name))

        dfc.create_fig(plt, 
                       list(range(0, cfg.nb_data, 1)), 
                       cfg.datas_list, 
                       cfg.xlabel,
                       cfg.ylabel,
                       cfg.title,
                       cfg.names_list,
                       cfg.target_file,
                       cfg.type)

        del cfg
        del parser

#start here
cmd_list=[['--json=lookup.json'], ['--json=insert.json'], ['--json=delete.json'], ['--json=mem.json']]
for cmd in cmd_list:
    test = __main__(cmd)
    del test

