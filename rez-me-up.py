import os
import datetime as dt
from mods.rezgen import rezme
from mods.htmlgen import htmlme

# variables
current_dir = os.path.dirname(os.path.realpath(__file__))
profile_path = os.path.join(current_dir, "profiles/profile.yaml")
jobs_path = os.path.join(current_dir, "postings")
gen_path = os.path.join(current_dir, "profiles/ai-gen")
template_path = os.path.join(current_dir, "resume-templates")
rez_path = os.path.join(current_dir, "resumes")
ts = dt.datetime.now().strftime("%Y-%m-%d")


# optional params. below are also the default values
# you can store your key in your shell environment
# or pass it as a string
rez_params = {
    "api_key": "your_api_key",  # Anthropic API key
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 4000,
    "version": "2023-06-01",
}

# choose your base resume template (see resume-templates folder)
template_id = "02"

# use your base resume profile and create tailored profiles
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

# choose your base html template and create tailored html resumes
h = htmlme()
profiles = os.listdir(gen_path)
profiles = [x for x in profiles if x.endswith(".yaml")]
for profile in profiles:
    profile_path = os.path.join(gen_path, profile)
    h.to_html(profile_path, template_id=template_id)
