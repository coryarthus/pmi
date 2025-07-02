# schema.py

# Medical Types
medical_types = [
    {
        "category": "Medical",
        "type": "Interaction",
        "description": "Questions about how a product interacts with other drugs, foods, or medical conditions.",
        "keywords": ["drug interaction", "contraindication", "combination", "co-administer", "compatibility"]
    },
    {
        "category": "Medical",
        "type": "Safety",
        "description": "Questions related to side effects, adverse reactions, toxicity, or warnings.",
        "keywords": ["side effect", "safety", "toxic", "risk", "adverse", "reaction"]
    },
    {
        "category": "Medical",
        "type": "Stability",
        "description": "Questions about storage conditions, shelf life, or how stable the product is over time.",
        "keywords": ["expiry", "expiration", "shelf life", "stability", "storage", "temperature"]
    },
    {
        "category": "Medical",
        "type": "Dosing",
        "description": "Questions about appropriate dosage, frequency, or administration routes.",
        "keywords": ["dose", "dosing", "frequency", "administration", "how to take"]
    },
    {
        "category": "Medical",
        "type": "Efficacy",
        "description": "Inquiries about how well a product works or clinical outcomes.",
        "keywords": ["efficacy", "effectiveness", "results", "response", "outcome"]
    },
    {
        "category": "Medical",
        "type": "Mechanism of Action",
        "description": "Questions about how the product works in the body.",
        "keywords": ["mechanism", "how it works", "mode of action", "MOA"]
    },
    {
        "category": "Medical",
        "type": "Formulation",
        "description": "Questions about ingredients, excipients, or formulation differences.",
        "keywords": ["ingredient", "formulation", "excipient", "inactive", "composition"]
    },
    {
        "category": "Medical",
        "type": "Pediatric Use",
        "description": "Questions about use in children, including dosing or safety.",
        "keywords": ["child", "pediatric", "baby", "infant", "kid", "age"]
    },
    {
        "category": "Medical",
        "type": "Off-label Use",
        "description": "Inquiries about uses not officially approved or indicated.",
        "keywords": ["off-label", "unapproved", "experimental", "not indicated"]
    },
    {
        "category": "Medical",
        "type": "Clinical Study Information",
        "description": "Questions requesting information about ongoing or past clinical trials.",
        "keywords": ["clinical trial", "study", "phase", "efficacy data", "research"]
    }
]

# Non-Medical Types
non_medical_types = [
    {
        "category": "Non-Medical",
        "type": "Directory Assistance",
        "description": "Requests for contact information or to be connected with a department or individual.",
        "keywords": ["phone", "email", "contact", "reach", "how do I talk to", "find person"]
    },
    {
        "category": "Non-Medical",
        "type": "Customer Feedback",
        "description": "General comments, praise, or complaints about products, services, or experiences.",
        "keywords": ["feedback", "complaint", "suggestion", "review", "comment", "experience"]
    },
    {
        "category": "Non-Medical",
        "type": "Legal",
        "description": "Questions related to legal concerns, including litigation, IP, or regulatory compliance.",
        "keywords": ["lawyer", "legal", "court", "lawsuit", "regulatory", "compliance"]
    },
    {
        "category": "Non-Medical",
        "type": "Order Status",
        "description": "Inquiries about order tracking, shipment, or fulfillment.",
        "keywords": ["order", "shipment", "track", "delivery", "status"]
    },
    {
        "category": "Non-Medical",
        "type": "Product Availability",
        "description": "Questions about whether a product is in stock, backordered, or discontinued.",
        "keywords": ["available", "stock", "backorder", "discontinued", "supply"]
    },
    {
        "category": "Non-Medical",
        "type": "Technical Support",
        "description": "Help with using a system, portal, or website.",
        "keywords": ["login", "portal", "website", "technical issue", "can't access"]
    },
    {
        "category": "Non-Medical",
        "type": "Rep Request",
        "description": "Requests for a sales representative to visit or contact.",
        "keywords": ["sales rep", "representative", "contact me", "speak with rep"]
    },
    {
        "category": "Non-Medical",
        "type": "Samples Request",
        "description": "Requests for product samples, typically for HCPs.",
        "keywords": ["sample", "request sample", "try", "starter pack"]
    },
    {
        "category": "Non-Medical",
        "type": "Careers",
        "description": "Inquiries about job openings or application status.",
        "keywords": ["job", "career", "hiring", "application", "apply"]
    },
    {
        "category": "Non-Medical",
        "type": "Media Inquiry",
        "description": "Requests from journalists or media representatives.",
        "keywords": ["press", "media", "news", "interview", "statement"]
    }
]
