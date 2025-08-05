#!/usr/bin/env python3
"""
TOP 23 PRACTICAL PROMPTS FOR INFERRIX BMS DAILY OPERATIONS
Organized by complexity: Simple, Magic, Medium Complex, Complex
Covering real-world scenarios that happen daily in building management
"""

# 🏢 TOP 23 PRACTICAL PROMPTS FOR INFERRIX BMS DAILY OPERATIONS

PRACTICAL_PROMPTS = {
    "WEATHER_RISK": [
        # Weather and Risk Analysis Prompts (New)
        {
            "prompt": "What is the weather prediction in Mumbai for tomorrow?",
            "scenario": "Weather forecasting for facility planning",
            "use_case": "Daily weather monitoring for HVAC optimization",
            "expected_response": "🌤️ **Weather Forecast for Mumbai (next 2 days):**\n\n📅 **Tomorrow (Friday, 07 Jun):**\n• Weather: Light rain with thunderstorms\n• Min Temperature: 27°C\n• Max Temperature: 32°C\n• Humidity: 85%\n• Wind: 15 km/h\n\n📅 **Day After (Saturday, 08 Jun):**\n• Weather: Partly cloudy\n• Min Temperature: 26°C\n• Max Temperature: 31°C\n• Humidity: 75%\n• Wind: 12 km/h\n\n💡 **Facility Impact:**\n• High humidity may affect HVAC efficiency\n• Consider dehumidification settings\n• Monitor for potential water ingress",
            "complexity": "Simple",
            "frequency": "Daily"
        },
        {
            "prompt": "What HVAC risks if it rains in Mumbai this week?",
            "scenario": "Weather-based risk assessment",
            "use_case": "Proactive facility risk management",
            "expected_response": "🌦️ **Weather Risk Analysis for HVAC in Mumbai (this_week):**\n\n📅 **Weather Forecast:**\n• Monday: Heavy rain, 25-30°C, 90% humidity\n• Tuesday: Moderate rain, 26-31°C, 85% humidity\n• Wednesday: Light rain, 27-32°C, 80% humidity\n• Thursday: Partly cloudy, 28-33°C, 75% humidity\n• Friday: Clear, 29-34°C, 70% humidity\n\n🚨 **HVAC Risks Identified:**\n\n🔴 **High Risk:**\n• **Moisture Ingress:** Heavy rain may cause water damage to outdoor units\n• **Electrical Issues:** High humidity can affect electrical components\n• **Efficiency Drop:** 90% humidity will reduce cooling efficiency by 25%\n\n🟡 **Medium Risk:**\n• **Filter Clogging:** Rain may introduce debris into air intakes\n• **Corrosion:** Prolonged humidity exposure\n• **Mold Growth:** High humidity in ductwork\n\n💡 **Recommended Actions:**\n\n🛡️ **Immediate (Today):**\n• Inspect outdoor HVAC units for water protection\n• Check electrical connections for moisture\n• Verify drainage systems are clear\n\n🔧 **This Week:**\n• Schedule filter replacement after rain\n• Monitor humidity levels in critical areas\n• Prepare dehumidification systems\n\n📊 **Expected Impact:**\n• Energy consumption: +20% due to humidity\n• Maintenance needs: +15% due to moisture\n• Guest comfort: Monitor closely\n\n✅ **Risk Mitigation:** All systems prepared for weather conditions",
            "complexity": "Magic",
            "frequency": "Weekly"
        },
        {
            "prompt": "Show me weather forecast for Delhi this week",
            "scenario": "Weekly weather planning",
            "use_case": "Strategic facility planning",
            "expected_response": "🌤️ **Weather Forecast for Delhi (this_week):**\n\n📅 **Monday:**\n• Weather: Clear sky\n• Min: 28°C, Max: 42°C\n• Humidity: 45%\n• Wind: 8 km/h\n\n📅 **Tuesday:**\n• Weather: Partly cloudy\n• Min: 29°C, Max: 41°C\n• Humidity: 50%\n• Wind: 10 km/h\n\n📅 **Wednesday:**\n• Weather: Clear sky\n• Min: 30°C, Max: 43°C\n• Humidity: 40%\n• Wind: 12 km/h\n\n📅 **Thursday:**\n• Weather: Dust storm possible\n• Min: 31°C, Max: 44°C\n• Humidity: 35%\n• Wind: 25 km/h\n\n📅 **Friday:**\n• Weather: Clear sky\n• Min: 32°C, Max: 45°C\n• Humidity: 30%\n• Wind: 15 km/h\n\n💡 **Facility Recommendations:**\n• High temperatures require increased cooling\n• Dust storm preparation needed for Wednesday\n• Energy consumption will be high due to heat\n• Consider guest comfort measures",
            "complexity": "Simple",
            "frequency": "Weekly"
        },
        {
            "prompt": "What are the lighting risks if temperature drops in Bangalore?",
            "scenario": "Temperature-based lighting risk assessment",
            "use_case": "Proactive lighting system management",
            "expected_response": "🌦️ **Weather Risk Analysis for Lighting in Bangalore:**\n\n📅 **Weather Forecast:**\n• Temperature drop: 32°C → 18°C over 48 hours\n• Weather: Heavy rain and thunderstorms\n• Humidity: 85-90%\n• Wind: 20-30 km/h\n\n🚨 **Lighting System Risks:**\n\n🔴 **High Risk:**\n• **Electrical Shorts:** Moisture ingress in outdoor lighting\n• **Power Fluctuations:** Storm-related power surges\n• **Fixture Damage:** High winds may damage outdoor lights\n\n🟡 **Medium Risk:**\n• **Sensor Malfunction:** Temperature sensors may need recalibration\n• **Timer Issues:** Daylight changes affect automatic timers\n• **Energy Waste:** Extended lighting hours due to overcast conditions\n\n💡 **Recommended Actions:**\n\n🛡️ **Immediate (Today):**\n• Inspect outdoor lighting fixtures for water protection\n• Install surge protectors on critical circuits\n• Secure loose fixtures and wiring\n\n🔧 **This Week:**\n• Adjust lighting timers for shorter daylight\n• Monitor energy consumption closely\n• Schedule post-storm inspection\n\n📊 **Expected Impact:**\n• Energy consumption: +15% due to extended lighting\n• Maintenance needs: +20% due to weather damage\n• Safety: Enhanced monitoring required\n\n✅ **Risk Mitigation:** All outdoor lighting secured and protected",
            "complexity": "Magic",
            "frequency": "As needed"
        }
    ],
    
    "SIMPLE": [
        # 1. Basic Device Status Check
        {
            "prompt": "What's the temperature of device 300186?",
            "scenario": "Daily temperature monitoring",
            "use_case": "Facility manager checking sensor readings",
            "expected_response": "🌡️ **Device 300186 (IAQ Sensor V2):**\n• Temperature: 22.5°C\n• Status: Online\n• Last Update: 2 minutes ago",
            "complexity": "Simple",
            "frequency": "Multiple times daily"
        },
        
        # 2. Device List
        {
            "prompt": "Show me all online devices",
            "scenario": "System health overview",
            "use_case": "Morning system check",
            "expected_response": "📱 **Online Devices (42/50):**\n\n🟢 **Thermostats (15):**\n  • Main Lobby Thermostat\n  • Conference Room A Thermostat\n  • Office Floor 1 Thermostat\n  ... and 12 more\n\n🟢 **Sensors (25):**\n  • IAQ Sensor V2 - 300186\n  • RH/T Sensor - 150002\n  ... and 23 more\n\n🟢 **HVAC Units (2):**\n  • HVAC Unit 1\n  • HVAC Unit 2",
            "complexity": "Simple",
            "frequency": "Daily"
        },
        
        # 3. Alarm Check
        {
            "prompt": "Are there any active alarms?",
            "scenario": "Emergency monitoring",
            "use_case": "Regular alarm status check",
            "expected_response": "🚨 **Active Alarms (2):**\n\n🔴 **CRITICAL:**\n  • HVAC Unit 1: Temperature exceeded safety limits\n  • Time: 14:30\n  • Action Required: Immediate\n\n🟡 **MAJOR:**\n  • Sensor 300186: Battery low (2.9V)\n  • Time: 13:15\n  • Action Required: Replace battery",
            "complexity": "Simple",
            "frequency": "Multiple times daily"
        },
        
        # 4. Basic Telemetry
        {
            "prompt": "What's the humidity in the main lobby?",
            "scenario": "Environmental monitoring",
            "use_case": "Guest comfort check",
            "expected_response": "💧 **Main Lobby Humidity:**\n• Current: 45%\n• Optimal Range: 40-60%\n• Status: Normal\n• Device: Main Lobby Sensor",
            "complexity": "Simple",
            "frequency": "Daily"
        },
        
        # 5. Device Status
        {
            "prompt": "Is device 150002 working properly?",
            "scenario": "Device health check",
            "use_case": "Troubleshooting verification",
            "expected_response": "✅ **Device 150002 (RH/T Sensor):**\n• Status: Online\n• Battery: 78%\n• Last Seen: 1 minute ago\n• Health: Good\n• No issues detected",
            "complexity": "Simple",
            "frequency": "Daily"
        }
    ],
    
    "MAGIC": [
        # 6. Multi-Device Temperature Check
        {
            "prompt": "Show me temperatures from all thermostats in the east wing",
            "scenario": "Zone monitoring",
            "use_case": "HVAC zone performance check",
            "expected_response": "🌡️ **East Wing Thermostat Temperatures:**\n\n📊 **Zone Summary:**\n• Average Temperature: 22.3°C\n• Range: 21.8°C - 23.1°C\n• Status: All within optimal range\n\n📱 **Individual Readings:**\n• East Wing Lobby: 22.5°C 🟢\n• East Wing Conference: 21.8°C 🟢\n• East Wing Office: 23.1°C 🟢\n• East Wing Storage: 22.0°C 🟢",
            "complexity": "Magic",
            "frequency": "Daily"
        },
        
        # 7. Proactive Health Analysis
        {
            "prompt": "Analyze the health of all HVAC units and tell me what needs attention",
            "scenario": "Preventive maintenance",
            "use_case": "Weekly system health review",
            "expected_response": "🔍 **HVAC System Health Analysis:**\n\n🏥 **Overall Health:** 85% (Good)\n\n🟢 **HVAC Unit 1:**\n  • Status: Healthy\n  • Efficiency: 92%\n  • Last Maintenance: 2 weeks ago\n  • Next Maintenance: 6 weeks\n\n🟡 **HVAC Unit 2:**\n  • Status: Warning\n  • Issue: Filter needs replacement\n  • Efficiency: 78%\n  • Action: Replace filter within 3 days\n\n💡 **Recommendations:**\n• Schedule filter replacement for Unit 2\n• Monitor Unit 1 performance\n• Consider efficiency optimization",
            "complexity": "Magic",
            "frequency": "Weekly"
        },
        
        # 8. Energy Optimization
        {
            "prompt": "How can I optimize energy consumption across all devices?",
            "scenario": "Energy management",
            "use_case": "Monthly energy review",
            "expected_response": "⚡ **Energy Optimization Recommendations:**\n\n📊 **Current Status:**\n• Total Consumption: 1,245 kWh/day\n• Efficiency Score: 76%\n• Potential Savings: 18%\n\n🎯 **Immediate Actions (Save 8%):**\n• Adjust HVAC setpoints by 1°C: Save 5%\n• Optimize ventilation schedules: Save 3%\n\n🔧 **Medium-term Actions (Save 10%):**\n• Replace 3 old thermostats: Save 6%\n• Install occupancy sensors: Save 4%\n\n💰 **Financial Impact:**\n• Daily Savings: $45\n• Monthly Savings: $1,350\n• Annual Savings: $16,200\n\n✅ **Recommended Implementation:** Start with immediate actions today",
            "complexity": "Magic",
            "frequency": "Monthly"
        },
        
        # 9. Smart Notifications
        {
            "prompt": "What notifications do I have and what should I prioritize?",
            "scenario": "Alert management",
            "use_case": "Daily notification review",
            "expected_response": "📬 **Smart Notifications Summary:**\n\n🔴 **High Priority (2):**\n• HVAC Unit 2: Filter replacement overdue\n• Sensor 300186: Battery critical (10%)\n\n🟡 **Medium Priority (3):**\n• 5 thermostats: Maintenance due next week\n• 2 sensors: Calibration needed\n• Energy usage: 15% above target\n\n🟢 **Low Priority (1):**\n• System update available\n\n📋 **Action Plan:**\n1. **Today:** Replace HVAC filter\n2. **Tomorrow:** Replace sensor battery\n3. **This Week:** Schedule maintenance\n\n💡 **Automated Actions:** System will send reminders for medium priority items",
            "complexity": "Magic",
            "frequency": "Daily"
        },
        
        # 10. Context-Aware Recommendations
        {
            "prompt": "Based on today's occupancy and weather, what should I adjust?",
            "scenario": "Adaptive control",
            "use_case": "Daily system optimization",
            "expected_response": "🌤️ **Context-Aware Recommendations:**\n\n📅 **Today's Context:**\n• Weather: Hot and humid (32°C, 75% humidity)\n• Occupancy: 85% (High season)\n• Events: Conference in main hall\n\n🎯 **Recommended Adjustments:**\n\n🌡️ **HVAC Optimization:**\n• Increase cooling capacity by 20%\n• Lower humidity setpoints to 45%\n• Extend cooling hours by 2 hours\n\n⚡ **Energy Management:**\n• Activate peak load management\n• Optimize ventilation for humidity control\n\n👥 **Guest Experience:**\n• Pre-cool conference hall 1 hour before event\n• Maintain lobby at 22°C for arrivals\n• Increase pool area dehumidification\n\n📊 **Expected Impact:**\n• Guest comfort: +30% improvement\n• Energy cost: +12% (justified by occupancy)\n• System efficiency: Maintained at 82%",
            "complexity": "Magic",
            "frequency": "Daily"
        }
    ],
    
    "MEDIUM_COMPLEX": [
        # 11. Predictive Maintenance Schedule
        {
            "prompt": "Create a maintenance schedule for the next 30 days based on device health and usage patterns",
            "scenario": "Predictive maintenance",
            "use_case": "Monthly maintenance planning",
            "expected_response": "📅 **30-Day Predictive Maintenance Schedule:**\n\n🔴 **Week 1 - Critical (3 items):**\n• **Monday:** Replace HVAC Unit 2 filter (overdue)\n• **Tuesday:** Replace Sensor 300186 battery (critical)\n• **Wednesday:** Calibrate Thermostat 150002 (drift detected)\n\n🟡 **Week 2 - High Priority (5 items):**\n• **Monday:** Maintenance on 3 thermostats\n• **Tuesday:** Calibrate 2 sensors\n• **Wednesday:** HVAC efficiency check\n• **Thursday:** System performance review\n• **Friday:** Energy optimization audit\n\n🟢 **Week 3-4 - Routine (8 items):**\n• Battery checks for 5 devices\n• Calibration for 3 sensors\n• Performance reviews\n\n📊 **Resource Planning:**\n• **Technicians Needed:** 2 full-time\n• **Parts Required:** $1,200 estimated\n• **Downtime:** Minimal (scheduled during off-hours)\n• **ROI:** 300% (preventive vs reactive)\n\n✅ **Automated Scheduling:** System will send reminders and track completion",
            "complexity": "Medium Complex",
            "frequency": "Monthly"
        },
        
        # 12. Multi-Zone Automation
        {
            "prompt": "Set up automated temperature control for different zones: guest rooms at 22°C, conference rooms at 20°C, and public areas at 24°C, with different schedules for weekdays and weekends",
            "scenario": "Advanced automation",
            "use_case": "Seasonal system configuration",
            "expected_response": "🤖 **Multi-Zone Automation Configuration:**\n\n🌡️ **Temperature Zones:**\n• **Guest Rooms:** 22°C (Optimal comfort)\n• **Conference Rooms:** 20°C (Productivity focus)\n• **Public Areas:** 24°C (Energy efficient)\n\n⏰ **Schedule Configuration:**\n\n📅 **Weekdays (Mon-Fri):**\n• **6:00 AM - 8:00 AM:** Pre-cooling mode\n• **8:00 AM - 6:00 PM:** Business hours (full comfort)\n• **6:00 PM - 10:00 PM:** Evening mode (reduced)\n• **10:00 PM - 6:00 AM:** Night mode (energy saving)\n\n📅 **Weekends (Sat-Sun):**\n• **8:00 AM - 8:00 PM:** Weekend comfort mode\n• **8:00 PM - 8:00 AM:** Energy saving mode\n\n📱 **Devices Affected:**\n• 25 Guest Room Thermostats\n• 3 Conference Room Thermostats\n• 8 Public Area Thermostats\n• Total: 36 devices\n\n⚡ **Energy Impact:**\n• Weekday savings: 15%\n• Weekend savings: 25%\n• Monthly savings: $800\n\n✅ **Automation activated. System will adapt to occupancy patterns.**",
            "complexity": "Medium Complex",
            "frequency": "Seasonal"
        },
        
        # 13. Comprehensive System Health Report
        {
            "prompt": "Generate a comprehensive system health report with performance metrics, efficiency analysis, and recommendations for improvement",
            "scenario": "System audit",
            "use_case": "Quarterly system review",
            "expected_response": "📊 **Comprehensive System Health Report:**\n\n🏥 **Overall System Health:** 82% (Good)\n\n📈 **Performance Metrics:**\n• **Uptime:** 98.7% (Target: 99.5%)\n• **Response Time:** 2.3s (Target: <2s)\n• **Energy Efficiency:** 76% (Target: 85%)\n• **Guest Satisfaction:** 4.2/5 (Target: 4.5/5)\n\n📱 **Device Status Summary:**\n• **Online:** 42/50 devices (84%)\n• **Optimal Performance:** 38 devices (76%)\n• **Needs Attention:** 8 devices (16%)\n• **Critical Issues:** 2 devices (4%)\n\n⚡ **Energy Analysis:**\n• **Total Consumption:** 37,450 kWh/month\n• **Peak Usage:** 12:00-14:00 daily\n• **Efficiency Score:** 76% (below target)\n• **Cost:** $4,493/month\n\n🎯 **Key Performance Indicators:**\n• **HVAC Efficiency:** 78% (Target: 85%)\n• **Sensor Accuracy:** 94% (Target: 95%)\n• **Alarm Response Time:** 8 minutes (Target: <5)\n• **Maintenance Compliance:** 92% (Target: 95%)\n\n💡 **Improvement Recommendations:**\n\n🔴 **High Priority:**\n• Replace 3 old thermostats: +8% efficiency\n• Upgrade HVAC controls: +12% efficiency\n• Implement smart scheduling: +15% savings\n\n🟡 **Medium Priority:**\n• Install occupancy sensors: +6% efficiency\n• Improve maintenance scheduling: +5% uptime\n• Enhanced monitoring: +3% response time\n\n💰 **ROI Analysis:**\n• Investment Required: $25,000\n• Monthly Savings: $1,200\n• Payback Period: 21 months\n• 5-year ROI: 288%\n\n✅ **Next Steps:** Implement high priority items within 3 months",
            "complexity": "Medium Complex",
            "frequency": "Quarterly"
        },
        
        # 14. Anomaly Detection and Resolution
        {
            "prompt": "Detect any anomalies in the system, analyze their root causes, and provide resolution strategies",
            "scenario": "Problem detection and resolution",
            "use_case": "System troubleshooting",
            "expected_response": "🚨 **Anomaly Detection and Analysis Report:**\n\n🔍 **Anomalies Detected (3):**\n\n🔴 **Critical Anomaly 1:**\n• **Issue:** Temperature spike in Room 301\n• **Pattern:** 32°C vs normal 22°C\n• **Duration:** 4 hours\n• **Root Cause:** HVAC unit malfunction\n• **Impact:** Guest comfort affected\n• **Resolution:** Immediate HVAC technician call\n\n🟡 **Warning Anomaly 2:**\n• **Issue:** Energy consumption surge\n• **Pattern:** 40% increase in HVAC usage\n• **Duration:** 6 hours\n• **Root Cause:** Compressor inefficiency\n• **Impact:** Higher energy costs\n• **Resolution:** Schedule compressor maintenance\n\n🟡 **Warning Anomaly 3:**\n• **Issue:** Communication delays\n• **Pattern:** 3 devices responding slowly\n• **Duration:** 2 hours\n• **Root Cause:** Network congestion\n• **Impact:** Reduced monitoring accuracy\n• **Resolution:** Network optimization\n\n📊 **Anomaly Summary:**\n• **Critical:** 1 issue (immediate action)\n• **Warning:** 2 issues (schedule action)\n• **System Health:** 78% (down from 85%)\n\n🔧 **Resolution Strategy:**\n1. **Immediate (0-2 hours):** Fix Room 301 HVAC\n2. **Today (2-8 hours):** Optimize network\n3. **This Week:** Schedule compressor maintenance\n4. **This Month:** Implement anomaly monitoring\n\n💡 **Prevention Measures:**\n• Enhanced monitoring for temperature spikes\n• Regular HVAC performance checks\n• Network capacity planning\n• Predictive maintenance scheduling",
            "complexity": "Medium Complex",
            "frequency": "As needed"
        },
        
        # 15. Multi-Language Technical Support
        {
            "prompt": "Je suis technicien et j'ai besoin d'un diagnostic complet du système HVAC avec des recommandations de réparation en français",
            "scenario": "International technical support",
            "use_case": "Multi-language maintenance",
            "expected_response": "🛠️ **Diagnostic Technique HVAC - Rapport Complet:**\n\n🔧 **État du Système:**\n• **Santé Globale:** 78% (Attention requise)\n• **Unités Actives:** 2/3\n• **Efficacité Moyenne:** 72%\n\n🔴 **Problèmes Critiques:**\n• **Unité HVAC 1:** Compresseur surchauffe (85°C)\n  - Cause: Filtres bouchés + réfrigérant bas\n  - Impact: Surchauffe + inefficacité\n  - Solution: Remplacement filtres + recharge réfrigérant\n  - Temps: 3 heures\n\n• **Unité HVAC 2:** Fuite de réfrigérant\n  - Cause: Joint défectueux\n  - Impact: Perte de performance\n  - Solution: Réparation d'urgence\n  - Temps: 4 heures\n\n🟡 **Problèmes Majeurs:**\n• 5 thermostats: Calibration nécessaire\n• 3 capteurs: Batteries faibles\n• 2 unités: Maintenance préventive due\n\n📋 **Plan d'Action Technique:**\n1. **Maintenant:** Arrêter Unité HVAC 1\n2. **Aujourd'hui:** Réparer fuite Unité HVAC 2\n3. **Cette semaine:** Calibrer thermostats\n4. **Ce mois:** Maintenance préventive\n\n🛠️ **Actions Techniques Disponibles:**\n• Voir guide de dépannage détaillé\n• Commander pièces détachées\n• Contacter support technique\n• Planifier maintenance\n\n💰 **Coût Estimé:** €2,500 (réparations + pièces)\n⏱️ **Temps Total:** 2 jours\n\n✅ **Recommandation:** Commencer immédiatement avec Unité HVAC 1",
            "complexity": "Medium Complex",
            "frequency": "As needed"
        },
        
        # 16. Emergency Response and Recovery
        {
            "prompt": "There's a power outage affecting the east wing. What systems are impacted, what's the emergency response plan, and how do we minimize guest disruption?",
            "scenario": "Emergency management",
            "use_case": "Crisis response",
            "expected_response": "🚨 **Emergency Response - Power Outage East Wing:**\n\n⚡ **Systèmes Impactés:**\n\n🔴 **Systèmes Critiques Arrêtés:**\n• 8 unités HVAC chambres d'hôtes\n• 3 systèmes salles de conférence\n• 2 ascenseurs\n• Éclairage principal (éclairage de secours actif)\n\n🟡 **Systèmes Partiellement Affectés:**\n• Système d'alarme incendie (alimentation de secours OK)\n• Caméras de sécurité (alimentation de secours OK)\n• Wi-Fi (couverture réduite)\n\n📋 **Plan de Réponse d'Urgence:**\n\n🚨 **Actions Immédiates (0-15 minutes):**\n1. **Sécurité:** Évacuer les zones affectées si nécessaire\n2. **Communication:** Informer les clients de la situation\n3. **Systèmes de Secours:** Activer l'alimentation d'urgence\n4. **Alerte Technique:** Contacter la maintenance d'urgence\n\n⏰ **Actions Court Terme (15-60 minutes):**\n1. **Relocalisation Clients:** Déplacer vers chambres non affectées\n2. **Refroidissement Alternatif:** Déployer unités AC portables\n3. **Communication:** Mettre à jour tout le personnel\n4. **Évaluation:** Évaluer l'étendue des dégâts\n\n📞 **Contacts d'Urgence:**\n• Maintenance: +1-555-0123 (De garde)\n• Compagnie Électrique: +1-555-0124 (Signalé)\n• Direction: +1-555-0125 (Notifié)\n\n⏱️ **Résolution Estimée:** 2-4 heures\n\n💡 **Impact Clients:** 12 chambres affectées, relocalisation en cours\n\n🔄 **Plan de Récupération:**\n• Restauration progressive des systèmes\n• Vérification de l'intégrité des données\n• Tests de sécurité post-récupération",
            "complexity": "Medium Complex",
            "frequency": "Emergency"
        },
        
        # 17. Performance Analytics and Optimization
        {
            "prompt": "Analyze system performance over the last 30 days, identify bottlenecks, and provide optimization strategies with ROI calculations",
            "scenario": "Performance optimization",
            "use_case": "Monthly performance review",
            "expected_response": "📈 **30-Day Performance Analytics & Optimization Report:**\n\n📊 **Performance Metrics:**\n\n🏥 **System Health:**\n• **Average Uptime:** 98.7% (Target: 99.5%)\n• **Critical Failures:** 2 (Target: 0)\n• **Response Time:** 2.3s (Target: <2s)\n• **Guest Satisfaction:** 4.2/5 (Target: 4.5/5)\n\n⚡ **Energy Performance:**\n• **Total Consumption:** 37,450 kWh\n• **Efficiency Score:** 76% (Target: 85%)\n• **Peak Usage:** 12:00-14:00 daily\n• **Cost:** $4,493 (Target: $3,745)\n\n🔍 **Bottleneck Analysis:**\n\n🔴 **Critical Bottlenecks:**\n• **HVAC Efficiency:** 78% (Target: 85%)\n  - Cause: Old thermostats + poor scheduling\n  - Impact: 15% energy waste\n  - Solution: Smart thermostat upgrade\n\n• **Response Time:** 2.3s (Target: <2s)\n  - Cause: Network congestion + old sensors\n  - Impact: Delayed monitoring\n  - Solution: Network optimization + sensor upgrade\n\n🟡 **Medium Bottlenecks:**\n• **Maintenance Compliance:** 92% (Target: 95%)\n• **Sensor Accuracy:** 94% (Target: 95%)\n• **Alarm Response:** 8 minutes (Target: <5)\n\n🎯 **Optimization Strategies:**\n\n💰 **High Impact (Save $800/month):**\n• **Smart Thermostat Upgrade:** $15,000 investment\n  - Energy savings: 20%\n  - Monthly savings: $500\n  - Payback: 30 months\n  - 5-year ROI: 200%\n\n• **Network Optimization:** $8,000 investment\n  - Response time improvement: 40%\n  - Efficiency gain: 8%\n  - Monthly savings: $300\n  - Payback: 27 months\n  - 5-year ROI: 225%\n\n📈 **Medium Impact (Save $400/month):**\n• **Sensor Upgrade:** $12,000 investment\n  - Accuracy improvement: 3%\n  - Maintenance reduction: 15%\n  - Monthly savings: $200\n  - Payback: 60 months\n  - 5-year ROI: 100%\n\n• **Process Optimization:** $5,000 investment\n  - Response time improvement: 25%\n  - Efficiency gain: 5%\n  - Monthly savings: $200\n  - Payback: 25 months\n  - 5-year ROI: 240%\n\n📊 **Total Investment:** $40,000\n📊 **Total Monthly Savings:** $1,200\n📊 **Payback Period:** 33 months\n📊 **5-year ROI:** 180%\n\n✅ **Recommended Implementation:** Phase 1 (High Impact) - 3 months",
            "complexity": "Medium Complex",
            "frequency": "Monthly"
        },
        
        # 18. Integration and Workflow Automation
        {
            "prompt": "Integrate with the hotel booking system to automatically adjust room conditions based on check-ins, check-outs, and guest preferences",
            "scenario": "System integration",
            "use_case": "Workflow automation",
            "expected_response": "🔗 **Hotel Booking System Integration - Smart Room Automation:**\n\n📅 **Today's Schedule:**\n• **Check-ins:** 18 rooms (2:00 PM - 6:00 PM)\n• **Check-outs:** 15 rooms (10:00 AM - 12:00 PM)\n• **Current Occupancy:** 82% (164/200 rooms)\n• **VIP Guests:** 3 rooms (special preferences)\n\n🤖 **Automated Room Optimization:**\n\n🟢 **Pre-Check-in Preparation (2 hours before):**\n• **Rooms 201-218:** Pre-cooling to 22°C\n• **VIP Rooms 301-303:** Pre-cooling to 20°C (VIP preference)\n• **Humidity:** Optimizing to 45%\n• **Air Quality:** Fresh air circulation activated\n• **Lighting:** Welcome mode activated\n\n🔄 **Check-out Optimization:**\n• **Rooms 401-415:** Energy-saving mode activated\n• **HVAC:** Reduced to maintenance temperature (18°C)\n• **Ventilation:** Eco-mode for cleaning\n• **Lighting:** Maintenance mode\n\n📊 **Smart Adjustments:**\n• **Public Areas:** Increased cooling for guest arrivals\n• **Lobby:** Optimal comfort for check-in process\n• **Corridors:** Enhanced ventilation for guest flow\n• **Pool Area:** Humidity control for comfort\n\n💡 **Integration Benefits:**\n• **Energy Savings:** 25% on vacant rooms\n• **Guest Satisfaction:** 100% on room temperature\n• **Operational Efficiency:** Automated coordination\n• **Real-time Tracking:** Live occupancy monitoring\n• **Personalization:** VIP guest preferences\n\n📈 **Performance Metrics:**\n• **Check-in Efficiency:** +30% improvement\n• **Energy Optimization:** +25% savings\n• **Guest Comfort:** 4.8/5 rating\n• **Staff Productivity:** +20% improvement\n\n✅ **Integration active. 18 rooms being prepared for check-in.**\n\n🔄 **Next Steps:**\n• Monitor integration performance\n• Adjust automation rules based on feedback\n• Expand to other hotel systems",
            "complexity": "Medium Complex",
            "frequency": "Implementation"
        },
        
        # 19. Predictive Analytics and Forecasting
        {
            "prompt": "Predict energy consumption, maintenance needs, and guest comfort issues for the next 90 days based on historical data and seasonal patterns",
            "scenario": "Predictive analytics",
            "use_case": "Strategic planning",
            "expected_response": "🔮 **90-Day Predictive Analytics & Forecasting Report:**\n\n📊 **Energy Consumption Forecast:**\n\n📈 **Monthly Predictions:**\n• **Month 1:** 38,200 kWh (Peak summer)\n• **Month 2:** 35,800 kWh (Late summer)\n• **Month 3:** 32,400 kWh (Early fall)\n\n💰 **Cost Forecast:**\n• **Total 90-day Cost:** $12,600\n• **Average Monthly:** $4,200\n• **Peak Day:** July 15th (1,450 kWh)\n\n🔧 **Maintenance Needs Prediction:**\n\n📅 **Month 1 (High Priority):**\n• **Week 1:** 3 HVAC filter replacements\n• **Week 2:** 5 thermostat calibrations\n• **Week 3:** 2 sensor battery replacements\n• **Week 4:** 1 HVAC unit maintenance\n\n📅 **Month 2 (Medium Priority):**\n• **Week 1-2:** 8 device maintenance checks\n• **Week 3-4:** 3 system optimizations\n\n📅 **Month 3 (Low Priority):**\n• **Week 1-4:** 12 routine maintenance items\n\n👥 **Guest Comfort Issues Prediction:**\n\n🌡️ **Temperature-Related Issues:**\n• **High Risk Period:** July 10-20 (Heat wave)\n• **Affected Areas:** South-facing rooms\n• **Predicted Issues:** 8-12 comfort complaints\n• **Prevention:** Pre-cooling + humidity control\n\n💧 **Humidity-Related Issues:**\n• **High Risk Period:** August 1-15 (Humid weather)\n• **Affected Areas:** Pool area + basement\n• **Predicted Issues:** 3-5 humidity complaints\n• **Prevention:** Enhanced dehumidification\n\n📊 **Risk Assessment:**\n\n🔴 **High Risk (Immediate Action):**\n• HVAC system overload during heat wave\n• Energy cost spike in July\n• Guest comfort issues in south rooms\n\n🟡 **Medium Risk (Plan Action):**\n• Maintenance backlog in August\n• Humidity issues in pool area\n• Sensor accuracy drift\n\n🟢 **Low Risk (Monitor):**\n• Routine maintenance scheduling\n• Energy efficiency optimization\n• System performance monitoring\n\n💡 **Strategic Recommendations:**\n\n🎯 **Immediate Actions (Next 30 days):**\n• Upgrade 3 HVAC units for heat wave\n• Install 5 additional sensors in south rooms\n• Implement smart scheduling for energy optimization\n\n📈 **Medium-term Actions (30-60 days):**\n• Predictive maintenance scheduling\n• Enhanced humidity control systems\n• Guest preference learning algorithms\n\n🔮 **Long-term Actions (60-90 days):**\n• System-wide efficiency optimization\n• Advanced predictive analytics implementation\n• Integration with weather forecasting\n\n💰 **Investment Required:** $35,000\n📊 **Expected Savings:** $8,400 (90 days)\n📊 **ROI:** 240% (90 days)\n\n✅ **Recommendation:** Implement immediate actions within 2 weeks",
            "complexity": "Medium Complex",
            "frequency": "Quarterly"
        },
        
        # 20. Future-Proofing and Technology Roadmap
        {
            "prompt": "What are the emerging trends in building automation and how should we prepare our system for future technologies like IoT, AI, and smart city integration?",
            "scenario": "Strategic planning",
            "use_case": "Technology roadmap",
            "expected_response": "🔮 **Future-Proofing Analysis - Building Automation Technology Roadmap:**\n\n📈 **Emerging Trends (2024-2025):**\n\n🤖 **AI & Machine Learning Evolution:**\n• **Predictive Analytics:** 99% accuracy in failure prediction\n• **Behavioral Learning:** Real-time guest preference adaptation\n• **Energy Optimization:** AI-driven load balancing\n• **Anomaly Detection:** Advanced pattern recognition\n• **Natural Language Processing:** Conversational AI interfaces\n\n🌱 **Sustainability & Green Technology:**\n• **Carbon Footprint Tracking:** Real-time emissions monitoring\n• **Renewable Integration:** Solar/wind power optimization\n• **Circular Economy:** Waste heat recovery systems\n• **Green Certifications:** LEED compliance automation\n• **ESG Reporting:** Automated sustainability metrics\n\n📱 **IoT & Connectivity Revolution:**\n• **5G Integration:** Ultra-low latency control\n• **Edge Computing:** Local AI processing\n• **Blockchain:** Secure device authentication\n• **Digital Twins:** Virtual system modeling\n• **Mesh Networks:** Self-healing connectivity\n\n🏙️ **Smart City Integration:**\n• **Grid Integration:** Demand response participation\n• **Traffic Optimization:** Guest arrival coordination\n• **Environmental Monitoring:** Air quality integration\n• **Emergency Services:** Automated emergency coordination\n• **Public Transportation:** Guest journey optimization\n\n🎯 **Our System Readiness Assessment:**\n\n✅ **Already Implemented (2024):**\n• AI-powered insights and automation\n• Multi-device operations\n• Predictive analytics\n• Smart notifications\n• Multi-language support\n• Self-healing capabilities\n\n🔄 **Recommended Upgrades (Next 6 months):**\n• **Advanced ML Models:** Upgrade to GPT-4 level AI\n• **IoT Expansion:** Add 100+ smart sensors\n• **Cloud Integration:** Real-time data analytics\n• **Mobile App:** Guest control interface\n• **API Integration:** Third-party system connectivity\n\n🚀 **Future Roadmap (2025-2026):**\n\n📅 **Phase 1 (2025 Q1-Q2):**\n• **Quantum Computing Integration:** Ultra-fast optimization\n• **AR/VR Maintenance:** Virtual reality troubleshooting\n• **Autonomous Systems:** Self-healing buildings\n• **Advanced Analytics:** Machine learning optimization\n\n📅 **Phase 2 (2025 Q3-Q4):**\n• **Smart City Integration:** Grid participation\n• **Environmental Monitoring:** Air quality networks\n• **Guest Experience AI:** Personalized automation\n• **Sustainability Tracking:** Carbon footprint monitoring\n\n📅 **Phase 3 (2026):**\n• **Fully Autonomous Buildings:** Self-managing systems\n• **AI-Powered Optimization:** Continuous improvement\n• **Global Integration:** Multi-location management\n• **Future-Ready Infrastructure:** Scalable architecture\n\n💰 **Investment Strategy:**\n\n📊 **Phase 1 Investment:** $75,000\n• Advanced AI models: $30,000\n• IoT expansion: $25,000\n• Cloud integration: $20,000\n\n📊 **Phase 2 Investment:** $125,000\n• Smart city integration: $50,000\n• AR/VR systems: $40,000\n• Environmental monitoring: $35,000\n\n📊 **Phase 3 Investment:** $200,000\n• Autonomous systems: $100,000\n• Global integration: $60,000\n• Future infrastructure: $40,000\n\n📈 **ROI Projections:**\n• **Phase 1 ROI:** 250% over 2 years\n• **Phase 2 ROI:** 300% over 3 years\n• **Phase 3 ROI:** 400% over 5 years\n\n🎯 **Competitive Advantages:**\n• **First Mover:** Early adoption of emerging technologies\n• **Guest Experience:** Superior personalized service\n• **Operational Efficiency:** Reduced costs and improved performance\n• **Sustainability:** Green building leadership\n• **Scalability:** Future-ready architecture\n\n✅ **Recommendation:** Start Phase 1 implementation immediately\n\n🔮 **Success Metrics:**\n• **Technology Adoption:** 90% of emerging features\n• **Guest Satisfaction:** 4.8/5 rating\n• **Operational Efficiency:** 95% target\n• **Sustainability Score:** LEED Platinum\n• **ROI Achievement:** 300% over 3 years",
            "complexity": "Medium Complex",
            "frequency": "Annual"
        }
    ],
    
    "COMPLEX": [
        # 21. Multi-Location Enterprise Management
        {
            "prompt": "I manage 5 hotels across different cities. Create a unified dashboard showing critical alerts, energy consumption comparison, and maintenance schedules across all locations with automated cross-location optimization recommendations",
            "scenario": "Multi-location enterprise management",
            "use_case": "Corporate facility management",
            "expected_response": "🏢 **Multi-Location Enterprise Dashboard:**\n\n📊 **Unified Overview (5 Hotels):**\n• **Total Devices:** 250 across all locations\n• **Overall Health:** 87% (Excellent)\n• **Total Energy Consumption:** 185,000 kWh/month\n• **Active Alerts:** 8 (3 critical, 5 warning)\n\n📍 **Location-Specific Status:**\n\n🏨 **Hotel A (Downtown):**\n• Health: 92% 🟢\n• Energy: 42,000 kWh/month\n• Alerts: 1 critical (HVAC filter)\n• Occupancy: 95%\n\n🏨 **Hotel B (Airport):**\n• Health: 85% 🟡\n• Energy: 38,000 kWh/month\n• Alerts: 2 warning (sensor calibration)\n• Occupancy: 78%\n\n🏨 **Hotel C (Resort):**\n• Health: 89% 🟢\n• Energy: 45,000 kWh/month\n• Alerts: 1 critical (pool heater)\n• Occupancy: 88%\n\n🏨 **Hotel D (Business):**\n• Health: 83% 🟡\n• Energy: 35,000 kWh/month\n• Alerts: 3 warning (thermostat drift)\n• Occupancy: 82%\n\n🏨 **Hotel E (Luxury):**\n• Health: 94% 🟢\n• Energy: 25,000 kWh/month\n• Alerts: 1 warning (lighting system)\n• Occupancy: 92%\n\n🚨 **Critical Cross-Location Alerts:**\n• **Hotel A:** HVAC Unit 1 filter replacement (overdue)\n• **Hotel C:** Pool heating system malfunction\n• **System-wide:** Network connectivity issues affecting 3 locations\n\n⚡ **Energy Optimization Opportunities:**\n• **Cross-location load balancing:** Save 12% ($2,200/month)\n• **Peak demand coordination:** Save 8% ($1,400/month)\n• **Maintenance scheduling optimization:** Save 15% ($2,600/month)\n\n📅 **Unified Maintenance Schedule:**\n• **This Week:** 15 critical items across all locations\n• **Next Week:** 28 routine maintenance items\n• **This Month:** 45 preventive maintenance tasks\n\n🤖 **Automated Cross-Location Optimization:**\n• **Load Sharing:** Redistribute HVAC load during peak hours\n• **Resource Allocation:** Optimize technician deployment\n• **Inventory Management:** Centralized parts ordering\n• **Best Practice Sharing:** Successful strategies from high-performing locations\n\n💰 **Enterprise ROI Analysis:**\n• **Monthly Savings:** $6,200 across all locations\n• **Annual Savings:** $74,400\n• **Investment Required:** $150,000\n• **Payback Period:** 24 months\n• **5-year ROI:** 248%\n\n✅ **Automated Actions Initiated:**\n• Cross-location alert prioritization\n• Unified maintenance scheduling\n• Energy consumption optimization\n• Resource allocation optimization",
            "complexity": "Complex",
            "frequency": "Daily"
        },
        
        # 22. AI-Powered Predictive Maintenance with Machine Learning
        {
            "prompt": "Implement advanced machine learning algorithms to predict equipment failures 30 days in advance, analyze historical failure patterns, and automatically generate preventive maintenance schedules with 95% accuracy",
            "scenario": "AI-powered predictive maintenance",
            "use_case": "Advanced preventive maintenance",
            "expected_response": "🤖 **AI-Powered Predictive Maintenance System:**\n\n🧠 **Machine Learning Analysis:**\n• **Data Points Analyzed:** 2.5 million historical data points\n• **Failure Patterns Identified:** 47 distinct failure modes\n• **Prediction Accuracy:** 96.8% (exceeds 95% target)\n• **Model Confidence:** 94.2%\n\n📊 **30-Day Failure Predictions:**\n\n🔴 **High Risk (Immediate Action Required):**\n• **HVAC Unit 2 (Hotel A):** 89% failure probability\n  - Predicted Failure: Compressor malfunction\n  - Time to Failure: 12-18 days\n  - Root Cause: Wear pattern analysis + vibration data\n  - Recommended Action: Schedule replacement within 7 days\n\n• **Water Pump 3 (Hotel C):** 76% failure probability\n  - Predicted Failure: Bearing failure\n  - Time to Failure: 15-22 days\n  - Root Cause: Increased vibration + temperature rise\n  - Recommended Action: Replace bearings within 10 days\n\n🟡 **Medium Risk (Schedule Action):**\n• **5 Thermostats:** 45-65% failure probability\n• **3 Sensors:** 35-55% failure probability\n• **2 HVAC Units:** 25-40% failure probability\n\n📈 **Historical Pattern Analysis:**\n\n🔍 **Failure Pattern 1 - HVAC Compressors:**\n• **Frequency:** Every 18-24 months\n• **Common Causes:** Refrigerant contamination, filter neglect\n• **Prevention Strategy:** Enhanced monitoring + early replacement\n• **Success Rate:** 94% prevention\n\n🔍 **Failure Pattern 2 - Water System Components:**\n• **Frequency:** Every 12-15 months\n• **Common Causes:** Corrosion, sediment buildup\n• **Prevention Strategy:** Regular flushing + corrosion inhibitors\n• **Success Rate:** 91% prevention\n\n🔍 **Failure Pattern 3 - Electrical Systems:**\n• **Frequency:** Every 8-12 months\n• **Common Causes:** Voltage fluctuations, heat buildup\n• **Prevention Strategy:** Voltage monitoring + thermal imaging\n• **Success Rate:** 89% prevention\n\n🤖 **AI-Generated Maintenance Schedule:**\n\n📅 **Week 1 (Critical):**\n• **Day 1-2:** HVAC Unit 2 replacement (Hotel A)\n• **Day 3-4:** Water pump bearing replacement (Hotel C)\n• **Day 5-7:** Emergency response training\n\n📅 **Week 2-4 (Preventive):**\n• **15 HVAC filter replacements**\n• **8 sensor calibrations**\n• **12 thermostat maintenance**\n• **6 water system inspections**\n• **4 electrical system checks**\n\n📊 **Predictive Analytics Dashboard:**\n• **Real-time Risk Assessment:** Updated every 6 hours\n• **Failure Probability Trends:** Historical + predictive\n• **Maintenance Effectiveness:** Success rate tracking\n• **Cost-Benefit Analysis:** ROI calculations\n• **Resource Optimization:** Technician allocation\n\n💰 **Financial Impact:**\n• **Prevented Failures:** 23 in last 6 months\n• **Cost Avoidance:** $185,000\n• **Maintenance Efficiency:** +35%\n• **Downtime Reduction:** 78%\n• **Annual Savings:** $320,000\n\n🎯 **Success Metrics:**\n• **Prediction Accuracy:** 96.8% (Target: 95%)\n• **False Positive Rate:** 3.2%\n• **False Negative Rate:** 1.8%\n• **Maintenance Cost Reduction:** 28%\n• **Equipment Lifespan Extension:** +22%\n\n✅ **AI System Status:**\n• **Model Training:** Complete (updated weekly)\n• **Real-time Monitoring:** Active\n• **Automated Alerts:** Configured\n• **Maintenance Scheduling:** Automated\n• **Performance Optimization:** Continuous",
            "complexity": "Complex",
            "frequency": "Weekly"
        },
        
        # 23. Autonomous Building Management with Self-Healing Systems
        {
            "prompt": "Activate autonomous building management mode where the AI system can independently diagnose issues, execute repairs through automated systems, optimize energy consumption in real-time, and learn from outcomes to improve future performance without human intervention",
            "scenario": "Autonomous building management",
            "use_case": "Self-healing building systems",
            "expected_response": "🤖 **Autonomous Building Management System - ACTIVATED:**\n\n🧠 **AI System Status:**\n• **Autonomy Level:** 95% (Full autonomous operation)\n• **Learning Mode:** Active (continuous improvement)\n• **Decision Confidence:** 92.3%\n• **Human Override:** Available (emergency only)\n\n🔍 **Real-Time System Analysis:**\n\n📊 **Current Autonomous Actions:**\n• **HVAC Optimization:** Real-time load balancing across 5 zones\n• **Energy Management:** Dynamic pricing response + demand shifting\n• **Predictive Maintenance:** 3 repairs scheduled automatically\n• **Guest Comfort:** Personalized room adjustments for 45 guests\n• **Security Integration:** Automated access control + monitoring\n\n🤖 **Self-Healing Operations:**\n\n🔧 **Automated Repairs in Progress:**\n• **Issue:** Thermostat 150002 calibration drift\n• **AI Diagnosis:** Temperature sensor accuracy degradation\n• **Automated Action:** Remote calibration + validation\n• **Status:** 85% complete (2 minutes remaining)\n• **Success Probability:** 94%\n\n🔧 **Preventive Actions Executed:**\n• **HVAC Filter Replacement:** 3 units automatically serviced\n• **Sensor Calibration:** 8 devices calibrated\n• **System Optimization:** 12 performance improvements applied\n• **Energy Load Balancing:** 15% efficiency improvement\n\n📈 **Real-Time Learning & Adaptation:**\n\n🧠 **Pattern Recognition:**\n• **Guest Preference Learning:** 1,247 patterns identified\n• **Energy Usage Optimization:** 89% efficiency improvement\n• **Maintenance Prediction:** 96% accuracy achieved\n• **System Performance:** 23% improvement over baseline\n\n📊 **Autonomous Decision Making:**\n• **Energy Optimization:** $2,400/month savings achieved\n• **Maintenance Scheduling:** 45% efficiency improvement\n• **Guest Satisfaction:** 4.7/5 rating maintained\n• **System Uptime:** 99.3% (target exceeded)\n\n🔄 **Continuous Improvement Loop:**\n\n📈 **Performance Metrics:**\n• **Response Time:** 0.8 seconds (target: <2s)\n• **Issue Resolution:** 94% automated (6% human intervention)\n• **Energy Efficiency:** 89% (target: 85%)\n• **Guest Comfort:** 4.8/5 (target: 4.5/5)\n• **System Reliability:** 99.7% (target: 99.5%)\n\n🤖 **AI Learning Outcomes:**\n• **New Optimization Patterns:** 23 discovered this week\n• **Failure Prevention:** 8 potential issues avoided\n• **Efficiency Improvements:** 15% average gain\n• **Cost Savings:** $3,200 this month\n• **Guest Satisfaction:** +12% improvement\n\n🔮 **Predictive Capabilities:**\n• **Equipment Failures:** 30-day advance warning\n• **Energy Demand:** 24-hour prediction with 94% accuracy\n• **Guest Preferences:** Real-time adaptation\n• **Maintenance Needs:** 7-day advance scheduling\n• **System Performance:** Continuous optimization\n\n💰 **Autonomous ROI:**\n• **Monthly Operational Savings:** $4,800\n• **Maintenance Cost Reduction:** 45%\n• **Energy Cost Savings:** 28%\n• **Staff Productivity:** +35%\n• **Annual ROI:** 340%\n\n🛡️ **Safety & Compliance:**\n• **Emergency Protocols:** Active (human override available)\n• **Safety Monitoring:** 24/7 autonomous surveillance\n• **Compliance Tracking:** Automated regulatory adherence\n• **Audit Trail:** Complete action logging\n• **Risk Management:** Real-time threat assessment\n\n✅ **Autonomous System Status:**\n• **All Systems:** Operating autonomously\n• **Learning Mode:** Active and improving\n• **Performance:** Exceeding all targets\n• **Safety:** All protocols active\n• **Human Oversight:** Available but not required\n\n🎯 **Next Autonomous Actions:**\n• **Scheduled:** 3 preventive maintenance tasks (next 4 hours)\n• **Predicted:** Energy optimization during peak hours\n• **Learning:** Guest preference pattern analysis\n• **Optimization:** System performance fine-tuning",
            "complexity": "Complex",
            "frequency": "Continuous"
        },
        {
            "prompt": "Show me the energy usage trend for the last 6 months.",
            "scenario": "Trend analysis",
            "use_case": "Energy forecasting for planning",
            "expected_response": "📈 **Energy Usage Trend:**\n- Usage increased 8% in summer.\n- Projected to decrease 5% in fall.\n- Recommendation: Schedule maintenance before next peak."
        },
        {
            "prompt": "Forecast occupancy for the next week.",
            "scenario": "Occupancy forecasting",
            "use_case": "Staffing and resource planning",
            "expected_response": "📊 **Occupancy Forecast:**\n- Peak expected on Friday/Saturday.\n- Average: 78%\n- Recommendation: Adjust HVAC and staffing accordingly."
        },
        {
            "prompt": "What are the top alarm trends this quarter?",
            "scenario": "Alarm trend analysis",
            "use_case": "Proactive risk management",
            "expected_response": "🚨 **Alarm Trends:**\n- Most frequent: High temp (22%), Low battery (15%)\n- Trend: Downward after filter replacements\n- Recommendation: Continue preventive maintenance."
        },
        {
            "prompt": "Why did the east wing temperature spike yesterday?",
            "scenario": "Root cause analysis",
            "use_case": "Incident investigation",
            "expected_response": "🔍 **Root Cause:**\n- HVAC filter clog + high occupancy\n- Action: Replace filter, review schedule."
        },
        {
            "prompt": "Analyze the root cause of repeated HVAC alarms.",
            "scenario": "Root cause analysis",
            "use_case": "System reliability improvement",
            "expected_response": "🔍 **Root Cause:**\n- Repeated alarms due to sensor drift and filter issues.\n- Action: Calibrate sensors, replace filters."
        },
        {
            "prompt": "Suggest optimizations for lighting during low occupancy.",
            "scenario": "Automated recommendations",
            "use_case": "Energy savings",
            "expected_response": "🤖 **Lighting Optimization:**\n- Enable automation in common areas.\n- Reduce brightness by 30% after 10pm.\n- Estimated savings: 12%."
        },
        {
            "prompt": "What maintenance actions are recommended for next month?",
            "scenario": "Automated recommendations",
            "use_case": "Proactive maintenance planning",
            "expected_response": "🤖 **Maintenance Recommendations:**\n- Schedule chiller and HVAC maintenance.\n- Replace 5 sensor batteries.\n- Review alarm history for new patterns."
        }
    ]
}

ADVANCED_ANALYTICS_PROMPTS = [
    "Show me the energy usage trend for the last 6 months.",
    "Forecast occupancy for the next week.",
    "What are the top alarm trends this quarter?",
    "Why did the east wing temperature spike yesterday?",
    "Analyze the root cause of repeated HVAC alarms.",
    "Suggest optimizations for lighting during low occupancy.",
    "What maintenance actions are recommended for next month?",
]

PRACTICAL_PROMPTS["ADVANCED_ANALYTICS"] = [{"prompt": p} for p in ADVANCED_ANALYTICS_PROMPTS]

def print_practical_prompts():
    """Print all practical prompts organized by complexity"""
    print("🏢 **TOP 23 PRACTICAL PROMPTS FOR INFERRIX BMS DAILY OPERATIONS**")
    print("=" * 80)
    print("🎯 **Real-world scenarios that happen daily in building management**")
    print("=" * 80)
    
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        print(f"\n{complexity.replace('_', ' ').title()} PROMPTS:")
        print("-" * 60)
        
        for i, prompt_data in enumerate(prompts, 1):
            print(f"\n{i}. 📝 **{prompt_data['scenario']}**")
            print(f"   **Prompt:** {prompt_data['prompt']}")
            print(f"   **Use Case:** {prompt_data['use_case']}")
            print(f"   **Frequency:** {prompt_data['frequency']}")
            print(f"   **Expected Response:** {prompt_data['expected_response'][:100]}...")
            print()
    
    print("=" * 80)
    print("🎯 **DEMO STRATEGY:**")
    print("1. Start with SIMPLE prompts to show basic functionality")
    print("2. Move to MAGIC prompts to demonstrate AI capabilities")
    print("3. End with MEDIUM COMPLEX prompts to show enterprise features")
    print("=" * 80)

def get_prompts_by_complexity(complexity):
    """Get prompts by complexity level"""
    return PRACTICAL_PROMPTS.get(complexity.upper(), [])

def get_prompts_by_frequency(frequency):
    """Get prompts by usage frequency"""
    all_prompts = []
    for complexity, prompts in PRACTICAL_PROMPTS.items():
        all_prompts.extend(prompts)
    
    return [p for p in all_prompts if frequency.lower() in p['frequency'].lower()]

if __name__ == "__main__":
    print_practical_prompts() 
