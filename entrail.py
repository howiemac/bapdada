# run as su

from os import system




for f in (
"bapdada.110215.sql",
"bapdada.110627.sql",
"bapdada.110805.sql",
"bapdada.120210.sql",
"bapdada.120316.sql",
"bapdada.120418.sql",
"bapdada.120522.sql",
"bapdada.120526.sql",
"bapdada.120622.sql",
"bapdada.120701.sql",
"bapdada.120709.sql",
"bapdada.120721.sql",
"bapdada.120727.sql",
"bapdada.120809.sql",
"bapdada.120822.sql",
):
  db=f.replace('.','').replace('sql','')
  system('mysql -e "create database %s;"' % db)  
  system("mysql %s < %s " % (db,f))
    

