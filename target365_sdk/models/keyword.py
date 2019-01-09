from .model import Model

class Keyword(Model):

    def _accepted_params(self) -> list:
        return [
            'keywordId',
            'shortNumberId',
            'keywordText',
            'mode',
            'forwardUrl',
            'enabled',
            'created',
            'lastModified',
            'tags',
            'customProperties',
            'ownerAccountId',
        ]
