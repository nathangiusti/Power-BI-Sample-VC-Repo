# Power BI Sample VC Repo

This repository contains a sample implementation of DevOps for Power BI.

In this readme I will explain what each of the workflows is doing. 

The workflow used here is that when a pull request is opened, the asset (a report or a dataset) is deployed to our test workspace. When the pull request is merged, the asset is deployed to our production workspace. 

There is a folder for datasets and a folder for reports. Within those folders is one folder for each workspace these assets may need to be deployed to. 

For more details on the reusable workflow including additional configuration options, see the [Reusable Power BI Workflows Repo](https://github.com/nathangiusti/Power-BI-Reusable-Workflows)

# Prerequisites

Before using these workflows you may have to update how you develop in Power BI. The workflow given here is generally considered to be best practice for enterprise managed Power BI.

## Service Principal

For many of these actions you will need a service principal with which to run the API's. Create a service principal with the necessary permissions and add the credentials to your GitHub's environment so that they can be referenced. 

## Tabular Editor

Datasets must be created in tabular editor and saved in folder format, not bim file format. 

## "Thin" PBIX Files

PBIX files should directly connect to a dataset. They should not contain data. 


# Workflows:

## [format_json.yaml](.github/workflows/format_json.yaml)

This is configured so that every time a pull request is created, all changed PBIX files will be deserialized and have their JSON printed to a folder. You can set the commit message used.

```yaml
name: Reformat Power BI Assets
on: [pull_request]
jobs:
  Deserialize-PBIX-Files:
    uses: nathangiusti/Power-BI-Reusable-Workflows/.github/workflows/deserialize-pbix.yml@main
    with:
      commit_message: "Deserialize PBIX files"
```


## [deploy_report_to_test.yaml](.github/workflows/deploy_report_to_test.yaml)

This is configured so that every time a pull request is created, all changed PBIX files will be deployed to the workspace listed in the config file located at [.github/config/report_deploy_config.yaml](.github/config/report_deploy_config.yaml). 

You must create one folder for each workspace you will deploy to. The name of the folder must match the key in the config file. We have these set up to deploy to the second stage (the test stage) of a deployment pipeline. This will allow us to use the pipeline action to migrate to prod as we will see later. 

It is possible to use workspace to deploy both, but there are additional options available in the pipeline deploy API that may be useful. To deploy to both test and prod you would need a second configuration file to list the prod workspaces.

```yaml
name: Deploy to test
on: [pull_request]
jobs:
  workspace-deploy:
    uses: nathangiusti/Power-BI-Reusable-Workflows/.github/workflows/workspace-deploy.yml@main
    with:
      tenant_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
      config_file: .github/config/report_deploy_config.yaml
    secrets:
      client_id: ${{ secrets.CLIENT_ID }}
      client_secret: ${{ secrets.CLIENT_SECRET }} 
```

## [migrate_report_to_prod.yaml](.github/workflows/migrate_report_to_prod.yaml)

This is configured so that every time a branch is merged to main, all changed PBIX files will be moved along the pipeline listed in [.github/config/report_deploy_config.yaml](.github/config/report_deploy_config.yaml). 

The action works by looking at the name of the changed PBIX file and migrating the report file with that name from the test to the prod stage of the pipeline. If there is no report with that name or multiple reports with that same name, the workflow will fail. 

To deploy from dev to test, set source stage order to `0`. Since we are moving from test to prod, we set source stage order to `1`.  

```yaml
name: Deploy via pipeline to prod
on:
  push:
    branches:
      - main
jobs:
  pipeline-deploy:
    uses: nathangiusti/Power-BI-Reusable-Workflows/.github/workflows/pipeline-deploy.yml@main
    with:
      tenant_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
      config_file: .github/config/report_deploy_config.yaml
      source_stage_order: 1
    secrets:
      client_id: ${{ secrets.CLIENT_ID }}
      client_secret: ${{ secrets.CLIENT_SECRET }} 
```

## [deploy_dataset_to_test.yaml](.github/workflows/deploy_dataset_to_test.yaml)

This workflow deploys a dataset to our test workspace on creation of a pull request. Similar to reports you must create a configuration file to map folder names to workspace urls. The format is different than the config file for reports. See the sample [here](.github/config/test_dataset_deploy.yaml)

If reports and datasets are being version controlled in the same repo, you will need to create a separate folder to house your datasets in order to prevent confusion with other json files in the repo. Pass that folder as an argument to the workflow. If datasets are in their own repo, they require only the workspace folders. 

We need a separate config file to deploy to production. As we do not use pipelines for datasets. 


```yaml
name: Deploy to test
on: [pull_request]
jobs:
  deploy_to_test:
    uses: nathangiusti/Power-BI-Reusable-Workflows/.github/workflows/te-deploy.yml@main
    with:
      folder: Datasets
      tenant_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
      config_file: .github/config/test_dataset_deploy.yaml
      deploy_roles: true
      deploy_partitions: true
    secrets:
      client_id: ${{ secrets.CLIENT_ID }}
      client_secret: ${{ secrets.CLIENT_SECRET }}
```

## [deploy_dataset_to_prod.yaml](.github/workflows/deploy_dataset_to_prod.yaml)

This workflow deploys a dataset to our prod workspace on when a branch is merged to master. It uses a separate config file located [here](.github/config/prod_dataset_deploy.yaml)


```yaml
name: Deploy to prod
on:
  push:
    branches:
      - main
jobs:
  deploy_to_test:
    uses: nathangiusti/Power-BI-Reusable-Workflows/.github/workflows/te-deploy.yml@main
    with:
      tenant_id: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
      config_file: .github/config/prod_dataset_deploy.yaml
      folder: Datasets
      deploy_roles: true
      deploy_partitions: true
    secrets:
      client_id: ${{ secrets.CLIENT_ID }}
      client_secret: ${{ secrets.CLIENT_SECRET }}
```
