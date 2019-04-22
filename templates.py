# from jinja2 import Template, Environment, FileSystemLoader

# env = Environment(loader=FileSystemLoader('.'))
# template = env.get_template('sample.tpl')

# data = {'items': ['みかん', 'りんご', 'バナナ']}
# disp_text = template.render(data)
# print(disp_text)
import jinja2 as j2
import os.path as path

BASE_DIR = path.abspath(path.dirname(__file__))
TEMPLATES_DIR = path.join(BASE_DIR, 'templates')


class Templates:
    def __init__(self, directory: str = TEMPLATES_DIR):
        if not path.exists(directory):
            raise Exception('{} does not exist'.format(
                path.abspath(directory)))
        self.__env = j2.Environment(loader=j2.FileSystemLoader(directory))

    @staticmethod
    def default():
        return Templates()

    def read(self, src: str, **kwargs) -> str:
        template = self.__env.get_template(src)
        data = kwargs
        return template.render(data)

    def readme(self, contest_name: str, contest_num: str, problems: list) -> str:
        return self.read(
            'README.j2',
            contest_name=contest_name,
            contest_num=contest_num,
            problems=problems)
