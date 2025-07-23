def sales_prompt(company, date, context):
    return f"""
**Standard Operating Procedure (SOP)**

**Company:** {company}  
**Department:** Sales  
**Date:** {date}

---

**1. Document Control**

| Version | Author        | Date       | Description         |
|---------|---------------|------------|---------------------|
| 1.0     | Sales Manager | {date}     | Initial SOP Draft   |

---

**2. Purpose and Scope**

The Sales department is responsible for generating revenue by acquiring and retaining customers. Its scope includes lead generation, pipeline management, customer engagement, deal closure, and account management.

Below is context provided from department insights:
{context}

---

**3. Procedures**

Sales procedures may include:
{context}

Examples:
1. Lead qualification and segmentation  
2. Sales call preparation  
3. CRM documentation  
4. Negotiation and proposal process  
5. Deal closure and hand-off to account team  
6. Performance tracking and reporting

---

**4. Compliance**

Include:
- CRM usage guidelines  
- Discount approval workflows  
- Sales ethics and legal contracts  
- Internal sales policy and target declarations

---

**5. Revision History**

| Version | Date       | Changes             |
|---------|------------|---------------------|
| 1.0     | {date}     | First draft created |
"""
