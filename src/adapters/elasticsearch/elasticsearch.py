from elasticsearch import Elasticsearch


class ElasticsearchAdapter:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
    ):
        self._es = Elasticsearch(
            hosts=f'https://{host}:{port}',
            basic_auth=(user, password),
            verify_certs=False,
        )

    @property
    def es(self):
        return self._es

    def add_document(self, index: str, id: str, document: dict):
        """Добавить документ в индекс"""
        return self.es.index(index=index, id=id, document=document)

    def upsert_document(self, index: str, id: str, document: dict, document_for_update: dict):
        """Добавить или обновить документ в индексе"""
        script = {'source': self._generate_script(document_for_update), 'params': {**document_for_update}}

        return self.es.update(index=index, id=id, body={'script': script, 'upsert': document})

    @staticmethod
    def _generate_script(dictionary):
        script_parts = []
        for key, value in dictionary.items():
            part = f'ctx._source.{key} = params.{key};'
            script_parts.append(part)

        script = ' '.join(script_parts)
        return script

    def delete_document(self, index: str, id: str):
        """Удалить документ по ID"""
        return self.es.delete(index=index, id=id)
