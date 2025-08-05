import React, { useState, useEffect } from 'react';

function DeviceDropdown({ devices, selectedDeviceId, onSelect }) {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    if (selectedDeviceId) {
      fetch(`/api/plugins/telemetry/DEVICE/${selectedDeviceId}/keys/timeseries`)
        .then(res => res.json())
        .then(data => setMetrics(Array.isArray(data) ? data : Object.keys(data)))
        .catch(() => setMetrics([]));
    } else {
      setMetrics([]);
    }
  }, [selectedDeviceId]);

  const tooltip = metrics.length ? `Available metrics: ${metrics.join(', ')}` : 'Select a device';

  return (
    <select
      value={selectedDeviceId || ''}
      onChange={e => onSelect(e.target.value)}
      title={tooltip}
      style={{ minWidth: 250 }}
    >
      <option value="">Select device</option>
      {devices.map(device => (
        <option key={device.id} value={device.id}>
          {device.name}
        </option>
      ))}
    </select>
  );
}

export default DeviceDropdown; 