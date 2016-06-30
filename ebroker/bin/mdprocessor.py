#!/usr/local/bin/python
import sys
import types
connector = __import__(sys.argv[2])
convertor = __import__(sys.argv[3])
def recursive_convert_feedstream(gen):
        if isinstance(gen,types.GeneratorType):
            for genout in gen:
               recursive_convert_feedstream(genout)
        else:
            print gen
            yield convertor.convertor(gen)

if __name__ == "__main__":
       feedstream = connector.getfeedstream()
       converted_data = recursive_convert_feedstream(feedstream)
       convertor.recursive_expand_generator(converted_data)
