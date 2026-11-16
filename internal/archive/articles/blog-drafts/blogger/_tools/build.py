import markdown, glob, os, re
D='/workspace/blog-drafts/blogger'
allparts=['# Blogger versions — Newanforbi case-record series\n\nDistinct Blogger (newanforbi.blogspot.com) rewrites of the nine Substack posts. Each section below is one post; Title and Search description lines are for the Blogger post settings.\n']
for f in sorted(glob.glob(D+'/0*.md')):
    t=open(f,encoding='utf-8').read()
    lines=t.split('\n')
    body=[l for l in lines if not l.startswith(('Title:','Search description:')) and not l.startswith('# ')]
    md='\n'.join(body).strip()+'\n'
    html=markdown.markdown(md, extensions=['tables','sane_lists'], output_format='html5')
    html=html.strip()+'\n'
    assert not html.lstrip().startswith('<!--')
    out=os.path.join(D,'html',os.path.basename(f)[:-3]+'.html')
    open(out,'w',encoding='utf-8').write(html)
    allparts.append('\n---\n\n'+t.strip()+'\n')
open(D+'/ALL-BLOGGER.md','w',encoding='utf-8').write('\n'.join(allparts))
print('ok')
