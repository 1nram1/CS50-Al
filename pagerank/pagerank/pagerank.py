import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    keys = corpus.keys()
    result = {}
    num_of_pages = len(corpus)
    probability_equal =  1 / num_of_pages
    if len(corpus[page]) == 0 :
        for web_page in  keys :
            result[web_page] = probability_equal
        return result
    else :
        probability_link = 1 / len(corpus[page])
        for web_page in keys :
            result[web_page] = (1 - damping_factor) * probability_equal
        for link_page in corpus[page]:
            result[link_page] += damping_factor * probability_link
        return result
   

import random

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    result = {}
    i = 0
    page = random.choice(list(corpus.keys()))
    samples.append(page)
    while i < n :
        transition_probability = transition_model(corpus,page,damping_factor)
        pages = list(transition_probability.keys())
        probabilities = list(transition_probability.values())
        page = random.choices(pages, weights=probabilities, k=1)[0]
        samples.append(page)
        i += 1
    for web_page in corpus.keys() :
        result[web_page] = len([target_page for target_page in samples if target_page == web_page]) / n
    return result


    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    threshold = 0.001
    is_converge = False
    keys = corpus.keys()
    N = len(keys)
    for alone_page in keys:
        if not corpus[alone_page] :
            corpus[alone_page] = list(keys)

    for page in keys:
        page_rank[page] = 1 / N
    while not is_converge:
        is_converge = True
        for web_page in keys:
            old_rank = page_rank[web_page]
            probability_i = 0
            for link_page in keys:
                # if link_page == web_page :
                #     continue
                if web_page in corpus[link_page] :
                    probability_i += page_rank[link_page] / len(corpus[link_page]) 
            page_rank[web_page] = (1 - damping_factor) / N + damping_factor  * (probability_i)
            if abs(page_rank[web_page] - old_rank) > threshold:
                is_converge = False
    return page_rank
            
        

    



if __name__ == "__main__":
    main()
