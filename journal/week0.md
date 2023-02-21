# Week 0 — Billing and Architecture

## Required Homework/Tasks

### Installed AWS CLI in Gitpod Environment

The AWS CLI will be used often in the bootcamp, so I configured the gitpod.yml to install the AWS CLI when the Gitpod environment launches, and also set the CLI to use partial auto-prompt mode to make it easer for writing CLI commands. The bash commands we are referenced from: [AWS CLI Install Instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

The `.gitpod.yml` was updated to include the following task.

```sh
tasks:
  - name: aws-cli
    env:
      AWS_CLI_AUTO_PROMPT: on-partial
    init: |
      cd /workspace
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      cd $THEIA_WORKSPACE_ROOT
```

### Created a New IAM User and Generated AWS Credentials

In the IAM User Console, I followed the steps below to create an Admin User:
- `Enable console access` for the user
- Create a new `Admin` Group and apply `AdministratorAccess`
- Create the user and go find and click into the user
- Click on `Security Credentials` and `Create Access Key`
- Choose AWS CLI Access
- Download the CSV with the credentials

### Set Env Vars

I configured the environment variables in Gitpod to securely hold the access information for my workspaces.
```
gp env AWS_ACCESS_KEY_ID=""
gp env AWS_SECRET_ACCESS_KEY=""
gp env AWS_DEFAULT_REGION=us-east-1
```

### Confirmed with the AWS CLI in Gitpod that the user was successfully added

```sh
aws sts get-caller-identity
```

The following output confirmed the configuration was successful
```json
{
    "UserId": "****************5O4B",
    "Account": "237457675866",
    "Arn": "arn:aws:iam::237457675866:user/Ace"
}
```

### Enabled Billing and Created Budget
To enable Billing, I turned on Billing Alerts to recieve alerts by going to my Root Account [Billing Page](https://console.aws.amazon.com/billing/), and, under `Billing Preferences`, I chose the option to `Receive Billing Alerts`, and saved the preferences. I then followed the instructions, referencing Chirag's video on Youtube [AWS-SNSTopic-and-BillingAlarm-Reference](https://www.youtube.com/watch?v=OVw3RrlP-sI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=13) to create the following:

#### Created SNS Topic to send emails when billing alarm is activated
![SNS-Topic-Created](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/SNS-Subscriptions-for-CloudWatchBillingAlarm-and-EventBridgeHealthAlert.PNG)
#### Created BillingAlarm that detects when cost threshold is reached
![AWS-BillingAlarm-Created](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/AWS-BillingAlarm-Created.PNG)

#### Created an AWS Budget for forecastable monthly spending
![AWS-Budget-Created](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/AWS-Budget-Created.PNG)

### Created Conceptual Diagram of Cruddur Application on Napkin
![Cruddur-Conceptual-Napkin-by-AceCloud](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/CruddurNapkinDiagram-by-AceCloud.jpg)

### Created Logical Diagram of Cruddur Application in LucidChart
I followed along with Andrew, referencing [Logical-Chart-Recreation-Youtube-Video](https://www.youtube.com/watch?v=K6FDrI_tz0k&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv)

*Please access the following link to view the diagram in LucidChart: 

[Logical-Diagram]([https://lucid.app/lucidchart/e49790d0-441a-45d6-a8d8-feb6192ea71e/edit?viewport_loc=-300%2C-403%2C2576%2C1175%2C0_0](https://lucid.app/lucidchart/e49790d0-441a-45d6-a8d8-feb6192ea71e/edit?viewport_loc=-300%2C-403%2C2576%2C1175%2C0_0&invitationId=inv_ae568b21-cca3-4961-92d2-78f1a8535336)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Homework Challenges

### Used EventBridge to hookup Health Dashboard to SNS and send notifications when there are service health issues.
Referencing AWS documentation, I learned how to create a service health alert with EventBridge and SNS to hookup the Health DashBoard.
The following EventBridge documentation provided a step-by-step process of the various sources and targets that can be configured to EventBridge rules to set up notifications for purposes such as Health Alerts: [EventBridge-Docs-to-Configure-Rules](https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html)
The following SNS documentation was also a useful refresher for practicing with setting up SNS topics to become more familiar with the configuration of notification messages via email: [SNS-Docs-to-Configure-Email-Notification](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/US_SetupSNS.html)

As a result, I was able to configure EventBridge and SNS for service health alerts with the following outputs:
#### Created SNS Email Topic for Health Alerts
![SNS-Topic-including-Service-Health-Alert](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/SNS-Subscriptions-for-CloudWatchBillingAlarm-and-EventBridgeHealthAlert.PNG)
#### Created EventBridge Rule configured with the Health Dashboard
![EventBridge-Output-of-Service-Health-Alert](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/EventBridge-HealthCheck.PNG)

### Reviewed all the questions of each pillars in the Well Architected Tool (No specialized lens)
Referencing Andrew's Youtube video on getting started with the Well-Architected Framework Tool [Well-Architected-Framework-Tool-Youtube-Video](https://www.youtube.com/watch?v=i-hOfAJb3cE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=16), I reviewed quite a few of the 58 questions and took the time to answer a few from each pillar. There were quite a few considerations when providing notes for each of the questions, however, this was a great brainstorming opportunity to work through some of the questions by providing notes with the checklist. I went through all of the questions in the Operational Excellence Pillar as it provided the most opportunity for conceptual thinking regarding organizational planning and how it would look like to mobilize teams to take on such a critical project for the organization and its stakeholders, and then I also spent some more time working on some of the Security pillar questions as that is a group of services in the Cloud that I am particularly interested in and the kinds of considerations that critical to think about in the verbage including network topology, resiliency, and adapting to the ever-changing threat landscape. Then, I also answered a few of the questions in the other pillars which revolved around optimizing performance, redundancy, cost, and sustainability which are also critical domains in the overall AWS domain space. Please see attached a PDF output of my work on these questions generated from the Well-Architected Framework Tool in AWS: [AceCloud's-Well-Architected-Framework-Tool-Responses](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/Cruddur_wellarchitectedframework-draft.pdf)

### Created an architectural diagram (to the best of my ability) of the CI/CD logical pipeline in Lucid Charts
I was not able to add the CI/CD logical pipeline to the actual Logical Diagram due to encountering an issue with the Free account, where I reached the maximum limit of shapes that I could add to the chart in the Homework Tasks section above. The free account imposed a limitation, for which, to keep using LucidChart, I needed to make a separate LucidChart for the CI/CD pipeline, which connects to the ECS component that I have boxed as part of the Application Architecture in this supplementary diagram.

*Please access the following link to view the CI/CD diagram in LucidChart: [CI/CD-Diagram](https://lucid.app/lucidchart/fffe4463-fb79-4449-be76-2b4dbf01f01e/edit?viewport_loc=-436%2C-20%2C2560%2C1168%2C0_0&invitationId=inv_55a82f8c-9b70-48ac-82ab-3004f69db31a)

I created the above CI/CD logical pipeline chart by researching a few AWS Blogs and encountered the following link [AWS-CI/CD-Blog-Reference](https://aws.amazon.com/blogs/containers/create-a-ci-cd-pipeline-for-amazon-ecs-with-github-actions-and-aws-codebuild-tests/), which seemed to match the use-case for creating a CI/CD pipeline for the frontend and backend containerized workloads that are sought to be deployed for Cruddur as per the initial logical diagram. Following through the chart, from left to right: 
- Users/Developers commit updates to the Github repository 
- AWS CodePipeline + AWS CodeCommit + AWS CodeBuild provides a testing environment for additions / changes to the code and resulting images that are built
- Image builds that are test successfully report status updates to Github
- Successful tests/implementations are submitted through Github Actions in a series of status checks and checkouts, and then get pushed to AWS
- Once connected to AWS, images get pushed to the ECR container registry, and deployed to the application's ECS cluster as part of updated task definitions 
- This would unfold repeatedly in the CI/CD pipeline with each test and resulting implementation to the application architecture

### Researched the technical and service limits of specific services (ECS) and requested a Service Limit Increase via the ServiceQuota Tool
Service Limits exist to impose limitations on the number of resources that can be allocated at once. This exists as a safety mechanism to avoid over-allocating AWS resources and / or prevent allocating resources that are not available. As a limitation, this prevents a larger-scale project from being deployable if there are services that encroach the current limits, however, this is resolved by requesting service quota limits. As an example, for the current Cruddur project, ECS is an essential service for deploying the containerized code workload for the frontend and backend components for which, if a service limit is encountered, would prevent the application from scaling up to the appropriate size to accommodate the number of users that are interacting with Cruddur, which presents a limitation on the workload's scalability. I took a look at the existing service limits for ECS, and found the following results using the Service Quota Tool in AWS.
![List-of-Researched-Service-Limits-for-ECS](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/List-of-some-Researched-ECS-ServiceLimits.PNG)
As part of practice, I requested service limits for two features below, which could pose an issue with scalability for services per ECS Namespace and ECS Targets as the number of users for the application increases and Cruddur gains traction and popularity as an ephemeral social media application in a hypothetical situation, which would be necesary to implement as its workload increases:
![ServiceLimit-Increase-for-Services-per-NameSpace](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/ServiceQuotaIncrease-ServicesPerECSNamespace.PNG)
![ServiceLimit-Increase-for-Scalable-ECS-Targets](https://github.com/acgecloud/aws-bootcamp-cruddur-2023/blob/main/_docs/assets/week0/ServiceQuotaIncrease-ScalableECSTargets.PNG)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
*End of Journal.
