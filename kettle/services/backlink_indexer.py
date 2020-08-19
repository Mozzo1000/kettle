import markdown2
import os


class BacklinkIndexer:
    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.gathered_links = {}

    def add(self, file, node):
        with open(os.path.join(self.root_folder, file), 'r', encoding='utf-8', errors='ignore') as markdown_file:
            markdown_content = markdown2.markdown(markdown_file.read(), extras=['metadata'])

        if markdown_content.metadata:
            markdown_list = markdown_content.metadata['links'].split(',')
            self.gathered_links[node] = markdown_list

    def get_links(self):
        return self.gathered_links