import numpy as np
import matplotlib.pyplot as plt
import data_file_cal as dfc
import sys, getopt
import re # regex
import traceback

'global var'
class Config_Var:
    xlabel='x'
    ylabel='y'
    nb_file = 0
    nb_data = 0
    files_list = []
    datas_list = []
    names_list = []
    title = 'test'
    target_file = "out.png"
    type = 'bar'

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
        print("usage:")
        print("\t-d:\t source data file and name, file will be used as data source file path, name will be used as figure label, form is look as [file, name]:[file1,name1]")
        print("\t-t:\t target figure file")
        print("\t--xlabel=, --ylabel=, --title=\t:content of xlabel, ylabel and title")
        print("\t--type : bar, plot")
        print("\texample\t:python create_fig.py -d [data1,met1]:[data2,met2] -t out.png --xlabel=rounds --ylabel=\"value(ms)\" --title=\"name empty\" --type=plot")
        return

    def __parse_cmd__(self, argv, cfg):
        try:
            opts, args = getopt.getopt(argv, "d:t:h", ["xlabel=", "ylabel=", "title=", "type="])
        except getopt.GetoptError as err:
            print("Error:"+str(err))
            self.__usage__()
            sys.exit(2)

        'return and notification for none option'
        if(len(opts) == 0):
            self.__error_out()
            return

        for opt, arg in opts:
            if opt == '-d':
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
                        with open(res[0], mode='r') as file:
                            for item in file.readlines():
                                data_list_temp.append(float(item.replace('\n','')))
                        # print(data_list_temp)

                        cfg.datas_list.append(data_list_temp)

                cfg.nb_data = len(cfg.datas_list[0])

            elif opt == '-t':
                cfg.target_file = arg

            elif opt == '--xlabel':
                cfg.xlabel = arg

            elif opt == '--ylabel':
                cfg.ylabel = arg

            elif opt == '--title':
                cfg.title = arg
            
            elif opt == '--type':
                cfg.type = arg

            elif opt == '-h':
                self.__usage__()
                exit(0)

            else:
                self.__error_out()

'main api class'
class __main__():

    def __init__(self):
        cfg = Config_Var()
        parser = Cmd_Helper()

        parser.__parse_cmd__(sys.argv[1:], cfg)

        # print(cfg.datas_list)

        print("%d datas in each data file"%(cfg.nb_data))
        for file_name, name in zip(cfg.files_list, cfg.names_list):
            print("file '%s' is labeled as '%s'"%(file_name, name))

        dfc.create_fig(plt, 
                       list(range(1, cfg.nb_data+1, 1)), 
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
test = __main__()
del test

