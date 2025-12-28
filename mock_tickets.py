from typing import List, Optional
from pydantic import BaseModel, Field

class RootCauseAnalysis(BaseModel):
    summary: str = Field(description="A summary of the issue.")
    category: str = Field(description="The category of the issue, e.g., 'Payment Failure', 'Login Issue'.")
    root_cause: str = Field(description="The identified root cause of the issue.")
    issue_type: str = Field(description="Classification of the issue, e.g., 'Bug', 'UX gap', 'Performance', 'Misconfiguration', 'User error'.")
    severity: str = Field(description="The severity of the issue, e.g., 'High', 'Medium', 'Low'.")
    confidence: float = Field(description="A confidence score (0-1) in the analysis.")
    engineering_actions: List[str] = Field(description="Suggested actions for the engineering team.")
    product_actions: List[str] = Field(description="Suggested actions for the product team.")
    support_reply_suggestion: str = Field(description="A suggested reply for the support team.")
    similar_incidents: Optional[List[str]] = Field(default_factory=list, description="List of IDs of similar past incidents.")

MOCK_TICKETS_DATA = [
    {
        "ticket_id": "INC-2024-001",
        "ticket_content": "Subject: Payments failing again!!!\n\nHi team,\nThis is the third time this week that payments have failed for our EU customers.\nThe checkout page just spins and then errors out.\nWe lost customers because of this.\nPlease fix ASAP.",
        "analysis": {
            "summary": "EU customers are unable to complete payments due to checkout timeout.",
            "category": "Payment Failure",
            "root_cause": "Third-party payment gateway timeout in EU region",
            "issue_type": "Bug",
            "severity": "High",
            "confidence": 0.86,
            "engineering_actions": [
                "Add timeout handling and retries",
                "Implement regional fallback gateway",
                "Improve gateway monitoring"
            ],
            "product_actions": [
                "Display clearer payment failure messages",
                "Add status page for payment incidents"
            ],
            "support_reply_suggestion": "Acknowledge issue, explain temporary workaround, provide ETA.",
            "similar_incidents": ["INC-2024-11-EU-PAYMENTS"]
        }
    },
    {
        "ticket_id": "INC-2024-002",
        "ticket_content": "Subject: Login issue on mobile app\n\nI can't log in to the mobile app (Android). It keeps saying 'invalid credentials' even though I'm using the correct password. I've tried reinstalling.",
        "analysis": {
            "summary": "User unable to log in to Android mobile app with correct credentials.",
            "category": "Authentication",
            "root_cause": "Mobile app cache corruption or API authentication token mismatch.",
            "issue_type": "Bug",
            "severity": "Medium",
            "confidence": 0.92,
            "engineering_actions": [
                "Investigate recent Android app updates for login regressions",
                "Check authentication service logs for failed attempts from mobile clients"
            ],
            "product_actions": [
                "Add 'forgot password' link directly in mobile app login flow",
                "Improve error messages for login failures"
            ],
            "support_reply_suggestion": "Suggest clearing app cache manually, confirm correct password, offer password reset."
        }
    },
    {
        "ticket_id": "INC-2024-003",
        "ticket_content": "Subject: Can't upload profile picture\n\nEvery time I try to upload a new profile picture, it just fails with a generic error. The file is a JPG and less than 2MB.",
        "analysis": {
            "summary": "User unable to upload profile picture, receiving generic error.",
            "category": "Profile Management",
            "root_cause": "Backend image processing service failing or incorrect file type validation.",
            "issue_type": "Bug",
            "severity": "Low",
            "confidence": 0.80,
            "engineering_actions": [
                "Check image upload service logs for errors",
                "Verify file type and size validation logic on the backend"
            ],
            "product_actions": [
                "Provide clearer error messages for image uploads (e.g., 'Invalid file type', 'File too large')",
                "Add supported file types and size limits to the UI"
            ],
            "support_reply_suggestion": "Ask for browser/OS details, suggest trying a different image or browser, offer to upload on user's behalf."
        }
    },
    {
        "ticket_id": "INC-2024-004",
        "ticket_content": "Subject: Slow loading dashboard\n\nMy dashboard is loading very slowly this morning, especially the analytics charts. It takes almost 30 seconds to load.",
        "analysis": {
            "summary": "User experiencing slow loading times on the analytics dashboard.",
            "category": "Performance",
            "root_cause": "Inefficient database queries for analytics data or overloaded dashboard service.",
            "issue_type": "Performance",
            "severity": "Medium",
            "confidence": 0.88,
            "engineering_actions": [
                "Optimize database queries for dashboard analytics",
                "Scale up dashboard service instances",
                "Implement caching for frequently accessed analytics data"
            ],
            "product_actions": [
                "Introduce loading spinners or skeleton screens for slow-loading components",
                "Consider displaying partial data faster with full data loading incrementally"
            ],
            "support_reply_suggestion": "Acknowledge performance issue, thank for feedback, mention team is investigating, suggest refreshing."
        }
    },
    {
        "ticket_id": "INC-2024-005",
        "ticket_content": "Subject: Email notification not working\n\nI'm not receiving any email notifications for new messages, even though they are enabled in my settings.",
        "analysis": {
            "summary": "User not receiving email notifications despite settings being enabled.",
            "category": "Notifications",
            "root_cause": "Email sending service outage or incorrect user email preferences stored in the database.",
            "issue_type": "Bug",
            "severity": "Low",
            "confidence": 0.85,
            "engineering_actions": [
                "Check email sending service logs for failures",
                "Verify user's notification settings in the database"
            ],
            "product_actions": [
                "Add in-app notification center as a fallback",
                "Improve clarity of notification settings UI"
            ],
            "support_reply_suggestion": "Verify user's email address, check spam folder, ask about recent changes to settings, offer to manually trigger a test notification."
        }
    }
]
