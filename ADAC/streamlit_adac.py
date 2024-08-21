import streamlit as st
import subprocess
from env_local import AD_DOMAIN, AD_PATH, AD_SERVER, FROM_EMAIL, PORT, PS_USERNAME, PS_PASSWORD, SMTP_SERVER, TO_EMAIL




st.title("New User Request")

with st.form("my_form",clear_on_submit=True):
    st.write("User information")
    USER_FNAME = st.text_input("First name: ").lower().strip()
    USER_LNAME = st.text_input("Last name: ").lower().strip()
    USER_JTITLE = st.text_input("Job Title: ").lower().strip()
    USER_DEPARTMENT = st.text_input("Department: ").lower().strip()
    USER_COMPANY = st.text_input("Company: ").lower().strip()

    submitted = st.form_submit_button("Submit")
    if submitted:
        PS_EMAIL_VARS = f""" 

        $username = {PS_USERNAME}
        $password = {PS_PASSWORD}
        $sstr = ConvertTo-SecureString -string $password -AsPlainText -Force
        $cred = New-Object System.Management.Automation.PSCredential -argumentlist $username, $sstr

"""
        EMAIL_SUBJ = f"'New user request for {USER_FNAME.capitalize()} {USER_LNAME.capitalize()}'"
        EMAIL_CSS = """ 

        code {
            background-color: #272822;
            color: #f8f8f2;
            border-radius: 0.3em;
            padding: 4px 5px 6px;
            margin: 1em;
        }

        h4, h5 {
            margin: 1em;
        }

        .main {
            background-color: #BCD0C7;
            border-radius: 1em;
        }

"""
        EMAIL_BODY = f"""
        "
        <style>
        {EMAIL_CSS}
        </style>

        <div class='main'>

            <h4> Check for pre-existing user: </h4>
            
            <code>
                Get-ADUser -Identity '{USER_FNAME[0]}{USER_LNAME}'
            </code>

            <h4> New user CMD: </h4>

            <code>
                New-ADUser -Company:'{USER_COMPANY}' -Department:'{USER_DEPARTMENT}'``
                -DisplayName:'{USER_FNAME} {USER_LNAME}' -GivenName:'{USER_FNAME}' -Initials:'' -Name:'{USER_FNAME} {USER_LNAME}' -Path:'{AD_PATH}'``
                -SamAccountName:'{USER_FNAME[0]}{USER_LNAME}' -Server:'{AD_SERVER}.{AD_DOMAIN}' -Surname:'{USER_LNAME}' -Title:'{USER_JTITLE}' -Type:'user'``
                -UserPrincipalName:'{USER_FNAME[0]}{USER_LNAME}@{AD_DOMAIN}'
            </code>

            <h4> Set user password CMD: </h4>

            <h5> Create password variable: </h5>
            <code>
                `${USER_FNAME[0]}{USER_LNAME}pass = ConvertTo-SecureString -string 'NEW_PASSWORD_HER3!' -AsPlainText -Force
            </code>

            <h5> set password: </h5>
            <code>
                Set-ADAccountPassword -Identity:'CN={USER_FNAME} {USER_LNAME},{AD_PATH}' -NewPassword:`${USER_FNAME[0]}{USER_LNAME}pass -Reset:`$true -Server:'{AD_SERVER}.{AD_DOMAIN}'
            </code>
            
            <h4> Remove user CMD: </h4>

            <code>
                Remove-ADObject -Confirm:`$false -Identity:'CN={USER_FNAME} {USER_LNAME},{AD_PATH}' -Recursive:`$true -Server:'{AD_SERVER}.{AD_DOMAIN}'
            </code>

        </div>
        "

"""
        PS_EMAIL_SPLAT_PRE = "$sendMailMessageSplat = @{"
        PS_EMAIL_SPLAT_OBJ = f""" 

        From = {FROM_EMAIL}
        To = {TO_EMAIL}
        Subject = {EMAIL_SUBJ}
        Body = {EMAIL_BODY}
        DeliveryNotificationOption = 'OnSuccess', 'OnFailure'
        SmtpServer = {SMTP_SERVER}
        Credential = $cred
        port = {PORT}
        UseSsl = $true
        BodyAsHtml = $true

"""
        PS_EMAIL_SPLAT_SUF = "}"
        PS_EMAIL_CMD = "\n\nSend-MailMessage @sendMailMessageSplat"
        PS_SPLAT_EMAIL = PS_EMAIL_VARS + PS_EMAIL_SPLAT_PRE.strip() + PS_EMAIL_SPLAT_OBJ + PS_EMAIL_SPLAT_SUF.strip() + PS_EMAIL_CMD
        # print(PS_SPLAT_EMAIL)
        process = subprocess.Popen(["powershell", PS_SPLAT_EMAIL], stdout=subprocess.PIPE)
        result = process.communicate()[0]
        if not result.decode('utf-8').strip():
            print("\nEmail sent successfully!\n")
        else:
            print(result.decode('utf-8'))