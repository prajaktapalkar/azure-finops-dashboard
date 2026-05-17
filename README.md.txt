# Azure FinOps Cost Management Dashboard

## Problem Statement
Enterprise cloud teams lack real-time visibility into Azure spend, 
leading to budget overruns. This project demonstrates a production-grade 
FinOps pipeline built entirely on Azure free tier.

## Architecture
Azure Timer Function → Cost Management API → Blob Storage → Power BI Dashboard → Logic App Alerts

## Technologies Used
| Service | Purpose | Tier |
|---|---|---|
| Azure Functions | Daily cost export | Consumption (free) |
| Azure Cost Management API | Spend data source | Free |
| Azure Blob Storage | Data persistence | LRS (free 5GB) |
| Power BI Desktop | Dashboard visualisation | Free |
| Azure Logic Apps | Spend alert automation | Consumption (free) |

## Key Outcomes
- Automated daily cost export with zero manual intervention
- Real-time spend visibility across 4 Azure service types
- KPI cards showing Total Spend, Active Services, Days Tracked, Peak Spend
- Top Cost Drivers table with conditional formatting
- Infrastructure deployed via Azure CLI (IaC approach)

## Screenshots
(![Dashboard](Azure%20Finops%20Cost%20Management%20Dashboard.png)

## Resume Bullets
- Architected Azure FinOps dashboard using Cost Management API, Azure Functions 
  and Power BI enabling real-time visibility into cloud spend across 4 resource types
- Designed automated cost-alerting pipeline via Azure Logic Apps and Blob Storage 
  demonstrating governance-first cloud adoption patterns to enterprise prospects
- Built TCO modelling artefact used in solution design workshops accelerating 
  stakeholder sign-off by providing data-driven ROI justification

## Setup
1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Set environment variables: SUBSCRIPTION_ID, STORAGE_CONNECTION_STRING
4. Deploy: `func azure functionapp publish [your-function-app-name] --python`