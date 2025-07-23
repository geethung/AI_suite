def hr_prompt(company: str, date: str, context: str) -> str:
    return f"""
**Standard Operating Procedure (SOP) - Human Resources Department**

**Company:** {company}  
**Date:** {date}

---

**Background & Inputs:**

{context}

---

**SOP Document:**

Based on the above inputs, please draft a comprehensive SOP for the Human Resources (HR) department. The SOP should cover:

1. Department goals and objectives  
2. Recruitment and onboarding process  
3. Compliance and regulatory responsibilities  
4. Employee performance management  
5. Conflict resolution policies  
6. Any additional HR-specific workflows

Use clear, professional, and concise language. The SOP should be suitable for inclusion in a company handbook.
"""
