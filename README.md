# python-aws-autobuilder
## Description
A Template Repository tuned for launching Python projects to AWS infrastructure.

## Configure this Repo
1. **Environment Secrets** - As a default this repo is configured to sync with an S3 bucket when feature versions are updated. Configure the S3 bucket endpoint in the AWS console using whatever name you desire, inserting that name into `house-keeping/resource-manifest.json > "#/Config/S3/bucket"`. Don't forget to create a secret for the ARN associated with github, so that the bucket can be written to. If you have multiple deployment environments now is when you want to configure those. `Default Secret Namme: AWS_S3_ARN`
2. **Project Structure** - To resolve the issue with shallow directory structures, you need to put a sub-project folder into the `projects` directory. (i.e. `./projects/my-project/<stuff>`)
3. **House Keeping** - This directory contains tools used to build and deploy scripts to AWS. You can define what features get deployed and how using `house-keeping/resource-manifest.json`. The manifest can be extended as you find new cases to implement. `Gantry` is the tools which is run when the Environment Deployment Action launches, it packages and builds scripts into S3 while cloning the structure of your repo starting at the `./projects` directory. 
> It's highly recommended practice deployment using this unaltered template to learn about how this project interacts with your AWS account.
4. **Updating Build Artifacts** - To build a new artifact, you need to update the version of the artifact in the manifest, or delete the existing artifact from the bucket then make a push or pull request to an environment branch where it will deploy from.
## Centralized Python Environment
To solve the issue with having multiple development environments in you team a master requirements document is provided. This can be used to define and manage the environments your team uses, so you're all on the same page. *At deploy time

## Automated Infrstructure
> Infrastructure as Code - In Progress

### **TL;DR**
* Play with deploying this blank template to ensure consistent behavior between github and your AWS account.
* Builds to multiple stages and accounts.
* Updates remote versions without redeploying all scripts.
* Maintains consistent local environments using centralized dependencies.
* Automates build and deployment of scripts.
* Reduces storage requirements of built packages.