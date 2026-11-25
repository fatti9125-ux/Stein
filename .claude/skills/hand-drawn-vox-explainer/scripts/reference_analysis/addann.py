# usage: python3 addann.py CID <<< "first|type|desc" lines (appends; creates header if needed)
import sys,os
cid=sys.argv[1];p=f'/home/user/Stein/reference_analysis/01/annot/{cid}.tsv' if len(sys.argv)<3 else f'/home/user/Stein/reference_analysis/{sys.argv[2]}/annot/{cid}.tsv'
os.makedirs(os.path.dirname(p),exist_ok=True)
new=not os.path.exists(p)
with open(p,'a') as f:
    if new:f.write('first\ttype\tdescription\tevidence\tconfidence\n')
    elif not open(p).read().endswith('\n'):f.write('\n')
    for l in sys.stdin.read().strip().splitlines():
        a,t,d=l.split('|',2);f.write(f"{a}\t{t}\t{d}\tobserved\t{'medium' if t in('subtle','motion_step','expression_swap') else 'high'}\n")
