import os
import yaml
import datetime as dt


# paths
current_dir = os.path.dirname(os.path.realpath(__file__))
ai_profiles = os.path.join(current_dir, "../profiles/ai-gen")
template_path = os.path.join(current_dir, "../resume-templates")
resume_path = os.path.join(current_dir, "../resumes")
ts = dt.datetime.now().strftime("%Y-%m-%d")


class htmlme:
    def __init__(self):
        self.ai_profiles = ai_profiles
        self.resume_path = resume_path

    def to_html(self, profile, template_id="01"):
        template = f"{template_path}/template-{template_id}/index.html"
        output_file_name = f"{profile.split('/')[-1].replace('.yaml', '.html')}"

        with open(profile, "r") as file:
            profile_data = yaml.safe_load(file)

        with open(template, "r") as html_file:
            html_content = html_file.read()

        # personal info
        name = profile_data["personal_info"]["name"]
        location = profile_data["personal_info"]["location"]
        email = profile_data["personal_info"]["email"]
        phone = profile_data["personal_info"]["phone"]
        title = profile_data["personal_info"]["title"]
        url = profile_data["personal_info"]["url"]

        html_content = html_content.replace("<!--name -->", name)
        html_content = html_content.replace("<!--location -->", location)
        html_content = html_content.replace("<!--email -->", email)
        html_content = html_content.replace("<!--phone -->", phone)
        html_content = html_content.replace("<!--title -->", title)
        html_content = html_content.replace("<!--url -->", url)

        # about
        about = profile_data["about"]["intro"]
        html_content = html_content.replace("<!--intro -->", about)

        # skills data
        skills = profile_data.get("skills", [])
        skills_body = ""
        for skill in skills:
            skills_body += f"<li>{skill}</li>"

        html_content = html_content.replace("<!--skills -->", skills_body)

        # experience data
        experiences = profile_data.get("experience", [])
        exp_body = ""
        for experience in experiences:
            html_exp = ""
            html_exp += f"""
                <h4>{experience["title"]} @ {experience["company"]}</h4>
                <p><small><i>{experience["start_date"]} - {experience["end_date"]}</i></small></p>
            """
            html_exp += "<ul>"
            for task in experience["tasks"]:
                html_exp += f"""<li>{task}</li>"""
            html_exp += "</ul>"

            exp_body += html_exp
        html_content = html_content.replace("<!--experience -->", exp_body)

        # education data
        education = profile_data.get("education", [])
        university = education.get("university", "")
        degree = education.get("degree", "")
        html_content = html_content.replace("<!--university -->", university)
        html_content = html_content.replace("<!--degree -->", degree)

        # hobbies
        hobbies = profile_data.get("hobbies", [])
        hobbies_body = ""
        for hobby in hobbies:
            hobbies_body += f"<li>{hobby}</li>"

        html_content = html_content.replace("<!--hobbies -->", hobbies_body)

        # create new directory based on timestamp
        os.makedirs(f"{resume_path}/{ts}", exist_ok=True)

        # copy the css from the template path to the new folder
        css_source = os.path.join(
            template_path, f"template-{template_id}", "styles.css"
        )
        css_destination = os.path.join(resume_path, ts, "styles.css")
        if os.path.exists(css_source):
            with open(css_source, "r") as css_file:
                css_content = css_file.read()
            with open(css_destination, "w") as css_output_file:
                css_output_file.write(css_content)

        # write to output file
        with open(f"{resume_path}/{ts}/{output_file_name}", "w") as output_file:
            output_file.write(html_content)

        return f"{resume_path}/{ts}/{output_file_name}"


def main():
    h = htmlme()
    profiles = os.listdir(ai_profiles)
    profiles = [x for x in profiles if x.endswith(".yaml")]
    for profile in profiles:
        profile_path = os.path.join(ai_profiles, profile)
        h.to_html(profile_path, "02")


if __name__ == "__main__":
    main()
