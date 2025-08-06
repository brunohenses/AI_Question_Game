import json
from pathlib import Path
from datetime import datetime
from config import STATS_FILE
import logging

class StatsManager:
    def __init__(self):
        self.file = Path(STATS_FILE)
        self._load()

    def _load(self):
        if self.file.exists():
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception as e:
                logging.warning(f"Falha ao carregar stats: {e}")
                self.stats = []
        else:
            self.stats = []

    def add_record(self, perguntas_respondidas: int, ajudas_usadas: dict, pontuacao: int):
        record = {
            'timestamp': datetime.now().isoformat(),
            'perguntas_respondidas': perguntas_respondidas,
            'ajudas_usadas': ajudas_usadas,
            'pontuacao': pontuacao
        }
        self.stats.append(record)
        self._save()

    def _save(self):
        try:
            # garante pasta existe
            self.file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            logging.info(f"Stats salvas em {self.file}")
        except Exception as e:
            logging.error(f"Erro ao salvar stats: {e}")

    def get_all(self):
        return self.stats.copy()
