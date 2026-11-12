import re, sys, glob, os
SRC='/workspace/blog-drafts'; DST='/workspace/blog-drafts/blogger'
def clean(md, blogger):
    lines=md.split('\n')
    out=[]; 
    for l in lines:
        if l.startswith(('Title:','Search description:','Subtitle:')): continue
        if l.startswith('>'):  # case record / at-a-glance box
            if blogger: continue
            # in source, also drop box (case record and at a glance) for fairness
            continue
        if l.startswith('*Brendan Ngehsi Newanforbi is a self-represented') or l.startswith('More from Newanforbi') or l.startswith('This case summary is also') or l.startswith('More case summaries'): continue
        out.append(l)
    t='\n'.join(out)
    t=re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)   # links -> anchor text
    t=re.sub(r'\[([^\]]*)\]\([^)]*\)', '', t)
    t=re.sub(r'"[^"\n]{0,200}"', ' ', t)  # quotations (single-line)
    return t
def words(t):
    return re.findall(r"[a-z0-9§\.\-']+", t.lower().replace('*','').replace('|',' '))
def wc(md):
    t='\n'.join(l for l in md.split('\n') if not l.startswith(('Title:','Search description:')))
    t=re.sub(r'\]\([^)]*\)', ']', t)
    t=re.sub(r'^\|?[-| ]+\|?$', '', t, flags=re.M)
    return len(re.findall(r"[A-Za-z0-9§][^\s|]*", t))
def shingles(w,n=8): return {tuple(w[i:i+n]) for i in range(len(w)-n+1)}
for f in sorted(glob.glob(DST+'/0*.md')):
    name=os.path.basename(f); src=open(os.path.join(SRC,name)).read(); b=open(f).read()
    wb=words(clean(b,True)); ws=words(clean(src,False))
    sb=shingles(wb); ss=shingles(ws); inter=sb&ss
    pct=100*len(inter)/max(1,len(sb))
    print(f"{name}: words={wc(b)} overlap8={pct:.1f}% ({len(inter)}/{len(sb)})")
    if '-v' in sys.argv:
        for s in sorted(inter): print('   ',' '.join(s))
    bad=[x for x in ['frivolous','@'] if x in b.lower().replace('medium.com/@newanforbi','')]
    if bad: print('   BAD',bad)
    m=re.match(r'Search description: (.*)',b.split('\n')[1]); print('   desc len',len(m.group(1)) if m else 'MISSING')
