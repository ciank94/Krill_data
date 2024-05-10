#Wrapper for GFW API: https://github.com/GlobalFishingWatch/gfwr
#Find IMO and MMSI identifiers: https://www.marinetraffic.com/en/ais/home/centerx:-21.8/centery:10.1/zoom:2
#Token: https://globalfishingwatch.org/our-apis/tokens
#install.packages("devtools")
#devtools::install_github("GlobalFishingWatch/gfwr")
#usethis::edit_r_environ() #to modify .Renviron
# .Renviron is here: Note: //home.ansatt.ntnu.no/ciank/Documents/.Renviron
#Token is GFW_TOKEN = "Krill_SFI"
# IMO: 9827891; Antarctic Endurance
#install.packages("R.matlab")
setwd("C:/Users/ciank/PycharmProjects/sinmod/Krill_data/GFWR/")
library(gfwr)
library(R.matlab)
key <- gfw_auth()
fleetIDs <- get_vessel_info(query = "shipname LIKE '%Antarctic Endurance%' OR shipname LIKE '%Saga Sea%' OR shipname LIKE '%Antarctic Sea%'

OR imo = '8607115' OR imo = '85059770' OR imo = '8607385' OR imo = '8717453' OR imo = '8724315' OR imo = '9160358'

OR mmsi = '412440689' OR imo = '8607373' OR imo = '9849332' OR imo = '7042538' OR imo = '8505977'",
                            
                            search_type = "advanced", dataset = "fishing_vessel", key = key)
# t1 = get_vessel_info(query = "imo = '7390416'", 
#                 search_type = "advanced", 
#                 dataset = "all", 
#                 key = key)
# t2 = get_vessel_info(query = "imo = '9827891'", 
#                     search_type = "advanced", 
#                     dataset = "all", 
#                     key = key)
# t3 = get_vessel_info(query = "imo = '9160358'", 
#                      search_type = "advanced", 
#                      dataset = "all", 
#                      key = key)
ship_files = paste(fleetIDs$shipname, ".csv", sep="")
for (i in 1:10) {
  if (i == 3){
    next
  }
print(ship_files[i])
e1 = get_event(event_type = 'fishing', vessel = fleetIDs$id[i], start_date = "1990-01-01",
               end_date = "2024-04-30", key = key)

df = data.frame(e1$lat,e1$lon,e1$start,e1$end)
write.table(df,ship_files[i],row.names=FALSE,sep=",")
#e2 = get_event(event_type = 'port_visit', vessel = fleetIDs$id, start_date = "2000-01-01",
               #end_date = "2016-12-31", key = key)
#e3 = get_event(event_type = 'encounter', vessel = t1$id, start_date = "2016-01-01",
#   end_date = "2016-12-31", key = key)

}

#ta = table(e1$start,e1$end,e1$lat,e1$lon)
#write.csv(e1$start,e1$end,e1$lat,e1$lon,file = 'vess.csv')
#writeMat("e1.mat",A = e1$start)

#df2 = data.frame(e12$lat,e12$lon,e12$start,e12$end)
#write.table(df2,"esv2.csv",row.names=FALSE,sep=",")

