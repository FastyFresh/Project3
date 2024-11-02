import logging
import psutil
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SystemMonitor:
    def __init__(self):
        self.metrics_history: List[Dict] = []
        self.max_history_size = 1000
        self.alert_thresholds = {
            "cpu_percent": 80.0,      # 80% CPU usage
            "memory_percent": 80.0,    # 80% memory usage
            "disk_percent": 80.0,      # 80% disk usage
            "network_errors": 100,     # Network error count
            "latency_ms": 1000        # 1 second latency
        }
        self.monitoring = False
        self.alert_callbacks = []
        
    async def start_monitoring(self) -> None:
        """Start the monitoring system"""
        try:
            self.monitoring = True
            asyncio.create_task(self._monitor_loop())
            logger.info("System monitoring started")
            
        except Exception as e:
            logger.error(f"Failed to start monitoring: {str(e)}")
            self.monitoring = False
            
    async def stop_monitoring(self) -> None:
        """Stop the monitoring system"""
        self.monitoring = False
        logger.info("System monitoring stopped")
        
    async def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                metrics = self._collect_system_metrics()
                
                # Store metrics
                self.metrics_history.append(metrics)
                if len(self.metrics_history) > self.max_history_size:
                    self.metrics_history.pop(0)
                    
                # Check for alerts
                await self._check_alerts(metrics)
                
                # Wait before next collection
                await asyncio.sleep(60)  # Collect metrics every minute
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(60)
                
    def _collect_system_metrics(self) -> Dict:
        """Collect current system metrics"""
        try:
            metrics = {
                "timestamp": datetime.now(),
                "cpu_percent": psutil.cpu_percent(),
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "percent": psutil.disk_usage('/').percent
                },
                "network": self._get_network_stats(),
                "process": self._get_process_stats()
            }
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
            return {}
            
    def _get_network_stats(self) -> Dict:
        """Collect network statistics"""
        try:
            network_stats = psutil.net_io_counters()
            return {
                "bytes_sent": network_stats.bytes_sent,
                "bytes_recv": network_stats.bytes_recv,
                "packets_sent": network_stats.packets_sent,
                "packets_recv": network_stats.packets_recv,
                "errin": network_stats.errin,
                "errout": network_stats.errout,
                "dropin": network_stats.dropin,
                "dropout": network_stats.dropout
            }
        except Exception as e:
            logger.error(f"Failed to get network stats: {str(e)}")
            return {}
            
    def _get_process_stats(self) -> Dict:
        """Collect process statistics"""
        try:
            process = psutil.Process()
            return {
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "threads": process.num_threads(),
                "fds": process.num_fds() if hasattr(process, 'num_fds') else 0,
                "connections": len(process.connections())
            }
        except Exception as e:
            logger.error(f"Failed to get process stats: {str(e)}")
            return {}
            
    async def _check_alerts(self, metrics: Dict) -> None:
        """Check metrics against alert thresholds"""
        try:
            alerts = []
            
            # CPU usage alert
            if metrics.get("cpu_percent", 0) > self.alert_thresholds["cpu_percent"]:
                alerts.append(f"High CPU usage: {metrics['cpu_percent']}%")
                
            # Memory usage alert
            if metrics.get("memory", {}).get("percent", 0) > self.alert_thresholds["memory_percent"]:
                alerts.append(f"High memory usage: {metrics['memory']['percent']}%")
                
            # Disk usage alert
            if metrics.get("disk", {}).get("percent", 0) > self.alert_thresholds["disk_percent"]:
                alerts.append(f"High disk usage: {metrics['disk']['percent']}%")
                
            # Network error alert
            network = metrics.get("network", {})
            total_errors = network.get("errin", 0) + network.get("errout", 0)
            if total_errors > self.alert_thresholds["network_errors"]:
                alerts.append(f"High network errors: {total_errors}")
                
            # Trigger alerts
            if alerts:
                await self._trigger_alerts(alerts)
                
        except Exception as e:
            logger.error(f"Failed to check alerts: {str(e)}")
            
    async def _trigger_alerts(self, alerts: List[str]) -> None:
        """Trigger alert callbacks"""
        try:
            for alert in alerts:
                logger.warning(f"System Alert: {alert}")
                for callback in self.alert_callbacks:
                    try:
                        await callback(alert)
                    except Exception as e:
                        logger.error(f"Alert callback failed: {str(e)}")
                        
        except Exception as e:
            logger.error(f"Failed to trigger alerts: {str(e)}")
            
    def add_alert_callback(self, callback) -> None:
        """Add a new alert callback"""
        self.alert_callbacks.append(callback)
        
    def remove_alert_callback(self, callback) -> None:
        """Remove an alert callback"""
        if callback in self.alert_callbacks:
            self.alert_callbacks.remove(callback)
            
    def get_current_metrics(self) -> Dict:
        """Get the most recent metrics"""
        return self.metrics_history[-1] if self.metrics_history else {}
        
    def get_metrics_history(self, 
                          minutes: Optional[int] = None) -> List[Dict]:
        """Get historical metrics, optionally filtered by time"""
        if not minutes:
            return self.metrics_history
            
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return [
            m for m in self.metrics_history 
            if m.get("timestamp", datetime.now()) >= cutoff
        ]
        
    def set_alert_threshold(self, metric: str, value: float) -> None:
        """Update an alert threshold"""
        if metric in self.alert_thresholds:
            self.alert_thresholds[metric] = value