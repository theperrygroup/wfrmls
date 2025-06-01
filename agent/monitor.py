"""Monitoring module for WFRMLS Background Agent.

This module provides monitoring capabilities including alerts,
health checks, and system status monitoring.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError

from .config import AgentConfig


class DataMonitor:
    """Monitors WFRMLS data and system health.

    This class provides monitoring functionality for:
    - API connectivity and response times
    - Data quality and validation
    - Alert generation and notification
    - System performance metrics
    """

    def __init__(self, client: WFRMLSClient, config: AgentConfig) -> None:
        """Initialize the data monitor.

        Args:
            client: WFRMLS client instance.
            config: Agent configuration instance.
        """
        self.client = client
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.alert_history: List[Dict[str, Any]] = []
        self.last_health_check = datetime.utcnow()
        self.performance_metrics: Dict[str, Any] = {
            "api_response_times": [],
            "error_count": 0,
            "success_count": 0,
            "last_sync_duration": 0,
        }

    async def check_alerts(self) -> None:
        """Check for various alert conditions and send notifications."""
        try:
            await self._check_api_health()
            await self._check_data_quality()
            await self._check_error_rates()
            await self._check_response_times()

        except Exception as e:
            self.logger.error(f"Error in alert checking: {e}")

    async def _check_api_health(self) -> None:
        """Check API connectivity and health."""
        try:
            start_time = datetime.utcnow()

            # Test API with a simple request
            response = self.client.property.get_properties(top=1)

            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds()

            # Record performance metrics
            self.performance_metrics["api_response_times"].append(response_time)
            self.performance_metrics["success_count"] += 1

            # Keep only last 100 response times
            if len(self.performance_metrics["api_response_times"]) > 100:
                self.performance_metrics["api_response_times"] = (
                    self.performance_metrics["api_response_times"][-100:]
                )

            # Alert if response time is too slow
            if response_time > 30:  # 30 seconds threshold
                await self._create_alert(
                    "slow_api_response",
                    f"API response time: {response_time:.2f}s exceeds 30s threshold",
                    severity="warning",
                )

            self.last_health_check = datetime.utcnow()
            self.logger.debug(f"API health check passed in {response_time:.2f}s")

        except WFRMLSError as e:
            self.performance_metrics["error_count"] += 1
            await self._create_alert(
                "api_error", f"API health check failed: {e}", severity="error"
            )

    async def _check_data_quality(self) -> None:
        """Check data quality and consistency."""
        try:
            # Get recent properties to check data quality
            recent_time = datetime.utcnow() - timedelta(hours=1)
            filter_query = f"ModificationTimestamp gt {recent_time.isoformat()}Z"

            properties = self.client.property.get_properties(
                filter_query=filter_query, top=50
            )

            property_list = properties.get("value", [])

            # Check for data quality issues
            missing_required_fields = 0
            invalid_prices = 0

            for prop in property_list:
                # Check for required fields
                if not prop.get("ListingId") or not prop.get("StandardStatus"):
                    missing_required_fields += 1

                # Check for invalid prices
                price = prop.get("ListPrice")
                if price is not None and (price < 0 or price > 50000000):
                    invalid_prices += 1

            # Alert on data quality issues
            if missing_required_fields > 0:
                await self._create_alert(
                    "data_quality",
                    f"{missing_required_fields} properties missing required fields",
                    severity="warning",
                )

            if invalid_prices > 0:
                await self._create_alert(
                    "data_quality",
                    f"{invalid_prices} properties with invalid prices",
                    severity="warning",
                )

            self.logger.debug(
                f"Data quality check completed for {len(property_list)} properties"
            )

        except Exception as e:
            self.logger.error(f"Error in data quality check: {e}")

    async def _check_error_rates(self) -> None:
        """Check error rates and alert if too high."""
        total_requests = (
            self.performance_metrics["success_count"]
            + self.performance_metrics["error_count"]
        )

        if total_requests > 0:
            error_rate = self.performance_metrics["error_count"] / total_requests

            # Alert if error rate exceeds 10%
            if error_rate > 0.1:
                await self._create_alert(
                    "high_error_rate",
                    f"Error rate: {error_rate:.1%} exceeds 10% threshold",
                    severity="error",
                )

    async def _check_response_times(self) -> None:
        """Check API response times and alert if degraded."""
        response_times = self.performance_metrics["api_response_times"]

        if len(response_times) >= 10:
            avg_response_time = sum(response_times[-10:]) / 10

            # Alert if average response time exceeds 15 seconds
            if avg_response_time > 15:
                await self._create_alert(
                    "slow_performance",
                    f"Average API response time: {avg_response_time:.2f}s exceeds 15s threshold",
                    severity="warning",
                )

    async def _create_alert(
        self, alert_type: str, message: str, severity: str = "info"
    ) -> None:
        """Create and process an alert.

        Args:
            alert_type: Type/category of the alert.
            message: Alert message.
            severity: Alert severity (info, warning, error, critical).
        """
        if not self.config.enable_alerts:
            return

        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": severity,
            "agent_id": "wfrmls-agent",
        }

        # Add to alert history
        self.alert_history.append(alert)

        # Keep only last 1000 alerts
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]

        # Log the alert
        log_level = {
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }.get(severity, logging.INFO)

        self.logger.log(log_level, f"ALERT [{alert_type}]: {message}")

        # Send webhook notification if configured
        if self.config.webhook_url:
            await self._send_alert_webhook(alert)

    async def _send_alert_webhook(self, alert: Dict[str, Any]) -> None:
        """Send alert via webhook.

        Args:
            alert: Alert data to send.
        """
        try:
            # Import aiohttp only when needed to avoid dependency issues
            import aiohttp

            payload = {"event_type": "alert", "alert": alert}

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 200:
                        self.logger.debug(
                            "Alert webhook notification sent successfully"
                        )
                    else:
                        self.logger.warning(
                            f"Alert webhook failed with status {response.status}"
                        )

        except ImportError:
            self.logger.warning("aiohttp not available for webhook notifications")
        except Exception as e:
            self.logger.error(f"Error sending alert webhook: {e}")

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and metrics.

        Returns:
            Dictionary containing system status information.
        """
        total_requests = (
            self.performance_metrics["success_count"]
            + self.performance_metrics["error_count"]
        )

        error_rate = 0.0
        if total_requests > 0:
            error_rate = self.performance_metrics["error_count"] / total_requests

        avg_response_time = 0.0
        response_times = self.performance_metrics["api_response_times"]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)

        return {
            "last_health_check": self.last_health_check.isoformat(),
            "total_requests": total_requests,
            "success_count": self.performance_metrics["success_count"],
            "error_count": self.performance_metrics["error_count"],
            "error_rate": error_rate,
            "average_response_time": avg_response_time,
            "recent_alerts": len(
                [
                    alert
                    for alert in self.alert_history
                    if datetime.fromisoformat(alert["timestamp"])
                    > datetime.utcnow() - timedelta(hours=24)
                ]
            ),
            "status": (
                "healthy" if error_rate < 0.1 and avg_response_time < 15 else "degraded"
            ),
        }

    def get_recent_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get alerts from the specified time period.

        Args:
            hours: Number of hours to look back for alerts.

        Returns:
            List of recent alerts.
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)

        return [
            alert
            for alert in self.alert_history
            if datetime.fromisoformat(alert["timestamp"]) > cutoff_time
        ]

    def reset_metrics(self) -> None:
        """Reset performance metrics and alert history."""
        self.performance_metrics = {
            "api_response_times": [],
            "error_count": 0,
            "success_count": 0,
            "last_sync_duration": 0,
        }
        self.alert_history = []
        self.logger.info("Performance metrics and alert history reset")
