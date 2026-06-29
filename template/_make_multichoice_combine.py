#
#  Program to convert several questionnaries in YAML format to
#  Docx document.
#
#  Test Picuino Copyright (c) 2021 Carlos Félix Pardo Martín
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from _make_multichoice import Questionary
import random

multichoice_path = ''
build_path = 'build'
moodle_path = '../moodle'
html_path = '../docs'
images_path= '../images'

moodle_template = 'moodle-multichoice-template.xml'
json_template = 'json-template.json'
html_template = 'game-template.html'

random_seed = 2025


projects = [
{
   'yaml_files': [
      'es-test.yaml',
      ],
   'filename_output': 'es-test-combine',
   'yaml_category': 'Test',
   'yaml_title': 'Test global',
   'max_questions': 50,
   'random_seed': random_seed,
},

]
   

def main():
   """Main program"""
   for project in projects:

      # Read yaml files
      questionary = Questionary()
      all_questions = []
      Copyrights = []
      Licenses = []
      License_links = []
      Modify_times = []
      for yaml_file in project['yaml_files']:
         print(yaml_file)
         questionary.read_yaml(yaml_file, path=multichoice_path)
         all_questions += questionary.questions
         Copyrights.append(questionary.header['Copyright'])
         Licenses.append(questionary.header['License'])
         License_links.append(questionary.header['License_link'])
         Modify_times.append(questionary.mtime)

      # Shuffle and select questions
      if project['random_seed']:
         random.seed(project['random_seed'])
      else:
         random.seed()
      random.shuffle(all_questions)

      # Write questions
      questionary = Questionary()
      questionary.yaml_path = ''
      questionary.yaml_file = project['yaml_files'][0]
      questionary.filename = project['filename_output']
      questionary.header = {
         'Category': project['yaml_category'],
         'Title': project['yaml_title'],
         'Copyright': Copyrights[0],
         'License': Licenses[0],
         'License_link': License_links[0],
         'Show_max': project['max_questions'],
         }
      questionary.questions = all_questions
      questionary.mtime = max(Modify_times)
      questionary.docx_generate(path=build_path)
      questionary.moodle_generate(moodle_template, path=moodle_path)
      questionary.html_generate(html_template, path=html_path)
      questionary.json_generate(json_template, path=html_path)

      print()


if __name__ == "__main__":
   main()
