V='/home/claude/vendor/'
MAP={'d3.min.js':V+'d3-7.8.5/package/dist/d3.min.js','three.min.js':V+'three-0.147.0/package/build/three.min.js','OrbitControls.js':V+'three-0.147.0/package/examples/js/controls/OrbitControls.js'}
async def route(r):
    u=r.request.url
    for k,v in MAP.items():
        if u.endswith(k): return await r.fulfill(path=v,content_type='application/javascript')
    if u.startswith('http') and 'localhost' not in u: return await r.abort()
    await r.continue_()
