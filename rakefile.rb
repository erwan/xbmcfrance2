task :default => [:xpi]

task :xpi do
  rm_f 'vgspy.xpi'
  `cd ..;find xbmcfrance2/skins xbmcfrance2/xbmcutils xbmcfrance2/*.py -type f \
   | egrep -v "(#|~|pyo)" | xargs zip -r xbmcfrance2/xbmcfrance2.zip`
end 
