import os
from enum import Enum

from core.handler import Handler
from core.utils import *

class CompletionItem(Handler):
    name = "completion_item_resolve"
    method = "completionItem/resolve"
    cancel_on_change = True
    send_document_uri = False

    def process_request(self, item_key, item) -> dict:
        self.item_key = item_key
        return item

    def process_response(self, response: dict) -> None:
        if response is not None and "documentation" in response:
            response_doc = response["documentation"]
            if type(response_doc) == dict:
                if "value" in response_doc:
                    response_doc = response_doc["value"]
                else:
                    response_doc = ""
            
            self.file_action.completion_item_update(
                self.item_key, 
                response_doc.strip(),
                response["additionalTextEdits"] if "additionalTextEdits" in response else [])
        else:
            eval_in_emacs("acm-doc-hide")
