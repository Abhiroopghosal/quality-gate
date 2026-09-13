#validation contexts : dataset, history, evidence(whole data itself), metrics 

#using dataclass for storing

from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True) 
class ValidationContext : 
    dataset : Any | None = None
    evidence : Any | None = None  #might be like some sort of schema description in a dict
    metrics : Any | None = None
    history : Any | None = None
    