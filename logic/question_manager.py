import json
import random
import logging
from pathlib import Path
from typing import List, Dict
from config import PERGUNTAS_FILE, CACHE_FILE, STATS_FILE
from logic.api_manager import ApiManager

class QuestionManager:
    def __init__(self):
        self.api_manager = ApiManager()
        self.perguntas = {"facil": [], "medio": [], "dificil": []}
        self.cache = {"facil": [], "medio": [], "dificil": []}
        self.usadas = {"facil": [], "medio": [], "dificil": []}
        self._carregar_perguntas_estaticas()
        self._carregar_cache()

    def _carregar_perguntas_estaticas(self):
        try:
            with open(PERGUNTAS_FILE, "r", encoding="utf-8") as f:
                self.perguntas = json.load(f)
                logging.info(f"Perguntas estáticas carregadas de {PERGUNTAS_FILE}")
        except Exception as e:
            logging.warning(f"Erro ao carregar perguntas estáticas: {e}")
        
    def _carregar_cache(self):
        if Path(CACHE_FILE).exists():
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                    logging.info(f"Cache carregado de {CACHE_FILE}")
            except Exception as e:
                logging.warning(f"Erro ao carregar cache: {e}")

    def _salvar_cache(self):
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
                logging.info(f"Cache salvo em {CACHE_FILE}")
        except Exception as e:
            logging.error(f"Erro ao salvar cache: {e}")

    def obter_pergunta(self, nivel: str) -> Dict:
        # Retorna uma pergunta do nível especificado. Usa cache, offline ou API. Evita repetição.
        origem = ""
        pergunta = None

        # 1. Tenta pegar do cache
        while self.cache[nivel]:
            candidata = self.cache[nivel].pop(0)
            if candidata not in self.usadas[nivel]:
                pergunta = candidata
                origem = "cache"
                break
        
        if origem == "cache":
            self._salvar_cache()
        
        # 2. Se offline ou falhou API, usa pergunta estática (evitando repetição)
        if not pergunta and (not self.api.online or not pergunta):
            pool = [q for q in self.perguntas[nivel] if q not in self.usadas[nivel]]
            if pool:
                pergunta = random.choice(pool)
                self.perguntas[nivel].remove(pergunta)  # evitar repetição
                origem = "estatica"

        # 3. Tenta gerar pela API e salvar no cache
        if not pergunta and self.api.online:
            try:
                pergunta = self.api.generate_question(nivel)
                self.cache[nivel].append(pergunta)
                self._salvar_cache()
                origem = "api"
            except Exception:
                pool = [q for q in self.perguntas[nivel] if q not in self.usadas[nivel]]
                if pool:
                    pergunta = random.choice(pool)
                    self.perguntas[nivel].remove(pergunta)
                    origem = "fallback"

        if pergunta:
            self.usadas[nivel].append(pergunta)
            logging.info(f"Pergunta retornada do nível '{nivel}' via {origem}.")
            return pergunta
        else:
            raise ValueError(f"Nenhuma pergunta disponível para o nível '{nivel}'")
            