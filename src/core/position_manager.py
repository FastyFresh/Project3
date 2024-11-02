import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class Position:
    def __init__(self, 
                 symbol: str, 
                 size: float, 
                 entry_price: float, 
                 direction: str,
                 stop_loss: Optional[float] = None,
                 take_profit: Optional[float] = None):
        self.symbol = symbol
        self.size = size
        self.entry_price = entry_price
        self.direction = direction  # "long" or "short"
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_time = datetime.now()
        self.pnl = 0.0
        self.status = "open"

    def update(self, current_price: float) -> None:
        """Update position P&L based on current price"""
        multiplier = 1 if self.direction == "long" else -1
        self.pnl = (current_price - self.entry_price) * self.size * multiplier

class PositionManager:
    def __init__(self):
        self.positions: Dict[str, Position] = {}
        self.max_positions = 10
        self.total_exposure = 0.0
        self.max_exposure = 100000.0  # $100k max exposure
    
    async def open_position(self, 
                          symbol: str, 
                          size: float, 
                          entry_price: float,
                          direction: str,
                          stop_loss: Optional[float] = None,
                          take_profit: Optional[float] = None) -> bool:
        """Open a new position if within limits"""
        try:
            # Check position limits
            if len(self.positions) >= self.max_positions:
                logger.warning("Maximum number of positions reached")
                return False
            
            # Check exposure limits
            new_exposure = size * entry_price
            if self.total_exposure + new_exposure > self.max_exposure:
                logger.warning("Maximum exposure limit would be exceeded")
                return False
            
            # Create and store new position
            position = Position(symbol, size, entry_price, direction, stop_loss, take_profit)
            self.positions[symbol] = position
            self.total_exposure += new_exposure
            
            logger.info(f"Opened {direction} position in {symbol}: {size} @ {entry_price}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open position: {str(e)}")
            return False
    
    async def close_position(self, symbol: str, exit_price: float) -> bool:
        """Close an existing position"""
        try:
            if symbol not in self.positions:
                logger.warning(f"No position found for {symbol}")
                return False
            
            position = self.positions[symbol]
            position.update(exit_price)
            
            # Update exposure
            self.total_exposure -= position.size * position.entry_price
            
            # Archive position
            position.status = "closed"
            del self.positions[symbol]
            
            logger.info(f"Closed position in {symbol} @ {exit_price}, PnL: {position.pnl}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to close position: {str(e)}")
            return False
    
    async def update_positions(self, prices: Dict[str, float]) -> None:
        """Update all positions with current market prices"""
        for symbol, position in self.positions.items():
            if symbol in prices:
                position.update(prices[symbol])
                
                # Check stop loss and take profit
                if position.stop_loss and position.direction == "long" and prices[symbol] <= position.stop_loss:
                    await self.close_position(symbol, prices[symbol])
                elif position.stop_loss and position.direction == "short" and prices[symbol] >= position.stop_loss:
                    await self.close_position(symbol, prices[symbol])
                elif position.take_profit and position.direction == "long" and prices[symbol] >= position.take_profit:
                    await self.close_position(symbol, prices[symbol])
                elif position.take_profit and position.direction == "short" and prices[symbol] <= position.take_profit:
                    await self.close_position(symbol, prices[symbol])
    
    def get_positions(self) -> List[Dict]:
        """Get all current positions"""
        return [
            {
                "symbol": p.symbol,
                "size": p.size,
                "entry_price": p.entry_price,
                "direction": p.direction,
                "pnl": p.pnl,
                "entry_time": p.entry_time,
                "stop_loss": p.stop_loss,
                "take_profit": p.take_profit
            }
            for p in self.positions.values()
        ]
    
    def get_exposure(self) -> float:
        """Get current total exposure"""
        return self.total_exposure
    
    def get_position_count(self) -> int:
        """Get number of open positions"""
        return len(self.positions)