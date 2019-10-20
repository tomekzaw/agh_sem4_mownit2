from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys
import math
import time
import json
import nltk
import numpy
import string
import pickle
import pandas
import operator
import collections
import scipy.sparse
import urllib.parse
import sklearn.preprocessing
import sklearn.decomposition
import matplotlib.pyplot as plt

downloads = {
    'stopwords': 'corpora/stopwords.zip',
    'punkt': 'tokenizers/punkt',
}
for key, value in downloads.items():
    try:
        nltk.data.find(value)
    except LookupError:
        nltk.download(name)

class Termifier:
    def __init__(self):
        self.translate_table = str.maketrans('', '', string.punctuation)
        self.stemmer = nltk.stem.PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words('english')

    def termify(self, content):
        return [
            self.stemmer.stem(token)
            for token in nltk.word_tokenize(content.translate(self.translate_table))
            if len(token) >= 3 and token.isalnum() and token not in self.stopwords
        ]

class Source(object):
    def id(self):
        return self.__class__.__name__

class SimpleEnglishWikipedia(Source):
    def documents(self):
        with open('sources/{}.txt'.format(self.id()), 'r', encoding='utf-8') as f:
            for article in f.read().split('\n\n'):
                name, content = article.split('\n', 1)
                url = 'https://simple.wikipedia.org/wiki/' + name.replace(' ', '_')
                yield (name, url, content)

class Search:
    def __init__(self, source=SimpleEnglishWikipedia(), svd_k=None, termifier=Termifier()):
        self.source = source
        self.svd_k = svd_k
        self.termifier = termifier

        try:
            self.documents, self.terms = self.load_documents_and_terms()
        except FileNotFoundError:
            self.documents, self.terms = self.generate_documents_and_terms()

        try:
            self.matrix = self.load_tfidf()
        except FileNotFoundError:
            self.matrix = self.generate_tfidf()

        if self.svd_k is not None:
            try:
                self.svd_matrix, self.svd_components = self.load_svd()
            except FileNotFoundError:
                self.svd_matrix, self.svd_components = self.generate_svd()

    def mkdir(self, path):  
        if not os.path.exists(path):
            os.mkdir(path)

    def load_documents_and_terms(self):
        with open('cache/{}/documents.pickle'.format(self.source.id()), 'rb') as handle:
            documents = pickle.load(handle)
        with open('cache/{}/terms.pickle'.format(self.source.id()), 'rb') as handle:
            terms = pickle.load(handle)
        return documents, terms

    def save_documents_and_terms(self, documents, terms):
        self.mkdir('cache')
        self.mkdir('cache/{}'.format(self.source.id()))
        with open('cache/{}/documents.pickle'.format(self.source.id()), 'wb') as handle:
            pickle.dump(documents, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('cache/{}/terms.pickle'.format(self.source.id()), 'wb') as handle:
            pickle.dump(terms, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def generate_documents_and_terms(self):
        documents = dict(enumerate(self.source.documents())) # todo: don't cache content

        terms = set()
        for name, _, content in documents.values():
            terms |= set(self.termifier.termify(name + ' ' + content))
        terms = {v: k for k, v in enumerate(list(terms))}

        self.save_documents_and_terms(documents, terms)
        return documents, terms

    def load_tfidf(self):
        return scipy.sparse.load_npz('cache/{}/matrix.npz'.format(self.source.id()))

    def save_tfidf(self, matrix):
        scipy.sparse.save_npz('cache/{}/matrix.npz'.format(self.source.id()), matrix)

    def generate_tfidf(self):
        documents, terms = self.documents, self.terms

        # Preparing term-by-document term-frequency matrix
        matrix = scipy.sparse.lil_matrix((len(terms), len(documents)))
        for document_id, (name, url, content) in documents.items():
            for term_id, tf in collections.Counter(
                [terms[term] for term in self.termifier.termify(name + ' ' + content)]
            ).items():
                matrix[term_id, document_id] = tf
        
        # Calculating inverse document frequency
        occurrences = scipy.sparse.linalg.norm(matrix, ord=0, axis=1)
        idf = numpy.log(float(len(documents)) * numpy.reciprocal(occurrences, dtype=numpy.float64))

        # Multiplying by inverse document frequency
        matrix = matrix.T.multiply(idf).T

        # Normalization of document vectors
        matrix = sklearn.preprocessing.normalize(matrix, axis=0, norm='l2', copy=False)

        # Verifying documents vector norm
        for document_id in range(min(len(documents), 100)):
            assert(abs((matrix[:,document_id].T * matrix[:,document_id])[0,0] - 1.0) < 1e-9)

        # Converting to CSC sparse matrix
        matrix = scipy.sparse.csc_matrix(matrix)

        self.save_tfidf(matrix)
        return matrix

    def load_svd(self):
        svd_matrix = numpy.load('cache/{}/svd_{}/matrix.npy'.format(self.source.id(), self.svd_k))
        svd_components = numpy.load('cache/{}/svd_{}/components.npy'.format(self.source.id(), self.svd_k))
        return svd_matrix, svd_components

    def save_svd(self, svd_matrix, svd_components):
        numpy.save('cache/{}/svd_{}/matrix.npy'.format(self.source.id(), self.svd_k), svd_matrix)
        numpy.save('cache/{}/svd_{}/components.npy'.format(self.source.id(), self.svd_k), svd_components)

    def generate_svd(self):
        matrix = self.matrix
        self.mkdir('cache/{}/svd_{}'.format(self.source.id(), self.svd_k))

        svd = sklearn.decomposition.TruncatedSVD(n_components=self.svd_k).fit(matrix.T)
        svd_matrix = svd.transform(matrix.T)
        svd_components = svd.components_

        self.save_svd(svd_matrix, svd_components)
        return svd_matrix, svd_components

    def search(self, query):
        time_start = time.time()

        q = scipy.sparse.lil_matrix((len(self.terms), 1))
        term_ids = list(set([self.terms[term] for term in set(self.termifier.termify(query)) if term in self.terms]))
        if len(term_ids) == 0:
            return {'error': 'no_query'}
        q[term_ids,0] = 1.0 / math.sqrt(len(term_ids))

        if self.svd_k is not None:
            svd_q = self.svd_components.dot(q.todense())
            svd_c = self.svd_matrix.dot(svd_q)
            correlations = {document_id: svd_c[document_id,0] for document_id in range(len(self.documents))}
            results_count = int((svd_c > max(svd_c) / 10).sum())
        else:
            correlations = {document_id: correlation for (_, document_id), correlation in numpy.abs(q.T.dot(self.matrix)).todok().items()}
            results_count = len(correlations)

        all_results = sorted(correlations.items(), key=operator.itemgetter(1), reverse=True)
        N = 10

        plt.figure(figsize=(4,3))
        plt.plot(list(map(operator.itemgetter(1), all_results[:N*10])), 'o', markersize=1, color='#4285F4')
        plt.xticks(fontname='Arial')
        plt.yticks(fontname='Arial')
        plt.tight_layout()
        plt.savefig('correlations.png', dpi=300)

        results = []
        for i, (document_id, correlation) in enumerate(all_results[:N]):
            name, url, content = self.documents[int(document_id)]
            results.append({
                'name': name,
                'url': url,
                'content': content,
                'correlation': correlation,
            })

        time_end = time.time()
        return {
            'results': results,
            'results_count': results_count,
            'search_time': time_end - time_start
        }

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        request_uri = parsed_url.path
        request_params = urllib.parse.parse_qs(parsed_url.query)

        for uri, file_name, mime_type in [
            ('/aghoogle.css', 'assets/aghoogle.css', 'text/css'),
            ('/aghoogle.js', 'assets/aghoogle.js', 'text/javascript'),
            ('/favicon.ico', 'assets/favicon.ico', 'image/x-icon'),
            ('/correlations.png', 'correlations.png', 'image/png'),
        ]:
            if request_uri == uri:
                with open(file_name, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-Type', mime_type + '; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f.read())
                    return

        if request_uri == '/':
            with open('assets/' + ('search' if 'q' in request_params else 'welcome') + '.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read())
                return
                
        if request_uri == '/search':
            if 'q' in request_params:      
                query = request_params['q'][0]
                data = self.server.search.search(query)         
            else:
                data = {'error': 'no_query'}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        self.send_error(404)

class Aghoogle():
    def __init__(self, server_address, search):
        self.httpd = HTTPServer(server_address, HTTPRequestHandler)
        self.httpd.search = search
        print('Serving HTTP on {} port {} ...'.format(*server_address))

    def run(self):
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    Aghoogle(
        server_address=('127.0.0.1', 80),
        search=Search(
            source=SimpleEnglishWikipedia(),
            svd_k=1000
        )
    ).run()
