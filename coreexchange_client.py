"""
Robust exchange client with comprehensive error handling and circuit breakers
"""
import ccxt
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

@dataclass
class MarketData:
    """Structured market data container"""
    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    last: float
    volume_24h: float
    high_24h: float
    low_24h: float
    spread_pct: float

class ExchangeClient:
    """Robust exchange client with circuit breakers and retry logic"""
    
    def __init__(self, exchange_name: str = 'binance', is_paper: bool = True):
        self.exchange_name = exchange_name
        self.is_paper = is_paper
        self.exchange: Optional[ccxt.Exchange] = None
        self.circuit_breaker = CircuitBreaker()
        self.last_successful_call: Optional[datetime] = None
        
    def initialize(self) -> bool:
        """Initialize exchange connection with validation"""
        try:
            logger.info(f"Initializing {self.exchange_name} exchange client")
            
            # Check if exchange is supported
            if self.exchange_name not in ccxt.exchanges:
                logger.error(f"Exchange {self.exchange_name} not supported")
                return False