# 6. Dataset Design

## 6.1 Overview

BusinessPilot AI uses a fully synthetic enterprise dataset that simulates the operations of a B2B Software-as-a-Service (SaaS) company.

The dataset is generated programmatically using predefined business rules rather than random values. Every record represents a realistic business event, ensuring logical consistency across sales, marketing, finance, customer success, and subscription management.

The synthetic dataset enables the development and testing of analytics pipelines, machine learning models, dashboards, and APIs without relying on confidential business information.

---

# 6.2 Dataset Objectives

The dataset is designed to:

- Simulate a real SaaS company's daily operations.
- Support transactional (OLTP) workloads.
- Support analytical (OLAP) workloads.
- Train and evaluate machine learning models.
- Power executive dashboards.
- Enable business simulations.
- Maintain referential integrity across all entities.

---

# 6.3 Business Scenario

The fictional company, **TechNova Solutions**, provides enterprise SaaS products to organizations across multiple industries.

The company offers products such as:

- Customer Relationship Management (CRM)
- Human Resource Management (HRMS)
- Accounting Software
- AI Analytics Platform
- Customer Support Platform

Organizations purchase subscription plans, interact with sales representatives, receive invoices, make recurring payments, submit support tickets, and renew subscriptions.

This business environment forms the basis of the synthetic dataset.

---

# 6.4 Dataset Characteristics

| Property | Value |
|----------|-------|
| Dataset Type | Synthetic Enterprise Data |
| Industry | B2B SaaS |
| Geography | Global |
| Currency | USD (Base) |
| Time Span | 5 Years |
| Granularity | Daily |
| Database | PostgreSQL |
| Generator | Python |

---

# 6.5 Business Entities

The dataset consists of the following business entities.

## Account Domain

- Accounts
- Contacts
- Industries
- Account Segments
- Account Health

---

## Sales Domain

- Sales Representatives
- Opportunities
- Opportunity Stages
- Quotes
- Orders
- Order Items

---

## Subscription Domain

- Products
- Pricing Plans
- Subscriptions
- Subscription Events
- Renewals
- Licenses

---

## Finance Domain

- Invoices
- Payments
- Refunds

---

## Marketing Domain

- Campaigns
- Lead Sources
- Leads
- Marketing Touchpoints

---

## Customer Success Domain

- Support Tickets
- Ticket Comments
- Customer Success Activities

---

## Machine Learning Domain

- Prediction History
- Feature Store
- Model Registry

---

## Monitoring Domain

- API Logs
- ETL Logs
- System Logs

---

# 6.6 Initial Dataset Volume (Version 1)

| Entity | Records |
|---------|---------:|
| Accounts | 5,000 |
| Contacts | 15,000 |
| Products | 20 |
| Pricing Plans | 60 |
| Sales Representatives | 50 |
| Opportunities | 25,000 |
| Quotes | 20,000 |
| Orders | 18,000 |
| Order Items | 45,000 |
| Subscriptions | 12,000 |
| Subscription Events | 50,000 |
| Invoices | 25,000 |
| Payments | 25,000 |
| Refunds | 500 |
| Campaigns | 100 |
| Leads | 15,000 |
| Marketing Touchpoints | 60,000 |
| Support Tickets | 20,000 |
| Ticket Comments | 60,000 |
| Customer Success Activities | 30,000 |

---

# 6.7 Business Rules

The dataset follows predefined business rules to ensure consistency.

Examples include:

- Every contact belongs to one account.
- Every subscription belongs to one account.
- Every invoice belongs to one subscription.
- Every payment belongs to one invoice.
- Every opportunity is owned by one sales representative.
- Every order originates from a successful opportunity.
- Every support ticket belongs to one account.
- Every lead is associated with a marketing campaign.
- Opportunities progress through defined sales stages.
- Renewals occur before subscription expiration.
- Refunds cannot exceed invoice amounts.

---

# 6.8 Temporal Behaviour

Business activity changes over time to reflect realistic operational patterns.

The dataset includes:

- Seasonal sales cycles.
- Monthly recurring revenue.
- Quarterly growth.
- Marketing campaign spikes.
- End-of-quarter sales acceleration.
- Customer renewals.
- Customer churn.
- Random operational fluctuations.

---

# 6.9 Machine Learning Support

The dataset is intentionally designed to support:

- Sales Forecasting
- Customer Churn Prediction
- Lead Scoring
- Customer Lifetime Value Prediction
- Customer Segmentation
- Recommendation Systems
- Anomaly Detection

Every target variable is generated using explainable business logic rather than arbitrary labels.

---

# 6.10 Data Quality

The generated dataset maintains:

- Referential Integrity
- Consistent Foreign Keys
- Valid Date Relationships
- Realistic Monetary Values
- Controlled Missing Values
- Duplicate Prevention
- Business Rule Validation
- Audit Timestamps

---

# 6.11 Dataset Evolution

Future versions of the dataset will introduce:

- Real-time event streams.
- Multi-currency transactions.
- International taxation.
- Multiple business units.
- Multiple SaaS products.
- Streaming analytics.
- Enterprise-scale datasets (1M+ records).