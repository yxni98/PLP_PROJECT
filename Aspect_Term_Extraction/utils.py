# -*- coding: utf-8 -*-
"""utils.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1twAipRAJ2p8WgSi2YZw4K8Rv88NPtMHk
"""

from base import BaseEmbedder
from sentence_transformer import SentenceTransformerBackend


def select_backend(embedding_model) -> BaseEmbedder:
    """
    根据语言或特定的句子转换器模型选择嵌入模型。

    返回值:
        一个Sentence Transformer模型
    """
    # keybert language backend
    if isinstance(embedding_model, BaseEmbedder):
        return embedding_model



    # Sentence Transformer 嵌入
    if "sentence_transformers" in str(type(embedding_model)):
        return SentenceTransformerBackend(embedding_model)

    # 基于字符串创建句子转换器模型
    if isinstance(embedding_model, str):
        return SentenceTransformerBackend(embedding_model)

    return SentenceTransformerBackend("paraphrase-multilingual-MiniLM-L12-v2")