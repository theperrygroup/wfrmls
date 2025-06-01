"""Configuration module for WFRMLS Background Agent.

This module provides configuration management for the background agent,
including environment variable loading and validation.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentConfig:
    """Configuration class for WFRMLS Background Agent.
    
    Attributes:
        bearer_token: WFRMLS API bearer token
        sync_interval: Interval between data sync operations (seconds)
        monitor_interval: Interval between monitoring checks (seconds)
        health_check_interval: Interval between health checks (seconds)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Whether to log to file in addition to stdout
        max_retries: Maximum number of retries for failed operations
        batch_size: Number of records to process in each batch
        webhook_url: Optional webhook URL for notifications
        enable_alerts: Whether to enable alert notifications
    """
    
    bearer_token: str
    sync_interval: int = 900  # 15 minutes
    monitor_interval: int = 300  # 5 minutes
    health_check_interval: int = 600  # 10 minutes
    log_level: str = "INFO"
    log_to_file: bool = True
    max_retries: int = 3
    batch_size: int = 200
    webhook_url: Optional[str] = None
    enable_alerts: bool = True

    @classmethod
    def from_environment(cls) -> "AgentConfig":
        """Create configuration from environment variables.
        
        Returns:
            AgentConfig instance loaded from environment variables.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
        bearer_token = os.getenv("WFRMLS_BEARER_TOKEN")
        if not bearer_token:
            raise ValueError(
                "WFRMLS_BEARER_TOKEN environment variable is required"
            )
        
        return cls(
            bearer_token=bearer_token,
            sync_interval=int(os.getenv("WFRMLS_SYNC_INTERVAL", "900")),
            monitor_interval=int(os.getenv("WFRMLS_MONITOR_INTERVAL", "300")),
            health_check_interval=int(os.getenv("WFRMLS_HEALTH_CHECK_INTERVAL", "600")),
            log_level=os.getenv("WFRMLS_LOG_LEVEL", "INFO"),
            log_to_file=os.getenv("WFRMLS_LOG_TO_FILE", "true").lower() == "true",
            max_retries=int(os.getenv("WFRMLS_MAX_RETRIES", "3")),
            batch_size=int(os.getenv("WFRMLS_BATCH_SIZE", "200")),
            webhook_url=os.getenv("WFRMLS_WEBHOOK_URL"),
            enable_alerts=os.getenv("WFRMLS_ENABLE_ALERTS", "true").lower() == "true",
        )

    def validate(self) -> None:
        """Validate configuration values.
        
        Raises:
            ValueError: If configuration values are invalid.
        """
        if self.sync_interval < 60:
            raise ValueError("sync_interval must be at least 60 seconds")
        
        if self.monitor_interval < 30:
            raise ValueError("monitor_interval must be at least 30 seconds")
        
        if self.health_check_interval < 60:
            raise ValueError("health_check_interval must be at least 60 seconds")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            raise ValueError("log_level must be one of DEBUG, INFO, WARNING, ERROR")
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        
        if self.batch_size < 1 or self.batch_size > 1000:
            raise ValueError("batch_size must be between 1 and 1000") 