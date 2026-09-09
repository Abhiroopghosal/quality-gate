#validation contexts : dataset, history, evidence(whole data itself), metrics 

#using dataclass for storing

from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True) 
class ValidationContext : 
    dataset : Any | None = None
    evidence : Any | None = None
    metrics : Any | None = None
    history : Any | None = None
    