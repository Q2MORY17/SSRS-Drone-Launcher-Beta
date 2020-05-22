*** Keywords ***

User Click Button Max pitch     #To maximize the pitch position
        Click Button        //*[@id="script_max_pitch"]
		Sleep                       1

User Click Button Min pitch   #to minimize the pitch position
        Click Button             //*[@id="script_min_pitch"]
		Sleep                       1

User Click Button Max lift      #to maximize the lift position
        Click Button            //*[@id="script_max_lift"]
		Sleep                       1

User Click Button Min lift         #to minimize the lift position
        Click Button            //*[@id="script_min_lift"]
		Sleep                       1
User Expects To Get A Error Messege
   Alert Should Be Present	action=ACCEPT

