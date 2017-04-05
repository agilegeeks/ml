import sys,getopt
from pprint import pprint
import drest

"""
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-18T23:54:00.000Z -e 2017-03-21T12:00:00.000Z --target=0 >datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-21T12:00:00.000Z -e 2017-03-25T08:47:12.000Z --target=0 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-09T13:16:00.000Z -e 2017-03-18T09:36:12.000Z --target=0 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-31T17:28:00.000Z -e 2017-03-31T20:26:00.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-18T14:17:59.000Z -e 2017-03-18T15:30:00.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-03-09T08:10:30.000Z -e 2017-03-09T08:57:30.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-01-19T17:26:00.000Z -e 2017-01-20T02:26:00.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-01-20T12:56:00.000Z -e 2017-01-20T22:26:00.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-01-08T15:20:00.000Z -e 2017-01-08T20:55:00.000Z --target=1 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2017-02-18T22:22:22.000Z -e 2017-02-19T01:14:22.000Z --target=2 >>datasets/rotld_whois/whois_hits.txt
python3 get_whoishits_dataset.py -a http://orchestrator.rotld.ro:9090/api/v1 -s 2016-10-12T10:25:00.000Z -e 2016-10-25T08:55:00.000Z --target=2 >>datasets/rotld_whois/whois_hits.txt
"""

argv = sys.argv[1:]
try:
  opts, args = getopt.getopt(argv,"h:a:s:e:t",["api=","start=","end=","target="])
except getopt.GetoptError:
  print ('get_whoishits_dataset.py -s <start_date> -e <end_date> -t <target> -a <api_url>')
  sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('get_whoishits_dataset.py -s <start_date> -e <end_date> -t <target> -a <api_url>')
        sys.exit()
    elif opt in ("-s", "--start"):
        start = arg
    elif opt in ("-e", "--end"):
        end = arg
    elif opt in ("-t", "--target"):
        target = arg
    elif opt in ("-a", "--api"):
        api_url = arg
    else:
        print ('get_whoishits_dataset.py -s <start_date> -e <end_date> -t <target> -a <api_url>')
        sys.exit()

step = '30s'

req = drest.request.TastyPieRequestHandler()
req.add_param('query','increase(mdw_whois_hits{service="whois_pub"}[15m])')
req.add_param('start', start)
req.add_param('end',end)
req.add_param('step',step)

response = req.make_request('GET', api_url+'/query_range/')

results = response.data['data']['result']
sample_size = len(results[0]['values'])

found_values = results[0]['values']
not_found_values = results[1]['values']

if results[0]['metric']['status']=='not_found':
    found_values, not_found_values = not_found_values, found_values

dataset=[]
i=0
while i<sample_size:
    entry1 = found_values[i]
    entry2 = not_found_values[i]
    #dataset.append([entry1[0],float(entry1[1]),float(entry2[1])])
    print ("%d %.2f %.2f %s" % (entry1[0],float(entry1[1]),float(entry2[1]),target))
    i=i+1
