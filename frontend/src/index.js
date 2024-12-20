import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';

// 确保 'root' 元素存在
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}
