# -*- coding: utf-8 -*-
"""Multi-Channel Inventory Ghost Stock Deconfliction for GenPark Agentic Commerce."""
import json
from typing import Dict, Any

class MultiChannelInventoryGhostStockDeconflictionEngine:
    @staticmethod
    def deconflict_shared_inventory_pool(physical_on_hand_stock: int, channel_order_velocities: Dict[str, float], sync_latency_minutes: int = 5) -> Dict[str, Any]:
        total_velocity = sum(channel_order_velocities.values())
        safety_buffer = max(5, int((total_velocity / 60.0) * sync_latency_minutes * 2.0))
        distributable = max(0, physical_on_hand_stock - safety_buffer)
        allocations = {}
        for ch, vel in channel_order_velocities.items():
            ratio = vel / max(0.1, total_velocity)
            allocations[ch] = int(distributable * ratio)
        return {"physical_stock": physical_on_hand_stock, "safety_buffer_withheld": safety_buffer, "channel_allocations": allocations, "oversell_risk": "PROTECTED" if physical_on_hand_stock > safety_buffer else "HIGH_DANGER"}

    @staticmethod
    def trigger_oversell_emergency_circuit_breaker(sku: str, available_unallocated_units: int) -> Dict[str, Any]:
        is_circuit_tripped = available_unallocated_units <= 0
        return {"sku": sku, "circuit_tripped": is_circuit_tripped, "action": "ZERO_OUT_ALL_CHANNELS" if is_circuit_tripped else "NORMAL_ROUTING"}
