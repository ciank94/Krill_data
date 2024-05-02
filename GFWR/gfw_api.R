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
setwd("C:/Users/ciank/OneDrive - NTNU/PostDoc/e_gfwr")
library(gfwr)
library(R.matlab)
key <- gfw_auth()
t1 = get_vessel_info(query = "imo = '7390416'", 
                search_type = "advanced", 
                dataset = "all", 
                key = key)
t2 = get_vessel_info(query = "imo = '9827891'", 
                    search_type = "advanced", 
                    dataset = "all", 
                    key = key)
t3 = get_vessel_info(query = "imo = '9160358'", 
                     search_type = "advanced", 
                     dataset = "all", 
                     key = key)

e1 = get_event(event_type = 'fishing', vessel = t1$id, start_date = "2010-01-01",
               end_date = "2022-12-31", key = key)
e12 = get_event(event_type = 'fishing', vessel = t2$id, start_date = "2010-01-01",
               end_date = "2022-12-31", key = key)
e2 = get_event(event_type = 'port_visit', vessel = t1$id, start_date = "2016-01-01",
               end_date = "2016-12-31", key = key)
#e3 = get_event(event_type = 'encounter', vessel = t1$id, start_date = "2016-01-01",
            #   end_date = "2016-12-31", key = key)
#ta = table(e1$start,e1$end,e1$lat,e1$lon)
#write.csv(e1$start,e1$end,e1$lat,e1$lon,file = 'vess.csv')
#writeMat("e1.mat",A = e1$start)
df = data.frame(e1$lat,e1$lon,e1$start,e1$end)
write.table(df,"esv.csv",row.names=FALSE,sep=",")
df2 = data.frame(e12$lat,e12$lon,e12$start,e12$end)
write.table(df2,"esv2.csv",row.names=FALSE,sep=",")

