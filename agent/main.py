"""WFRMLS Background Agent Main Module.

This module provides the main entry point for the WFRMLS background agent
that continuously monitors and processes real estate data.
"""

import asyncio
import logging
import os
import signal
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from wfrmls import WFRMLSClient
from wfrmls.exceptions import WFRMLSError

from .config import AgentConfig
from .data_processor import DataProcessor
from .monitor import DataMonitor
from .scheduler import TaskScheduler


class WFRMLSAgent:
    """Background agent for WFRMLS data processing and monitoring.
    
    This agent runs continuously and performs the following tasks:
    - Monitors for new property listings
    - Processes data updates every 15 minutes
    - Handles error recovery and retry logic
    - Provides health check endpoints
    - Logs all activities for monitoring
    """

    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        """Initialize the WFRMLS background agent.
        
        Args:
            config: Agent configuration. If None, loads from environment.
        """
        self.config = config or AgentConfig.from_environment()
        self.client = WFRMLSClient(bearer_token=self.config.bearer_token)
        self.data_processor = DataProcessor(self.config)
        self.monitor = DataMonitor(self.client, self.config)
        self.scheduler = TaskScheduler(self.config)
        self.running = False
        self.logger = self._setup_logging()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration.
        
        Returns:
            Configured logger instance.
        """
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('/app/logs/agent.log', mode='a')
            ] if self.config.log_to_file else [logging.StreamHandler(sys.stdout)]
        )
        return logging.getLogger(__name__)

    def _signal_handler(self, signum: int, frame: Any) -> None:
        """Handle shutdown signals gracefully.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False

    async def start(self) -> None:
        """Start the background agent.
        
        This method runs the main event loop and coordinates all background tasks.
        """
        self.logger.info("Starting WFRMLS Background Agent...")
        self.running = True
        
        try:
            # Verify API connection
            await self._health_check()
            
            # Start background tasks
            tasks = [
                asyncio.create_task(self._data_sync_loop()),
                asyncio.create_task(self._monitoring_loop()),
                asyncio.create_task(self._scheduled_tasks_loop()),
                asyncio.create_task(self._health_check_loop())
            ]
            
            self.logger.info("All background tasks started successfully")
            
            # Wait for all tasks to complete or for shutdown signal
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            self.logger.error(f"Fatal error in agent: {e}")
            raise
        finally:
            self.logger.info("WFRMLS Background Agent stopped")

    async def _health_check(self) -> bool:
        """Perform health check by testing API connectivity.
        
        Returns:
            True if health check passes, False otherwise.
            
        Raises:
            WFRMLSError: If API connection fails.
        """
        try:
            # Test API connection with a simple request
            properties = self.client.property.get_properties(top=1)
            self.logger.info("Health check passed - API connection successful")
            return True
        except WFRMLSError as e:
            self.logger.error(f"Health check failed - API connection error: {e}")
            raise

    async def _data_sync_loop(self) -> None:
        """Main data synchronization loop.
        
        Runs every 15 minutes to sync incremental updates from WFRMLS API.
        """
        self.logger.info("Starting data sync loop...")
        
        while self.running:
            try:
                start_time = time.time()
                
                # Get incremental updates from the last 15 minutes
                cutoff_time = datetime.utcnow() - timedelta(minutes=15)
                
                # Sync properties
                await self._sync_properties(cutoff_time)
                
                # Sync members
                await self._sync_members(cutoff_time)
                
                # Sync offices
                await self._sync_offices(cutoff_time)
                
                # Sync open houses
                await self._sync_open_houses(cutoff_time)
                
                # Process deletions
                await self._process_deletions()
                
                sync_duration = time.time() - start_time
                self.logger.info(f"Data sync completed in {sync_duration:.2f} seconds")
                
                # Wait for next sync cycle
                await asyncio.sleep(self.config.sync_interval)
                
            except Exception as e:
                self.logger.error(f"Error in data sync loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    async def _sync_properties(self, cutoff_time: datetime) -> None:
        """Sync property updates.
        
        Args:
            cutoff_time: Only sync properties modified after this time.
        """
        try:
            filter_query = f"ModificationTimestamp gt {cutoff_time.isoformat()}Z"
            properties = self.client.property.get_properties(
                filter_query=filter_query,
                top=200
            )
            
            processed_count = await self.data_processor.process_properties(properties)
            self.logger.info(f"Processed {processed_count} property updates")
            
        except Exception as e:
            self.logger.error(f"Error syncing properties: {e}")

    async def _sync_members(self, cutoff_time: datetime) -> None:
        """Sync member updates.
        
        Args:
            cutoff_time: Only sync members modified after this time.
        """
        try:
            filter_query = f"ModificationTimestamp gt {cutoff_time.isoformat()}Z"
            members = self.client.member.get_members(
                filter_query=filter_query,
                top=200
            )
            
            processed_count = await self.data_processor.process_members(members)
            self.logger.info(f"Processed {processed_count} member updates")
            
        except Exception as e:
            self.logger.error(f"Error syncing members: {e}")

    async def _sync_offices(self, cutoff_time: datetime) -> None:
        """Sync office updates.
        
        Args:
            cutoff_time: Only sync offices modified after this time.
        """
        try:
            filter_query = f"ModificationTimestamp gt {cutoff_time.isoformat()}Z"
            offices = self.client.office.get_offices(
                filter_query=filter_query,
                top=200
            )
            
            processed_count = await self.data_processor.process_offices(offices)
            self.logger.info(f"Processed {processed_count} office updates")
            
        except Exception as e:
            self.logger.error(f"Error syncing offices: {e}")

    async def _sync_open_houses(self, cutoff_time: datetime) -> None:
        """Sync open house updates.
        
        Args:
            cutoff_time: Only sync open houses modified after this time.
        """
        try:
            filter_query = f"ModificationTimestamp gt {cutoff_time.isoformat()}Z"
            open_houses = self.client.openhouse.get_open_houses(
                filter_query=filter_query,
                top=200
            )
            
            processed_count = await self.data_processor.process_open_houses(open_houses)
            self.logger.info(f"Processed {processed_count} open house updates")
            
        except Exception as e:
            self.logger.error(f"Error syncing open houses: {e}")

    async def _process_deletions(self) -> None:
        """Process deleted records to maintain data integrity."""
        try:
            # Get deleted records from the last sync period
            deleted_records = self.client.deleted.get_deleted(
                top=200
            )
            
            processed_count = await self.data_processor.process_deletions(deleted_records)
            self.logger.info(f"Processed {processed_count} deletion records")
            
        except Exception as e:
            self.logger.error(f"Error processing deletions: {e}")

    async def _monitoring_loop(self) -> None:
        """Background monitoring loop for alerts and notifications."""
        self.logger.info("Starting monitoring loop...")
        
        while self.running:
            try:
                await self.monitor.check_alerts()
                await asyncio.sleep(self.config.monitor_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(60)

    async def _scheduled_tasks_loop(self) -> None:
        """Background loop for scheduled tasks."""
        self.logger.info("Starting scheduled tasks loop...")
        
        while self.running:
            try:
                await self.scheduler.run_pending_tasks()
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in scheduled tasks loop: {e}")
                await asyncio.sleep(60)

    async def _health_check_loop(self) -> None:
        """Background loop for periodic health checks."""
        while self.running:
            try:
                await self._health_check()
                await asyncio.sleep(self.config.health_check_interval)
                
            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
                await asyncio.sleep(60)

    def stop(self) -> None:
        """Stop the background agent gracefully."""
        self.logger.info("Stopping WFRMLS Background Agent...")
        self.running = False


async def main() -> None:
    """Main entry point for the WFRMLS background agent."""
    try:
        # Create and start the agent
        agent = WFRMLSAgent()
        await agent.start()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("/app/logs", exist_ok=True)
    
    # Run the agent
    asyncio.run(main()) 