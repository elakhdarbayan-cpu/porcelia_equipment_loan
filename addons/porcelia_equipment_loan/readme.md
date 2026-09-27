# Porcelia Equipment Loan Manager

Odoo module for managing equipment loans to employees.

**Module technical name:** `porcelia_equipment_loan`  
**Version:** 18.0.1.0.0  
**Author:** Bayan Elakhdar  
**License:** LGPL-3

---

## Features Implemented

### Backend
- **Models**
  - `equipment.category` (hierarchical categories with complete name)
  - `equipment.item` (code sequence, daily rate, condition score, computed state)
  - `equipment.loan` (full loan lifecycle with tracking)

- **Business Rules**
  - No double booking (overlap detection on confirm)
  - Date validation (due date must be after start date)
  - Penalty calculation on late return
  - Workflow: Draft → Confirmed → Returned / Cancelled
  - Deletion only allowed for draft/cancelled loans

- **Security**
  - Groups: Equipment User / Equipment Manager
  - Access rights per model
  - Record rule: User sees only own loans, Manager sees all

- **Views & UX**
  - List / Form / Search views for Loans
  - List / Form views for Items and Categories
  - Smart button on Item showing loan count
  - Statusbar + header buttons
  - Chatter tracking on loans
  - Overdue decoration in loan list

- **Wizard**
  - Return Loan wizard (date, condition score, note)

- **Data**
  - Sequences for Item codes and Loan references
  - Demo data (categories + items)
  
- QWeb PDF report

### Not Implemented (deliberately skipped)
- OWL Condition Gauge widget (Part B1)
- OWL Equipment Dashboard (Part B2)
- Systray counter (Bonus)
- Scheduled cron for overdue activities
- Unit tests

**Reason:** Focused on delivering a solid, working backend with correct security and business rules within the available time. Prefer a smaller correct submission over incomplete advanced frontend.

---

## Installation

1. Copy the module to your Odoo addons path
2. Update Apps List
3. Install **Porcelia Equipment Loan**

```bash
# Example
odoo-bin -d your_database -i porcelia_equipment_loan

Usage

Go to Equipment → Configuration → Categories and create categories
Go to Equipment → Items and create equipment items
Go to Equipment → Loans and create a loan
Confirm the loan → item becomes unavailable for overlapping periods
Return the loan (button or wizard) → penalty is calculated if late


Technical Notes

Odoo 18 compatible structure
Uses <list> views
No sudo() abuse in access logic
Standard ORM patterns (@api.depends, constraints, message_post)


GitHub
Repository: https://github.com/elakhdarbayan-cpu/porcelia_equipment_loan

