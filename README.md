# ePPN for Google Workspace

This is a sample script for adding eduPersonPrincipalName (ePPN) to
users in Google Workspace. The script assigns ePPN to users where the
custom attribute eduPersonPrincipalName is empty. The script retrieves
the highest ePPN from the directory and increments it before assigning
it to a new user.

The script creates a Base36 number (alphanumeric) left padded with zeros. ePPN is increased by 1 for each new user. In the configuration if the max lenght for ePPN is set to 6, that gives us 2176782336 (36^6) ePPNs before overflow occurs. In the configuration it is possible to set a value for Scope. If set, ePPN is stored with both prefix and suffix, if not then only prefix. This gives the possibility to add the suffix in e.g., the IdP.

Run it manually or as a scheduled job. Do not execute more than one
instance at a time to avoid race conditions

## Python Quickstart

Follow the [Python Quickstart](https://developers.google.com/admin-sdk/directory/v1/quickstart/python) to enable the Admin SDK API and set up app credentials.

**Project**  
Create a new project an be sure to select it before continuing.

**API**  
Enable the Admin SDK API.

**OAuth consent screen**  
 [Documentation](https://developers.google.com/workspace/guides/configure-oauth-consent)

 User type: Internal

 Add Scopes:
- https://www.googleapis.com/auth/admin.directory.userschema
- https://www.googleapis.com/auth/admin.directory.user


**Credentials**  
Create OAuth client ID credentials.

Application Type: Desktop app

Download the OAuth client JSON and set the configuration to use the downloaded file.

## Configuration

Copy config.yaml.example to config.yaml and change it to fit your needs.

### customer ID

Insert your customer ID in the configuration file.

When you signed up for Google Workspace or Cloud Identity, your account is assigned a unique customer ID. You can look up this ID in your Admin console.

Sign in to your Google Admin console using an administrator account [Google Admin](https://admin.google.com/)

In the Admin console, go to Menu -> @Account -> Account settingsand -> Profile. Next to Customer ID, find your organization's unique ID.

### Custom Attributes

To define custom fields for users you add custom user schemas to the domain. These fields are used to store information such as an ePPN. The schema is defined in the configuration file and added by using parameter --schema

## Install requirements

pip install -r requirements.txt

## Parameters

- **eppn \<String\>**  
Add ePPN to users
- **schema \<String\>**  
Adds custom schemas from the configuration file. The configuration contains the schema skolfederation which contains all the attributes from attribute profile 4.2. Check the schema thoroughly before inserting it.

## Execution

python eppn.py \<eppn|schema\> \<path to configuration file\>

## Google API Documentation

[Google API Documentation](https://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.html)
