from link_checker import link_checker

import sys
import json
from decimal import Decimal
import time

lc = link_checker(sys.argv[1], sys.argv[3])
lc.check_site(sys.argv[2])

d = {'checked_links':lc.checked_links, 'bad_links':lc.bad_links}

finish_time = time.time()

d['time'] = finish_time
print(d)

json_file = open('json_data/link_output_'+str(finish_time)+'.json',"w")
json_file.write(json.dumps(d, indent = 4))
json_file.close()