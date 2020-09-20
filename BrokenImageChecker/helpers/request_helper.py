import json
import concurrent.futures
from datetime import datetime

import requests

from helpers.user_agent_helpers import RandomUserAgent
from helpers.mongo_helper import crawl_links,broken_img

def get_link_response_code(link_to_check):
    headers = {'User-Agent': RandomUserAgent.get_random()}
    resp = requests.head(link_to_check,headers=headers)
    if resp.status_code == 405:
        resp = requests.get(link_to_check,headers=headers)
    return resp

def update_response(response_data,url,response):
    if(str(response.status_code) != "200"):
        response_data.append({
        "group_id":url["group_id"],
        "link":url["src"],
        "request_date":datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "status":response.status_code,
        "headers":response.headers,
        })

def execute_to_ping(g_id,crawl_urls):
    response_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(get_link_response_code, (url["src"])): url for url in crawl_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                resp = future.result()
            except Exception as exc:
                print('%r generated an exception: %s\n' % (url, exc))
            else:
                update_response(response_data,url,resp)
    if response_data:
        broken_img.insert_many(response_data)
    return response_data