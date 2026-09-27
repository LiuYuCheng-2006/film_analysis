def join_clist(v,q):
  if v.nxt is not v:
    v.nxt.prv =q.prv
    v.prv.nxt =q
    v.nxt.prv.nxt = v.nxt
    v.prv.nxt.prv = v.prv
    v.nxt = v.prv = v