import logging
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RiskCalculator:
    def __init__(self):
        self.max_drawdown_percent = 20  # 20% max drawdown
        self.position_size_percent = 2   # 2% per position
        self.max_correlation = 0.7       # Maximum allowed correlation
        self.min_sharpe = 1.5           # Minimum Sharpe ratio
        
    def calculate_position_size(self, 
                              account_value: float,
                              risk_per_trade: float,
                              stop_loss_percent: float) -> float:
        """Calculate appropriate position size based on risk parameters"""
        try:
            # Calculate maximum loss allowed for the trade
            max_loss = account_value * (risk_per_trade / 100)
            
            # Calculate position size that risks max_loss at stop_loss_percent
            position_size = max_loss / (stop_loss_percent / 100)
            
            # Ensure position size doesn't exceed account position size limit
            max_position = account_value * (self.position_size_percent / 100)
            position_size = min(position_size, max_position)
            
            return position_size
            
        except Exception as e:
            logger.error(f"Failed to calculate position size: {str(e)}")
            return 0.0
            
    def calculate_drawdown(self, 
                         equity_curve: List[float]) -> Dict[str, float]:
        """Calculate maximum drawdown and current drawdown"""
        try:
            equity_array = np.array(equity_curve)
            peak = np.maximum.accumulate(equity_array)
            drawdown = (peak - equity_array) / peak * 100
            
            max_drawdown = np.max(drawdown)
            current_drawdown = drawdown[-1]
            
            return {
                "max_drawdown": max_drawdown,
                "current_drawdown": current_drawdown
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate drawdown: {str(e)}")
            return {"max_drawdown": 0.0, "current_drawdown": 0.0}
    
    def calculate_sharpe_ratio(self,
                             returns: List[float],
                             risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio of returns"""
        try:
            returns_array = np.array(returns)
            excess_returns = returns_array - (risk_free_rate / 252)  # Daily risk-free rate
            
            if len(excess_returns) < 2:
                return 0.0
                
            sharpe = np.sqrt(252) * (np.mean(excess_returns) / np.std(excess_returns))
            return sharpe
            
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {str(e)}")
            return 0.0
            
    def calculate_var(self,
                     returns: List[float],
                     confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk at specified confidence level"""
        try:
            returns_array = np.array(returns)
            var = np.percentile(returns_array, (1 - confidence_level) * 100)
            return abs(var)
            
        except Exception as e:
            logger.error(f"Failed to calculate VaR: {str(e)}")
            return 0.0
            
    def calculate_correlation(self,
                            returns_a: List[float],
                            returns_b: List[float]) -> float:
        """Calculate correlation between two return series"""
        try:
            if len(returns_a) != len(returns_b):
                logger.warning("Return series have different lengths")
                return 0.0
                
            correlation = np.corrcoef(returns_a, returns_b)[0, 1]
            return correlation
            
        except Exception as e:
            logger.error(f"Failed to calculate correlation: {str(e)}")
            return 0.0
    
    def get_risk_metrics(self,
                        positions: List[Dict],
                        returns: List[float],
                        equity_curve: List[float]) -> Dict:
        """Get comprehensive risk metrics"""
        try:
            metrics = {
                "drawdown": self.calculate_drawdown(equity_curve),
                "sharpe": self.calculate_sharpe_ratio(returns),
                "var_95": self.calculate_var(returns),
                "position_count": len(positions),
                "timestamp": datetime.now()
            }
            
            # Calculate position correlations if multiple positions
            if len(positions) > 1:
                correlations = []
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        correlation = self.calculate_correlation(
                            positions[i].get("returns", []),
                            positions[j].get("returns", [])
                        )
                        correlations.append(correlation)
                metrics["max_correlation"] = max(correlations) if correlations else 0.0
                
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get risk metrics: {str(e)}")
            return {}