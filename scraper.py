import requests
import concurrent.futures


def get_html(url):
    try:
        return requests.get(url).content.decode("utf-8")
    except Exception as e:
        # print("GET ERROR " + url)
        # print(e)
        pass


def write(filepath, content):
    try:
        if content is not None:
            with open(filepath, "w") as w:
                w.writelines(content)
            w.close()
    except Exception as e:
        # print("WRITE ERROR " + filepath)
        # print(e)
        pass


def single_scrape(filepath, url, parse_func=None):
    try:
        html = get_html(url)
        if len(html) > 0:
            if parse_func is not None:
                content = parse_func(html)
            else:
                content = html
            write(filepath, content)
    except Exception as e:
        # print("SCRAPE ERROR " + url)
        # print(e)
        pass


def multi_scrape(filepath_url_dict, parse_func=None):
    total = len(filepath_url_dict)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        filepaths = filepath_url_dict.keys()
        future_to_url = {executor.submit(
            get_html, filepath_url_dict[fp]): fp for fp in filepaths}
        count = 0
        for future in concurrent.futures.as_completed(future_to_url):
            filepath = future_to_url[future]
            url = filepath_url_dict[filepath]
            try:
                data = future.result()
            except Exception as e:
                print('%r generated an exception: %s' % (url, e))
            else:
                # print('%r page is %d bytes' % (url, len(data)))
                html = data
                if html is not None and len(html) > 0:
                    if parse_func is not None:
                        content = parse_func(html)
                    else:
                        content = html
                    write(filepath, content)

                count += 1
                print("  %d/%d" % (count, total), end="\r", flush=True)
    print("")
