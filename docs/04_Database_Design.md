# 5. Database Design

## 5.1 Database Overview

BusinessPilot AI uses PostgreSQL as its primary relational database management system (RDBMS).

The database is designed to support transactional operations (OLTP), analytical workloads (OLAP), machine learning pipelines, and enterprise monitoring within a unified platform.

Instead of using a single schema for all data, the platform separates responsibilities into multiple logical schemas to improve maintainability, security, scalability, and analytical performance.

---

## 5.2 Database Technology

| Property | Value |
|----------|-------|
| Database Engine | PostgreSQL 17+ |
| Database Name | BusinessPilot_db |
| Character Encoding | UTF-8 |
| Time Zone | UTC |
| Primary Key Strategy | UUID |
| ORM | SQLAlchemy |
| Migration Tool | Alembic |
| Query Language | SQL |

---

## 5.3 Database Schemas

The platform is organized into five logical schemas.

| Schema | Purpose |
|---------|---------|
| app | Operational business data |
| staging | Temporary ETL and imported data |
| warehouse | Analytical star schema |
| ml | Machine learning metadata |
| monitoring | Logs, audits and monitoring |

---

## 5.4 Business Domains

The operational database is organized into the following business domains.

### Customer Management

Responsible for storing customer information, subscriptions, company profiles, contacts, and lifecycle data.

---

### Product Management

Stores SaaS products, pricing plans, product categories, and licensing information.

---

### Sales Management

Tracks opportunities, quotations, sales orders, invoices, and payments.

---

### Marketing

Stores campaigns, lead sources, campaign performance, and marketing attribution.

---

### Customer Success

Stores customer support tickets, renewals, customer health metrics, satisfaction scores, and churn indicators.

---

### Finance

Stores payments, revenue, subscriptions, refunds, and financial KPIs.

---

### Administration

Stores users, authentication, permissions, roles, audit logs, and application configuration.

---

### Artificial Intelligence

Stores model predictions, feature metadata, model versions, and prediction history.

---

## 5.5 Database Design Principles

The database follows the following principles.

- Third Normal Form (3NF) for operational tables
- Star Schema for analytical tables
- UUID primary keys
- Foreign key constraints
- Soft delete strategy where appropriate
- Audit columns on all operational tables
- Immutable warehouse fact tables
- Read-only analytical schema
- Consistent naming conventions