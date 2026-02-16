/**
 * ScoringRadar - V5-ULTIME
 * ========================
 */

import React from 'react';
import { 
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer 
} from 'recharts';

export const ScoringRadar = ({ data, color = '#F5A623', size = 'md' }) => {
  const sizes = {
    sm: 120,
    md: 200,
    lg: 300,
  };

  return (
    <div style={{ width: sizes[size], height: sizes[size] }}>
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid stroke="rgba(255,255,255,0.1)" />
          <PolarAngleAxis 
            dataKey="name" 
            tick={{ fill: '#9ca3af', fontSize: 10 }} 
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 100]} 
            tick={false}
            axisLine={false}
          />
          <Radar
            name="Score"
            dataKey="value"
            stroke={color}
            fill={color}
            fillOpacity={0.3}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ScoringRadar;
