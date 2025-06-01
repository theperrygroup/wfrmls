"""Data processing module for WFRMLS Background Agent.

This module handles the processing and storage of WFRMLS data updates,
including properties, members, offices, and open houses.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from .config import AgentConfig


class DataProcessor:
    """Processes WFRMLS data updates and maintains local data storage.
    
    This class handles the processing of various WFRMLS data types and
    can be extended to integrate with databases, webhooks, or other
    downstream systems.
    """

    def __init__(self, config: AgentConfig) -> None:
        """Initialize the data processor.
        
        Args:
            config: Agent configuration instance.
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

    async def process_properties(self, properties_data: Dict[str, Any]) -> int:
        """Process property data updates.
        
        Args:
            properties_data: Property data from WFRMLS API response.
            
        Returns:
            Number of properties processed.
        """
        properties = properties_data.get("value", [])
        processed_count = 0
        
        for property_data in properties:
            try:
                await self._process_single_property(property_data)
                processed_count += 1
                
                # Add small delay to avoid overwhelming downstream systems
                if processed_count % 10 == 0:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Error processing property {property_data.get('ListingId', 'unknown')}: {e}"
                )
        
        return processed_count

    async def _process_single_property(self, property_data: Dict[str, Any]) -> None:
        """Process a single property record.
        
        Args:
            property_data: Individual property data record.
        """
        listing_id = property_data.get("ListingId")
        if not listing_id:
            self.logger.warning("Property record missing ListingId")
            return
        
        # Example processing - customize based on your needs
        self.logger.debug(f"Processing property {listing_id}")
        
        # You can add custom processing logic here, such as:
        # - Saving to database
        # - Sending to webhook
        # - Validating data
        # - Enriching with additional data
        
        # For demonstration, we'll just log key information
        status = property_data.get("StandardStatus")
        price = property_data.get("ListPrice")
        address = property_data.get("StreetName", "Unknown")
        
        self.logger.info(
            f"Property {listing_id}: {status} - ${price:,} at {address}"
        )

    async def process_members(self, members_data: Dict[str, Any]) -> int:
        """Process member (agent) data updates.
        
        Args:
            members_data: Member data from WFRMLS API response.
            
        Returns:
            Number of members processed.
        """
        members = members_data.get("value", [])
        processed_count = 0
        
        for member_data in members:
            try:
                await self._process_single_member(member_data)
                processed_count += 1
                
                if processed_count % 10 == 0:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Error processing member {member_data.get('MemberKey', 'unknown')}: {e}"
                )
        
        return processed_count

    async def _process_single_member(self, member_data: Dict[str, Any]) -> None:
        """Process a single member record.
        
        Args:
            member_data: Individual member data record.
        """
        member_key = member_data.get("MemberKey")
        if not member_key:
            self.logger.warning("Member record missing MemberKey")
            return
        
        self.logger.debug(f"Processing member {member_key}")
        
        # Example processing
        name = f"{member_data.get('MemberFirstName', '')} {member_data.get('MemberLastName', '')}"
        status = member_data.get("MemberStatus")
        
        self.logger.info(f"Member {member_key}: {name.strip()} - {status}")

    async def process_offices(self, offices_data: Dict[str, Any]) -> int:
        """Process office data updates.
        
        Args:
            offices_data: Office data from WFRMLS API response.
            
        Returns:
            Number of offices processed.
        """
        offices = offices_data.get("value", [])
        processed_count = 0
        
        for office_data in offices:
            try:
                await self._process_single_office(office_data)
                processed_count += 1
                
                if processed_count % 10 == 0:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Error processing office {office_data.get('OfficeKey', 'unknown')}: {e}"
                )
        
        return processed_count

    async def _process_single_office(self, office_data: Dict[str, Any]) -> None:
        """Process a single office record.
        
        Args:
            office_data: Individual office data record.
        """
        office_key = office_data.get("OfficeKey")
        if not office_key:
            self.logger.warning("Office record missing OfficeKey")
            return
        
        self.logger.debug(f"Processing office {office_key}")
        
        # Example processing
        name = office_data.get("OfficeName", "Unknown")
        status = office_data.get("OfficeStatus")
        
        self.logger.info(f"Office {office_key}: {name} - {status}")

    async def process_open_houses(self, open_houses_data: Dict[str, Any]) -> int:
        """Process open house data updates.
        
        Args:
            open_houses_data: Open house data from WFRMLS API response.
            
        Returns:
            Number of open houses processed.
        """
        open_houses = open_houses_data.get("value", [])
        processed_count = 0
        
        for open_house_data in open_houses:
            try:
                await self._process_single_open_house(open_house_data)
                processed_count += 1
                
                if processed_count % 10 == 0:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Error processing open house {open_house_data.get('OpenHouseKey', 'unknown')}: {e}"
                )
        
        return processed_count

    async def _process_single_open_house(self, open_house_data: Dict[str, Any]) -> None:
        """Process a single open house record.
        
        Args:
            open_house_data: Individual open house data record.
        """
        open_house_key = open_house_data.get("OpenHouseKey")
        if not open_house_key:
            self.logger.warning("Open house record missing OpenHouseKey")
            return
        
        self.logger.debug(f"Processing open house {open_house_key}")
        
        # Example processing
        listing_id = open_house_data.get("ListingId")
        start_time = open_house_data.get("OpenHouseStartTime")
        end_time = open_house_data.get("OpenHouseEndTime")
        
        self.logger.info(
            f"Open house {open_house_key}: Listing {listing_id} "
            f"from {start_time} to {end_time}"
        )

    async def process_deletions(self, deletions_data: Dict[str, Any]) -> int:
        """Process deletion records to maintain data integrity.
        
        Args:
            deletions_data: Deletion data from WFRMLS API response.
            
        Returns:
            Number of deletion records processed.
        """
        deletions = deletions_data.get("value", [])
        processed_count = 0
        
        for deletion_data in deletions:
            try:
                await self._process_single_deletion(deletion_data)
                processed_count += 1
                
                if processed_count % 10 == 0:
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                self.logger.error(
                    f"Error processing deletion {deletion_data.get('ResourceRecordKey', 'unknown')}: {e}"
                )
        
        return processed_count

    async def _process_single_deletion(self, deletion_data: Dict[str, Any]) -> None:
        """Process a single deletion record.
        
        Args:
            deletion_data: Individual deletion record.
        """
        resource_key = deletion_data.get("ResourceRecordKey")
        resource_name = deletion_data.get("ResourceName")
        
        if not resource_key or not resource_name:
            self.logger.warning("Deletion record missing key fields")
            return
        
        self.logger.debug(f"Processing deletion {resource_name}:{resource_key}")
        
        # Example processing - you would implement actual deletion logic here
        self.logger.info(f"Deleted {resource_name} record: {resource_key}")

    async def send_webhook_notification(
        self, 
        event_type: str, 
        data: Dict[str, Any]
    ) -> None:
        """Send webhook notification for processed data.
        
        Args:
            event_type: Type of event (property_update, member_update, etc.)
            data: Event data to send.
        """
        if not self.config.webhook_url:
            return
        
        try:
            import aiohttp
            
            payload = {
                "event_type": event_type,
                "timestamp": data.get("timestamp"),
                "data": data
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.webhook_url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        self.logger.info(f"Webhook notification sent for {event_type}")
                    else:
                        self.logger.warning(
                            f"Webhook notification failed with status {response.status}"
                        )
                        
        except Exception as e:
            self.logger.error(f"Error sending webhook notification: {e}")

    def save_to_file(self, data: Dict[str, Any], filename: str) -> None:
        """Save data to a JSON file for debugging or backup purposes.
        
        Args:
            data: Data to save.
            filename: Name of the file to save to.
        """
        try:
            with open(f"/app/logs/{filename}", "w") as f:
                json.dump(data, f, indent=2, default=str)
            self.logger.debug(f"Data saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving data to file {filename}: {e}") 