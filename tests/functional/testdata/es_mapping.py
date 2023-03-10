es_settings = {
  "refresh_interval": "1s",
  "analysis": {
    "filter": {
      "english_stop": {
        "type":       "stop",
        "stopwords":  "_english_"
      },
      "english_stemmer": {
        "type": "stemmer",
        "language": "english"
      },
      "english_possessive_stemmer": {
        "type": "stemmer",
        "language": "possessive_english"
      },
      "russian_stop": {
        "type":       "stop",
        "stopwords":  "_russian_"
      },
      "russian_stemmer": {
        "type": "stemmer",
        "language": "russian"
      }
    },
    "analyzer": {
      "ru_en": {
        "tokenizer": "standard",
        "filter": [
          "lowercase",
          "english_stop",
          "english_stemmer",
          "english_possessive_stemmer",
          "russian_stop",
          "russian_stemmer"
        ]
      }
    }
  }
}

es_movies_index = {
  "settings": es_settings,
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "imdb_rating": {
        "type": "float"
      },
      "genre": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "title": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "creation_date": {
        "type": "date"
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "director": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "writers_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "writers": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
}

es_persons_index = {
  "settings": es_settings,
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "name": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "role": {
        "type": "keyword"
      },
      "film_ids": {
        "type": "keyword"
      }
    }
  }
}

es_genres_index = {
  "settings": es_settings,
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "name": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      }
    }
  }
}
