# RTK_Correction_Send
This will allow to pass rtcm data from ntrip server to flight controller using Pymavlink  over TCP/UDP.

Steps to build ntrip server:-

1. Ntrip server can be made using u-center which only runs on windows, by setting up the Time mode 3 parameter it starts the survey-in process by putting the time period and desired accuracy required.

   ![first](C:\Users\Bhaskar\Desktop\New folder\RTK_Correction_Send\first.PNG)

2. After or In between the survey-in process go to receiver on the u-center top panel and choose Ntrip server/caster option.

   ![Second](C:\Users\Bhaskar\Desktop\New folder\RTK_Correction_Send\Second.png)

3. Set up the name, mount name, username, password for your ntrip server that's it.

For Linux system or in windows we can also use RTKLIB which is basicallly cli version for configuring the reciever and seding its data through ntrip server. In RTKLIB we use RTKNAVI for setting up the base for rtk observation.

* After getting the data over ntrip server we get rtcm data correction which we pass to our gps through flight controller by utillizing the feature of mavlink.
* Run the python script included to pass the corrections.



Done by:

Bhaskar