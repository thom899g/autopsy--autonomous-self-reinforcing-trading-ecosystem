"""
Configuration module for the Autonomous Trading Ecosystem
Centralizes all configurable parameters with type validation
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os
from enum import Enum

class TradingMode(Enum):
    PAPER = "paper"
    LIVE = "live"
    BACKTEST = "backtest"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class TradingConfig:
    """Central configuration for trading parameters"""
    
    # Exchange settings
    exchange_name: str = "binance"
    trading_mode: TradingMode = TradingMode.PAPER
    risk_level: RiskLevel = RiskLevel.MEDIUM
    
    # Trading parameters
    max_position_size_usd: float = 1000.0
    max_open_positions: int = 3
    stop_loss_pct: float = 2.0
    take_profit_pct: float = 5.0
    
    # Risk management
    daily_loss_limit_pct: float = 5.0
    max_drawdown_pct: float = 15.0
    volatility_threshold: float = 0.02
    
    # Strategy parameters
    strategy_weights: Dict[str, float] = field(default_factory=lambda: {
        "momentum": 0.4,
        "mean_reversion": 0.3,
        "volatility": 0.3
    })
    
    # Technical indicators
    moving_average_periods: List[int] = field(default_factory=lambda: [20, 50, 200])
    rsi_period: int = 14
    rsi_oversold: float = 30.0
    rsi_overbought: float = 70.0
    
    # Execution settings
    slippage_tolerance_pct: float = 0.1
    order_timeout_seconds: int = 30
    
    # Monitoring
    health_check_interval_seconds: int = 60
    performance_report_interval_hours: int = 1
    
    @classmethod
    def from_env(cls) -> 'TradingConfig':
        """Create config from environment variables"""
        config = cls()
        
        # Override from environment if present
        if mode := os.getenv('TRADING_MODE'):
            config.trading_mode = TradingMode(mode.lower())
        
        if risk := os.getenv('RISK_LEVEL'):
            config.risk_level = RiskLevel(risk.lower())
            
        return config