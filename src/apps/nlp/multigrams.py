from django.db.models import Q
from dateutil.rrule import rrule, MONTHLY

from apps.nlp.stopwords import EXTRA_STOPWORDS
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.corpus import stopwords as nltk_stopwords
from collections import Counter
from string import punctuation
import re


def date_filter(start_date, end_date):
    return Q(speech__date__gte=start_date, speech__date__lte=end_date)


def months(queryset):
    start_date = queryset.first().date
    end_date = queryset.last().date
    return rrule(MONTHLY, dtstart=start_date, until=end_date)


def clear_speech(text):
    text = re.sub(r'\([^)]*\)', '', text)
    text = re.sub(r'[OA] SRA?[\w\s.]+-', '', text)
    text = re.sub(r'PRONUNCIAMENTO[\sA-Z]+\s', '', text)
#     text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s[\.\"]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[Vv]\.[Ee][Xx][Aa]\.', 'v.exa', text)
    text = re.sub(r'[Aa][Rr][Tt]\.', 'art', text)
    text = re.sub(r'[Ss][Rr][Ss]?\.', 'sr', text)
    text = re.sub(r'[Ss][Rr][Aa][Ss]?\.', 'sr', text)
    text = re.sub(r'\d', '', text)
    return text.strip()


def get_tokens(speech):
    """
    Função que retorna tokens de discursos removendo as "stopwords".
    Argumentos:
        speeches: Recebe uma lista de discursos.
        stopwords: Recebe uma lista de palavras a serem retiradas dos textos.
    Retorna:
        Uma lista palavras do discurso que não estão nas "stopwords".
    """
    special_stopwords = ['são', 'nossa']
    stopwords = (nltk_stopwords.words('portuguese') + list(punctuation) +
                 EXTRA_STOPWORDS)
    stopwords = [word for word in stopwords if word not in special_stopwords]
    tokens = []
    text = clear_speech(speech)
    tokens += [i for i in word_tokenize(
        text.lower(), language='portuguese') if i not in stopwords]

    return tokens


def ngrams_by_limit(tokens, n, limit=0):
    """
    Função que retorna uma lista de ngrams de acordo com os argumento passados.
    Argumentos:
        tokens: Recebe uma lista de tokens já processados pelo
                nltk.word_tokenize.
        n: Recebe o número de palavras que deseja dividir o ngram.
        limit: Recebe o limite mínimo de ocorrência.
    Retorna:
        Uma lista de ngrams com ocorrência maior que "limite" e com "n"
        palavras.
    """
    ngrams_count = Counter(ngrams(tokens, n)).most_common()
    result = [x for x in ngrams_count if x[1] >= limit]
    return result


def clean_tokens(tokens, fivegrams=[], quadgrams=[], trigrams=[], bigrams=[],
                 extra_stopwords=None):
    """
    Função que retorna uma lista de tokens filtradas pelos argumentos passados.
    Argumentos:
        tokens: Recebe uma lista de tokens já processados pelo
                nltk.word_tokenize.
        fivegrams: Recebe uma lista de fivegrams.
        quadgrams: Recebe uma lista de quadgrams.
        trigrams: Recebe uma lista de trigramas.
        bigrams: Recebe uma lista de bigramas.
        extra_stopwords: Recebe uma lista de stopwords.
    Retorna:
        Uma lista de tokens removendo os n-gramas e stopwords passados nos
        argumentos.
    """
    if fivegrams:
        pos_fivegram = []
        for i in range(len(tokens) - 4):
            for word1, word2, word3, word4, word5 in fivegrams:
                if (tokens[i] == word1 and tokens[i + 1] == word2 and
                   tokens[i + 2] == word3 and tokens[i + 3] == word4 and
                   tokens[i + 4] == word5):
                    pos_fivegram.append(i)

        for pos in reversed(pos_fivegram):
            del tokens[pos:pos + 5]

    if quadgrams:
        pos_quadgram = []
        for i in range(len(tokens) - 3):
            for word1, word2, word3, word4 in quadgrams:
                if (tokens[i] == word1 and tokens[i + 1] == word2 and
                   tokens[i + 2] == word3 and tokens[i + 3] == word4):
                    pos_quadgram.append(i)

        for pos in reversed(pos_quadgram):
            del tokens[pos:pos + 4]

    if trigrams:
        pos_trigram = []
        for i in range(len(tokens) - 2):
            for word1, word2, word3 in trigrams:
                if (tokens[i] == word1 and tokens[i + 1] == word2 and
                   tokens[i + 2] == word3):
                    pos_trigram.append(i)

        for pos in reversed(pos_trigram):
            del tokens[pos:pos + 3]

    if bigrams:
        pos_bigram = []
        for i in range(len(tokens) - 1):
            for word1, word2 in bigrams:
                if tokens[i] == word1 and tokens[i + 1] == word2:
                    pos_bigram.append(i)

        for pos in reversed(pos_bigram):
            del tokens[pos:pos + 2]

    if extra_stopwords:
        new_tokens = [token for token in tokens if token not in extra_stopwords]
    else:
        new_tokens = tokens

    return new_tokens
