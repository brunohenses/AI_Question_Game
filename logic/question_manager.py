import json
import random
import logging
from pathlib import Path
from typing import Dict
from config import PERGUNTAS_FILE, CACHE_FILE, STATS_FILE
from logic.api_manager import APIManager

class QuestionManager:
    def __init__(self):
        self.api = APIManager()
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
        loaded = {}
        if Path(CACHE_FILE).exists():
            try:
                loaded = json.load(open(CACHE_FILE, 'r', encoding='utf-8'))
            except Exception:
                logging.warning("Cache JSON vazio ou mal formatado.")
        for nivel in self.cache:
            self.cache[nivel] = loaded.get(nivel, [])

    def _salvar_cache(self):
        try:
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logging.info(f"Cache salvo em {CACHE_FILE}")
        except Exception as e:
            logging.error(f"Erro ao salvar cache: {e}")

    def obter_pergunta(self, nivel: str) -> Dict:
        # 0) Se cache para todos os níveis estiver vazio, tenta gerar batch
        empty = all(len(self.cache[n]) == 0 for n in self.cache)
        logging.info(f"Cache vazio? {empty} — online? {self.api.online}")
        
        if empty and self.api.online:
            logging.info("Tentando gerar o lote de perguntas via API...")
            batch = {}  # garante variável definida
            try:
                batch = self.api.generate_batch_questions()
                logging.info(f"Batch recebido via API: {list(batch.keys())}")
            except Exception as e:
                logging.warning(f"Batch via API falhou: {e}")
            else:
                # Aplica o batch somente se veio algo
                for n in self.cache:
                    self.cache[n] = batch.get(n, [])
                self._salvar_cache()

        # 1) Tenta cache (pop front)
        if self.cache[nivel]:
            pergunta = self.cache[nivel].pop(0)
            self._salvar_cache()
            self.usadas[nivel].append(pergunta)
            logging.info(f"Pergunta '{pergunta['pergunta'][:30]}...' via cache")
            return pergunta

        # 2) Fallback estático
        disponiveis = [q for q in self.perguntas[nivel] if q not in self.usadas[nivel]]
        if disponiveis:
            pergunta = random.choice(disponiveis)
            self.perguntas[nivel].remove(pergunta)
            self.usadas[nivel].append(pergunta)
            logging.info(f"Pergunta '{pergunta['pergunta'][:30]}...' via estática")
            return pergunta

        # Se nada disponível
        raise ValueError(f"Nenhuma pergunta disponível para nível '{nivel}'")
                