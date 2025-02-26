from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))

def get_email_template(template_name, **kwargs):
    template = env.get_template(template_name)
    rendered =  template.render(**kwargs)
    print("📧 Rendered Template Output:\n", rendered)  # Debugging
    return rendered