"""
Paradox Integration Layer
Bridges the paradox conservation engine with the existing system
"""

import asyncio
from typing import Optional, Dict, Any
from paradox_conservation_engine import paradox_conservation_engine_init, conserve_paradox, ParadoxState
from pi_density_operators import create_paradox_conservation_pipeline

class ParadoxIntegrationLayer:
    """Integrates paradox conservation with system operations"""
    
    def __init__(self):
        self.engine_initialized = False
        self.conservation_pipeline = None
        self.current_paradox_state = None
        self.crash_count = 0
        self.max_crash_recovery_attempts = 3
    
    async def initialize_engine(self) -> bool:
        """Initialize the paradox conservation engine"""
        try:
            # Initialize core engine
            init_result = paradox_conservation_engine_init()
            
            if init_result["initialized"]:
                self.engine_initialized = True
                
                # Create conservation pipeline
                self.conservation_pipeline = create_paradox_conservation_pipeline()
                
                # Set initial state
                self.current_paradox_state = ParadoxState(
                    contradiction_density=init_result["pi_density"],
                    boundary_coherence=init_result["boundary_coherence"],
                    conservation_factor=init_result["conservation_factor"],
                    temporal_phase=init_result["temporal_phase"]
                )
                
                print("Paradox Conservation Engine initialized successfully")
                return True
            
        except Exception as e:
            print(f"Engine initialization failed: {e}")
            self.crash_count += 1
            return False
    
    async def handle_contradiction(self, contradiction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming contradictions using paradox conservation"""
        if not self.engine_initialized:
            await self.initialize_engine()
        
        try:
            # Extract contradiction metrics
            contradiction_strength = contradiction_data.get('strength', 0.5)
            temporal_instability = contradiction_data.get('temporal_instability', 0.0)
            logical_tension = contradiction_data.get('logical_tension', 0.0)
            
            # Update paradox state with new contradiction
            new_density = (self.current_paradox_state.contradiction_density + 
                         contradiction_strength) / 2
            
            new_state = ParadoxState(
                contradiction_density=new_density,
                boundary_coherence=self.current_paradox_state.boundary_coherence,
                conservation_factor=self.current_paradox_state.conservation_factor,
                temporal_phase=self.current_paradox_state.temporal_phase + temporal_instability
            )
            
            # Conserve the paradox
            conserved_state = conserve_paradox(new_state)
            self.current_paradox_state = conserved_state
            
            # Run pipeline for advanced metrics
            pipeline_result = self.conservation_pipeline(
                initial_density=conserved_state.contradiction_density,
                iterations=10
            )
            
            return {
                'handled': True,
                'pi_density': conserved_state.contradiction_density,
                'boundary_coherence': conserved_state.boundary_coherence,
                'conservation_factor': conserved_state.conservation_factor,
                'pipeline_metrics': pipeline_result,
                'crash_recovered': False
            }
            
        except Exception as e:
            print(f"Contradiction handling failed: {e}")
            return await self.recover_from_crash(contradiction_data)
    
    async def recover_from_crash(self, contradiction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recovery mechanism for paradox conservation failures"""
        self.crash_count += 1
        
        if self.crash_count > self.max_crash_recovery_attempts:
            # Fallback to simple conservation
            return {
                'handled': False,
                'fallback_used': True,
                'pi_density': 0.5,  # Neutral density
                'boundary_coherence': 0.8,
                'conservation_factor': 0.9,
                'recovery_attempt': self.crash_count
            }
        
        # Try to reinitialize and retry
        print(f"Attempting recovery #{self.crash_count}")
        await asyncio.sleep(0.1)  # Brief pause
        
        # Reinitialize engine
        self.engine_initialized = False
        if await self.initialize_engine():
            # Retry with original data
            return await self.handle_contradiction(contradiction_data)
        else:
            return await self.recover_from_crash(contradiction_data)
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health metrics"""
        return {
            'engine_initialized': self.engine_initialized,
            'crash_count': self.crash_count,
            'current_pi_density': getattr(self.current_paradox_state, 'contradiction_density', None),
            'boundary_coherence': getattr(self.current_paradox_state, 'boundary_coherence', None),
            'conservation_factor': getattr(self.current_paradox_state, 'conservation_factor', None)
        }

# Global instance
paradox_integrator = ParadoxIntegrationLayer()

async def integrate_paradox_conservation(contradiction_event: Dict[str, Any]) -> Dict[str, Any]:
    """Main integration function for external calls"""
    return await paradox_integrator.handle_contradiction(contradiction_event)

def get_paradox_system_health() -> Dict[str, Any]:
    """Get current paradox system health"""
    return paradox_integrator.get_system_health()

# Example usage
if __name__ == "__main__":
    async def test_integration():
        # Test contradiction event
        test_event = {
            'strength': 0.7,
            'temporal_instability': 0.2,
            'logical_tension': 0.3,
            'source': 'llm_life_support_crash'
        }
        
        result = await integrate_paradox_conservation(test_event)
        print("Paradox Integration Result:")
        print(f"Handled: {result['handled']}")
        print(f"?-density: {result['pi_density']:.3f}")
        print(f"Conservation Factor: {result['conservation_factor']:.3f}")
        
        # Check system health
        health = get_paradox_system_health()
        print(f"System Health: {health}")
    
    asyncio.run(test_integration())
