"""Task scheduler module for WFRMLS Background Agent.

This module provides task scheduling functionality for periodic
operations and maintenance tasks.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

from .config import AgentConfig


class ScheduledTask:
    """Represents a scheduled task.

    Attributes:
        name: Task name
        func: Function to execute
        interval: Execution interval in seconds
        last_run: Timestamp of last execution
        next_run: Timestamp of next scheduled execution
        enabled: Whether the task is enabled
    """

    def __init__(
        self, name: str, func: Callable[[], Any], interval: int, enabled: bool = True
    ) -> None:
        """Initialize a scheduled task.

        Args:
            name: Task name
            func: Function to execute
            interval: Execution interval in seconds
            enabled: Whether the task is enabled
        """
        self.name = name
        self.func = func
        self.interval = interval
        self.enabled = enabled
        self.last_run: Optional[datetime] = None
        self.next_run = datetime.utcnow() + timedelta(seconds=interval)
        self.execution_count = 0
        self.error_count = 0

    def is_due(self) -> bool:
        """Check if the task is due for execution.

        Returns:
            True if the task should be executed now.
        """
        return self.enabled and datetime.utcnow() >= self.next_run

    def mark_executed(self) -> None:
        """Mark the task as executed and schedule next run."""
        self.last_run = datetime.utcnow()
        self.next_run = self.last_run + timedelta(seconds=self.interval)
        self.execution_count += 1

    def mark_error(self) -> None:
        """Mark that the task encountered an error."""
        self.error_count += 1

    def get_status(self) -> Dict[str, Any]:
        """Get task status information.

        Returns:
            Dictionary containing task status.
        """
        return {
            "name": self.name,
            "enabled": self.enabled,
            "interval": self.interval,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat(),
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "is_due": self.is_due(),
        }


class TaskScheduler:
    """Manages and executes scheduled tasks.

    This class provides a simple task scheduling system for periodic
    operations like cleanup, maintenance, and reporting.
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the task scheduler.

        Args:
            config: Agent configuration instance.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.tasks: List[ScheduledTask] = []
        self._setup_default_tasks()

    def _setup_default_tasks(self) -> None:
        """Setup default scheduled tasks."""
        # Cleanup old logs every 24 hours
        self.add_task(
            "cleanup_logs", self._cleanup_old_logs, interval=86400  # 24 hours
        )

        # Generate daily report
        self.add_task(
            "daily_report", self._generate_daily_report, interval=86400  # 24 hours
        )

        # Cleanup metrics every 6 hours
        self.add_task(
            "cleanup_metrics", self._cleanup_old_metrics, interval=21600  # 6 hours
        )

    def add_task(
        self, name: str, func: Callable[[], Any], interval: int, enabled: bool = True
    ) -> None:
        """Add a new scheduled task.

        Args:
            name: Task name
            func: Function to execute
            interval: Execution interval in seconds
            enabled: Whether the task is enabled
        """
        task = ScheduledTask(name, func, interval, enabled)
        self.tasks.append(task)
        self.logger.info(f"Added scheduled task: {name} (interval: {interval}s)")

    def remove_task(self, name: str) -> bool:
        """Remove a scheduled task by name.

        Args:
            name: Name of the task to remove

        Returns:
            True if task was found and removed, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.name == name:
                del self.tasks[i]
                self.logger.info(f"Removed scheduled task: {name}")
                return True
        return False

    def enable_task(self, name: str) -> bool:
        """Enable a task by name.

        Args:
            name: Name of the task to enable

        Returns:
            True if task was found and enabled, False otherwise
        """
        for task in self.tasks:
            if task.name == name:
                task.enabled = True
                self.logger.info(f"Enabled task: {name}")
                return True
        return False

    def disable_task(self, name: str) -> bool:
        """Disable a task by name.

        Args:
            name: Name of the task to disable

        Returns:
            True if task was found and disabled, False otherwise
        """
        for task in self.tasks:
            if task.name == name:
                task.enabled = False
                self.logger.info(f"Disabled task: {name}")
                return True
        return False

    async def run_pending_tasks(self) -> None:
        """Run all pending scheduled tasks."""
        for task in self.tasks:
            if task.is_due():
                await self._execute_task(task)

    async def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a single task.

        Args:
            task: Task to execute
        """
        try:
            self.logger.debug(f"Executing scheduled task: {task.name}")

            if asyncio.iscoroutinefunction(task.func):
                await task.func()
            else:
                task.func()

            task.mark_executed()
            self.logger.info(f"Scheduled task completed: {task.name}")

        except Exception as e:
            task.mark_error()
            self.logger.error(f"Error executing scheduled task {task.name}: {e}")

    async def _cleanup_old_logs(self) -> None:
        """Clean up old log files."""
        import glob
        import os

        try:
            log_dir = "/app/logs"
            if not os.path.exists(log_dir):
                return

            # Remove log files older than 7 days
            cutoff_time = datetime.utcnow() - timedelta(days=7)
            removed_count = 0

            for log_file in glob.glob(os.path.join(log_dir, "*.log*")):
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                    if file_time < cutoff_time:
                        os.remove(log_file)
                        removed_count += 1
                except Exception as e:
                    self.logger.warning(f"Error removing log file {log_file}: {e}")

            if removed_count > 0:
                self.logger.info(f"Cleaned up {removed_count} old log files")

        except Exception as e:
            self.logger.error(f"Error in log cleanup: {e}")

    async def _generate_daily_report(self) -> None:
        """Generate a daily activity report."""
        try:
            report_time = datetime.utcnow()

            # This is a placeholder for a daily report
            # You can customize this to generate actual reports
            report = {
                "timestamp": report_time.isoformat(),
                "type": "daily_report",
                "agent_uptime": "24h",  # Placeholder
                "tasks_executed": sum(task.execution_count for task in self.tasks),
                "total_errors": sum(task.error_count for task in self.tasks),
                "status": "operational",
            }

            # Save report to file
            import json

            report_filename = f"daily_report_{report_time.strftime('%Y%m%d')}.json"

            try:
                with open(f"/app/logs/{report_filename}", "w") as f:
                    json.dump(report, f, indent=2)
                self.logger.info(f"Daily report generated: {report_filename}")
            except Exception as e:
                self.logger.error(f"Error saving daily report: {e}")

        except Exception as e:
            self.logger.error(f"Error generating daily report: {e}")

    async def _cleanup_old_metrics(self) -> None:
        """Clean up old metric files and data."""
        try:
            # This is a placeholder for metrics cleanup
            # You can customize this based on your metrics storage
            self.logger.debug("Cleaning up old metrics data")

            # Example: Remove metric files older than 30 days
            import glob
            import os

            metrics_dir = "/app/logs"
            if not os.path.exists(metrics_dir):
                return

            cutoff_time = datetime.utcnow() - timedelta(days=30)
            removed_count = 0

            for metrics_file in glob.glob(
                os.path.join(metrics_dir, "*_metrics_*.json")
            ):
                try:
                    file_time = datetime.fromtimestamp(os.path.getmtime(metrics_file))
                    if file_time < cutoff_time:
                        os.remove(metrics_file)
                        removed_count += 1
                except Exception as e:
                    self.logger.warning(
                        f"Error removing metrics file {metrics_file}: {e}"
                    )

            if removed_count > 0:
                self.logger.info(f"Cleaned up {removed_count} old metrics files")

        except Exception as e:
            self.logger.error(f"Error in metrics cleanup: {e}")

    def get_task_status(self) -> List[Dict[str, Any]]:
        """Get status of all scheduled tasks.

        Returns:
            List of task status dictionaries.
        """
        return [task.get_status() for task in self.tasks]

    def get_task_by_name(self, name: str) -> Optional[ScheduledTask]:
        """Get a task by name.

        Args:
            name: Name of the task to find

        Returns:
            ScheduledTask if found, None otherwise
        """
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    async def run_task_now(self, name: str) -> bool:
        """Execute a specific task immediately.

        Args:
            name: Name of the task to run

        Returns:
            True if task was found and executed, False otherwise
        """
        task = self.get_task_by_name(name)
        if task:
            await self._execute_task(task)
            return True
        return False
