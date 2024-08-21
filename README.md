# Using Streamlit as a GUI for Powershell commands
The purpose of this repo is to provide examples of how Python's Streamlit package can be used alongside of PowerShell.
### ADAC Example
[ADAC_FINAL_01.webm](https://github.com/user-attachments/assets/b18f9b7a-ec63-4576-a61e-fab55534fe21)

##### Description:
The Active Directory Administrative Center (ADAC) example shows how Windows Server Admins can create forms with Streamlit to automate the user creation process. Use the "video playback speed" controls to slow down the video if you'd like to see the individual steps. 

The workflow could consist of: 
1. A form that is accessible to the appropriate personnel, allowing them to submit as new user request.
2. An intermediary step that requires the Admin's approval of the new user.
3. Action by the Admin, which could run a script or provide the commands as shown in the example.

The idea is that you should be able to modify or extend this to create an automation for create users that has the necessary checks to prevent blindly running Powershell scripts.

##### Step by Step:
1. Ensure that the [Active Directory (AD) Powershell Module](https://www.ninjaone.com/blog/powershell-active-directory-module/) is installed and you have Admin rights in your [AD Domain](https://www.techtarget.com/searchwindowsserver/definition/Active-Directory-domain-AD-domain#:~:text=An%20Active%20Directory%20domain%20\(AD,as%20a%20computer%20or%20printer.).

2. Ensure that [Python](https://www.python.org/downloads/) is installed.

3. Clone this repo `git clone --recursive https://github.com/DesignsbyBlanc/streamlit_as_gui.git` or copy and paste code from "_streamlit_adac.py_"

4. Create a "_env_local.py_" and fill in variables. Alternatively, you can import the "_os_" package to use environment variables.
   - Use the values provided in "_example_env.py_" to fill out variables used in "_streamlit_adac.py_"
5. Install Streamlit  `pip install streamlit` or `python -m pip install streamlit`

6. `streamlit run "your_script.py"`

7. Check your email and run the commands to create a user.