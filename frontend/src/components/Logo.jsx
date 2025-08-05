import React from 'react';

const Logo = ({ className = "h-10 w-auto" }) => {
  return (
    <div className={`flex items-center space-x-3 ${className}`} style={{ minWidth: 180 }}>
      {/* Icon */}
      <div className="relative">
        <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center border-2 border-blue-600 shadow-lg">
          {/* Brain symbol */}
          <div className="text-blue-700 text-lg font-bold">🧠</div>
          {/* Leaf symbol */}
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center shadow-md">
            <div className="text-white text-sm">🌱</div>
          </div>
        </div>
      </div>
      {/* Text */}
      <div className="flex flex-col">
        <div className="text-2xl font-extrabold text-gray-900 tracking-tight" style={{letterSpacing: '-1px'}}>
          IntelliSustain
        </div>
        <div className="text-xs text-green-600 font-medium -mt-1">
          AI-Powered Facility Management
        </div>
      </div>
    </div>
  );
};

export default Logo; 