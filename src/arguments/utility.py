from termcolor import colored
import requests
from rich.console import Console
import sys as sys

from .error import SearchError
from .save import SaveSearchResults
from .markdown import MarkdownRenderer

console = Console()


class Utility():
    def __init__(self):
        # the parent url
        self.search_content_url = "https://api.stackexchange.com/"

    def __get_search_url(self, question, tags):
        return f"{self.search_content_url}/2.2/search/advanced?order=desc&sort=relevance&tagged={tags}&title={question}&site=stackoverflow"

    def make_request(self, que, tag: str):
        """
        This function uses the requests library to make the rest api call to the stackexchange server.

        :param que: The user questions that servers as a question in the api.
        :type que: String
        :param tag: The tags that user wants for searching the relevant answers. For e.g. TypeError might be for multiple languages so is tag is used as "Python" then the api will return answers based on the tags and question.
        :type tag: String
        :return: Json response from the api call.
        :rtype: Json format data
        """
        print("\U0001F50E Searching for the answer")
        try:
            resp = requests.get(self.__get_search_url(que, tag))
        except:
            SearchError("\U0001F613 Search Failed", "\U0001F4BB Try connecting to the internet")
            sys.exit()
        return resp.json()

    def get_que(self, json_data):
        que_id = []
        for data in json_data['items']:
            if data["is_answered"]:
                que_id.append(data["question_id"])
        return que_id

    def get_ans(self, questions_list):
        ans = []
        for questions in range(1):
            try:
                resp = requests.get(
                    f"{self.search_content_url}/2.2/questions/{questions_list[questions]}/answers?order=desc&sort=votes&site=stackoverflow&filter=!--1nZwsgqvRX"
                )
            except:
                SearchError("\U0001F613 Search Failed", "\U0001F4BB Try connecting to the internet")
                sys.exit()
            json_ans_data = resp.json()

            for data in json_ans_data["items"]:
                output_content = [
                    colored(
                        "--------------------------------------------------------",
                        'red'), data["body_markdown"],
                    f"\U0001F517 Link to the answer:{data['link']}"
                ]

                for output_index, output_text in enumerate(output_content):
                    """
                    Loop through the output_text and print the element
                    if it the last one, the text[0] is printed
                    along with text[-1]

                    if text is markdown , render the markdown
                    """
                    if output_index == len(output_content) - 1:
                        console.print(output_text)

                        console.print(output_content[0])
                        break

                    if output_index == len(output_content) - 2:
                        renderer = MarkdownRenderer(output_text)

                        continue

                    console.print(output_text)
            ans.append(json_ans_data["items"])
        return ans