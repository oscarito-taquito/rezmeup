import requests
import json
import os


# Claude API endpoint and key
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")


# # Paths to resume and job posting files
current_dir = os.path.dirname(os.path.realpath(__file__))
profile_path = os.path.join(current_dir, "../profiles/profile.yaml")
jobs_path = os.path.join(current_dir, "../postings")
gen_path = os.path.join(current_dir, "../profiles/ai-gen")


class rezme:
    def __init__(
        self,
        api_key=CLAUDE_API_KEY,
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        version="2023-06-01",
        current_dir=current_dir,
        profile_path=profile_path,
        jobs_path=jobs_path,
        gen_path=gen_path,
    ):
        self.gen_path = gen_path
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.version = version

    def read_file(self, filename):
        with open(filename, "r") as file:
            return file.read()

    def write_file(self, filename, content):
        with open(filename, "w") as file:
            file.write(content)

    def update_resume(self, resume, job_posting):
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
            "anthropic-version": self.version,
        }

        data = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": f"""Here is my current resume:
                        \n\n{resume}\n\n

                        And here is a job posting:

                        \n\n{job_posting}

                        \n\nPlease update my resume to better match this job posting.
                        Highlight relevant skills and experiences, and tailor the content to the job requirements.
                        Return only the updated resume text""",
                }
            ],
        }

        response = requests.post(CLAUDE_API_URL, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")


def main():
    g = rezme()
    resume = g.read_file(profile_path)
    jobs = [x for x in os.listdir(jobs_path) if x.endswith(".txt")]
    for f in jobs:
        try:
            print(f"Processing file: {f}")
            g.read_file(f"{jobs_path}/{f}")
            updated_resume = g.update_resume(resume, g.read_file(f"{jobs_path}/{f}"))
            g.write_file(f"{gen_path}/{f.replace('.txt', '.yaml')}", updated_resume)
        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
