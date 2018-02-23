from abc import ABC
import json
from bfex.components.key_generation.key_generator import *


class KeyGenerationApproach(ABC):
    
    def __init__(self, approach_id, description):
        self.approach_id = approach_id
        self.description = description
        
    def generate_keywords(self,scrapp):
        pass

    def get_id(self):
        pass