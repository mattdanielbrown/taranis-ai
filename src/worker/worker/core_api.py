import requests
from urllib.parse import quote
from datetime import datetime

from worker.log import logger
from worker.config import Config


class CoreApi:
    def __init__(self):
        self.api_url = Config.TARANIS_NG_CORE_URL
        self.api_key = Config.API_KEY
        self.headers = self.get_headers()
        self.verify = Config.SSL_VERIFICATION


    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}", "Content-type": "application/json"}


    def check_response(self, response, url):
        if response.ok:
            return response.json()
        logger.critical(f"Call to {url} failed {response.status}: {response.text}")
        return None

    def api_put(self, url, json_data=None):
        url = f"{self.api_url}{url}"
        response = requests.put(url=url, headers=self.headers, verify=self.verify, json=json_data)
        return self.check_response(response, url)

    def api_post(self, url, json_data=None):
        url = f"{self.api_url}{url}"
        response = requests.post(url=url, headers=self.headers, verify=self.verify, json=json_data)
        return self.check_response(response, url)

    def api_get(self, url, params=None):
        url = f"{self.api_url}{url}{params}"
        response = requests.get(url=url, headers=self.headers, verify=self.verify)
        return self.check_response(response, url)

    def api_delete(self, url):
        url = f"{self.api_url}{url}"
        response = requests.delete(url=url, headers=self.headers, verify=self.verify)
        return self.check_response(response, url)



    def get_bot_config(self, bot_id: str) -> dict | None:
        try:
            return self.api_get('/api/v1/worker/bots/', bot_id)
        except Exception:
            logger.log_debug_trace("Can't get OSINT Sources")
            return None

    def get_osint_source(self, source_id: str) -> dict | None:
        try:
            return self.api_get(
                '/api/v1/worker/osint-sources/', source_id
            )
        except Exception:
            logger.log_debug_trace("Can't get OSINT Sources")
            return None

    def get_schedule(self) -> dict | None:
        try:
            return self.api_get(url='/api/v1/beat/schedule',)
        except Exception:
            return None

    def get_categories(self, id) -> dict | None:
        try:
            return self.api_get(
                url='/api/v1/bots/word-list-categories/',
                params=id,
            )
        except Exception:
            return None

    def get_news_items_data(self, limit) -> dict | None:
        try:
            return self.api_get('/api/v1/bots/news-item-data', f'?limit={limit}')
        except Exception:
            return None

    def get_news_items_aggregate(self, source_group, limit) -> dict | None:
        try:
            return self.api_get('/api/v1/bots/news-item-aggregates', f'?group={source_group}')
        except Exception:
            logger.log_debug_trace("get_news_items_aggregate failed")
            return None



    def update_schedule(self, schedule):
        try:
            url = f"{self.api_url}/api/v1/beat/schedule"
            response = requests.put(
                url=url,
                json=schedule,
                headers=self.headers,
            )
            return self.check_response(response, url)
        except Exception:
            return None

    def update_news_item_attributes(self, id, attributes):
        try:
            response = requests.put(
                f"{self.api_url}/api/v1/bots/news-item-data/{id}/attributes",
                json=attributes,
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            return None

    def update_news_item_tags(self, id, tags):
        try:
            response = requests.put(
                f"{self.api_url}/api/v1/bots/news-item-data/{id}/tags",
                json=tags,
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            logger.log_debug_trace("update_news_item_tags failed")
            return None

    def delete_word_list_category_entries(self, id, name):
        try:
            response = requests.delete(
                f"{self.api_url}/api/v1/bots/word-list-categories/{id}/entries/{name}",
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            return None

    def update_word_list_category_entries(self, id, name, entries):
        try:
            response = requests.put(
                f"{self.api_url}/api/v1/bots/word-list-categories/{id}/entries/{name}",
                json=entries,
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            return None


    def add_word_list_category(self, id, category):
        try:
            response = requests.put(
                f"{self.api_url}/api/v1/bots/word-list-categories/{id}",
                json=category,
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            return None

    def news_items_grouping(self, data):
        try:
            response = requests.put(
                f"{self.api_url}/api/v1/bots/news-item-aggregates/group",
                json=data,
                headers=self.headers,
            )
            return response.status_code
        except Exception:
            return None

    def add_news_items(self, news_items) -> bool:
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/collectors/news-items", json=news_items, headers=self.headers, verify=self.verify
            )

            return response.ok
        except Exception:
            logger.log_debug_trace("Cannot add Newsitem")
            return False

    def update_osintsource_status(self, osint_source_id, status):
        try:
            response = requests.put(f"{self.api_url}/api/v1/collectors/osint-source/{osint_source_id}", headers=self.headers, verify=self.verify, json={"error": status})
            return response.ok
        except Exception:
            logger.log_debug_trace("Cannot update OSINT Source status")
            return False

    def update_next_run_time(self, name: str, next_run_time: datetime):
        try:
            url = f"{self.api_url}/api/v1/beat/next-run-time"
            response = requests.put(url=url, headers=self.headers, verify=self.verify, json={name: next_run_time.isoformat()})
            return self.check_response(response, url)
        except Exception:
            logger.log_debug_trace("Cannot update schedule entry")
            return False

    def cleanup_token_blacklist(self):
        try:
            url = f"{self.api_url}/api/v1/worker/token-blacklist"
            response = requests.post(url=url, headers=self.headers, verify=self.verify)
            return self.check_response(response, url)
        except Exception:
            logger.log_debug_trace("Cannot cleanup token blacklist")
            return False