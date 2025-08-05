import React from 'react';

// Dynamic Table Component based on React table examples
const DynamicTable = ({ data, headers }) => {
  if (!data || data.length === 0) {
    return <div className="text-gray-500 italic">No data available</div>;
  }

  // Helper function to get cell styling based on content
  const getCellStyle = (cell, headerIndex) => {
    const header = headers[headerIndex]?.toLowerCase() || '';
    const cellLower = cell.toLowerCase();
    
    // Handle empty or placeholder cells
    if (cell === '-' || cell === '' || cell === 'N/A') {
      return 'px-4 py-3 text-sm text-gray-400 italic';
    }
    
    // Severity column styling
    if (header.includes('severity')) {
      if (cellLower === 'critical') {
        return 'px-4 py-3 text-sm font-semibold text-white bg-red-600 rounded-md';
      } else if (cellLower === 'major') {
        return 'px-4 py-3 text-sm font-semibold text-black bg-yellow-400 rounded-md';
      } else if (cellLower === 'minor') {
        return 'px-4 py-3 text-sm font-semibold text-gray-800 bg-yellow-100 rounded-md';
      } else if (cellLower === 'warning') {
        return 'px-4 py-3 text-sm font-semibold text-purple-800 bg-purple-100 rounded-md';
      }
    }
    
    // Status column styling
    if (header.includes('status')) {
      if (cellLower.includes('active')) {
        return 'px-4 py-3 text-sm font-medium text-green-800 bg-green-100 rounded-md';
      } else if (cellLower.includes('unreachable')) {
        return 'px-4 py-3 text-sm font-medium text-red-800 bg-red-100 rounded-md';
      }
    }
    
    // Default styling
    return 'px-4 py-3 text-sm text-gray-900';
  };

  return (
    <div className="overflow-x-auto">
      <div className="max-h-96 overflow-y-auto border border-gray-300 rounded-lg shadow-lg bg-white">
        <table className="min-w-full text-sm border-collapse">
          <thead className="bg-gray-100 sticky top-0 z-10">
            <tr>
              {headers.map((header, index) => (
                <th key={index} className="px-4 py-3 text-left text-xs font-extrabold text-gray-900 uppercase tracking-wider border-b-2 border-gray-400 shadow-sm">
                  <strong>{header}</strong>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-gray-50 transition-colors duration-150">
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex} className={getCellStyle(cell, cellIndex)}>
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DynamicTable; 