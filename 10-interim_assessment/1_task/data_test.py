import pytest
import pandas as pd
from pandas import testing
from data import extract_emails, read_csv_to_df

@pytest.mark.parametrize(
    "text, expected_match",
    [
        ("user@example.com", True),
        ("test.email+tag@domain.us.sr", True),

        ("admin@site.org some other text", False),
        ("Hello user@example.com", False),
        ("Contact: test@domain.com", False),
        ("  user@example.com", False),  
        ("not-an-email", False),
        ("user@", False),
        ("@domain.com", False),
        ("", False),
        ("user@domain", False),
        ("user@domain.r", False),
        ("юзер@domain.ru", False),
    ]
)
def test_extract_emails(text, expected_match):
    assert extract_emails(text) == expected_match

def test_read_csv_to_df():
    got = read_csv_to_df("./10-interim_assessment/1_task/test_data/test.csv")
    want = pd.DataFrame(
        {
                'Unnamed: 0': ['Row_1', 'Row_5'],
                'Column_1': ['1', 'no'],
                'Column_2': ['120', 'Non'],
                'Column_3': ['8', 'Nan']
        }
    )
    
    # https://stackoverflow.com/questions/51655623/how-to-ignore-index-comparison-for-pandas-assert-frame-equal
    testing.assert_frame_equal(
        got.reset_index(drop=True), 
        want.reset_index(drop=True)
    )
