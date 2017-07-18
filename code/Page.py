"""
override class for base.page

"""
from base.render import html
from base.lib import *
from base.Page import Page as basePage

from base.data import execute

import os, string

import urllib,re 

from calendar import month_name 


class Page(basePage):

  def post(self,req):
    """fix date and format when posting a draft
       - overrides base post()
    """
    if self.kind!='page': #safety valve
      return basePage.post(self,req)
    if basePage._posted(self,req):  
      self.fix_bapdada_date(req)
#      self.reform_text(req)
#      if not req.warning:
#        req.warning='comments reformed'
      self.flush()
    return self.view(req)
  post.permit='create page'

  def latest(self, req):    
    "override base version"
    req.pages=self._latest(req,order="uid desc")
    req.title="additions"
    req.prep="to"
    req.page='latest' # for paging
    return self.listing(req)

  def get_navbar_links(self):
    "override base version"
    home=self.get(1)
    return (
     ("bapdada.info",home.url(),"home"),
     ("additions",home.url("latest"),"latest additions"),
     ("at twitter","http://twitter.com/bapdadainfo","@bapdadainfo"),
    )


################# publishing (test) ####################

  def publish(self,req):
    "publish site to flat files"
    pass



################# temporary import/fix routines for setting up text versioning #####################

  from base.data import execute

  @classmethod
  def entrail(self,req):
    "temporary import process to incorporate old data in trail"
    if req.user.uid!=2:
      return req.user.error(req,"not authorised")
    all=self.list()
    xsource=""
    for source in (
"110215",
"110627",
"110805",
"120210",
"120316",
"120418",
"120522",
"120526",
"120622",
"120701",
"120709",
"120721",
"120727",
"120809",
"120822",
):
      print "processing bapdada"+source
      c=0
      for i in all:
        res=execute("select name,text from bapdada%s.pages where uid=%s" % (source,i.uid))
        if res:
          if xsource:
            xres=execute("select name,text from bapdada%s.pages where uid=%s" % (xsource,i.uid))
          else:
            xres=[] 
          if xres:
            xn=str(xres[0]["name"])
            xt=str(xres[0]["text"])
          else:
            xn=xt=""
          n=str(res[0]["name"])
          t=str(res[0]["text"])
          if (n!=xn) or (t!=xt):
            text="%s\n##\n\n%s" % (n,t)
            self.Text.create(page=i.uid,text=text,when=int("20"+source))
            c+=1
      print '%s texts added' % c
      xsource=source
    return "DONE"

############################### utilities ###############################

  _fifties=(764,) # children of this require special date handling

#  comment_rule=re.compile(r'(\()(.*?)(\))')
#
#  def reform_text(self,req,bolden=False):
#    "fix italics and bold to be consistent with trance messages"
#  
#    def italicise(match):
#      ""
#      source=match.groups()[1].strip()
#      return " ~ ("+source+") ~ "
  
#    if self.kind=='episode':
#      if (self.name.find("trance")>0):
#        req.warning="trance message - reform skipped"
#      elif (bolden and (self.text.find("^")>=0)) or (self.text.find(" ~ (")>=0):
#        req.warning="reformed already - skipped"
#      else:
#        if bolden:
#          self.text=self.text.replace("~","^")  #make italic words bold
#        self.text=self.comment_rule.sub(italicise,self.text)
#        self.flush() #store changes
#  reform_text.permit='dummy' 

#  def reform(self,req):
#    "make text between ( ) italic"
#    self.reform_text(req,bolden=False)
#    req.message="comments reformed"
#    return self.view(req) 
#  reform.permit='admin page' 

#  def reform_all(self,req):
#    "fix italics and bold etc for every episode"
#    murlis=self.list(kind='episode',where='(name like "avyakt bapdada %") or (name like "sakar bapdada %")')
#    c=0
#    s=0
#    for i in murlis:
#      i.reform_text(req)
#      if req.warning:
#        s+=1 
#        req.warning=''
#      else:
#        c+=1
#    req.message=" %s reformed, %s skipped" % (c,s)     
#    return self.get(1).view(req) 
#  reform_all.permit='admin page' 

  def fix_bapdada_date(self,req):
    ""
    try:
     if self.parent in self._fifties:
      date='1/1/1950'    
     elif "revision" in self.name:
      date='1/1/1960'    
     else:
      title,day,month,year=self.name.rsplit(' ',3)
#      print i.uid,':',day,' - ',month,' - ',year
      if day[1] in ['0','1','2','3','4','5','6','7','8','9']:
        day=day[:2]
      else:
        day=day[0]	 
      month=list(month_name).index(month)
      date='%s/%s/%s' % (day,month,year)
     self.when=DATE(date)
#     print "WHEN=>",self.when
     self.set_seq()
     self.flush()
    except:
#     raise
     req.error="date handling problem - date not set"
 
  def fix_bapdada_dates(self,req):
    ""
    murlis=self.list(kind='episode',where='(name like "avyakt bapdada %") or (name like "sakar bapdada %")')
    for i in murlis:
     i.fix_bapdada_date(req) 
    req.message="BapDada dates updated"
    return self.get(1).view(req)
  fix_bapdada_dates.permit='admin page'
  fix_bapdada_dates=classmethod(fix_bapdada_dates)
   