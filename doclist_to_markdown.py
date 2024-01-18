doclist = open("doclist.txt", "r").read()
doclist = doclist.split("\n")

import requests
import warnings
import urllib3

# Filter out the InsecureRequestWarning
warnings.filterwarnings(
    "ignore",
    message="Unverified HTTPS request is being made",
    category=urllib3.exceptions.InsecureRequestWarning,
)

# os.environ["http_proxy"] = ""
# os.environ["https_proxy"] = ""
# os.environ["all_proxy"] = ""
sess = requests.Session()

abnormal_names = []
abnormal_sitemaps = []

url_prefix = "https://james4ever0.github.io/"
passed_sitemap_urls = []

for line in doclist:
    line = line.strip()
    if line:
        url = url_prefix + line
        sitemap_url = url + "/sitemap.xml"
        resp = sess.get(url, verify=False, stream=True)
        if not resp.status_code == 200:
            abnormal_names.append(line)
        else:
            print(f"[{line if not line.endswith('_doc') else line[:-4]}]({url})")
            resp = sess.get(sitemap_url, verify=False, stream=True)
            if not resp.status_code == 200:
                abnormal_sitemaps.append(sitemap_url)
            else:
                passed_sitemap_urls.append(sitemap_url)
        resp.close()

from jinja2 import Environment, FileSystemLoader

# Load the template from file
file_loader = FileSystemLoader(
    "."
)  # Replace 'path_to_templates_directory' with the actual path
env = Environment(loader=file_loader)
template = env.get_template(
    "sitemap.xml.j2"
)  # Replace 'sitemap_template.html' with the actual template file name

# Render the template with the data
rendered_template = template.render(url_list=passed_sitemap_urls)

# Write the template content to a file
with open("sitemap.xml", "w+", encoding="utf-8") as file:
    file.write(rendered_template)

print("sitemap rendered successfully")
if abnormal_names:
    print("[ABNORMAL NAMES]".center(60, "-"))
    for it in abnormal_names:
        print(it)

if abnormal_sitemaps:
    print("[ABNORMAL SITEMAPS]".center(60, "-"))
    for it in abnormal_sitemaps:
        print(it)
