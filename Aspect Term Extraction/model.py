# -*- coding: utf-8 -*-
"""Untitled15.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dzj2p9J0gmLOKhb0E_gw_bFlcUu5dU7v
"""

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
from tqdm import tqdm
from typing import List, Union, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# KeyBERT
from keybert._mmr import mmr
from keybert.backend._utils import select_backend


class KeyBERT:
    """
     首先，首先从文档中创建候选关键字或关键短语列表。（暂定CountVectorizer，后补TFIDF） 
     接下来，我们将文档以及候选关键字/关键短语都转换为数字数据。 
     最后，我们使用余弦相似度来找到与文档最相似的单词/短语。

    """

    def __init__(self, model="all-MiniLM-L6-v2"):

        self.model = select_backend(model)

    def extract_keywords(
        self,
        docs: Union[str, List[str]],
        candidates: List[str] = None,
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: Union[str, List[str]] = "english",
        top_n: int = 5,
        min_df: int = 1,
        use_mmr: bool = False,
        diversity: float = 0.5,
        nr_candidates: int = 20,
        vectorizer: CountVectorizer = None,
        seed_keywords: List[str] = None,
    ) -> Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]:

        if isinstance(docs, str):
            keywords = self._extract_keywords_single_doc(
                doc=docs,
                candidates=candidates,
                keyphrase_ngram_range=keyphrase_ngram_range,
                stop_words=stop_words,
                top_n=top_n,
                use_mmr=use_mmr,
                diversity=diversity,
                nr_candidates=nr_candidates,
                vectorizer=vectorizer,
                seed_keywords=seed_keywords,
            )

            return keywords

        elif isinstance(docs, list):
            warnings.warn(
                "单个文档进行测试会快捷很多 "
            )
            return self._extract_keywords_multiple_docs(
                docs, keyphrase_ngram_range, stop_words, top_n, min_df, vectorizer
            )

    def _extract_keywords_single_doc(
        self,
        doc: str,
        candidates: List[str] = None,
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: Union[str, List[str]] = "english",
        top_n: int = 5,
        use_maxsum: bool = False,
        use_mmr: bool = False,
        diversity: float = 0.5,
        nr_candidates: int = 20,
        vectorizer: CountVectorizer = None,
        seed_keywords: List[str] = None,
    ) -> List[Tuple[str, float]]:
        """
        以单个文件进行关键字的提取

        返回值:
            相似度最高的N个关键词
        """
        try:
            # 提取关键词建立后备词表
            if candidates is None:
                if vectorizer:
                    count = vectorizer.fit([doc])
                else:
                    count = CountVectorizer(
                        ngram_range=keyphrase_ngram_range, stop_words=stop_words
                    ).fit([doc])
                candidates = count.get_feature_names()

            # 嵌入sentence-transformers模型
            doc_embedding = self.model.embed([doc])
            candidate_embeddings = self.model.embed(candidates)

            if seed_keywords is not None:
                seed_embeddings = self.model.embed([" ".join(seed_keywords)])
                doc_embedding = np.average(
                    [doc_embedding, seed_embeddings], axis=0, weights=[3, 1]
                )

            # 相似度比较以及关键词提取
            if use_mmr:
                keywords = mmr(
                    doc_embedding, candidate_embeddings, candidates, top_n, diversity
                )

            else:
                distances = cosine_similarity(doc_embedding, candidate_embeddings)
                keywords = [
                    (candidates[index], round(float(distances[0][index]), 4))
                    for index in distances.argsort()[0][-top_n:]
                ][::-1]

            return keywords
        except ValueError:
            return []

    def _extract_keywords_multiple_docs(
        self,
        docs: List[str],
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: str = "english",
        top_n: int = 5,
        min_df: int = 1,
        vectorizer: CountVectorizer = None,
    ) -> List[List[Tuple[str, float]]]:
        """
        多文件提取关键词测试

        """
        # 关键词提取
        if vectorizer:
            count = vectorizer.fit(docs)
        else:
            count = CountVectorizer(
                ngram_range=keyphrase_ngram_range, stop_words=stop_words, min_df=min_df
            ).fit(docs)
        words = count.get_feature_names()
        df = count.transform(docs)

        # Extract embeddings
        doc_embeddings = self.model.embed(docs)
        word_embeddings = self.model.embed(words)

        # Extract keywords
        keywords = []
        for index, doc in tqdm(enumerate(docs)):
            doc_words = [words[i] for i in df[index].nonzero()[1]]

            if doc_words:
                doc_word_embeddings = np.array(
                    [word_embeddings[i] for i in df[index].nonzero()[1]]
                )
                distances = cosine_similarity(
                    [doc_embeddings[index]], doc_word_embeddings
                )[0]
                doc_keywords = [
                    (doc_words[i], round(float(distances[i]), 4))
                    for i in distances.argsort()[-top_n:]
                ]
                keywords.append(doc_keywords)
            else:
                keywords.append(["None Found"])

        return keywords