import json,sys
sys.path.insert(0,'/home/claude/vdp'); from glyphs import G,TERM
T=json.load(open('/home/claude/vdp/norm.json'))
def icon(term,col,bg='#E6DED0'):
    k=TERM[term]
    return f'<svg viewBox="0 0 40 40" style="color:{col};--bgc:{bg}" aria-hidden="true"><circle cx="20" cy="20" r="18.6" fill="none" stroke="currentColor" stroke-width="1.5"/><g fill="currentColor" transform="{T[k]}">{G[k]}</g></svg>'
