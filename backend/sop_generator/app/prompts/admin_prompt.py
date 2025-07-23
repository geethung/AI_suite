def admin_prompt(company: str, date: str, context: str) -> str:
    return f"""
**Standard Operating Procedure (SOP) - Administration Department**

**Company:** {company}  
**Date:** {date}

---

**Background & Inputs:**

{context}

---

**SOP Document:**

Using the above inputs, draft a detailed SOP for the Administration department. The SOP should include:

1. Overview of administrative goals and responsibilities  
2. Standard workflows and processes  
3. Office and facility management procedures  
4. Document and record management policies  
5. Approval hierarchies and escalation protocols  
6. Any other administration-specific tasks or best practices

Use formal, structured language that aligns with professional business standards. The SOP should be ready for inclusion in a company-wide policy manual.
"""
