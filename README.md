## Dependencies
- Python 3.10
  - Dependencies are listed in `requirements.txt`
- Anthropic API Key
  - got to: https://www.anthropic.com/pricing#anthropic-api

## Running Program
1. Clone the repository
2. Install dependencies

```bash pip install -r requirements.txt```

3. Copy and Paste job descriptions in separate text files in the *postings* folder
4. Fill out the `profiles.yaml` file in the *profiles* folder
  - Optional - save your profile picture in the *assets* folder if you use resume template 01
5. Run the program
  - Be sure to enter your API key if not already in your environment variables

```python rez-me-up.py```

6. Check the *resumes* folder for your resume(s)
7. Edit the HTML resume to your liking
8. Print to PDF via your browser, excluding headers and footers
