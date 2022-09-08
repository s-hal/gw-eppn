# ePPN for Google Workspace

This is a sample script for adding eduPersonPrincipalName (ePPN) to
users in Google Workspace. The script assigns ePPN to users where the
attribute is empty. The script check the directory for the highest assigned
ePPN, increments it, and then assign the new ePPN. This script can be
run manually or as a scheduled job. Do not execute more than one
instance of the script at a time for search query that could find the same user
to avoid race conditions

The script creates a Base36 number (alphanumeric) that is stored as a
string, padding the string left with zeros for sorting. ePPN is
incremented for every new user. If we use a length of 6 (36^6), that
gives us 2176782336 ePPN's before overflow occurs. Either append the
scope, a owned domain, before storing the ePPN or do it later e.g., in
the IdP.

## Internal App

**TBD**

## Custom Attributes

To define custom fields for users you add custom user schemas to the domain. These fields are used to store information such as an ePPN. The schema is defined in the example configuration file and added by using parameter --schema. Check the schema thoroughly before inserting it.

## Installation requirements

pip install -r requirements.txt
copy config.yaml.example to config.yaml and change it to fit your needs.

## Parameters

**TBD**

- **eppn \<String\>**  
Add eppn
- **schema \<String\>**  
Add custom schemas


## Execution

python ad-eppn.py \<eppn|schema\> \<path to configuration file\> 


## Find your customer ID

When you signed up for Google Workspace or Cloud Identity, your account is assigned a unique customer ID. You can look up this ID in your Admin console.

    Sign in to your Google Admin console using an administrator account .
    [Google Admin](https://admin.google.com/)

    In the Admin console, go to Menu -> @Account -> Account settingsand -> Profile.
    Next to Customer ID, find your organization's unique ID.


## Google API Documentation

**TBD**

https://googleapis.github.io/google-api-python-client/docs/dyn/admin_directory_v1.html
