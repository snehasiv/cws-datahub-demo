# cws-datahub-demo
Azure Function app for managing NGO Centre for World Solidarity (CWS) DataHub application

## Github setup


Remote repository is base code setup. 
Locally maintain two branches: dev and main.

On local system setup, Github for Desktop. 

To make any changes, go to "dev" branch, make changes, validate locally, then make a git commit and git push. 
Deploy to dev Azure Function App for testing remotely.


To finalise changes, go to github page, select "Pull Requests", select "New Pull Request", base: main compare: "dev". Select "Create Pull Request".
Then "Merge Pull Request".

To test, deploy locally to prod setup, on IDE switch to main branch, then build and deploy. 



## Setting up datastore and APIs


1.	Create official CWS Azure account and subscription. Reference doc [here](https://learn.microsoft.com/en-us/training/modules/create-an-azure-account). 
2.	Create resource groups (datahub-dev and datahub-prod). From step (3), repeat per resource group, documentation [here](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal).
3.	Create Storage Account, documentation [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)
    1.	Create data table for local data collection: `statereports`. Translation of this database and current data is below:


      ```python
      'PartitionKey': 'projectId'_'state',
      'RowKey': 'reportName'_'reportSubmissionDate',
      'State': 'state',
      'ReportName': 'reportName',
      'ProjectId': 'projectId',
      'CreatedBy': 'createdBy',
      'ReportWindowStartDate': 'reportWindowStartDate' ('%Y-%m-%d'),
      'ReportWindowEndDate': 'reportWindowEndDate' ('%Y-%m-%d'),
      'ReportSubmissionDate': 'reportSubmissionDate' ('%Y-%m-%d'),
      'Data': json of rest of the report-specific data.

      ```


    2.	Create data table for for local data collection: `localrecords`. Translation of this database from local form data is below:


      ```python
      'PartitionKey': 'projectId'_'state',
      'RowKey': 'pincode'_’recordID’,
      'State': 'state',
      'Pincode': 'village pincode',
      'ActivityName': 'acivity',
      ‘RecordID’: ‘recordId’,
      'ProjectId': 'projectId',
      'SubmittedBy': 'submittedBy',
      'SubmissionDate': 'reportSubmissionDate' ('%Y-%m-%d'),
      'Data': json of rest of the report-specific data.

      ```
      
      
    3.	Create data table for tracking changes made to state reports, with name = `statereportslog`.

      ```python
      'PartitionKey': 'reportName'_'reportSubmissionDate',
      'RowKey': 'current timestamp',
      'ModifiedBy': 'submitter name',
      'ChangesMade': text field.

      ```

    4.	Setup secure credentials for storage account, documentation [here](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal)
4.	Create Azure key vault for storing storage account connection string, documentation [here](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-portal)
    ```python
    Add STORAGE-ACCOUNT-CONNECTION-STRING secret in created vault, with value = storage account connection string (under storage account -> access keys -> connection string on UI Portal)
    ```
5.	Create Function App for DataHub APIs (name= cws-api). 
6.	Setup local environment for working on API code:
    1.	Install azure client, reference doc [here](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwitq9zzn7D7AhVhIbcAHdZ9BtgQFnoECBQQAQ&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fcli%2Fazure%2Finstall-azure-cli&usg=AOvVaw2wU-IOK9bJspNOnFD8Hwz_)
    2. Setup Azure Function local tools, reference doc [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cmacos%2Ccsharp%2Cportal%2Cbash#v2)
    3. Test locally: 
        ``` python
        #Initialise project 
        func init

        #create environment variable in terminal for storage account name (Name: 'STORAGE_ACCOUNT_CONNECTION_STRING') and account key (Name: 'STORAGE_ACCOUNT_KEY')
        ##powershell needed in windows.
        export STORAGE_ACCOUNT_CONNECTION_STRING="" 

        #Install project python dependencies locally
        pip install -r requirements.txt

        Then run: "func host start"
        ```
    4.  Writing a new API: ``func new --template "Http Trigger" --name <api name>``

    5. Setup environment variables on Azure Functions on Azure Portal, documentation [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings?tabs=portal)

        ```python
        Go to azure portal -> your function app -> Configuration -> Add application setting 
        Add following secrets:

            #get values from vault.
            STORAGE_ACCOUNT_CONNECTION_STRING = @Microsoft.KeyVault(VaultName=""; SecretName=STORAGE-ACCOUNT-CONNECTION-STRING; SecretVersion="") 

        ```

    6. Deploy changes to Azure account: 
      ```
      func azure functionapp publish
      ```
7. Create a container for older records and reports, documentation [here](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal)


8. Monitoring can be done via Application Insights integrated within function app. For more details, refer documentation [here](https://learn.microsoft.com/en-us/azure/azure-functions/configure-monitoring?tabs=v2)

9. Securing Azure Function APIs
    1. Enforce HTTPs TLS v1.2 for all APIs, doc [here](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-bindings#enforce-https)
    2. Add master API Key under "Function Keys" option on portal, after which API calls can be made only if key is correct. Further details [here](https://learn.microsoft.com/en-us/azure/azure-functions/security-concepts?tabs=v4) under API Key Management.
    3. CORS Configuration, set default allowed origins to "*".




Note:
*	For all new resources recommended location is: “Central US”.
* Ensure codebase in git is in sync with what is deployed on Azure. Recommendations:
    * Create 1 branch per azure resource group (eg. two branches: dev and prod). 
    * Future enhancements: enable Github Actions to automatically initiate Azure Function Build and Deploy when code is merged in branch.
* Generate Azure resources via templates.
