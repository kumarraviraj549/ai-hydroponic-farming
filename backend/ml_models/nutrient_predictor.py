"""AI/ML Nutrient Predictor for HydroAI platform."""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class NutrientPredictor:
    """AI-powered nutrient recommendation system using rule-based logic.
    
    This class analyzes sensor data and generates actionable recommendations
    for optimizing hydroponic farming conditions.
    """
    
    def __init__(self):
        """Initialize the predictor with optimal ranges and rules."""
        # Optimal ranges for different parameters
        self.optimal_ranges = {
            'ph': {'min': 5.5, 'max': 6.5, 'ideal': 6.0},
            'temperature': {'min': 18, 'max': 26, 'ideal': 22},
            'humidity': {'min': 60, 'max': 80, 'ideal': 70},
            'nutrients': {'min': 800, 'max': 1200, 'ideal': 1000},  # ppm
            'dissolved_oxygen': {'min': 5, 'max': 8, 'ideal': 6.5},  # mg/L
        }
        
        # Recommendation templates
        self.recommendation_templates = {
            'ph_low': {
                'title': 'pH Level Too Low',
                'description': 'Current pH is {current:.1f}. Increase pH to optimal range (5.5-6.5) by adding pH Up solution gradually.',
                'type': 'ph',
                'priority': 'high'
            },
            'ph_high': {
                'title': 'pH Level Too High', 
                'description': 'Current pH is {current:.1f}. Decrease pH to optimal range (5.5-6.5) by adding pH Down solution gradually.',
                'type': 'ph',
                'priority': 'high'
            },
            'temperature_low': {
                'title': 'Temperature Too Low',
                'description': 'Current temperature is {current:.1f}°C. Increase temperature to optimal range (18-26°C) using heating equipment.',
                'type': 'temperature',
                'priority': 'medium'
            },
            'temperature_high': {
                'title': 'Temperature Too High',
                'description': 'Current temperature is {current:.1f}°C. Reduce temperature to optimal range (18-26°C) using cooling systems.',
                'type': 'temperature',
                'priority': 'medium'
            },
            'humidity_low': {
                'title': 'Humidity Too Low',
                'description': 'Current humidity is {current:.1f}%. Increase humidity to optimal range (60-80%) using humidifiers.',
                'type': 'humidity',
                'priority': 'medium'
            },
            'humidity_high': {
                'title': 'Humidity Too High',
                'description': 'Current humidity is {current:.1f}%. Reduce humidity to optimal range (60-80%) using dehumidifiers or ventilation.',
                'type': 'humidity',
                'priority': 'medium'
            },
            'nutrients_low': {
                'title': 'Nutrient Concentration Low',
                'description': 'Current nutrient level is {current:.0f}ppm. Increase nutrient concentration to optimal range (800-1200ppm).',
                'type': 'nutrient',
                'priority': 'high'
            },
            'nutrients_high': {
                'title': 'Nutrient Concentration High',
                'description': 'Current nutrient level is {current:.0f}ppm. Dilute nutrient solution to optimal range (800-1200ppm).',
                'type': 'nutrient', 
                'priority': 'high'
            },
            'preventive_maintenance': {
                'title': 'Preventive Maintenance Recommended',
                'description': 'System has been running smoothly. Consider checking pumps, cleaning sensors, and testing backup systems.',
                'type': 'general',
                'priority': 'low'
            },
            'optimization': {
                'title': 'System Optimization Opportunity',
                'description': 'All parameters are within normal ranges. Consider fine-tuning to ideal values for maximum yield.',
                'type': 'general',
                'priority': 'low'
            }
        }
    
    def predict(self, sensor_data: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """Generate recommendations based on sensor data.
        
        Args:
            sensor_data: Dictionary with sensor types as keys and readings as values
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            recommendations = []
            
            # Analyze each sensor type
            for sensor_type, readings in sensor_data.items():
                if not readings:
                    continue
                    
                # Get latest reading
                latest_reading = readings[0]  # Assuming sorted by timestamp desc
                current_value = latest_reading['value']
                
                # Generate recommendations based on rules
                recs = self._analyze_sensor_parameter(sensor_type, current_value, readings)
                recommendations.extend(recs)
            
            # Add general recommendations if system is stable
            if self._is_system_stable(sensor_data):
                recommendations.extend(self._generate_general_recommendations(sensor_data))
            
            # Limit recommendations and prioritize
            recommendations = self._prioritize_recommendations(recommendations)
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations()
    
    def _analyze_sensor_parameter(self, sensor_type: str, current_value: float, readings: List[Dict]) -> List[Dict]:
        """Analyze specific sensor parameter and generate recommendations."""
        recommendations = []
        
        if sensor_type not in self.optimal_ranges:
            return recommendations
        
        optimal = self.optimal_ranges[sensor_type]
        confidence = self._calculate_confidence(readings)
        
        # Check if value is outside optimal range
        if current_value < optimal['min']:
            template_key = f"{sensor_type}_low"
            if template_key in self.recommendation_templates:
                rec = self._create_recommendation(
                    template_key, current_value, confidence
                )
                recommendations.append(rec)
        
        elif current_value > optimal['max']:
            template_key = f"{sensor_type}_high"
            if template_key in self.recommendation_templates:
                rec = self._create_recommendation(
                    template_key, current_value, confidence
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _create_recommendation(self, template_key: str, current_value: float, confidence: float) -> Dict:
        """Create recommendation from template."""
        template = self.recommendation_templates[template_key]
        
        return {
            'title': template['title'],
            'description': template['description'].format(current=current_value),
            'type': template['type'],
            'priority': template['priority'],
            'confidence': confidence,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _calculate_confidence(self, readings: List[Dict]) -> float:
        """Calculate confidence score based on data quality."""
        if len(readings) < 3:
            return 0.6  # Low confidence with limited data
        
        # Calculate variance to assess data stability
        values = [r['value'] for r in readings[:10]]  # Last 10 readings
        variance = np.var(values) if len(values) > 1 else 0
        
        # Higher variance = lower confidence
        confidence = max(0.5, min(0.95, 0.9 - (variance / 100)))
        return round(confidence, 2)
    
    def _is_system_stable(self, sensor_data: Dict) -> bool:
        """Check if all system parameters are stable."""
        for sensor_type, readings in sensor_data.items():
            if not readings or sensor_type not in self.optimal_ranges:
                continue
                
            current_value = readings[0]['value']
            optimal = self.optimal_ranges[sensor_type]
            
            # If any parameter is outside optimal range, system is not stable
            if current_value < optimal['min'] or current_value > optimal['max']:
                return False
        
        return True
    
    def _generate_general_recommendations(self, sensor_data: Dict) -> List[Dict]:
        """Generate general maintenance and optimization recommendations."""
        recommendations = []
        
        # Add preventive maintenance recommendation
        maintenance_rec = self._create_recommendation(
            'preventive_maintenance', 0, 0.8
        )
        recommendations.append(maintenance_rec)
        
        # Check if system can be optimized further
        optimization_score = self._calculate_optimization_potential(sensor_data)
        if optimization_score > 0.3:
            optimization_rec = self._create_recommendation(
                'optimization', 0, optimization_score
            )
            recommendations.append(optimization_rec)
        
        return recommendations
    
    def _calculate_optimization_potential(self, sensor_data: Dict) -> float:
        """Calculate potential for system optimization."""
        total_score = 0
        param_count = 0
        
        for sensor_type, readings in sensor_data.items():
            if not readings or sensor_type not in self.optimal_ranges:
                continue
                
            current_value = readings[0]['value']
            optimal = self.optimal_ranges[sensor_type]
            
            # Calculate distance from ideal value
            distance_from_ideal = abs(current_value - optimal['ideal'])
            range_size = optimal['max'] - optimal['min']
            
            # Normalize score (0 = at ideal, 1 = at range boundary)
            param_score = min(1.0, distance_from_ideal / (range_size / 2))
            total_score += param_score
            param_count += 1
        
        return total_score / param_count if param_count > 0 else 0
    
    def _prioritize_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Sort and limit recommendations by priority."""
        # Priority order
        priority_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        
        # Sort by priority and confidence
        recommendations.sort(
            key=lambda x: (priority_order.get(x['priority'], 0), x['confidence']),
            reverse=True
        )
        
        # Limit to top 5 recommendations
        return recommendations[:5]
    
    def _get_fallback_recommendations(self) -> List[Dict]:
        """Return basic recommendations when analysis fails."""
        return [{
            'title': 'System Check Required',
            'description': 'Unable to analyze current sensor data. Please check sensor connections and data quality.',
            'type': 'system',
            'priority': 'medium',
            'confidence': 0.5,
            'timestamp': datetime.utcnow().isoformat()
        }]


# Utility functions for testing
def generate_sample_sensor_data() -> Dict[str, List[Dict]]:
    """Generate sample sensor data for testing."""
    now = datetime.utcnow()
    
    return {
        'ph': [
            {'value': 5.2, 'timestamp': (now - timedelta(minutes=5)).isoformat(), 'unit': 'pH'},
            {'value': 5.3, 'timestamp': (now - timedelta(minutes=10)).isoformat(), 'unit': 'pH'},
            {'value': 5.1, 'timestamp': (now - timedelta(minutes=15)).isoformat(), 'unit': 'pH'},
        ],
        'temperature': [
            {'value': 24.5, 'timestamp': (now - timedelta(minutes=5)).isoformat(), 'unit': '°C'},
            {'value': 24.2, 'timestamp': (now - timedelta(minutes=10)).isoformat(), 'unit': '°C'},
            {'value': 24.8, 'timestamp': (now - timedelta(minutes=15)).isoformat(), 'unit': '°C'},
        ],
        'nutrients': [
            {'value': 1150, 'timestamp': (now - timedelta(minutes=5)).isoformat(), 'unit': 'ppm'},
            {'value': 1140, 'timestamp': (now - timedelta(minutes=10)).isoformat(), 'unit': 'ppm'},
            {'value': 1160, 'timestamp': (now - timedelta(minutes=15)).isoformat(), 'unit': 'ppm'},
        ]
    }


if __name__ == '__main__':
    # Test the predictor
    predictor = NutrientPredictor()
    sample_data = generate_sample_sensor_data()
    
    recommendations = predictor.predict(sample_data)
    
    print("Generated Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['title']} ({rec['priority']} priority)")
        print(f"   {rec['description']}")
        print(f"   Confidence: {rec['confidence']:.0%}")
