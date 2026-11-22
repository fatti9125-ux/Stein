import sys,json,time,urllib.request,urllib.parse
UA={'User-Agent':'motion-graphics-sample/1.0 (educational video research)'}
def api(params):
    u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({**params,'format':'json'})
    for i in range(4):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30);return json.load(r)
        except Exception as e: err=e; time.sleep(3*(i+1))
    print('FAIL',err);return {}
if __name__=='__main__':
    for q in sys.argv[1:]:
        d=api(dict(action='query',list='search',srnamespace=6,srlimit=6,srsearch=q))
        print('==',q);[print('  ',x['title']) for x in d.get('query',{}).get('search',[])];time.sleep(1.5)
