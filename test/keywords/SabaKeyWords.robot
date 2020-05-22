*** Keywords ***

Display Page
       Wait Until Page Contains      Positions
	   Click Button	  xpath://button[@id="script_reset_encoders"]
	    Sleep                                   1

User Click Button Max pitch     #To maximize the pitch position
        Click Button        //*[@id="script_max_pitch"]
         Sleep                                   1


User Click Button Min pitch   #to minimize the pitch position
        Click Button             //*[@id="script_min_pitch"]
         Sleep                                   1

User Click Button Max lift      #to maximize the lift position
        Click Button            //*[@id="script_max_lift"]
         Sleep                                   1


User Click Button Min lift         #to minimize the lift position
        Click Button            //*[@id="script_min_lift"]
         Sleep                                   1