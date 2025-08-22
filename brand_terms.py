import re
import pandas as pd

def get_brand_terms():
    return [
        # General Brand
        "leapscholar", "leap scholar", "joinleap", "join leap", "leap platform",

        # Leap Finance
        "leap finance", "leapfinance", "leap funding", "leapfunding",
        "leap loan", "leap loans", "leapfinance loan", "leap finance review",

        # IELTS Prep & Training
        "leap ielts", "leapielts", "leap scholar ielts", "ielts with leap",
        "leap coaching", "leap classes", "leap training", "leap preparation", "ielts leap scholar",

        # Mentorship & Counseling
        "leap mentor", "leap mentors", "leap mentorship", "leap scholar mentorship",
        "leap counselor", "leap consultant", "leap support",

        # Visa & Immigration
        "leap visa", "leap visa help", "leap immigration", "leap visa team",
        "visa with leap", "leap scholar visa",

        # Funding & Loans
        "loan from leap", "leap study loan", "leap loan approval",
        "leap loan delay", "leap funding issue",

        # Student Experience
        "leap journey", "my leap experience", "leap student",
        "leap university admit", "leap admit", "leap scholar canada",

        # Indirect mentions
        "leap referral", "referred by leap", "leap study abroad", "leap abroad help"
    ]

def filter_by_brand_terms(df: pd.DataFrame, column: str = 'Text') -> pd.DataFrame:
    terms = get_brand_terms()
    pattern = '|'.join([r'\b' + re.escape(term) + r'\b' for term in terms])
    return df[df[column].str.contains(pattern, case=False, na=False)]
