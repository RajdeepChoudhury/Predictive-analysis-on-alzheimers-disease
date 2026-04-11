const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = 3000;

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// Proxy API requests to Python Flask backend
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5000',
    changeOrigin: true,
    pathRewrite: {
        '^/api': ''
    },
    on: {
        error: (err, req, res) => {
            console.error('Proxy error:', err.message);
            res.status(502).json({
                error: 'Backend server is unavailable. Please ensure the Python server is running on port 5000.'
            });
        }
    }
}));

app.listen(PORT, () => {
    console.log(`\n🌐 Node.js frontend server running at: http://localhost:${PORT}`);
    console.log(`📡 Proxying API requests to Python backend at: http://localhost:5000`);
    console.log(`\n⚠️  Make sure the Python server is also running:`);
    console.log(`   python server.py\n`);
});
