#!/usr/bin/env python


# This function probably takes the query string args
# and strips them down into a lookup thingy
def get_query_string(qs):
    args = {}
    args_a = qs.split('?')[0]
    if len(args_a) > 0:
        args_a = args_a.split('&')
        for arg in args_a:
            value_pair = arg.split('=')
            if len(value_pair) > 0:
                args[value_pair[0]] = value_pair[1]
    return args
