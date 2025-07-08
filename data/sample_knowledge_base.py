"""
Sample knowledge base data for TechCorp customer support.
This includes FAQs, product information, and company policies.
"""

COMPANY_INFO = {
    "name": "TechCorp",
    "description": "A leading technology company providing innovative software solutions",
    "established": "2010",
    "headquarters": "San Francisco, CA",
    "contact": {
        "phone": "1-800-TECHCORP",
        "email": "support@techcorp.com",
        "website": "https://www.techcorp.com"
    }
}

PRODUCTS = [
    {
        "name": "CloudSync Pro",
        "category": "Cloud Storage",
        "description": "Enterprise-grade cloud storage solution with advanced synchronization",
        "features": [
            "Unlimited storage",
            "Real-time sync across devices",
            "Advanced security encryption",
            "Team collaboration tools",
            "API integrations"
        ],
        "pricing": {
            "basic": "$9.99/month",
            "professional": "$19.99/month",
            "enterprise": "Custom pricing"
        }
    },
    {
        "name": "DataAnalytics Suite",
        "category": "Analytics",
        "description": "Comprehensive data analytics platform for business intelligence",
        "features": [
            "Real-time data visualization",
            "Custom dashboard creation",
            "Machine learning insights",
            "Multi-source data integration",
            "Automated reporting"
        ],
        "pricing": {
            "starter": "$49.99/month",
            "business": "$99.99/month",
            "enterprise": "Custom pricing"
        }
    },
    {
        "name": "SecureVPN",
        "category": "Security",
        "description": "High-speed VPN service with military-grade encryption",
        "features": [
            "256-bit AES encryption",
            "No-logs policy",
            "Global server network",
            "Kill switch protection",
            "Multi-device support"
        ],
        "pricing": {
            "monthly": "$12.99/month",
            "annual": "$79.99/year",
            "lifetime": "$299.99 one-time"
        }
    }
]

FAQS = [
    {
        "category": "General",
        "question": "What is TechCorp?",
        "answer": "TechCorp is a leading technology company founded in 2010, specializing in innovative software solutions including cloud storage, data analytics, and security services."
    },
    {
        "category": "General",
        "question": "How can I contact customer support?",
        "answer": "You can reach our customer support team by phone at 1-800-TECHCORP, email at support@techcorp.com, or through our website chat feature available 24/7."
    },
    {
        "category": "Account",
        "question": "How do I create an account?",
        "answer": "To create an account, visit our website at www.techcorp.com and click 'Sign Up'. You'll need to provide your email address, create a password, and verify your email."
    },
    {
        "category": "Account",
        "question": "I forgot my password. How can I reset it?",
        "answer": "Click 'Forgot Password' on the login page, enter your email address, and we'll send you a password reset link. Follow the instructions in the email to create a new password."
    },
    {
        "category": "Account",
        "question": "How do I change my account information?",
        "answer": "Log into your account and go to 'Account Settings'. You can update your personal information, change your password, and manage your subscription preferences."
    },
    {
        "category": "Billing",
        "question": "What payment methods do you accept?",
        "answer": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers for enterprise customers."
    },
    {
        "category": "Billing",
        "question": "How do I cancel my subscription?",
        "answer": "You can cancel your subscription anytime by going to 'Account Settings' > 'Subscription' and clicking 'Cancel Subscription'. Your service will continue until the end of your current billing period."
    },
    {
        "category": "Billing",
        "question": "Do you offer refunds?",
        "answer": "Yes, we offer a 30-day money-back guarantee for all our products. If you're not satisfied, contact our support team within 30 days of purchase for a full refund."
    },
    {
        "category": "CloudSync Pro",
        "question": "How much storage do I get with CloudSync Pro?",
        "answer": "CloudSync Pro offers unlimited storage for all plans. You can store as many files as you need without worrying about storage limits."
    },
    {
        "category": "CloudSync Pro",
        "question": "Can I share files with my team?",
        "answer": "Yes, CloudSync Pro includes team collaboration features. You can share files and folders with team members, set permissions, and collaborate in real-time."
    },
    {
        "category": "CloudSync Pro",
        "question": "Is my data secure?",
        "answer": "Absolutely. CloudSync Pro uses advanced AES-256 encryption for all data transfers and storage. Your files are protected with military-grade security."
    },
    {
        "category": "DataAnalytics Suite",
        "question": "What data sources can I connect to?",
        "answer": "DataAnalytics Suite supports connections to databases (MySQL, PostgreSQL, MongoDB), cloud services (AWS, Google Cloud, Azure), APIs, CSV files, and many other data sources."
    },
    {
        "category": "DataAnalytics Suite",
        "question": "Do you provide training for new users?",
        "answer": "Yes, we offer comprehensive training including video tutorials, documentation, webinars, and one-on-one training sessions for enterprise customers."
    },
    {
        "category": "SecureVPN",
        "question": "How many devices can I use with SecureVPN?",
        "answer": "SecureVPN supports up to 10 simultaneous connections on a single account, allowing you to protect all your devices including computers, phones, and tablets."
    },
    {
        "category": "SecureVPN",
        "question": "Do you keep logs of my activity?",
        "answer": "No, we have a strict no-logs policy. We don't track, collect, or store any information about your online activities while using SecureVPN."
    },
    {
        "category": "Technical",
        "question": "What are your system requirements?",
        "answer": "Our products are compatible with Windows 10+, macOS 10.14+, iOS 12+, and Android 8+. For web applications, we support Chrome, Firefox, Safari, and Edge browsers."
    },
    {
        "category": "Technical",
        "question": "Do you offer API access?",
        "answer": "Yes, we provide RESTful APIs for all our products. API documentation and developer resources are available in our developer portal."
    }
]

POLICIES = [
    {
        "title": "Privacy Policy",
        "summary": "TechCorp is committed to protecting your privacy. We collect only necessary information and never sell your data to third parties.",
        "key_points": [
            "We collect minimal personal information",
            "Data is encrypted and securely stored",
            "We don't sell or share your data",
            "You can request data deletion at any time",
            "We comply with GDPR and CCPA regulations"
        ]
    },
    {
        "title": "Terms of Service",
        "summary": "By using TechCorp services, you agree to our terms which outline acceptable use and service limitations.",
        "key_points": [
            "Service is provided 'as is'",
            "Users must comply with acceptable use policy",
            "TechCorp reserves the right to modify services",
            "Disputes are resolved through arbitration",
            "Service availability is not guaranteed 100%"
        ]
    },
    {
        "title": "Refund Policy",
        "summary": "We offer a 30-day money-back guarantee for all products and services.",
        "key_points": [
            "30-day money-back guarantee",
            "Refunds processed within 5-7 business days",
            "No questions asked for first 30 days",
            "Enterprise customers may have custom refund terms",
            "Refunds are issued to original payment method"
        ]
    }
]

TROUBLESHOOTING = [
    {
        "product": "CloudSync Pro",
        "issue": "Sync not working",
        "solution": "1. Check your internet connection\n2. Restart the CloudSync application\n3. Verify your account credentials\n4. Check if you have sufficient storage space\n5. Contact support if issue persists"
    },
    {
        "product": "CloudSync Pro",
        "issue": "Slow upload speeds",
        "solution": "1. Check your internet speed\n2. Pause other bandwidth-intensive applications\n3. Try uploading during off-peak hours\n4. Use the desktop application instead of web interface\n5. Contact support for speed optimization tips"
    },
    {
        "product": "DataAnalytics Suite",
        "issue": "Dashboard not loading",
        "solution": "1. Clear your browser cache and cookies\n2. Try a different browser\n3. Check if JavaScript is enabled\n4. Disable browser extensions temporarily\n5. Contact support if problem continues"
    },
    {
        "product": "SecureVPN",
        "issue": "Cannot connect to VPN",
        "solution": "1. Check your internet connection\n2. Try a different VPN server location\n3. Restart your device\n4. Update the VPN application\n5. Check firewall settings\n6. Contact support for advanced troubleshooting"
    }
]

def get_knowledge_base_data():
    """
    Return all knowledge base data as a structured dictionary.
    """
    return {
        "company_info": COMPANY_INFO,
        "products": PRODUCTS,
        "faqs": FAQS,
        "policies": POLICIES,
        "troubleshooting": TROUBLESHOOTING
    }

def get_searchable_content():
    """
    Return knowledge base content formatted for search and memory storage.
    """
    searchable_items = []
    
    # Add company info
    searchable_items.append({
        "type": "company_info",
        "content": f"{COMPANY_INFO['name']} is {COMPANY_INFO['description']}. Founded in {COMPANY_INFO['established']}, headquartered in {COMPANY_INFO['headquarters']}. Contact: {COMPANY_INFO['contact']['phone']}, {COMPANY_INFO['contact']['email']}"
    })
    
    # Add product information
    for product in PRODUCTS:
        content = f"{product['name']} is a {product['category']} product. {product['description']}. Features: {', '.join(product['features'])}."
        searchable_items.append({
            "type": "product_info",
            "product": product['name'],
            "content": content
        })
    
    # Add FAQs
    for faq in FAQS:
        content = f"Q: {faq['question']} A: {faq['answer']}"
        searchable_items.append({
            "type": "faq",
            "category": faq['category'],
            "content": content
        })
    
    # Add policies
    for policy in POLICIES:
        content = f"{policy['title']}: {policy['summary']} Key points: {', '.join(policy['key_points'])}"
        searchable_items.append({
            "type": "policy",
            "title": policy['title'],
            "content": content
        })
    
    # Add troubleshooting
    for trouble in TROUBLESHOOTING:
        content = f"Issue: {trouble['issue']} for {trouble['product']}. Solution: {trouble['solution']}"
        searchable_items.append({
            "type": "troubleshooting",
            "product": trouble['product'],
            "content": content
        })
    
    return searchable_items 