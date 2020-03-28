

import sys
import signal
import subprocess
try:    import argparse
except: print('argparse required, run: pip install argparse');  sys.exit(1)

#global variables------------------------------------------------------------------
current_version     =   '0.1'
outgoing_open_ports =   []
process             =   None
#----------------------------------------------------------------------------------
def print_usage():
    result  =   "out_firewalking_server.py"+"\n"
    result  +=  "2020-03-28 , github.com/glezo1"+"\n\n"
    result  +=  "[-h] | [--help]       display this help"+"\n"
    result  +=  "[-v] | [--version]    show version"+"\n"
    result  +=  "[-i] | [--interface]  interface to listen all. Default: any"+"\n"
    result  +=  "-t   | --target       target. The ip/hostname executing the out_firewalking_client"+"\n"
    result  +=  "\n"
    print(result)
#-----------------------------------------------------------------------------------
def gen_ranges(lst):
    s = e = None
    for i in sorted(lst):
        if s is None:
            s = e = i
        elif i == e or i == e + 1:
            e = i
        else:
            yield (s, e)
            s = e = i
    if s is not None:
        yield (s, e)
#-----------------------------------------------------------------------------------
def control_c_handler(signal,frame):
    print('#SIGINT DETECTED!')
    if(process!=None):
        process.terminate()
    outgoing_open_ports.sort()
    print(repr(','.join(['%d' % s if s == e else '%d-%d' % (s, e) for (s, e) in gen_ranges(outgoing_open_ports)])))
    sys.exit(0)
#-----------------------------------------------------------------------------------
def main():
    argument_parser =   argparse.ArgumentParser(usage=None,add_help=False)
    argument_parser.add_argument('-h','--help'      ,action='store_true',default=False                 ,dest='help'      ,required=False  )
    argument_parser.add_argument('-v','--version'   ,action='store_true',default=False                 ,dest='version'   ,required=False  )
    argument_parser.add_argument('-i','--interface' ,action='store'     ,default=None                  ,dest='iface'     ,required=False  )
    argument_parser.add_argument('-t','--target'    ,action='store'     ,default=None                  ,dest='target'    ,required=True   )
    
    
    argument_parser_result      =   argument_parser.parse_args()
    option_help                 =   argument_parser_result.help
    option_version              =   argument_parser_result.version
    iface                       =   argument_parser_result.iface
    target                      =   argument_parser_result.target
    
    if(  option_version):
        print(current_version)
        sys.exit(0)
    elif(option_help):
        print_usage()
        sys.exit(0)
    else:
        if(iface==None):
            iface   =   'any'
        print("#Calling tcpdump. Control+c when you thing you're ready")
        tcpdump_line        =   "sudo tcpdump -l -i "+iface+" -n tcp[tcpflags]=2 and src host "+target
        print(tcpdump_line)
        process             =   subprocess.Popen(tcpdump_line,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
        signal.signal(signal.SIGINT,control_c_handler)
        while(True):
            output_line =   process.stdout.readline()
            if(output_line):
                output_line     =   output_line.decode('utf-8')
                print('#'+output_line.strip())
                if(output_line.strip()!=''):
                    tokens          =   output_line.split(' ')
                    local_dest_port =   tokens[4].split('.')[-1].split(':')[0]
                    if(local_dest_port.isnumeric() and int(local_dest_port) not in outgoing_open_ports):
                        outgoing_open_ports.append(int(local_dest_port))
#---------------------------------------------------------
if(__name__=='__main__'):
    main()
