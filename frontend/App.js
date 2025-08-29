import React, { useState } from 'react';

function App() {
  const [items, setItems] = useState([]);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-4">
          My App
        </h1>
        <p className="text-gray-600">
          Starter React app with Tailwind CSS
        </p>
      </div>
    </div>
  );
}

export default App;