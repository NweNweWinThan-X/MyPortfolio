const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 3000;

const TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'text/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.ico': 'image/x-icon',
    '.md': 'text/markdown; charset=utf-8',
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
};

const server = http.createServer((req, res) => {
    const decoded = decodeURIComponent(req.url.split('?')[0]);

    // Resolve inside the project directory only — never above it.
    const target = path.join(__dirname, path.normalize(decoded));
    if (!target.startsWith(__dirname)) {
        res.writeHead(403);
        return res.end('Forbidden');
    }

    const serve = (file) => {
        fs.readFile(file, (err, data) => {
            if (err) {
                res.writeHead(500);
                return res.end('Error loading ' + path.basename(file));
            }
            const type = TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream';
            res.writeHead(200, { 'Content-Type': type });
            res.end(data);
        });
    };

    fs.stat(target, (err, stat) => {
        // Unknown path or a directory falls back to the single-page entry point.
        if (err || stat.isDirectory()) return serve(path.join(__dirname, 'index.html'));
        serve(target);
    });
});

server.listen(port, () => {
    console.log(`Portfolio running at http://localhost:${port}`);
});
