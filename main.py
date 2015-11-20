from rtpreader import RTPReader
from network.sipmessage import calls, ports

import getopt
import sys

# Filter class will be directly translated into BPF format.
# The filter can be initialized here and passed to incoming messages.
# These messages can then update the filter when calls start or end.
# Each message will inherit from a class and implement filter(..)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                             "hi:o:",
                             ["help", "input-file=", "output-file="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    # in_pcap = "/home/gerlof/gntel/puppet/bg10-eth0.3600-split.pcap"
    in_pcap = None
    # out_pcap = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input-file"):
            in_pcap = a
        # elif o in ("-o", "--output-file"):
        #     out_pcap = a
        else:
            assert False, "Unhandled option"

    try:
        RTPReader(in_pcap).parse()
        print(calls)
        print(ports)
    except NotImplementedError as err:
        print(str(err))
        sys.exit(2)


def usage():
    print("Usage: " + sys.argv[0] + " -i <input.pcap> [options]")
    print("Options: -i,--input-file  [file] : specify input pcap")
    print("         -o,--output-file [file] : specify output pcap")
    print("         -h,--help               : print this message")


if __name__ == "__main__":
    main()
