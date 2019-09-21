import time

import requests

from tlbx.logging_utils import dbg


def poll_call(
    func, result_param, result_value, sleep_time, max_iter, *_args, **_kwargs
):
    i = 0
    while True:
        result = func(*_args, **_kwargs)
        if result[result_param] == result_value:
            return result
        i += 1
        assert i < max_iter, (
            "Exhausted poll_call, no result in %d tries. Last result: %s"
            % (max_iter, result)
        )
        dbg(
            "Polling %s, iteration %d/%d, %s=%s"
            % (func.__name__, i, max_iter, result_param, result[result_param])
        )
        if sleep_time:
            time.sleep(sleep_time)


def paged_call(func, size_param, offset_param, page_size, *_args, **_kwargs):
    offset = 0
    results = []

    while True:
        _kwargs.update({size_param: page_size, offset_param: offset})
        result = func(*_args, **_kwargs)
        results.extend(result)
        result_len = len(result)
        offset += result_len
        if result_len < page_size:
            break

    print("Got %d results" % offset)
    return results


def paged_get(url, size_param, offset_param, page_size, *_args, **_kwargs):
    offset = 0
    results = []

    while True:
        _kwargs["params"] = _kwargs.get("params", {})
        _kwargs["params"].update({size_param: page_size, offset_param: offset})
        resp = requests.get(url, *_args, **_kwargs)
        resp.raise_for_status()
        result = resp.json()
        results.extend(result)
        result_len = len(result)
        offset += result_len
        if result_len < page_size:
            break

    print("Got %d results" % offset)
    return results
